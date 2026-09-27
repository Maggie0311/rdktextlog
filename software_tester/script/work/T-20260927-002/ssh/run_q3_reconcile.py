# -*- coding: utf-8 -*-
"""Q3 对账补跑：上传对账脚本并针对已存在的 q3 目录执行。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "board_output")
SSH_DIR = os.path.dirname(os.path.abspath(__file__))

b = Board()
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    b.run("mkdir -p /root/rmlog_test/q3", timeout=30)
    b.put(os.path.join(SSH_DIR, "q3_reconcile.py"), "/root/rmlog_test/q3/q3_reconcile.py")
    rc, out, err = b.run(
        "cd /root/rmlog_test/src && python3 /root/rmlog_test/q3/q3_reconcile.py "
        "/root/rmlog_test/q3/solo 1 300 /root/rmlog_test/q3/multi 2 300 /root/rmlog_test/q3/combo 3 400",
        timeout=120)
    with open(os.path.join(OUT, "q3_reconcile_raw.txt"), "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s\n[stderr]\n%s\n" % (rc, out, err))
    print("rc=%d" % rc, flush=True)
    print(out, flush=True)
    if err.strip():
        print("[stderr]", err, flush=True)
finally:
    b.close()
print("Q3_RECON_DONE", flush=True)
