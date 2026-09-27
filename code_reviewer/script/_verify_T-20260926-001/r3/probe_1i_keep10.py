# probe_1i_keep10 — 抽查 developer 1010 轮 FAIL 的"参数误校准"论证
# 用例: 与 selftest 完全同参（3 worker x 400, max_bytes=8000）但 keep=10（1010 轮的参数）
# 预期（若论证成立）: 磁盘可见 ≈ 810-820（= 正常链容量淘汰）, 各 worker 幸存为
#   连续后缀（从最老端整文件淘汰）, 无半行、无中途缺号、无 worker 全灭 ——
#   即 FAIL 是"keep 太小导致整文件正常淘汰", 不是协议销毁。
import os, sys, shutil, subprocess, re
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3\pkg"
OUT = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3"
D = os.path.join(OUT, "probe_1i_keep10")
shutil.rmtree(D, ignore_errors=True)
sys.path.insert(0, BASE)

procs = [subprocess.Popen(
    [sys.executable, "-m", "rmlog.worker", D, "400", "8000", "10"],
    cwd=BASE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(3)]
rcs = []
for p in procs:
    out, err = p.communicate(timeout=180)
    rcs.append(p.returncode)

per = {}
halves = 0
files = []          # (file, mtime) — 以轮转链序近似（字典序 .1<.10<.2 需数值排序）
def fkey(name):
    if name == "rmlog.log":
        return (0, 0)
    return (1, int(name.split(".")[-1]))
names = [f for f in os.listdir(D) if f == "rmlog.log" or f.startswith("rmlog.log.")]
for f in sorted(names, key=fkey):
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
                per.setdefault(int(m.group(1)), set()).add(int(m.group(2)))

total_visible = sum(len(v) for v in per.values())
print("rc=%s files=%d halves=%d visible=%d/1200" % (rcs, len(files), halves, total_visible))
for wid, items in sorted(per.items()):
    lo, hi = min(items), max(items)
    holes = [i for i in range(lo, hi + 1) if i not in items]
    # 幸存下界应一致（三 worker 从同一批最老文件被淘汰）
    print("  wid=%d surviving=%d range=[%d..%d] holes=%d %s"
          % (wid, len(items), lo, hi, len(holes), holes[:8]))
print("VERDICT: visible≈%d → %s" % (total_visible,
      "容量淘汰解释成立(810±20, 连续后缀)" if 790 <= total_visible <= 840 and halves == 0
      else "与'参数误校准'论证不符, 需进一步排查"))
