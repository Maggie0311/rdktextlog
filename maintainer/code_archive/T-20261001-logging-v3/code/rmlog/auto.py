# （maintainer 补注，T-20261001-logging-v3 归档 001，来源 commit d77d36c）
# 导读：auto.py = P0/P1「低打点自动化运行时」入口 LogRuntime。业务循环用 heartbeat/sample/emit
# 提供事实；emit 写 ERROR/FATAL 后自动倒出黑匣子快照（并补一条 E-SYS-005）。它把日志、
# 黑匣子、会话属性组合成业务侧单一入口，同时保留 v2 Writer.event / AsyncWriter.emit 兼容用法。
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
        self._heartbeat_started = {}
        self._lock = threading.Lock()
        self.write_failures = 0
        self.blackbox_failures = 0
        self.last_error = None

    def sample(self, kind, **values):
        """记录一个高频样本；仅入内存，不落盘。"""
        self.blackbox.record(kind, **values)

    def heartbeat(self, name="main", count=None, **values):
        """更新指定主循环心跳并自动进入黑匣子样本。"""
        with self._lock:
            self._heartbeat_started.setdefault(name, time.monotonic())
            self._heartbeat[name] = (time.monotonic(), count)
        self.sample("heartbeat", name=name, count=count, **values)

    def emit(self, code, module, message, level=None, attrs=None):
        """写一条事件；ERROR/FATAL 之后立即倒出错误前窗口。"""
        if self.session is not None:
            attrs = self.session.attrs(attrs)
        method = getattr(self.writer, "event", None) or getattr(self.writer, "emit")
        try:
            ok = method(code, module, message, level=level, attrs=attrs)
        except Exception as exc:
            self.write_failures += 1
            self.last_error = repr(exc)
            ok = False
        else:
            if not ok:
                self.write_failures += 1
        effective = level or catalog.default_level(code) or "INFO"
        if effective in ("ERROR", "FATAL"):
            path = self.blackbox.snapshot("error", code)
            if path:
                try:
                    method("E-SYS-005", "blackbox", "blackbox snapshot written",
                           attrs={"code": code, "path": path})
                except Exception as exc:
                    self.write_failures += 1
                    self.last_error = repr(exc)
            else:
                self.blackbox_failures += 1
        return ok

    def health_attrs(self):
        """返回可挂在诊断事件上的当前心跳状态。"""
        with self._lock:
            now = time.monotonic()
            names = set(self._heartbeat_started) | set(self._heartbeat)
            return {"heartbeat_%s" % key: int((now - self._heartbeat.get(
                key, (self._heartbeat_started[key], None))[0]) * 1000)
                    for key in names}

    def ensure_heartbeat(self, name="main"):
        """注册尚未喂过的心跳，使看门狗能发现主循环从未启动。"""
        with self._lock:
            self._heartbeat_started.setdefault(name, time.monotonic())
