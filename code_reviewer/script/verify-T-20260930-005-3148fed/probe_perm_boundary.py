# -*- coding: utf-8 -*-
"""确认 PermissionError 边界：系统临时目录 vs 工作区（防御式，每步独立 try）。"""
import os
import tempfile

def try_mkfile(path):
    try:
        fd = os.open(path, os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o644)
        os.close(fd)
        return "OK"
    except OSError as e:
        return "%s(%d)" % (type(e).__name__, getattr(e, "winerror", 0) or e.errno or 0)

def try_mkdir(path):
    try:
        os.makedirs(path, exist_ok=True)
        return "OK"
    except OSError as e:
        return "%s(%d)" % (type(e).__name__, getattr(e, "winerror", 0) or e.errno or 0)

ws = os.path.dirname(os.path.abspath(__file__))

print("TMP  env = %s" % os.environ.get("TMP"))
print("TEMP env = %s" % os.environ.get("TEMP"))

# A) 系统临时目录 mkdtemp（顶层）
try:
    d = tempfile.mkdtemp(prefix="permprobe_")
    print("A mkdtemp -> OK : %s" % d)
    print("A mkfile in temp   : %s" % try_mkfile(os.path.join(d, "x.log")))
    print("A mkdir nested     : %s" % try_mkdir(os.path.join(d, "sub")))
except Exception as e:
    print("A mkdtemp FAILED: %r" % e)

# B) 工作区
print("B mkfile in ws      : %s" % try_mkfile(os.path.join(ws, "permprobe_ws.log")))
print("B mkdir in ws       : %s" % try_mkdir(os.path.join(ws, "permprobe_ws_sub")))

# 清理工作区探测产物
for p in (os.path.join(ws, "permprobe_ws.log"),):
    if os.path.exists(p):
        os.remove(p)
for p in (os.path.join(ws, "permprobe_ws_sub"),):
    if os.path.isdir(p):
        try: os.rmdir(p)
        except OSError: pass
