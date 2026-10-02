"""T-20261001-logging-v3 P0：最小、可测的 Python 崩溃遗言路径。"""

import os
import signal
import time


class EmergencyWriter:
    """预打开 fd 的低级遗言写入器，供单测直接调用。"""

    def __init__(self, directory):
        os.makedirs(directory, exist_ok=True)
        self.path = os.path.join(directory, "crash-%d.log" % os.getpid())
        self.fd = os.open(self.path, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o644)

    def write(self, signum):
        """只执行一次低级写；失败时吞掉异常，不反向影响崩溃处理。"""
        data = ("CRASH|signal=%d|pid=%d|mono_ns=%d\n" %
                (int(signum), os.getpid(), time.monotonic_ns())).encode("ascii")
        try:
            os.write(self.fd, data)
        except (OSError, ValueError):
            pass

    def close(self):
        try:
            os.close(self.fd)
        except OSError:
            pass


def install_signal_hooks(runtime, signals=None, directory=None):
    """安装最小遗言钩子；处理器不触碰 runtime。"""
    del runtime  # 保留旧签名，避免在 handler 中调用复杂日志路径
    emergency = EmergencyWriter(directory or ".")
    signals = signals or (signal.SIGABRT, signal.SIGBUS, signal.SIGFPE, signal.SIGSEGV)

    def handler(signum, _frame):
        emergency.write(signum)
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)

    for signum in signals:
        try:
            signal.signal(signum, handler)
        except (OSError, RuntimeError, ValueError):
            pass
    return emergency
