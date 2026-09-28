# -*- coding: utf-8 -*-
"""T-003 R-Q3: 多进程×轮转组合对账回归确认（与上轮 T-002 同参: 3 worker×400 keep=20 + 2×300 keep 缺省 + solo 基线）。
判定标准（同上轮）: keep 足够组 写成功==可见 且 无半行/无全灭/无缺号; keep 小组 无全灭 且 幸存为连续后缀。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "board_output")
os.makedirs(OUT, exist_ok=True)
SSH_DIR = os.path.dirname(os.path.abspath(__file__))

SETUP = r"""
set -e
rm -rf /root/rmlog_test/rq3
mkdir -p /root/rmlog_test/rq3
cd /root/rmlog_test/src
echo "=== SOLO baseline: 1 writer x300 max_bytes=1200 keep=3 ==="
python3 -c "
import sys; sys.path.insert(0,'/root/rmlog_test/src')
from rmlog.writer import Writer
w=Writer(log_dir='/root/rmlog_test/rq3/solo', max_bytes=1200, keep=3)
for i in range(300):
    w.event('E-SYS-005','solo','solo line %03d pad-pad-pad' % i)
w.close()
print('solo done')
"
echo "=== MULTI: 2 workers x300 max_bytes=1200 (keep default 5) ==="
python3 -m rmlog.worker /root/rmlog_test/rq3/multi 300 1200 >/root/rmlog_test/rq3/multi.w1.log 2>&1 & P1=$!
python3 -m rmlog.worker /root/rmlog_test/rq3/multi 300 1200 >/root/rmlog_test/rq3/multi.w2.log 2>&1 & P2=$!
wait $P1; R1=$?
wait $P2; R2=$?
echo "MULTI_EXIT=$R1/$R2"
echo "=== COMBO: 3 workers x400 max_bytes=8000 keep=20 (AC5 组合参) ==="
python3 -m rmlog.worker /root/rmlog_test/rq3/combo 400 8000 20 >/root/rmlog_test/rq3/combo.w1.log 2>&1 & C1=$!
python3 -m rmlog.worker /root/rmlog_test/rq3/combo 400 8000 20 >/root/rmlog_test/rq3/combo.w2.log 2>&1 & C2=$!
python3 -m rmlog.worker /root/rmlog_test/rq3/combo 400 8000 20 >/root/rmlog_test/rq3/combo.w3.log 2>&1 & C3=$!
wait $C1; S1=$?
wait $C2; S2=$?
wait $C3; S3=$?
echo "COMBO_EXIT=$S1/$S2/$S3"
echo "=== worker stderr (如有写失败) ==="
cat /root/rmlog_test/rq3/multi.w1.log /root/rmlog_test/rq3/multi.w2.log /root/rmlog_test/rq3/combo.w1.log /root/rmlog_test/rq3/combo.w2.log /root/rmlog_test/rq3/combo.w3.log
echo "=== file listing ==="
ls -l /root/rmlog_test/rq3/solo /root/rmlog_test/rq3/multi /root/rmlog_test/rq3/combo
"""

RECON = r"""
cd /root/rmlog_test/src
python3 /root/rmlog_test/rq3/q3_reconcile.py /root/rmlog_test/rq3/solo 1 300 /root/rmlog_test/rq3/multi 2 300 /root/rmlog_test/rq3/combo 3 400
"""

b = Board()
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    b.run("mkdir -p /root/rmlog_test/rq3", timeout=30)
    b.put(os.path.join(SSH_DIR, "q3_reconcile.py"), "/root/rmlog_test/rq3/q3_reconcile.py")
    rc, out, err = b.run(SETUP, timeout=300)
    with open(os.path.join(OUT, "rq3_probe_raw.txt"), "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s\n[stderr]\n%s\n" % (rc, out, err))
    print("=== SETUP rc=%d ===" % rc, flush=True)
    print(out, flush=True)
    if err.strip():
        print("[stderr]", err, flush=True)

    rc2, out2, err2 = b.run(RECON, timeout=120)
    with open(os.path.join(OUT, "rq3_reconcile_raw.txt"), "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s\n[stderr]\n%s\n" % (rc2, out2, err2))
    print("=== RECON rc=%d ===" % rc2, flush=True)
    print(out2, flush=True)
    if err2.strip():
        print("[stderr]", err2, flush=True)

    # 打包下载对账目录留档
    rc3, out3, err3 = b.run(
        "cd /root/rmlog_test && tar -cf /root/rmlog_test/rq3.tar rq3 2>&1; echo TAR_EXIT=$?",
        timeout=120)
    print("TAR:", out3.strip(), err3.strip(), flush=True)
    if "TAR_EXIT=0" in out3:
        b.get("/root/rmlog_test/rq3.tar", os.path.join(OUT, "rq3_logs.tar"))
        print("DOWNLOADED rq3_logs.tar", flush=True)
finally:
    b.close()
print("RQ3_DONE", flush=True)
