import os, sys, shutil, subprocess
BASE = r"D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r2"
sys.path.insert(0, BASE)
D = os.path.join(BASE, "probe_until")
shutil.rmtree(D, ignore_errors=True)
from rmlog.writer import Writer
w = Writer(log_dir=D, max_bytes=1000000, keep=3)
# 3 条事件: 12:00:00.100 / 12:01:00.500 / 12:01:59.900 —— 用 encode 直接控制 wall_ts
from rmlog import format as fmt
from rmlog.writer import Writer as W
import rmlog.writer as wr
# 直接构造文件 (绕过真实时钟): 手写三行合法日志
os.remove(os.path.join(D, "rmlog.log"))
with open(os.path.join(D, "rmlog.log"), "w", encoding="utf-8") as fh:
    fh.write("LOGV1|1|2026-09-26T12:00:00.100|100|INFO|E-SYS-005|m|in minute 12:00\n")
    fh.write("LOGV1|2|2026-09-26T12:01:00.500|200|INFO|E-SYS-005|m|first of minute 12:01\n")
    fh.write("LOGV1|3|2026-09-26T12:01:59.900|300|ERROR|E-SYS-002|m|last of minute 12:01\n")
w.close()
READER = os.path.join(BASE, "rmlog_read.py")
LOG = os.path.join(D, "rmlog.log")
def run(*extra):
    p = subprocess.run([sys.executable, READER, "filter", LOG] + list(extra),
                       capture_output=True, text=True)
    return p.stdout.strip().splitlines(), p.stderr.strip()
# 按分钟前缀查询 (USAGE §5 示例用法): --until 12:01
out, err = run("--until", "2026-09-26T12:01")
print("[until=12:01 minute-prefix] got %d lines (expect 2 if inclusive-of-minute):" % len(out))
for l in out: print("   ", l)
print("   stderr:", err)
# 全精度时间戳: 应含 12:01:59.900
out2, err2 = run("--until", "2026-09-26T12:01:59.900")
print("[until=full ts] got %d lines (expect 3):" % len(out2))
# --since 分钟前缀: 应含 12:01 的行
out3, err3 = run("--since", "2026-09-26T12:01")
print("[since=12:01 minute-prefix] got %d lines (expect 2):" % len(out3))
for l in out3: print("   ", l)
