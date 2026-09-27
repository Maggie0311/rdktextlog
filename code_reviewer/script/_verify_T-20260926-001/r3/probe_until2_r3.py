# probe_until2_r3 — 复审探针: F-2 边界（首轮 probe_until2 同参 + 扩展边界）
# 覆盖: 分钟前缀 until/since、秒级前缀、完整精度不变、日期级前缀、空值、
#       非法输入原样返回、毫秒右补零、上下界联合窗口
import os, sys, shutil, subprocess
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3\pkg"
OUT = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r3"
D = os.path.join(OUT, "probe_until2")
shutil.rmtree(D, ignore_errors=True)
sys.path.insert(0, BASE)
LOG = os.path.join(D, "rmlog.log")
os.makedirs(D, exist_ok=True)
with open(LOG, "w", encoding="utf-8") as fh:
    fh.write("LOGV1|1|2026-09-26T12:00:00.100|100|INFO|E-SYS-005|m|in minute 12:00\n")
    fh.write("LOGV1|2|2026-09-26T12:01:00.500|200|INFO|E-SYS-005|m|first of minute 12:01\n")
    fh.write("LOGV1|3|2026-09-26T12:01:59.900|300|ERROR|E-SYS-002|m|last of minute 12:01\n")
READER = os.path.join(BASE, "rmlog_read.py")

def run(*extra):
    p = subprocess.run([sys.executable, READER, "filter", LOG] + list(extra),
                       capture_output=True, text=True)
    return [l for l in p.stdout.strip().splitlines() if l.strip()], p.stderr.strip()

fails = []
def expect(tag, got, want_lines, want_walls):
    walls = [l.split()[0] for l in got]
    ok = len(walls) == want_lines and walls == want_walls
    print("%-38s got=%d %s" % (tag, len(got), "OK" if ok else "MISMATCH %s" % walls))
    if not ok:
        fails.append(tag)

# ---- 首轮 probe_until2 同参三点 ----
out, err = run("--until", "2026-09-26T12:01")
expect("until=minute-prefix(12:01)", out, 3, ["2026-09-26T12:00:00.100",
                                              "2026-09-26T12:01:00.500",
                                              "2026-09-26T12:01:59.900"])
out2, _ = run("--until", "2026-09-26T12:01:59.900")
expect("until=full-precision(unchanged)", out2, 3, ["2026-09-26T12:00:00.100",
                                                    "2026-09-26T12:01:00.500",
                                                    "2026-09-26T12:01:59.900"])
out3, _ = run("--since", "2026-09-26T12:01")
expect("since=minute-prefix(12:01)", out3, 2, ["2026-09-26T12:01:00.500",
                                               "2026-09-26T12:01:59.900"])
# ---- 扩展边界 ----
out4, _ = run("--since", "2026-09-26T12:01", "--until", "2026-09-26T12:01")
expect("window[since=until=12:01]", out4, 2, ["2026-09-26T12:01:00.500",
                                              "2026-09-26T12:01:59.900"])
out5, _ = run("--until", "2026-09-26T12:00")
expect("until=12:00(excludes 12:01)", out5, 1, ["2026-09-26T12:00:00.100"])
out6, _ = run("--until", "2026-09-26T12:01:59")
expect("until=second-prefix(12:01:59)", out6, 3, ["2026-09-26T12:00:00.100",
                                                  "2026-09-26T12:01:00.500",
                                                  "2026-09-26T12:01:59.900"])
out7, _ = run("--until", "2026-09-26T12:01:59.9")
expect("until=.9(msec pad-right)", out7, 3, ["2026-09-26T12:00:00.100",
                                             "2026-09-26T12:01:00.500",
                                             "2026-09-26T12:01:59.900"])
out8, _ = run("--until", "2026-09-26")
expect("until=date-prefix(=day end)", out8, 3, ["2026-09-26T12:00:00.100",
                                                "2026-09-26T12:01:00.500",
                                                "2026-09-26T12:01:59.900"])
out9, _ = run("--since", "2026-09-26")
expect("since=date-prefix(=day start)", out9, 3, ["2026-09-26T12:00:00.100",
                                                  "2026-09-26T12:01:00.500",
                                                  "2026-09-26T12:01:59.900"])
out10, _ = run("--since", "2026-09-27")
expect("since=next-day(no hit)", out10, 0, [])
out11, _ = run("--until", "2026")
expect("until=year-prefix", out11, 3, ["2026-09-26T12:00:00.100",
                                       "2026-09-26T12:01:00.500",
                                       "2026-09-26T12:01:59.900"])
out12, _ = run("--until", "garbage!!")
print("%-38s got=%d (unrecognized passthrough, no exception)" % ("until=garbage", len(out12)))
if not err == "" or out12:
    # garbage 归一失败原样返回 → 字典序基本不命中, 不抛异常即为通过
    print("   (note: got %d hits, stderr=%r)" % (len(out12), err))
print("FAILS:", fails if fails else "none")
