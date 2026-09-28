# -*- coding: utf-8 -*-
"""T-003 R-Q3b: 重传对账工具并执行（SETUP 数据目录已生成且完好；上一步脚本被 SETUP 的 rm -rf 先删，属测试工件时序问题）。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "board_output")
os.makedirs(OUT, exist_ok=True)
SSH_DIR = os.path.dirname(os.path.abspath(__file__))

RECON = r"""
cd /root/rmlog_test/src
python3 /root/rmlog_test/rq3/q3_reconcile.py /root/rmlog_test/rq3/solo 1 300 /root/rmlog_test/rq3/multi 2 300 /root/rmlog_test/rq3/combo 3 400
"""

b = Board()
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    # 确认数据目录仍在
    rc0, out0, err0 = b.run("ls -d /root/rmlog_test/rq3/solo /root/rmlog_test/rq3/multi /root/rmlog_test/rq3/combo", timeout=30)
    print(out0, flush=True)
    if rc0 != 0:
        raise RuntimeError("rq3 data dirs missing")
    b.put(os.path.join(SSH_DIR, "q3_reconcile.py"), "/root/rmlog_test/rq3/q3_reconcile.py")
    rc, out, err = b.run(RECON, timeout=120)
    with open(os.path.join(OUT, "rq3_reconcile_raw.txt"), "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s\n[stderr]\n%s\n" % (rc, out, err))
    print("=== RECON rc=%d ===" % rc, flush=True)
    print(out, flush=True)
    if err.strip():
        print("[stderr]", err, flush=True)
    # 重打包下载（含对账脚本后的最终状态留档）
    rc3, out3, err3 = b.run(
        "cd /root/rmlog_test && tar -cf /root/rmlog_test/rq3.tar rq3 2>&1; echo TAR_EXIT=$?",
        timeout=120)
    print("TAR:", out3.strip(), err3.strip(), flush=True)
    if "TAR_EXIT=0" in out3:
        b.get("/root/rmlog_test/rq3.tar", os.path.join(OUT, "rq3_logs.tar"))
        print("DOWNLOADED rq3_logs.tar", flush=True)
finally:
    b.close()
print("RQ3B_DONE", flush=True)
