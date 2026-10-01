# -*- coding: utf-8 -*-
# Maintainer archive note (v001): source snapshot 3148fed; comments only.
"""T-20260930-005：比赛/启动会话标识，便于跨文件和 systemd 查询。"""
import os, time, uuid

class Session:
    """生成稳定的本次启动 session_id，并在事件属性中注入它。"""
    def __init__(self, name="match", session_id=None):
        self.id = session_id or "%s-%s-%s" % (name, time.strftime('%Y%m%d-%H%M%S'), uuid.uuid4().hex[:8])
        self.pid = os.getpid()

    def attrs(self, attrs=None):
        """返回不修改调用者字典的会话属性。"""
        result = dict(attrs or {})
        result.setdefault("session", self.id)
        result.setdefault("pid", self.pid)
        return result

    def event(self, writer, code, module, message, level=None, attrs=None):
        """将事件实际写入给定 writer，并注入本会话属性。"""
        return writer.event(code, module, message, level=level,
                            attrs=self.attrs(attrs))

    def wrap(self, writer):
        """返回轻量会话视图，适合把 writer 注入业务组件。"""
        session = self
        class _Bound:
            def event(self, code, module, message, level=None, attrs=None):
                return session.event(writer, code, module, message, level, attrs)
        return _Bound()
