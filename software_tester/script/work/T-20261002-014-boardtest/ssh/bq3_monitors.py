# -*- coding: utf-8 -*-
"""bq3_monitors.py — BQ3 板端监控层真实数据源读取（事实采集，非语义适配）。

本脚本是 software_tester 的测试辅助（非 developer 源码），在板端 /tmp 下运行，
只调用被测库 rmlog 的公开入口（LogRuntime / ResourceMonitor / DmesgMonitor），
读取真实 dmesg / sysfs / procfs，逐字打印观察结果，不做任何改写。
"""
import json
import os
import sys
import threading
import time

ROOT = "/tmp/rmlog-v3-test"
sys.path.insert(0, ROOT)

from rmlog.auto import LogRuntime       # noqa: E402
from rmlog.writer import Writer         # noqa: E402
from rmlog.resources import ResourceMonitor  # noqa: E402
from rmlog.monitors import DmesgMonitor      # noqa: E402

work = os.path.join(ROOT, "bq3-work")
os.makedirs(work, exist_ok=True)
writer = Writer(log_dir=work)
runtime = LogRuntime(writer, os.path.join(work, "blackbox"), capacity=64)

print("=== 1) raw sysfs/procfs ground truth (只读) ===")
print("--- ls /sys/class/thermal ---")
for name in sorted(os.listdir("/sys/class/thermal")):
    print("  " + name)
print("--- thermal zone temp 值 ---")
for name in sorted(os.listdir("/sys/class/thermal")):
    p = os.path.join("/sys/class/thermal", name, "temp")
    if os.path.exists(p):
        try:
            print("  %s/temp = %s" % (name, open(p, encoding="ascii").read().strip()))
        except OSError as exc:
            print("  %s/temp 读取失败: %r" % (name, exc))
print("--- ls /sys/class/power_supply ---")
if os.path.isdir("/sys/class/power_supply"):
    names = sorted(os.listdir("/sys/class/power_supply"))
    print("  " + (" ".join(names) if names else "(空)"))
else:
    print("  (目录不存在)")
print("--- /proc/meminfo MemTotal/MemAvailable ---")
for line in open("/proc/meminfo", encoding="ascii"):
    if line.startswith(("MemTotal:", "MemAvailable:")):
        print("  " + line.rstrip())

print("=== 2) ResourceMonitor.check_once() 真实 provider ===")
rm = ResourceMonitor(runtime)
vals = rm.check_once()
print("ResourceMonitor.values = " + json.dumps(vals, sort_keys=True))
print("runtime.write_failures = %d" % runtime.write_failures)
print("runtime.last_error = %r" % runtime.last_error)

print("=== 3) DmesgMonitor 真实 dmesg --follow (有界 2s) ===")
dm = DmesgMonitor(runtime)
t = threading.Thread(target=dm.run, daemon=True)
t.start()
time.sleep(2.0)
dm.stop()
t.join(3.0)
print("DmesgMonitor 线程在 stop 后仍存活 = %s" % t.is_alive())

writer.close()
print("=== 4) rmlog.log 事件（本脚本会话内产出） ===")
log = os.path.join(work, "rmlog.log")
if os.path.exists(log):
    print(open(log, encoding="utf-8", errors="replace").read(), end="")
else:
    print("(rmlog.log 不存在)")
print("BQ3 DONE")
