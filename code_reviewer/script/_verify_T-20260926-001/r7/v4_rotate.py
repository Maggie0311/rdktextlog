# -*- coding: utf-8 -*-
"""code_reviewer R7 验证脚本 V4: USAGE §2.4/§5 轮转文件族（max_bytes=400, keep=3, 60 条）。

观察: .rmlog.ROTLOCK 是否出现; rmlog.log / .1/.2/.3 文件族形态;
轮转后主文件是否"待下次写入重建"（FAQ Q6 依据）。
"""
import os

from rmlog.writer import Writer

w = Writer(log_dir="./rotlog", max_bytes=400, keep=3)
for i in range(60):
    w.event("E-SYS-005", "sys", "rotate test line %03d" % i)
w.close()

print("rotlog dir listing (right after 60 writes):")
for name in sorted(os.listdir("./rotlog")):
    print("  " + name)

# FAQ Q6: 轮转后主文件待下次写入重建 —— 若主文件此刻不存在, 再写一条观察重建
if not os.path.exists("./rotlog/rmlog.log"):
    w2 = Writer(log_dir="./rotlog", max_bytes=400, keep=3)
    w2.event("E-SYS-005", "sys", "rebuild main file probe")
    w2.close()
    print("AFTER extra write:")
    print("  rmlog.log exists: %s" % os.path.exists("./rotlog/rmlog.log"))
else:
    print("main rmlog.log exists right after loop (last write rebuilt it)")
