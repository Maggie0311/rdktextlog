# -*- coding: utf-8 -*-
"""T-003 R-Q1: 板端 python3 -m rmlog.selftest 全量复跑，采集全文 + 退出码。
判定标准: 退出码 0 + 'SELFTEST PASS' + 13/13（上轮 11/13 FAIL 同口径对照）。"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "board_output")
os.makedirs(OUT, exist_ok=True)

b = Board()
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    t0 = time.time()
    rc, out, err = b.run(
        "cd /root/rmlog_test/src && python3 -m rmlog.selftest /root/rmlog_test/work 2>&1; "
        "echo \"__EXIT_CODE__=$?\"",
        timeout=600)
    used = time.time() - t0
    with open(os.path.join(OUT, "rq1_selftest_raw.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)
    print("elapsed=%.1fs" % used, flush=True)
    print(out, flush=True)
    if err.strip():
        print("[stderr]", err, flush=True)
finally:
    b.close()
print("RQ1_DONE", flush=True)
