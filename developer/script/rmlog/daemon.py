# -*- coding: utf-8 -*-
"""T-20261001-logging-v3：systemd 入口，负责启动 marker 与优雅停机。"""
import argparse
import signal
import threading
import time
import os
import subprocess

from .async_writer import AsyncWriter
from .session import Session
from .writer import Writer
from .auto import LogRuntime
from .crash import install_signal_hooks


def main(argv=None):
    p = argparse.ArgumentParser(description="rmlog 常驻服务入口示例")
    p.add_argument("directory")
    a = p.parse_args(argv)
    stop = threading.Event()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stop.set())
    session = Session("service")
    writer = AsyncWriter(Writer(log_dir=a.directory), session=session)
    runtime = LogRuntime(writer, os.path.join(a.directory, "blackbox"), session=session)
    install_signal_hooks(runtime)
    try:
        git = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                      stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.SubprocessError):
        git = "unknown"
    runtime.emit("E-INIT-000", "service", "logging service started",
                 attrs={"git": git, "power": "unknown", "session": session.id})
    try:
        while not stop.wait(1.0):
            pass
    finally:
        runtime.emit("E-SYS-005", "service", "logging service stopping")
        writer.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
