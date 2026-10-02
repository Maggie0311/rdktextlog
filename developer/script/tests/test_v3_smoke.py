"""T-20261001-logging-v3：P0/P1/P2 开发机可测烟测（不宣称板端事实）。"""

import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from rmlog.auto import LogRuntime
from rmlog.blackbox import BlackBox
from rmlog.code_map import decode, encode, hex_code
from rmlog.crash import EmergencyWriter
from rmlog.monitors import CommStats, DmesgMonitor, HeartbeatWatchdog
from rmlog.resources import ResourceMonitor
from rmlog.writer import Writer
from rmlog.format import parse_line


def main():
    work = tempfile.mkdtemp(prefix="rmlog-v3-")
    writer = Writer(log_dir=work, max_bytes=1024 * 1024)
    runtime = LogRuntime(writer, os.path.join(work, "blackbox"), capacity=8)
    runtime.sample("chassis", vx=1.2, vy=0.0, wz=0.1)
    runtime.sample("imu", yaw=3.0, pitch=0.1, roll=0.2)
    runtime.sample("custom", values={1, 2}, raw=b"abc", opaque=object())
    runtime.heartbeat("main", count=1)
    assert encode("E-INIT-000") is not None
    assert decode(encode("E-INIT-000")) == "E-INIT-000"
    assert hex_code("E-COMM-004") == "0x223004"
    comm = CommStats(runtime, "spi", fail_threshold=2, window=2)
    comm.failure("timeout")
    comm.failure("timeout")
    comm.success()
    comm.failure("timeout")
    assert comm.consecutive_failures == 1
    ResourceMonitor(runtime, provider=lambda: {"temp_mdeg": 90000,
                                                "voltage_mv": 12000,
                                                "memory_available_kb": 1000}).check_once()
    assert ResourceMonitor(runtime, provider=lambda: (_ for _ in ()).throw(RuntimeError("probe"))).check_once() == {}
    DmesgMonitor(runtime, source=["spi controller error\n", "ordinary line\n"]).run()
    lines = []
    for name in os.listdir(work):
        if name == "rmlog.log":
            lines.extend(open(os.path.join(work, name), encoding="utf8"))
    events = [parse_line(line) for line in lines]
    assert any(event and event["code"] == "E-COMM-004" for event in events)
    assert os.path.isdir(os.path.join(work, "blackbox"))
    assert any(name.endswith(".jsonl") for name in os.listdir(os.path.join(work, "blackbox")))
    bb = BlackBox(os.path.join(work, "bb"), capacity=2)
    bb.record("opaque", obj=object())
    first, second = bb.snapshot("x"), bb.snapshot("x")
    assert first != second and os.path.exists(first) and os.path.exists(second)
    emergency = EmergencyWriter(os.path.join(work, "crash"))
    emergency.write(6)
    emergency.close()
    assert "CRASH|signal=6" in open(emergency.path, encoding="ascii").read()
    watchdog = HeartbeatWatchdog(runtime, name="never", timeout=0.001, interval=0.001)
    watchdog.start()
    import time
    time.sleep(0.01)
    watchdog.stop()
    assert runtime.health_attrs()["heartbeat_never"] >= 1
    stats = subprocess.check_output([sys.executable, os.path.join(ROOT, "rmlog_read.py"),
                                    "stats", os.path.join(work, "rmlog.log")], text=True)
    assert "E-COMM-004" in stats and "总事件" in stats
    subprocess.check_call([sys.executable, "-m", "rmlog.gen_code"], cwd=ROOT,
                          env=dict(os.environ, PYTHONPATH=ROOT))
    print("V3 SMOKE PASS bit-map blackbox monitors stats schema")


if __name__ == "__main__":
    main()
