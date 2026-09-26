import os, sys, shutil, subprocess
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r2"
D = os.path.join(BASE, "probe_until2")
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
    return p.stdout.strip().splitlines(), p.stderr.strip()
out, err = run("--until", "2026-09-26T12:01")
print("[until=12:01 minute-prefix] got %d lines:" % len(out))
for l in out: print("   ", l)
print("   stderr:", err)
out2, err2 = run("--until", "2026-09-26T12:01:59.900")
print("[until=full-ts] got %d lines (expect 3):" % len(out2))
out3, err3 = run("--since", "2026-09-26T12:01")
print("[since=12:01 minute-prefix] got %d lines (expect 2):" % len(out3))
for l in out3: print("   ", l)
