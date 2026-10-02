"""T-20261001-logging-v3 P0：Python 崩溃遗言与快照钩子。"""

import os
import signal


def install_signal_hooks(runtime, signals=None):
    """安装 SIGSEGV/SIGABRT 等钩子；先写 FATAL 遗言并倒黑匣子再恢复默认动作。"""
    signals = signals or (signal.SIGABRT, signal.SIGBUS, signal.SIGFPE, signal.SIGSEGV)

    def handler(signum, _frame):
        runtime.emit("E-SYS-005", "crash", "fatal signal captured",
                     level="FATAL", attrs={"signal": signum, "pid": os.getpid()})
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)

    for signum in signals:
        try:
            signal.signal(signum, handler)
        except (OSError, RuntimeError, ValueError):
            pass
