# -*- coding: utf-8 -*-
"""定位：主线程 vs 后台线程、tempfile.mkdtemp 目录 vs 普通 os.makedirs 目录。"""
import os
import sys
import threading

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import tempfile

ws = ROOT

def mkfile(path):
    try:
        fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o644)
        os.close(fd)
        return "OK"
    except OSError as e:
        return "%s(%d)" % (type(e).__name__, getattr(e, "winerror", 0) or e.errno or 0)

def mkfile_bg(path, res):
    res.append((path, mkfile(path)))

# 1) 主线程：os.makedirs 目录（工作区内）
d1 = os.path.join(ws, "_probe_loc_mkdirs")
os.makedirs(d1, exist_ok=True)
print("1 main mkdirs dir file : %s" % mkfile(os.path.join(d1, "x.log")))

# 2) 主线程：tempfile.mkdtemp 目录（TMP 已指向工作区或系统区，看实际情况）
d2 = tempfile.mkdtemp(prefix="locprobe_")
print("2 mkdtemp dir = %s" % d2)
print("2 main mkdtemp dir file: %s" % mkfile(os.path.join(d2, "x.log")))

# 3) 后台线程：tempfile.mkdtemp 目录
d3 = tempfile.mkdtemp(prefix="locprobe_bg_")
res3 = []
t = threading.Thread(target=mkfile_bg, args=(os.path.join(d3, "x.log"), res3))
t.start(); t.join()
print("3 bg mkdtemp dir file  : %s (dir=%s)" % (res3[0][1] if res3 else "NO-RESULT", d3))

# 4) 后台线程：os.makedirs 目录（工作区内）
d4 = os.path.join(ws, "_probe_loc_bg_mkdirs")
os.makedirs(d4, exist_ok=True)
res4 = []
t = threading.Thread(target=mkfile_bg, args=(os.path.join(d4, "x.log"), res4))
t.start(); t.join()
print("4 bg mkdirs dir file   : %s" % (res4[0][1] if res4 else "NO-RESULT"))

print("TMP env = %s" % os.environ.get("TMP"))

# 清理工作区探测目录
for p in (d1, d4):
    for f in ("x.log",):
        fp = os.path.join(p, f)
        if os.path.exists(fp):
            os.remove(fp)
    try: os.rmdir(p)
    except OSError: pass
