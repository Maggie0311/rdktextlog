# -*- coding: utf-8 -*-
# （maintainer 补注：AC4 双端一致性用例集 —— 7 个固定输入用例（普通中文/含|/真实换行/反斜杠+制表/控制字符/
# 模块名含|/空消息）同时喂给 Python encode 与 C 探针，逐字节比对输出行。
# 传输用"长度前缀二进制"而非行式文本，是因为用例内容本身含换行，行式传输会失真；
# 一致性范围=无属性形态（C 端宏族 P0 不带 attrs，属声明的 P1 扩展）。）
"""rmlog.encode_cases — AC4 双端一致性用例集（C/Python 渲染对照的单一输入源）。

任务: T-20260926-001-logging-platform-p0（AC4）。

设计:
- 每个用例固定全部输入（seq/mono/墙钟/级别/码/模块/消息），不含时间随机性 ——
  双端一致性判定只针对**编码规则本身**（转义表、字段序、格式化），
  这是 REQ P0-c "同一事件双端同构行" 的可测化。
- 一致性范围（诚实声明）: 行的**无属性形态**。属性段（k=v）C 端 emit 路径
  P0 不支持（宏族签名无 attrs），其转义与解析规则已由 AC2 的 Python 往返
  用例覆盖; C 端引入 attrs 属 P1 扩展，届时补对照用例。
- 传输用二进制长度前缀（write_probe_input / read_probe_output）:
  消息含真实换行/制表符时行式或 TSV 传输会失真，二进制格式对任意内容鲁棒;
  探针与传输格式是开发机自测专用工具，不随板端交付（IMPL 已注明）。
"""

import struct

from .format import encode

# 用例集: 覆盖普通文本 / 分隔符 / 真实换行 / 反斜杠与制表 / 控制字符 / 中文混合
CASES = [
    {"desc": "普通中文消息",
     "seq": 1, "mono_ms": 1000, "wall_ts": "2026-09-26T16:00:00.000",
     "level": "INFO", "code": "E-INIT-000", "module": "ctrl",
     "message": "上电自检完成 state=1"},
    {"desc": "消息含字段分隔符 |",
     "seq": 2, "mono_ms": 2000, "wall_ts": "2026-09-26T16:00:01.000",
     "level": "ERROR", "code": "E-COMM-001", "module": "spi",
     "message": "超时|dev=/dev/spidev0.0|retry=3"},
    {"desc": "消息含真实换行",
     "seq": 3, "mono_ms": 3000, "wall_ts": "2026-09-26T16:00:02.000",
     "level": "WARN", "code": "E-HW-003", "module": "imu",
     "message": "第一行\n第二行\r\n第三行"},
    {"desc": "消息含反斜杠与制表符",
     "seq": 4, "mono_ms": 4000, "wall_ts": "2026-09-26T16:00:03.000",
     "level": "ERROR", "code": "E-SYS-002", "module": "io",
     "message": "路径 C:\\rmlog\\log 且 a\tb"},
    {"desc": "消息含控制字符与 DEL",
     "seq": 5, "mono_ms": 5000, "wall_ts": "2026-09-26T16:00:04.000",
     "level": "FATAL", "code": "E-FSM-004", "module": "fsm",
     "message": "bad\x01chars\x1fhere\x7f"},
    {"desc": "模块名含特殊字符(转义兜底)",
     "seq": 6, "mono_ms": 6000, "wall_ts": "2026-09-26T16:00:05.000",
     "level": "INFO", "code": "E-SYS-005", "module": "mod|x",
     "message": "milestone"},
    {"desc": "空消息与最小字段",
     "seq": 7, "mono_ms": 7000, "wall_ts": "2026-09-26T16:00:06.000",
     "level": "INFO", "code": "E-INIT-000", "module": "m",
     "message": ""},
]


def run_py_side(cases):
    """Python 端渲染全部用例，返回行列表（不含换行符）。"""
    return [encode(c["seq"], c["wall_ts"], c["mono_ms"], c["level"],
                   c["code"], c["module"], c["message"]) for c in cases]


# ---- 二进制传输格式 ----
# 输入: uint32 用例数; 每例 = int32 seq + int64 mono + 5 个字符串(ushort16 长度 + UTF-8 字节)
# 字符串顺序: wall_ts, level, code, module, message
# 输出: 每例 = ushort16 长度 + 渲染行 UTF-8 字节（与输入一一对应）
_STR_FIELDS = ("wall_ts", "level", "code", "module", "message")


def write_probe_input(path, cases):
    """把用例集写成 C 探针的二进制输入文件。"""
    with open(path, "wb") as fh:
        fh.write(struct.pack("<I", len(cases)))
        for c in cases:
            fh.write(struct.pack("<i", c["seq"]))
            fh.write(struct.pack("<q", c["mono_ms"]))
            for field in _STR_FIELDS:
                raw = c[field].encode("utf-8")
                fh.write(struct.pack("<H", len(raw)))
                fh.write(raw)


def read_probe_output(path):
    """读取 C 探针的二进制输出，返回渲染行列表（UTF-8 解码）。"""
    lines = []
    with open(path, "rb") as fh:
        data = fh.read()
    offset = 0
    while offset < len(data):
        (length,) = struct.unpack_from("<H", data, offset)
        offset += 2
        lines.append(data[offset:offset + length].decode("utf-8"))
        offset += length
    return lines
