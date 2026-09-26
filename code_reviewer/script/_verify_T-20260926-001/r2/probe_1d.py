import os, sys, shutil, subprocess
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r2"
sys.path.insert(0, BASE)

def count_all(d):
    tot, halves, seqs = 0, 0, []
    for f in sorted(os.listdir(d)):
        if not f.startswith("rmlog.log"): continue
        with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
            for l in fh:
                s = l.rstrip("\r\n")
                if not s: continue
                tot += 1
                if s.startswith("LOGV1|"):
                    seqs.append(int(s.split("|")[1]))
                else:
                    halves += 1
    return tot, halves, seqs

# ---- 单进程基线: 2 writer 实例顺序写, 等效总事件数 200 ----
D1 = os.path.join(BASE, "probe_1d_single")
shutil.rmtree(D1, ignore_errors=True)
from rmlog.writer import Writer
w1 = Writer(log_dir=D1, max_bytes=1200, keep=3)
for i in range(200):
    w1.event("E-SYS-005", "s", "single line %03d pad-pad-pad" % i)
w1.close()
t1, h1, s1 = count_all(D1)
print("SINGLE : total=%d halves=%d seqRange=[%d..%d] (written=200)" % (t1, h1, min(s1), max(s1)))

# ---- 双进程: 同一目录, 同参数 max_bytes=1200 ----
D2 = os.path.join(BASE, "probe_1d_multi")
shutil.rmtree(D2, ignore_errors=True)
rc = subprocess.call([sys.executable, "-m", "rmlog.worker", D2, "100", "1200"],
                     cwd=BASE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
rc2 = subprocess.call([sys.executable, "-m", "rmlog.worker", D2, "100", "1200"],
                      cwd=BASE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
t2, h2, s2 = count_all(D2)
print("MULTI  : total=%d halves=%d worker_rc=%d/%d (written=200)" % (t2, h2, rc, rc2))
print("VERDICT: single=%d multi=%d -> multi lost %d lines vs baseline" % (t1, t2, t1 - t2))
