# -*- coding: utf-8 -*-
"""rmlog_read — rmlog 读端工具: parse / tail / filter（REQ §4 P0-e）。

任务: T-20260926-001-logging-platform-p0。

比赛日"一条命令定位"示例（详见 USAGE.md §5）::

    python3 rmlog_read.py filter ./rmlog.log --level ERROR --code E-INIT-*
    python3 rmlog_read.py tail ./rmlog.log -n 20 --follow

子命令:
    parse   逐行解析并 pretty 打印（检查行格式/残行丢弃是否生效）
    tail    看最后 N 条（--follow 持续跟踪, 类 tail -f）
    filter  按级别/错误码/时间窗过滤 —— 场下定位的主力入口

残行策略（AC2）: 每行先过 rmlog.format.parse_line 三道闸（前缀/字段数/语义）,
不合法的行**丢弃并计数**, 结束时把丢弃数打到 stderr —— 比赛取证时必须
知道"有多少行没能读出来", 这是证据链诚实性的一部分。
"""

import argparse
import os
import sys
import time

# 允许脚本被直接执行（python3 rmlog_read.py ...）也可作为模块导入:
# 把脚本所在目录加入 sys.path, 保证 `from rmlog import ...` 在两种方式下都成立。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rmlog.format import parse_line, level_rank  # noqa: E402


def iter_events(paths):
    """逐行解析多个日志文件（含轮转副本）, 产出 (行号, 事件或 None, 原始行)。

    为什么不预读全文件: 比赛日志可达数十万行, tail/filter 都应流式处理,
    内存占用与文件大小解耦。
    """
    for path in paths:
        if not os.path.exists(path):
            sys.stderr.write("rmlog_read: 文件不存在: %s\n" % path)
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for lineno, raw in enumerate(fh, 1):
                ev = parse_line(raw)
                yield lineno, ev, raw.rstrip("\r\n")


def cmd_parse(args):
    """parse 子命令: pretty 打印每个合法事件; 残行以 [DROP] 标注（默认显示）。"""
    dropped = 0
    for lineno, ev, raw in iter_events([args.file]):
        if ev is None:
            dropped += 1
            if not args.quiet:
                print("  [DROP] L%-6d %s" % (lineno, raw[:80]))
            continue
        attrs = ("  " + " ".join("%s=%s" % kv for kv in sorted(ev["attrs"].items()))
                 if ev["attrs"] else "")
        print("L%-6d #%s %s (%s) [%s] %s %s: %s%s" % (
            lineno, ev["seq"], ev["wall_ts"], ev["mono_ts"], ev["level"],
            ev["code"], ev["module"], ev["message"], attrs))
    _summary(dropped)
    return 0


def cmd_tail(args):
    """tail 子命令: 输出最后 N 条; --follow 每秒轮询新行（类 tail -f）。

    follow 用"记住已读字节数 + 增量读"实现, 不依赖 inotify（板端探测 least
    surprise: 轮询在 Linux/Windows 行为一致, P0 不引入平台分支）。
    """
    path = args.file
    if args.follow:
        offset = 0
        if os.path.exists(path):
            offset = os.path.getsize(path)
            _tail_print(path, args.number)
        try:
            while True:
                if os.path.exists(path):
                    size = os.path.getsize(path)
                    if size < offset:      # 轮转/重建: 文件变小, 从头读新文件
                        offset = 0
                    if size > offset:
                        with open(path, "r", encoding="utf-8", errors="replace") as fh:
                            fh.seek(offset)
                            for raw in fh:
                                ev = parse_line(raw)
                                if ev is not None:
                                    _print_event(ev)
                        offset = size
                time.sleep(1.0)
        except KeyboardInterrupt:
            return 0
    else:
        return _tail_print(path, args.number)


def _tail_print(path, n):
    """非 follow 的 tail: 全量流式读, 仅打印最后 n 条合法事件。"""
    window = []
    dropped = 0
    for _, ev, _raw in iter_events([path]):
        if ev is None:
            dropped += 1
            continue
        window.append(ev)
        if len(window) > n:
            window.pop(0)
    for ev in window:
        _print_event(ev)
    _summary(dropped)
    return 0


def _print_event(ev):
    """单条事件的默认人读格式（tail/filter 共用; parse 用更详细的版式）。"""
    attrs = ("  " + " ".join("%s=%s" % kv for kv in sorted(ev["attrs"].items()))
             if ev["attrs"] else "")
    print("%s [%s] %s %s: %s%s" % (
        ev["wall_ts"], ev["level"], ev["code"], ev["module"], ev["message"], attrs))


def _summary(dropped):
    """把残行丢弃数打到 stderr —— stdout 保持纯事件流, 可安全重定向/管道。"""
    if dropped:
        sys.stderr.write("rmlog_read: 丢弃残行/非法行 %d 条\n" % dropped)


def _normalize_wall_prefix(value, is_upper_bound):
    """把墙上时间前缀归一为"可与毫秒精度 wall_ts 直接字典序比较"的定宽串。

    背景（F-2 修复）: --since/--until 允许分钟级前缀（如 2026-09-26T12:01, 见
    USAGE §5 演示与 argparse help 的示例）, 但行内 wall_ts 是毫秒定宽 ——
    原始字典序比较下 "12:01:00.500" > "12:01" 恒成立, --until 的截断前缀
    会系统性漏掉该分钟的全部事件（reviewer probe_until2 实证: 漏掉 12:01
    这一分钟, 却能命中全精度值）。修复选**前缀归一**而非"拒绝非全精度":
    取证者按日历语义输入"分钟"是自然用法, 工具应当正确解释它而不是报错
    （比赛现场没有翻文档试错的时间; 全精度值不受影响, 语义完全向后兼容）。

    规则（按已给段补齐, 未给段取该段边界）:
      - --since（下界, is_upper_bound=False）: 未给段补最小值
        （月=01、日=01、时=00、分=00、秒=00、毫秒=000）—— "从该时刻起含";
      - --until（上界, is_upper_bound=True）: 未给段补最大值
        （月=12、日=31、时=23、分=59、秒=59、毫秒=999）—— "到该段末含"。
        日按月补最大 31: 字典序上 31 是日字段的上界（2 月的 31 不存在,
        但比较只发生在"行内时间戳 vs 上界"之间, 不产生错误命中 ——
        任何真实时间戳的日字段 ≤ 31, 2 月 30/31 本就不存在对应行）。

    输入可以是任意前缀（YYYY / YYYY-MM / YYYY-MM-DD / ...T..HH / HH:MM /
    HH:MM:SS / HH:MM:SS.mmm）; 带分隔符或带 'T' 都接受。无法识别的输入
    原样返回（由比较层自然退化为"基本不命中", 不抛异常 —— 与读端整体的
    容错姿态一致; USAGE §5 的示例是合法形态）。
    """
    text = value.strip()
    if not text:
        return value
    # 拆日期与时间两部分（'T' 或空格分隔均可）
    if "T" in text:
        date_part, _, time_part = text.partition("T")
    elif " " in text:
        date_part, _, time_part = text.partition(" ")
    else:
        date_part, time_part = text, ""
    # ---- 日期段: YYYY[-MM[-DD]] ----
    dsegs = date_part.split("-") if date_part else []
    if not dsegs or not dsegs[0].isdigit() or len(dsegs[0]) != 4:
        return value                      # 不是以 4 位年份开头: 无法识别, 原样返回
    year = dsegs[0]
    mon = dsegs[1] if len(dsegs) > 1 and dsegs[1] else None
    day = dsegs[2] if len(dsegs) > 2 and dsegs[2] else None
    # ---- 时间段: HH[:MM[:SS[.mmm]]] ----
    tsegs = time_part.split(":") if time_part else []
    hh = tsegs[0] if len(tsegs) > 0 and tsegs[0] else None
    mi = tsegs[1] if len(tsegs) > 1 and tsegs[1] else None
    ss_mmm = tsegs[2] if len(tsegs) > 2 else None
    ss = None
    ms = None
    if ss_mmm:
        if "." in ss_mmm:
            ss, _, ms = ss_mmm.partition(".")
        else:
            ss = ss_mmm
        ss = ss or None
        ms = (ms or None)
    pad_hi = is_upper_bound               # 未给段: 上界补最大, 下界补最小
    mon = mon or ("12" if pad_hi else "01")
    day = day or ("31" if pad_hi else "01")
    hh = hh or ("23" if pad_hi else "00")
    mi = mi or ("59" if pad_hi else "00")
    ss = ss or ("59" if pad_hi else "00")
    ms = ms or ("999" if pad_hi else "000")
    # 毫秒不足 3 位时右补零（.5 -> 500）: 定宽对齐后再比较
    ms = (ms + "000")[:3]
    return "%s-%s-%sT%s:%s:%s.%s" % (year, mon, day, hh, mi, ss, ms)


def cmd_filter(args):
    """filter 子命令: 级别（不低于）/错误码（前缀通配）/时间窗三组条件 AND 组合。

    时间窗基于墙上时间戳的字符串比较: 行格式 v1 的 wall_ts 是定宽 ISO8601,
    字典序即时间序, 无需解析成 datetime —— 既快又避免时区二次解释。
    F-2 修复: --since/--until 接受任意前缀, 比较前经 _normalize_wall_prefix
    归一为毫秒定宽（--until 前缀 = 该段末, --since 前缀 = 该段始）,
    分钟级窗口不再漏掉该分钟内的事件。
    """
    code_prefix = None
    if args.code:
        # --code 支持 E-INIT-* 形式的前缀通配（REQ AC5 原话就是这种用法）
        code_prefix = args.code[:-1] if args.code.endswith("*") else args.code
    # 时间窗归一（F-2）: since 补该段最小、until 补该段最大 —— 全精度值不变
    since = _normalize_wall_prefix(args.since, False) if args.since else None
    until = _normalize_wall_prefix(args.until, True) if args.until else None
    dropped = 0
    matched = 0
    for _, ev, _raw in iter_events([args.file]):
        if ev is None:
            dropped += 1
            continue
        if args.level and level_rank(ev["level"]) < level_rank(args.level):
            continue
        if code_prefix is not None and not ev["code"].startswith(code_prefix):
            continue
        if args.session and ev["attrs"].get("session") != args.session:
            continue
        if since and ev["wall_ts"] < since:
            continue
        if until and ev["wall_ts"] > until:
            continue
        _print_event(ev)
        matched += 1
    _summary(dropped)
    sys.stderr.write("rmlog_read: 命中 %d 条\n" % matched)
    return 0


def build_parser():
    """参数解析器（三个子命令共用一套残行统计行为）。"""
    p = argparse.ArgumentParser(
        prog="rmlog_read.py",
        description="rmlog 读端工具: parse / tail / filter（行格式 v1）")
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("parse", help="逐行解析并 pretty 打印（含残行标注）")
    pp.add_argument("file")
    pp.add_argument("--quiet", action="store_true", help="不打印残行原文")

    tp = sub.add_parser("tail", help="看最后 N 条; --follow 持续跟踪")
    tp.add_argument("file")
    tp.add_argument("-n", "--number", type=int, default=20)
    tp.add_argument("--follow", action="store_true")

    fp = sub.add_parser("filter", help="按级别/错误码/时间窗过滤（场下定位主力）")
    fp.add_argument("file")
    fp.add_argument("--level", choices=["INFO", "WARN", "ERROR", "FATAL"],
                    help="只看不低于该级别的行")
    fp.add_argument("--code", help="错误码, 支持前缀通配（如 E-INIT-*）")
    fp.add_argument("--session", help="只显示属性 session 等于该 ID 的事件")
    fp.add_argument("--since", help="起始墙上时间（含）, 支持前缀: 2026-09-26T16:00 或 2026-09-26T16:00:00.000")
    fp.add_argument("--until", help="结束墙上时间（含）, 前缀视为该段末（如 T14:38 含 14:38 这一整分钟）")
    return p


def main(argv):
    """CLI 入口: 子命令分发。"""
    args = build_parser().parse_args(argv)
    if args.cmd == "parse":
        return cmd_parse(args)
    if args.cmd == "tail":
        return cmd_tail(args)
    return cmd_filter(args)


if __name__ == "__main__":
    # argv[0] 是脚本自身路径, 切掉后 argparse 才能拿到真正的子命令
    sys.exit(main(sys.argv[1:]))
