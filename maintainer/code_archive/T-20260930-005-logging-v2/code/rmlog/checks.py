# -*- coding: utf-8 -*-
# Maintainer archive note (v001): source snapshot 3148fed; comments only.
"""T-20260930-005：业务检测适配器与五类故障注入演示。

库只记录业务提供的事实；它不会自动理解 SPI、CAN、电机或传感器协议。
"""
from . import catalog

def emit_check(writer, kind, ok=True, detail=""):
    """把检测结果映射到错误码；kind 取 init/comm/hw/fsm/sys。"""
    mapping = {"init": ("E-INIT-000", "E-INIT-001"), "comm": ("E-COMM-003", "E-COMM-004"),
               "hw": ("E-HW-005", "E-HW-001"), "fsm": ("E-FSM-002", "E-FSM-003"),
               "sys": ("E-SYS-005", "E-SYS-002")}
    if kind not in mapping:
        raise ValueError("unknown check kind: %s" % kind)
    code = mapping[kind][0 if ok else 1]
    return writer.event(code, "check", detail or ("%s check ok" % kind), attrs={"check": kind})
