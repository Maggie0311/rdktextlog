"""T-20261001-logging-v3 P0：最小、可测的 Python 崩溃遗言路径。"""

import os
import signal


class EmergencyWriter:
    """预打开 fd 的低级遗言写入器，供单测直接调用。"""

    def __init__(self, directory):
        os.makedirs(directory, exist_ok=True)
        self.path = os.path.join(directory, "crash-%d.log" % os.getpid())
        self.fd = os.open(self.path, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o644)

    def write(self, signum):
        """只执行一次低级写；失败时吞掉异常，不反向影响崩溃处理。"""
        data = ("CRASH|signal=%d|pid=%d\n" % (int(signum), os.getpid())).encode("ascii")
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
    # 所有格式化和分配都发生在安装阶段；handler 只做 fd 写入和进程终止。
    messages = {signum: ("CRASH|signal=%d|pid=%d\n" % (signum, os.getpid())).encode("ascii")
                for signum in signals}
    fallback = b"CRASH|signal=unknown\n"

    def handler(signum, _frame):
        try:
            os.write(emergency.fd, messages.get(signum, fallback))
        finally:
            # 恢复默认动作再重抛，尽可能保留内核 core dump 行为。Python 层无法
            # 保证 handler 的完整 POSIX async-signal-safe 语义；是否生成 core 仍
            # 取决于板端 ulimit、kernel.core_pattern 和运行时配置。
            signal.signal(signum, signal.SIG_DFL)
            os.kill(os.getpid(), signum)

    for signum in signals:
        try:
            signal.signal(signum, handler)
        except (OSError, RuntimeError, ValueError):
            pass
    return emergency
