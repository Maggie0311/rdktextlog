import os, sys, shutil
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r2"
D = os.path.join(BASE, "probe_rot_mixed")
shutil.rmtree(D, ignore_errors=True)
sys.path.insert(0, os.path.join(BASE))
from rmlog.writer import Writer

p1 = Writer(log_dir=D, max_bytes=1200, keep=3)   # 进程1视角: 小上限, 频繁轮转
p2 = Writer(log_dir=D, max_bytes=100000, keep=3) # 进程2视角: 大上限 (两个进程各自合理的配置)

# 阶段A: p1 写满触发轮转 (p1 close旧fd+rename+reopen; p2 的fd仍绑旧inode)
for i in range(40):
    p1.event("E-SYS-005", "p1", "p1 line %03d pad-pad-pad" % i)
# 阶段B: p2 继续写 —— 观察它的行落在哪里
for i in range(10):
    p2.event("E-SYS-005", "p2", "p2 line %03d pad-pad-pad" % i)
# 阶段C: p1 再写一点, p2 继续写
for i in range(40, 60):
    p1.event("E-SYS-005", "p1", "p1 line %03d pad-pad-pad" % i)
for i in range(10, 20):
    p2.event("E-SYS-005", "p2", "p2 line %03d pad-pad-pad" % i)

def scan(d):
    out = {}
    for f in sorted(os.listdir(d)):
        path = os.path.join(d, f)
        with open(path, encoding="utf-8", errors="replace") as fh:
            ls = [l for l in fh if l.startswith("LOGV1|")]
        p1n = sum(1 for l in ls if "|p1|" in l)
        p2n = sum(1 for l in ls if "|p2|" in l)
        out[f] = (len(ls), p1n, p2n)
    return out

print("fragments after phase A-D:")
for f, (tot, a, b) in scan(D).items():
    print("  %-14s total=%-4d p1=%-4d p2=%-4d" % (f, tot, a, b))
p1_written, p2_written = 60, 20
tot_p1 = sum(v[1] for v in scan(D).values())
tot_p2 = sum(v[2] for v in scan(D).values())
print("p1 written=%d present=%d | p2 written=%d present=%d" % (p1_written, tot_p1, p2_written, tot_p2))
p1.close(); p2.close()
