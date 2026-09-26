import os, sys, shutil, subprocess, re
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r2"
D = os.path.join(BASE, "probe_1e")
shutil.rmtree(D, ignore_errors=True)
sys.path.insert(0, BASE)
from rmlog.writer import Writer

# 单写入者基线: 300条, max_bytes=1200, keep=3
w = Writer(log_dir=D, max_bytes=1200, keep=3)
for i in range(300):
    w.event("E-SYS-005", "solo", "solo line %03d pad-pad-pad" % i)
w.close()

def scan(d):
    per = {}   # tag -> set of i
    halves = 0
    for f in sorted(os.listdir(d)):
        if not f.startswith("rmlog.log"): continue
        with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
            for l in fh:
                s = l.rstrip("\r\n")
                if not s: continue
                if s.startswith("LOGV1|"):
                    m = re.search(r"\|solo\|solo line (\d+) ", s)
                    if m: per.setdefault("solo", set()).add(int(m.group(1)))
                    m2 = re.search(r"\|worker\|worker (\d+) event (\d+)", s)
                    if m2: per.setdefault(int(m2.group(1)), set()).add(int(m2.group(2)))
                else:
                    halves += 1
    return per, halves

def gaps_ok(per):
    # 每个写入者的幸存条目应为连续后缀 [m..N-1]
    report = []
    for tag, items in per.items():
        mx = max(items); missing = [i for i in range(min(items), mx+1) if i not in items]
        report.append((tag, len(items), min(items), mx, missing))
    return report

per, halves = scan(D)
print("SINGLE-WRITER: halves=%d" % halves)
for tag, n, lo, hi, missing in gaps_ok(per):
    print("  tag=%s surviving=%d range=[%d..%d] holes=%d %s" % (tag, n, lo, hi, len(missing), missing[:10]))

# 双进程: 各写300条 (超出 keep 容量, 淘汰由设计承担; 检验空洞=非设计损失)
D2 = os.path.join(BASE, "probe_1e_multi")
shutil.rmtree(D2, ignore_errors=True)
p1 = subprocess.Popen([sys.executable, "-m", "rmlog.worker", D2, "300", "1200"], cwd=BASE)
p2 = subprocess.Popen([sys.executable, "-m", "rmlog.worker", D2, "300", "1200"], cwd=BASE)
r1, r2 = p1.wait(), p2.wait()
per2, halves2 = scan(D2)
print("MULTI-WRITER: halves=%d rc=%d/%d" % (halves2, r1, r2))
for tag, n, lo, hi, missing in gaps_ok(per2):
    print("  pid=%s surviving=%d range=[%d..%d] holes=%d %s" % (tag, n, lo, hi, len(missing), missing[:10]))
