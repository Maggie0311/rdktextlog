# -*- coding: utf-8 -*-
"""T-20261001-logging-v3：systemd 入口，负责启动 marker 与优雅停机。"""
import argparse
import signal
import threading
import time
import os
import subprocess
import socket

from .async_writer import AsyncWriter
from .session import Session
from .writer import Writer
from .auto import LogRuntime
from .crash import install_signal_hooks
from .monitors import HeartbeatWatchdog


def sd_notify(message):
    """向 systemd 可选发送通知；没有 NOTIFY_SOCKET 时静默返回 False。"""
    address = os.environ.get("NOTIFY_SOCKET")
    if not address:
        return False
    if address.startswith("@"):
        address = "\0" + address[1:]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        sock.connect(address)
        sock.send(message.encode("utf-8"))
        return True
    except OSError:
        return False
    finally:
        sock.close()


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
    install_signal_hooks(runtime, directory=os.path.join(a.directory, "crash"))
    watchdog = HeartbeatWatchdog(runtime, timeout=1.5, interval=0.1)
    watchdog.start()
    try:
        git = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                      stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.SubprocessError):
        git = "unknown"
    runtime.emit("E-INIT-000", "service", "logging service started",
                 attrs={"git": git, "power": "unknown", "session": session.id})
    sd_notify("READY=1")
    try:
        while not stop.wait(0.5):
            runtime.heartbeat("main")
            sd_notify("WATCHDOG=1")
    finally:
        watchdog.stop()
        sd_notify("STOPPING=1")
        runtime.emit("E-SYS-005", "service", "logging service stopping")
        writer.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
