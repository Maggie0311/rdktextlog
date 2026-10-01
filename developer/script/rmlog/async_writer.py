# -*- coding: utf-8 -*-
"""T-20260930-005：有界异步接入层。

控制线程只执行内存入队，落盘由后台线程完成；队列满时显式丢弃并计数。
标准库实现，适用于 Linux/X5 与开发机，不能据此宣称硬实时保证。
"""
import queue
import threading
from .writer import Writer

class AsyncWriter:
    """把事件转交后台 Writer 的有界队列适配器。"""
    def __init__(self, writer=None, maxsize=1024, session=None):
        self.writer = writer or Writer()
        self.session = session
        self.queue = queue.Queue(maxsize=maxsize)
        self.dropped = 0
        self.write_failures = 0
        self.worker_failures = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="rmlog-writer", daemon=True)
        self._thread.start()

    def emit(self, code, module, message, level=None, attrs=None):
        """非阻塞入队；成功返回 True，满队列返回 False 并增加 dropped。"""
        if self.session is not None:
            attrs = self.session.attrs(attrs)
        item = (code, module, message, level, attrs)
        try:
            self.queue.put_nowait(item)
            return True
        except queue.Full:
            self.dropped += 1
            return False

    def _run(self):
        """后台消费；单条写失败不终止线程，失败计数保持可观察。"""
        while not self._stop.is_set() or not self.queue.empty():
            try:
                item = self.queue.get(timeout=0.05)
            except queue.Empty:
                continue
            try:
                if not self.writer.event(*item):
                    self.write_failures += 1
            except Exception:
                self.worker_failures += 1
            finally:
                self.queue.task_done()

    def flush(self, timeout=None):
        """等待当前队列排空；返回是否在 timeout 内排空。"""
        if timeout is None:
            self.queue.join()
            return True
        end = __import__('time').monotonic() + timeout
        while not self.queue.empty() and __import__('time').monotonic() < end:
            __import__('time').sleep(0.01)
        return self.queue.empty()

    def close(self, timeout=2.0):
        """停止后台线程并尽力排空，返回线程是否退出。"""
        self._stop.set()
        self.flush(timeout)
        self._thread.join(timeout=max(timeout, 0.0))
        return not self._thread.is_alive()
