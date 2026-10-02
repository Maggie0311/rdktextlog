"""T-20261001-logging-v3 P0/P1：低打点自动化运行时。

业务循环通过 ``heartbeat``、``sample`` 和 ``emit`` 提供事实；严重事件自动
触发黑匣子快照。这样业务不必每处手写 printf 式上下文拼接，同时保留 v2
``Writer.event`` 和 ``AsyncWriter.emit`` 的兼容用法。
"""

import os
import threading
import time

from .blackbox import BlackBox
from . import catalog


class LogRuntime:
    """把日志、黑匣子和会话属性组合成一个业务侧入口。"""

    def __init__(self, writer, blackbox_dir, capacity=2000, session=None):
        self.writer = writer
        self.session = session
        self.blackbox = BlackBox(blackbox_dir, capacity)
        self._heartbeat = {}
        self._lock = threading.Lock()

    def sample(self, kind, **values):
        """记录一个高频样本；仅入内存，不落盘。"""
        self.blackbox.record(kind, **values)

    def heartbeat(self, name="main", count=None, **values):
        """更新指定主循环心跳并自动进入黑匣子样本。"""
        with self._lock:
            self._heartbeat[name] = (time.monotonic(), count)
        self.sample("heartbeat", name=name, count=count, **values)

    def emit(self, code, module, message, level=None, attrs=None):
        """写一条事件；ERROR/FATAL 之后立即倒出错误前窗口。"""
        if self.session is not None:
            attrs = self.session.attrs(attrs)
        method = getattr(self.writer, "event", None) or getattr(self.writer, "emit")
        ok = method(code, module, message, level=level, attrs=attrs)
        effective = level or catalog.default_level(code) or "INFO"
        if effective in ("ERROR", "FATAL"):
            path = self.blackbox.snapshot("error", code)
            if path:
                method("E-SYS-005", "blackbox", "blackbox snapshot written",
                       attrs={"code": code, "path": path})
        return ok

    def health_attrs(self):
        """返回可挂在诊断事件上的当前心跳状态。"""
        with self._lock:
            return {"heartbeat_%s" % key: int((time.monotonic() - value[0]) * 1000)
                    for key, value in self._heartbeat.items()}
