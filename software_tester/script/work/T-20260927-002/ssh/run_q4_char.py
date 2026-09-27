# -*- coding: utf-8 -*-
"""Q4 表征（非语义适配：仅追加编译参数，不改源码）——定位编译失败边界。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "board_output")
os.makedirs(OUT, exist_ok=True)

CMDS = [
    ("gnu99", "gcc -std=gnu99 -Wall -Wextra -c rmlog/rmlog.c -o /root/rmlog_test/work/rmlog_gnu99.o 2>/root/rmlog_test/work/w_gnu99.txt; echo EXIT=$?; echo 'stderr-bytes:'; wc -c </root/rmlog_test/work/w_gnu99.txt; echo 'stderr:'; cat /root/rmlog_test/work/w_gnu99.txt"),
    ("c99_GNU_SOURCE", "gcc -std=c99 -D_GNU_SOURCE -Wall -Wextra -c rmlog/rmlog.c -o /root/rmlog_test/work/rmlog_gnusource.o 2>/root/rmlog_test/work/w_gnusource.txt; echo EXIT=$?; echo 'stderr-bytes:'; wc -c </root/rmlog_test/work/w_gnusource.txt; echo 'stderr:'; cat /root/rmlog_test/work/w_gnusource.txt"),
    ("c99_POSIX", "gcc -std=c99 -D_POSIX_C_SOURCE=200809L -Wall -Wextra -c rmlog/rmlog.c -o /root/rmlog_test/work/rmlog_posix.o 2>/root/rmlog_test/work/w_posix.txt; echo EXIT=$?; echo 'stderr-bytes:'; wc -c </root/rmlog_test/work/w_posix.txt; echo 'stderr:'; cat /root/rmlog_test/work/w_posix.txt"),
]

b = Board()
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    for name, cmd in CMDS:
        rc, out, err = b.run("cd /root/rmlog_test/src && " + cmd, timeout=120)
        with open(os.path.join(OUT, "q4_char_%s.txt" % name), "w", encoding="utf-8") as fh:
            fh.write("rc=%d\n%s\n[stderr]\n%s\n" % (rc, out, err))
        print("=" * 60, flush=True)
        print("[%s] rc=%d" % (name, rc), flush=True)
        print(out, flush=True)
        if err.strip():
            print("[stderr]", err, flush=True)
finally:
    b.close()
print("Q4_CHAR_DONE", flush=True)
