import os, sys
sys.path.insert(0, r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r2")
from rmlog.writer import Writer
log_dir = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r2\probe_rot"
w = Writer(log_dir=log_dir, max_bytes=1200, keep=3)
for i in range(400):
    ok = w.event("E-SYS-005", "probe", "probe line %03d pad-pad-pad-pad" % i)
    if not ok:
        print("write-failed at", i); break
w.close()
print("done")
