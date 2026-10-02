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
        self._snapshot_seq = 0

    @staticmethod
    def _safe_repr(value):
        """返回确定为字符串的降级表示，避免深层对象再次进入 JSON。"""
        try:
            result = repr(value)
            return result if isinstance(result, str) else "<unserializable>"
        except Exception:
            return "<unserializable>"

    @staticmethod
    def _safe_value(value, depth=0):
        """把业务对象转换成不会让取证路径抛异常的 JSON 值。"""
        if depth > 4:
            return BlackBox._safe_repr(value)
        if value is None or isinstance(value, (bool, int, float, str)):
            return value
        if isinstance(value, (bytes, bytearray, memoryview)):
            return bytes(value).hex()
        if isinstance(value, dict):
            result = {}
            for key, item in value.items():
                try:
                    safe_key = str(BlackBox._safe_value(key, depth + 1))
                except Exception:
                    safe_key = "<unserializable-key>"
                result[safe_key] = BlackBox._safe_value(item, depth + 1)
            return result
        if isinstance(value, (list, tuple, set, frozenset)):
            return [BlackBox._safe_value(v, depth + 1) for v in value]
        tolist = getattr(value, "tolist", None)
        if callable(tolist):
            try:
                return BlackBox._safe_value(tolist(), depth + 1)
            except Exception:
                pass
        return BlackBox._safe_repr(value)

    def record(self, kind, **values):
        """追加一条高频样本；不做字段白名单，便于不同机器人复用。"""
        try:
            safe_kind = str(kind)
        except Exception:
            safe_kind = "<unserializable-kind>"
        sample = {"mono_ms": int(time.monotonic() * 1000), "kind": safe_kind}
        sample.update({key: self._safe_value(value) for key, value in values.items()})
        with self._lock:
            self.samples.append(sample)

    def snapshot(self, reason, code=None):
        """原子写出当前窗口并返回文件路径；写失败返回 ``None``。"""
        with self._lock:
            rows = list(self.samples)
        try:
            os.makedirs(self.directory, exist_ok=True)
            with self._lock:
                self._snapshot_seq += 1
                sequence = self._snapshot_seq
            stamp = "%d-%d-%d-%d" % (int(time.time()), time.monotonic_ns(), os.getpid(), sequence)
            final = os.path.join(self.directory, "blackbox-%s.jsonl" % stamp)
            fd, temp = tempfile.mkstemp(prefix=".blackbox-", dir=self.directory, text=True)
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                header = {"reason": self._safe_value(reason), "code": self._safe_value(code),
                          "count": len(rows)}
                fh.write(json.dumps(header, ensure_ascii=False) + "\n")
                for row in rows:
                    fh.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
                fh.flush()
                os.fsync(fh.fileno())
            os.replace(temp, final)
            return final
        except Exception:
            try:
                os.unlink(temp)
            except (OSError, UnboundLocalError):
                pass
            return None
