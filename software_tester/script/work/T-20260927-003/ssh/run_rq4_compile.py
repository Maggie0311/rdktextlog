# -*- coding: utf-8 -*-
"""T-003 R-Q4: 板端 gcc -std=c99 -Wall -Wextra -c rmlog/rmlog.c —— 退出码 + stderr 字节数。
判定标准: 退出码 0 且 stderr 0 字节（与上轮 FAIL 证据同口径）。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "board_output")
os.makedirs(OUT, exist_ok=True)

CMD = (
    "cd /root/rmlog_test/src && "
    "rm -f /root/rmlog_test/work/rmlog_gcc.o /root/rmlog_test/work/q4_warn.txt; "
    "gcc -std=c99 -Wall -Wextra -c rmlog/rmlog.c -o /root/rmlog_test/work/rmlog_gcc.o "
    "2>/root/rmlog_test/work/q4_warn.txt; "
    "echo \"GCC_EXIT=$?\"; "
    "echo '--- stderr bytes ---'; wc -c </root/rmlog_test/work/q4_warn.txt; "
    "echo '--- stderr content (if any) ---'; cat /root/rmlog_test/work/q4_warn.txt; "
    "echo '--- object file ---'; ls -l /root/rmlog_test/work/rmlog_gcc.o 2>&1"
)

b = Board()
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    rc, out, err = b.run(CMD, timeout=120)
    with open(os.path.join(OUT, "rq4_compile_raw.txt"), "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s\n[stderr]\n%s\n" % (rc, out, err))
    print("rc=%d" % rc, flush=True)
    print(out, flush=True)
    if err.strip():
        print("[stderr]", err, flush=True)
finally:
    b.close()
print("RQ4_DONE", flush=True)
