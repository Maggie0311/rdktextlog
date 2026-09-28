# -*- coding: utf-8 -*-
"""T-003 步骤 1b: 核对板端副本布局 + 逐文件 md5 采集（包根 = /root/rmlog_test/src）。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "board_output")
os.makedirs(OUT, exist_ok=True)

b = Board()
log = []
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    rc, out, err = b.run("ls /root/rmlog_test/src", timeout=30)
    log.append("=== ls src (rc=%d) ===\n%s" % (rc, out))
    print(out, flush=True)
    rc2, out2, err2 = b.run(
        "cd /root/rmlog_test/src && "
        "find . -type f ! -path '*__pycache__*' -print0 | sort -z | xargs -0 md5sum",
        timeout=120)
    log.append("=== remote md5 (rc=%d) ===\n%s" % (rc2, out2))
    with open(os.path.join(OUT, "remote_md5.txt"), "w", encoding="utf-8") as fh:
        fh.write(out2)
    if err2.strip():
        log.append("[remote stderr]\n%s" % err2)
        print("[remote stderr]", err2, flush=True)
    print("md5 lines:", len(out2.strip().splitlines()), flush=True)
finally:
    b.close()
with open(os.path.join(OUT, "r1b_md5_log.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(log) + "\n")
print("R1B_DONE", flush=True)
