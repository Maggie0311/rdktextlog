"""T-20261001-logging-v3 P0：比赛高频数据黑匣子环形缓冲。

黑匣子只保存最近 ``capacity`` 条结构化样本，正常运行不触碰磁盘；错误发生时
才一次性刷入独立 JSONL 快照，避免高频采样拖慢控制线程。字段保持业务可读，
建议使用底盘指令、IMU、状态机、心跳、通信/电压/温度/日志统计。
"""

import json
import os
import tempfile
import threading
import time
from collections import deque


class BlackBox:
    """线程安全的最近样本缓存与错误快照写入器。"""

    def __init__(self, directory, capacity=2000):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.directory = os.path.abspath(directory)
        self.samples = deque(maxlen=capacity)
        self._lock = threading.Lock()

    def record(self, kind, **values):
        """追加一条高频样本；不做字段白名单，便于不同机器人复用。"""
        sample = {"mono_ms": int(time.monotonic() * 1000), "kind": str(kind)}
        sample.update(values)
        with self._lock:
            self.samples.append(sample)

    def snapshot(self, reason, code=None):
        """原子写出当前窗口并返回文件路径；写失败返回 ``None``。"""
        with self._lock:
            rows = list(self.samples)
        try:
            os.makedirs(self.directory, exist_ok=True)
            stamp = "%d-%d" % (int(time.time()), os.getpid())
            final = os.path.join(self.directory, "blackbox-%s.jsonl" % stamp)
            fd, temp = tempfile.mkstemp(prefix=".blackbox-", dir=self.directory, text=True)
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"reason": reason, "code": code, "count": len(rows)}, ensure_ascii=False) + "\n")
                for row in rows:
                    fh.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(temp, final)
            return final
        except OSError:
            try:
                os.unlink(temp)
            except (OSError, UnboundLocalError):
                pass
            return None
