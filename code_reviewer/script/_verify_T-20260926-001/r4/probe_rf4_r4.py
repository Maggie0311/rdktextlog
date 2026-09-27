# -*- coding: utf-8 -*-
# probe_rf4_r4 — RF-4 复审动态探针（reviewer 副本, r4）:
# 1) Windows 写锁文件路径被同名目录占位 → 连写 40 条:
#    期望（RF-4 修复后）: 40 条全部落盘、event 全部 True、
#    write_failures=0（不再误计）、lock_degradations=40（改道正确）。
#    （修复前该场景实测为 write_failures=40 / lock_degradations=0 —— r3 probe_3in1。）
# 2) 正常锁文件路径回归: 60 条 → write_failures=0 / lock_degradations=0。
import os
import shutil
import sys

BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r4\pkg\developer\script"
OUT = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r4"
sys.path.insert(0, BASE)
from rmlog.writer import Writer

# ---- 1) 占位场景（RF-4 修复点） ----
d2 = os.path.join(OUT, "probe_rf4_rotlock")
shutil.rmtree(d2, ignore_errors=True)
w2 = Writer(log_dir=d2, max_bytes=600, keep=3)
os.makedirs(os.path.join(d2, ".rmlog.ROTLOCK"))   # 用目录占住锁文件名
oks = [w2.event("E-SYS-005", "probe", "rf4 line %03d pad-pad-pad-pad" % i)
       for i in range(40)]
main_log = os.path.join(d2, "rmlog.log")
visible = 0
if os.path.exists(main_log):
    with open(main_log, encoding="utf-8", errors="replace") as fh:
        visible = sum(1 for ln in fh if ln.strip())
print("RF4-PLACEHOLDER: ok=%d/40 visible=%d write_failures=%d lock_degradations=%d last_error_set=%s"
      % (sum(1 for x in oks if x), visible, w2.write_failures,
         w2.lock_degradations, w2.last_error is not None))

# ---- 2) 正常路径回归 ----
d3 = os.path.join(OUT, "probe_rf4_normal")
shutil.rmtree(d3, ignore_errors=True)
w3 = Writer(log_dir=d3, max_bytes=600, keep=3)
oks3 = [w3.event("E-SYS-005", "probe", "normal line %03d pad-pad-pad-pad" % i)
        for i in range(60)]
print("RF4-NORMAL: ok=%d/60 write_failures=%d lock_degradations=%d (expect 0/0)"
      % (sum(1 for x in oks3 if x), w3.write_failures, w3.lock_degradations))
