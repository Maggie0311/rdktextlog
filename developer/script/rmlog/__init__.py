# -*- coding: utf-8 -*-
"""rmlog — RoboMaster 文本日志平台（P0）: C/Python 双端同源错误码 + 同构行格式。

任务: T-20260926-001-logging-platform-p0（REQ §4 P0-a~f）。

面向业务的最简入口::

    import rmlog
    rmlog.event("E-INIT-000", "main", "上电启动完成")
    rmlog.event("E-COMM-001", "spi", "SPI 传输超时", attrs={"dev": "/dev/spidev0.0"})

层级结构（依赖只允许向下, 见 CODE-STYLE §2.5）::

    catalog.py  错误码单一来源（纯数据, 零依赖）
    format.py   行格式 v1 编码/解析（唯一权威定义, C 端同构实现）
    writer.py   多进程安全追加 + 轮转 + 可控 flush
    gen_code.py 由 catalog 生成 C 端 rmlog_errors.h
    worker.py   多进程并发写压测工作进程（selftest 专用）
    selftest.py 覆盖 AC1-AC6 的断言式自测入口

平台事实（诚实标注）: 本轮在 Windows 开发机自测（Python 3.13/3.14 + MinGW gcc 13.2）,
板端 X5（Ubuntu 22.04 aarch64 + PREEMPT-RT）验证按 Q1=A 裁决由用户按 USAGE.md
「板端自测步骤」执行 —— Windows 自测结果不得表述为 Linux 已验证。
"""

from .format import (LEVELS, PREFIX,
                     encode, parse_line, wall_timestamp, mono_timestamp,
                     level_rank)
from .writer import Writer, event, get_writer, set_default_writer
from .code_map import encode as encode_code, decode as decode_code, hex_code
from . import catalog

# 包版本（P0 交付; 行格式或错误码表破坏性变更时同步升版本）
__version__ = "0.2.0"

__all__ = [
    "event", "get_writer", "set_default_writer", "Writer",
    "encode", "parse_line", "wall_timestamp", "mono_timestamp", "level_rank",
    "LEVELS", "PREFIX", "catalog", "encode_code", "decode_code", "hex_code",
]


def encode_line(seq, wall_ts, mono_ms, level, code, module, message, attrs=None):
    """行编码的显式参数版包装 —— selftest 用它与 C 端输出做逐字段对照（AC4）。

    为什么不直接用 format.encode: 该包装把"构造同一事件的全部输入"显式化,
    与 C 端 rmlog_line() 的参数一一对应, 双端对照时不引入"Python 侧自己取时间"
    的隐藏差异 —— 双端一致性的判定边界更干净。
    """
    return encode(seq, wall_ts, mono_ms, level, code, module, message, attrs)
