import os, sys, shutil, subprocess, re
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r2"
sys.path.insert(0, BASE)

def scan(d):
    per, halves, frag = {}, 0, {}
    for f in sorted(os.listdir(d)):
        if not f.startswith("rmlog.log"): continue
        n = 0
        with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
            for l in fh:
                s = l.rstrip("\r\n")
                if not s: continue
                if s.startswith("LOGV1|"):
                    n += 1
                    m2 = re.search(r"\|worker\|worker (\d+) event (\d+)", s)
                    if m2: per.setdefault(int(m2.group(1)), set()).add(int(m2.group(2)))
                else:
                    halves += 1
        frag[f] = n
    return per, halves, frag

def report(tag, D, per, halves, frag, written_per_worker):
    print(tag, "fragments:", frag)
    print(tag, "halves=%d" % halves)
    allpid = set()
    for pid, items in per.items():
        mx = max(items); lo = min(items)
        holes = [i for i in range(lo, mx+1) if i not in items]
        print(tag, "pid=%s surviving=%d range=[%d..%d] holes=%d %s" % (pid, len(items), lo, mx, len(holes), holes[:8]))
    # 幸存 pid 集合 vs 预期两个
    import glob as g
    print(tag, "pids-with-survivors:", sorted(per.keys()))

# 对照组: 不轮转 (max_bytes=8MB 默认), 2x300
D1 = os.path.join(BASE, "probe_1f_norot")
shutil.rmtree(D1, ignore_errors=True)
p1 = subprocess.Popen([sys.executable, "-m", "rmlog.worker", D1, "300"], cwd=BASE)
p2 = subprocess.Popen([sys.executable, "-m", "rmlog.worker", D1, "300"], cwd=BASE)
r1, r2 = p1.wait(), p2.wait()
per, halves, frag = scan(D1)
tot = sum(frag.values())
print("NO-ROTATION: rc=%d/%d total=%d/600 halves=%d" % (r1, r2, tot, halves))
report("[norot]", D1, per, halves, frag, 300)

# 复跑组: 轮转 2x300 (与 1e 同参数)
D2 = os.path.join(BASE, "probe_1g_rot")
shutil.rmtree(D2, ignore_errors=True)
q1 = subprocess.Popen([sys.executable, "-m", "rmlog.worker", D2, "300", "1200"], cwd=BASE)
q2 = subprocess.Popen([sys.executable, "-m", "rmlog.worker", D2, "300", "1200"], cwd=BASE)
s1, s2 = q1.wait(), q2.wait()
per2, halves2, frag2 = scan(D2)
tot2 = sum(frag2.values())
print("ROTATION-RERUN: rc=%d/%d total=%d halves=%d" % (s1, s2, tot2, halves2))
report("[rot2]", D2, per2, halves2, frag2, 300)
