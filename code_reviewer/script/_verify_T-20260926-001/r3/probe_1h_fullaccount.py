# probe_1h_fullaccount — 复审新增探针: F-1 不变量直接对账
# 2 worker x 300 条, max_bytes=1200, keep=60（链槽位 61 > 总轮转次数 ~53,
# 全程无正常淘汰 → "写成功 == 磁盘可见"必须精确成立, 无任何缺号）
# 同时核对: 无半行、无 (wid,i) 重复、每个 worker 0..299 全齐、worker 退出码全 0。
import os, sys, shutil, subprocess, re
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3\pkg"
OUT = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3"
D = os.path.join(OUT, "probe_1h_fullaccount")
shutil.rmtree(D, ignore_errors=True)
sys.path.insert(0, BASE)

KEEP = 60
procs = [subprocess.Popen(
    [sys.executable, "-m", "rmlog.worker", D, "300", "1200", str(KEEP)],
    cwd=BASE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(2)]
rcs = []
for p in procs:
    out, err = p.communicate(timeout=180)
    rcs.append(p.returncode)
    if p.returncode != 0:
        print("WORKER FAIL rc=%d err=%s" % (p.returncode, err.decode("utf-8", "replace")[:300]))

per = {}
halves = 0
dup = 0
files = []
for f in sorted(os.listdir(D)):
    if not (f == "rmlog.log" or f.startswith("rmlog.log.")):
        continue
    files.append(f)
    with open(os.path.join(D, f), encoding="utf-8", errors="replace") as fh:
        for l in fh:
            s = l.rstrip("\r\n")
            if not s:
                continue
            if not s.startswith("LOGV1|"):
                halves += 1
                continue
            m = re.search(r"\|worker\|worker (\d+) event (\d+)", s)
            if m:
                key = (int(m.group(1)), int(m.group(2)))
                if key in per:
                    dup += 1
                per[key] = f

expect = {(pid, i) for pid in (procs[0].pid, procs[1].pid) for i in range(300)}
got = set(per.keys())
missing = expect - got
extra = got - expect
print("rc=%s halves=%d dup=%d files=%d visible=%d expect=%d"
      % (rcs, halves, dup, len(files), len(got), len(expect)))
print("missing=%d %s" % (len(missing), sorted(missing)[:8]))
print("extra=%d %s" % (len(extra), sorted(extra)[:8]))
ok = (rcs == [0, 0] and halves == 0 and dup == 0 and not missing and not extra
      and len(got) == 600)
print("FULL-ACCOUNT: %s" % ("PASS" if ok else "FAIL"))
