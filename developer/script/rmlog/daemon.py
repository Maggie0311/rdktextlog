# -*- coding: utf-8 -*-
"""持续运行的 systemd 入口示例；真实业务应在 loop 中接入自己的采集逻辑。"""
import argparse
import signal
import threading
import time

from .async_writer import AsyncWriter
from .session import Session
from .writer import Writer


def main(argv=None):
    p = argparse.ArgumentParser(description="rmlog 常驻服务入口示例")
    p.add_argument("directory")
    a = p.parse_args(argv)
    stop = threading.Event()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stop.set())
    session = Session("service")
    writer = AsyncWriter(Writer(log_dir=a.directory), session=session)
    writer.emit("E-INIT-000", "service", "logging service started")
    try:
        while not stop.wait(1.0):
            pass
    finally:
        writer.emit("E-SYS-005", "service", "logging service stopping")
        writer.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
