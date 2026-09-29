# -*- coding: utf-8 -*-
"""code_reviewer R7 验证脚本 V1+V3: USAGE §1.1 Python 快速上手原样命令 + 分钟前缀时间窗素材。

按 USAGE.md §1.1 逐字执行（2 行起步 + attrs 版 + 自定义目录版），
另在同一分钟内写入 3 条事件（2 ERROR + 1 INFO）作为 --since/--until 分钟前缀语义的素材。
"""
import datetime

from rmlog.writer import Writer, set_default_writer

# --- USAGE §1.1 自定义目录版（开发机演示路径）---
set_default_writer(Writer(log_dir="./v1log"))
import rmlog  # noqa: E402  按文档要求放在 set_default_writer 之后

# --- USAGE §1.1 基础 2 行 ---
rmlog.event("E-INIT-000", "ctrl", "上电启动完成")

# --- USAGE §1.1 attrs 版 ---
rmlog.event("E-COMM-001", "spi", "SPI 传输超时", attrs={"dev": "/dev/spidev0.0", "retry": 3})

# --- V3 素材: 同一分钟内 2 ERROR + 1 INFO ---
rmlog.event("E-FSM-001", "fsm", "状态机非法跃迁 test")
rmlog.event("E-SYS-001", "sys", "内存不足 test")
rmlog.event("E-SYS-005", "sys", "系统里程碑 test")

minute = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
print("V1_OK events=5 minute=%s" % minute)
