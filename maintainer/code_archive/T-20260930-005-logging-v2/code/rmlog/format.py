# -*- coding: utf-8 -*-
# Maintainer archive note (v001): source snapshot 3148fed; comments only.
"""rmlog.format — 行格式 v1 的唯一权威定义：编码（事件→行）与解析（行→事件）。

任务: T-20260926-001-logging-platform-p0（REQ §4 P0-b）。

行格式 v1（REQ 冻结的字段序，本文件是双端唯一权威定义，C 端同构实现）::

    LOGV1|<seq>|<墙上时间戳 ISO8601>|<单调时间戳 ms>|<LEVEL>|<CODE>|<MODULE>|<message>[|k=v...]

- 固定前缀 `LOGV1`：读端借此识别有效行；崩溃/断电截断的残行（无前缀或字段残缺）
  被安全丢弃并计数，绝不污染解析（AC2）。
- seq 为单调递增正整数（写入进程内的原子计数），用于并发写审计与行排序。
- 墙上时间戳 ISO8601 本地时间，精度毫秒（如 2026-09-26T16:20:00.123）；
  单调时间戳 = time.monotonic() 毫秒（防 NTP 跳变/倒流，可算事件间隔）。
- LEVEL ∈ {INFO, WARN, ERROR, FATAL}；CODE 必须来自 catalog.py（E-域-序号）。
- 属性区: 第 8 段起每段一个 `k=v`（k 与 v 均为单段），无属性时省略整个属性区。

转义规则（v1 冻结，双端一致）:
- 分隔符是 `|`，换行即行边界，因此消息/模块/属性值中出现 `|` 会破坏字段序，
  出现换行会破坏"一行一条事件"。处理方式选**编码替换**而非引用转义 ——
  理由: 引用转义（如 `\\|`）要求解析器做状态机扫描，C 端实现复杂易错；
  编码替换把不可见/危险字符变成 ASCII 可见序列，解析端零特殊逻辑，肉眼可读。
- `\\` → `\\\\`，`|` → `\\x7c`，`\\r` → `\\x0d`，`\\n` → `\\x0a`，
  其他 C0 控制字符（0x00-0x1F、0x7F）→ `\\xNN` 十六进制两位。
- 顺序: 先替换反斜杠，再替换其余字符（否则二次转义）。
- 解析端对 `\\xNN` 逆向解码；解码失败（截断的 xNN）按原文保留，不抛异常。

多进程行完整性（REQ P0-d）: 调用方（writer/C 端）必须把**一条完整行**放在
一次 write() 中以 O_APPEND 写出。OS 保证 O_APPEND 下单次 write 的数据
连续追加不交错（Linux 下相对小写入实际原子）；本模块负责保证行内无裸
`|`/换行，两者合起来构成"无丢行、无交错半行"的基础。

平台差异: 时间精度与编码逻辑本身跨平台一致；Windows 下 time.monotonic 与
Linux(CLOCK_MONOTONIC) 同为单调时钟，仅起点不同（单调时间只在同一次开机
内有意义，两端行为一致，无需适配）。
"""

import re
import time

# 行格式版本前缀 —— 读端识别依据（残行按"非 LOGV1 前缀"规则丢弃）
PREFIX = "LOGV1"

# 合法级别集合（表驱动，便于读端做白名单校验）
LEVELS = ("INFO", "WARN", "ERROR", "FATAL")

# 固定字段数（属性区之前的部分）：前缀+seq+两时间戳+级别+码+模块+消息 = 8 段
MIN_FIELDS = 8

# 级别优先级（数值越大越严重），读端 --level 过滤用：取"不低于指定级别"的行
_LEVEL_RANK = {"INFO": 0, "WARN": 1, "ERROR": 2, "FATAL": 3}

# ASCII 纯数字串校验。不用 str.isdigit: 它对 "²"(U+00B2) 等非 ASCII 数字
# 也返回 True，而 int() 解析这些串会抛 ValueError —— 会击穿"解析永不抛异常"
# 的承诺（fuzz 用例 P2 二进制字符恰好落在 seq/mono 字段时触发此路径）。
# fullmatch 保证整段匹配，拒绝 "12a"、"" 与 Unicode 数字。
_ASCII_DIGITS = re.compile(r"\A[0-9]+\Z")

# 转义映射表: 目标字符 -> 替换文本（除反斜杠外的项都变成 \xNN 形式，肉眼可读）
_ESCAPES = {
    "\\": "\\\\",   # 反斜杠必须最先处理，防止后续替换产物被二次转义
    "|": "\\x7c",   # 字段分隔符
    "\r": "\\x0d",  # 回车（Windows 文本模式下可能混入）
    "\n": "\\x0a",  # 换行（行边界）
    "\t": "\\x09",
}


def _escape(text):
    """对单段文本做转义，保证段内不含裸 `|`、换行等破坏字段序的字符。

    非显然点: 除表中显式列出的字符外，其余控制字符统一走 \\xNN 分支 ——
    用"先查表、再按需兜底"的两步策略，避免为 32 个控制字符各建一条映射。
    """
    if not text:
        return ""
    out = []
    for ch in text:
        if ch in _ESCAPES:
            out.append(_ESCAPES[ch])
        elif ord(ch) < 0x20 or ord(ch) == 0x7F:
            # 其余 C0 控制字符与 DEL: 统一转 \xNN，防止污染终端与行结构
            out.append("\\x%02x" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)


def _unescape(text):
    """解析端的逆向解码：把 \\xNN 还原为原字符。

    容错设计: 截断行可能留下残缺的反斜杠转义（如只有 `\\x` 或 `\\x1`）——
    此时按原文保留，不抛异常。理由: 读端面对的是"崩溃后磁盘上的任意字节"，
    解析必须永不抛异常（残行由前缀与字段数规则统一丢弃，见 parse_line）。
    """
    if "\\" not in text:
        return text
    out = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch != "\\" or i + 1 >= n:
            out.append(ch)
            i += 1
            continue
        nxt = text[i + 1]
        if nxt == "\\":
            out.append("\\")
            i += 2
        elif nxt == "x" and i + 3 < n:
            try:
                out.append(chr(int(text[i + 2:i + 4], 16)))
                i += 4
            except ValueError:
                # 非法十六进制（残行/外源数据）: 原样保留，避免静默吞字符
                out.append(ch)
                i += 1
        else:
            # 孤立反斜杠或未知转义: 原样保留（与上面同理，宁保守不猜测）
            out.append(ch)
            i += 1
    return "".join(out)


def wall_timestamp(now=None):
    """生成 ISO8601 本地时间字符串，毫秒精度（2026-09-26T16:20:00.123）。

    为什么不用 time.isoformat() 的默认微秒: 比赛取证只需毫秒，更短更可读，
    且与单调时间戳的毫秒精度对齐。非显然点: timespec="milliseconds" 若与
    Python 版本无关可直接用，此处显式给出以保证双端格式说明一致。
    """
    if now is None:
        now = time.time()
    local = time.localtime(now)
    ms = int(round((now - int(now)) * 1000))
    if ms >= 1000:  # 浮点进位保护：0.9997s 会被舍入成整秒
        ms -= 1000
        local = time.localtime(now + 1)
    return "%04d-%02d-%02dT%02d:%02d:%02d.%03d" % (
        local.tm_year, local.tm_mon, local.tm_mday,
        local.tm_hour, local.tm_min, local.tm_sec, ms)


def mono_timestamp():
    """单调时间戳（毫秒，整数）。

    取 time.monotonic()（防系统时间被 NTP 调整而倒流）；乘 1000 取整为毫秒。
    该值仅在同一次开机内有意义 —— 跨上电比较单调时间无意义，比对须用墙上时间。
    """
    return int(time.monotonic() * 1000)


def encode(seq, wall_ts, mono_ts, level, code, module, message, attrs=None):
    """事件 -> 一行文本（不含行尾换行符，换行由调用方 write 时统一追加）。

    参数:
        seq      事件序号（写入进程内单调递增）
        wall_ts  墙上时间戳字符串（由 wall_timestamp 生成）
        mono_ts  单调时间戳（毫秒整数）
        level    级别字符串（须在 LEVELS 内，非法值原样通过由读端拒绝）
        code     错误码（建议来自 catalog，未知码也允许 —— 目录表允许扩展期临时代码）
        module   模块名（建议 [a-zA-Z0-9_-]，不强制，转义兜底）
        message  消息文本（任意可打印内容，含 | 与换行也会被安全转义）
        attrs    k=v 属性字典或可迭代的 (k, v) 序列；值可为任意字符串

    设计原因: 编码函数保持"纯函数"（不做 IO、不用全局状态），C 端按同一
    算法实现，AC4 的双端一致性只依赖双方对齐本文件的规则。
    """
    parts = [
        PREFIX,
        str(int(seq)),
        wall_ts,
        str(int(mono_ts)),
        level,
        code,
        _escape(module),
        _escape(message),
    ]
    if attrs:
        items = attrs.items() if hasattr(attrs, "items") else attrs
        for key, value in items:
            # 属性 key 也要转义: key 里有 `|` 同样会破坏字段序（防御性，规范上禁止）
            parts.append("%s=%s" % (_escape(str(key)), _escape(str(value))))
    return "|".join(parts)


def parse_line(line):
    """一行文本 -> 事件字典；不合法（残行/外源行）返回 None。

    判定规则（AC2 残行丢弃的三道闸，顺序即执行序）:
      1. 前缀闸: 必须以 `LOGV1|` 开头 —— 崩溃截断大概率丢尾部，前缀在行首，
         而半行通常表现为"前缀在但字段残缺"，由第 2/3 道闸拦截；
         非 LOGV1 开头（如 journald 混入行、被截断的头部）直接丢弃。
      2. 字段数闸: 按 `|` 切分后段数 >= 8。
      3. 语义闸: seq 与单调时间戳必须是纯数字 —— 拦截"头几个字段恰好齐全、
         但内容被截断污染"的行（例如 seq 位置混入了消息文本）。

    返回字典字段: seq(int) / wall_ts / mono_ts(int) / level / code /
    module / message / attrs(dict)。解析永不抛异常。
    """
    line = line.rstrip("\r\n")
    if not line.startswith(PREFIX + "|"):
        return None
    fields = line.split("|")
    if len(fields) < MIN_FIELDS:
        return None
    if not _ASCII_DIGITS.fullmatch(fields[1]) or not _ASCII_DIGITS.fullmatch(fields[3]):
        return None
    attrs = {}
    for segment in fields[MIN_FIELDS:]:
        # 属性段必须形如 k=v；残行尾段可能缺 `=`，跳过而不报错
        if "=" not in segment:
            continue
        key, _, value = segment.partition("=")
        attrs[_unescape(key)] = _unescape(value)
    return {
        "seq": int(fields[1]),
        "wall_ts": fields[2],
        "mono_ts": int(fields[3]),
        "level": fields[4],
        "code": fields[5],
        "module": _unescape(fields[6]),
        "message": _unescape(fields[7]),
        "attrs": attrs,
    }


def level_rank(level):
    """级别 -> 严重度数值（未知级别按 0/INFO 处理，宁多给证据不误删）。"""
    return _LEVEL_RANK.get(level, 0)
