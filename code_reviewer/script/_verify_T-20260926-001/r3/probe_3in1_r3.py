# -*- coding: utf-8 -*-
# probe_3in1_r3 — 复审动态探针: F-5(Python 不抛异常/逐条重试) + F-7(锁降级可观测) + F-9 关联
import os, sys, shutil
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3\pkg"
OUT = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3"
sys.path.insert(0, BASE)
from rmlog.writer import Writer

# ---- 1) F-5 Python: 目录被删 → event 返回 False、write_failures 计数、不抛异常; 恢复后可写 ----
d1 = os.path.join(OUT, "probe_f5_py")
shutil.rmtree(d1, ignore_errors=True)
w = Writer(log_dir=d1)
shutil.rmtree(d1)                      # 模拟目录消失
exc = None
ok1 = None
try:
    ok1 = w.event("E-SYS-005", "probe", "after dir removed")
except Exception as e:
    exc = e
print("F5-PY after-remove: ok=%s exc=%r write_failures=%d" % (ok1, exc, w.write_failures))
os.makedirs(d1, exist_ok=True)
ok2 = w.event("E-SYS-005", "probe", "after dir recreated")
print("F5-PY after-recreate: ok=%s write_failures=%d (expected recovery True)" % (ok2, w.write_failures))

# ---- 2) F-7: 轮转锁文件位置被目录占位 → Linux 轮转锁 open 失败计数（本机 nt 走写锁路径,
#         写锁 open 失败计入 write_failures —— 与处置说明口径核对） ----
d2 = os.path.join(OUT, "probe_f7_rotlock")
shutil.rmtree(d2, ignore_errors=True)
w2 = Writer(log_dir=d2, max_bytes=600, keep=3)
os.makedirs(os.path.join(d2, ".rmlog.ROTLOCK"))   # 用目录占住锁文件名
for i in range(40):
    w2.event("E-SYS-005", "probe", "f7 line %03d pad-pad-pad-pad" % i)
print("F7-NT: write_failures=%d lock_degradations=%d last_error=%r"
      % (w2.write_failures, w2.lock_degradations, w2.last_error))

# ---- 3) F-7 正常路径回归: 锁文件正常时降级计数应为 0 ----
d3 = os.path.join(OUT, "probe_f7_normal")
shutil.rmtree(d3, ignore_errors=True)
w3 = Writer(log_dir=d3, max_bytes=600, keep=3)
for i in range(60):
    w3.event("E-SYS-005", "probe", "normal line %03d pad-pad-pad-pad" % i)
print("F7-NORMAL: write_failures=%d lock_degradations=%d (expected 0/0)"
      % (w3.write_failures, w3.lock_degradations))
