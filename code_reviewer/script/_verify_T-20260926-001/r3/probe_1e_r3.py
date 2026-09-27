# probe_1e_r3 — 复审探针: 与首轮 probe_1e 同参（单写基线 + 双进程轮转竞争）
# 差异: BASE 指向 r3/pkg（commit 45eeb04 的验证副本）; 判定增加"幸存者必须是连续后缀"
import os, sys, shutil, subprocess, re
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3\pkg"
OUT = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3"
D = os.path.join(OUT, "probe_1e")
shutil.rmtree(D, ignore_errors=True)
sys.path.insert(0, BASE)
from rmlog.writer import Writer

# 单写入者基线: 300条, max_bytes=1200, keep=3（与首轮完全同参）
w = Writer(log_dir=D, max_bytes=1200, keep=3)
for i in range(300):
    w.event("E-SYS-005", "solo", "solo line %03d pad-pad-pad" % i)
w.close()

def scan(d):
    per = {}
    halves = 0
    for f in sorted(os.listdir(d)):
        if not f.startswith("rmlog.log"):
            continue
        with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
            for l in fh:
                s = l.rstrip("\r\n")
                if not s:
                    continue
                if s.startswith("LOGV1|"):
                    m = re.search(r"\|solo\|solo line (\d+) ", s)
                    if m:
                        per.setdefault("solo", set()).add(int(m.group(1)))
                    m2 = re.search(r"\|worker\|worker (\d+) event (\d+)", s)
                    if m2:
                        per.setdefault(int(m2.group(1)), set()).add(int(m2.group(2)))
                else:
                    halves += 1
    return per, halves

def suffix_report(per):
    # 幸存条目应为连续后缀 [m..N-1]（洞 = 非淘汰性损失 = F-1 症状）
    for tag, items in per.items():
        mx = max(items); lo = min(items)
        missing = [i for i in range(lo, mx + 1) if i not in items]
        print("  tag=%s surviving=%d range=[%d..%d] holes=%d %s"
              % (tag, len(items), lo, mx, len(missing), missing[:10]))

per, halves = scan(D)
print("SINGLE-WRITER: halves=%d" % halves)
suffix_report(per)

# 双进程: 各写300条（与首轮同参: max_bytes=1200, keep 缺省 5）
D2 = os.path.join(OUT, "probe_1e_multi")
shutil.rmtree(D2, ignore_errors=True)
p1 = subprocess.Popen([sys.executable, "-m", "rmlog.worker", D2, "300", "1200"], cwd=BASE)
p2 = subprocess.Popen([sys.executable, "-m", "rmlog.worker", D2, "300", "1200"], cwd=BASE)
r1, r2 = p1.wait(), p2.wait()
per2, halves2 = scan(D2)
print("MULTI-WRITER: halves=%d rc=%d/%d" % (halves2, r1, r2))
suffix_report(per2)
print("MULTI-WRITER pids-with-survivors:", sorted(per2.keys()))
