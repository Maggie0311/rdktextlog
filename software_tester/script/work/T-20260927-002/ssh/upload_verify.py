# -*- coding: utf-8 -*-
"""上传 2d83644 副本到板端并核对关键文件 md5 与本地一致。"""
import sys, os, hashlib, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_SRC = os.path.join(BASE, "src", "developer", "script")
REMOTE = "/root/rmlog_test/src"
OUT = os.path.join(BASE, "board_output")
os.makedirs(OUT, exist_ok=True)

KEYFILES = [
    "rmlog/rmlog.c", "rmlog/rmlog.h", "rmlog/selftest.py", "rmlog/writer.py",
    "rmlog/worker.py", "rmlog/__init__.py", "rmlog/format.py", "rmlog/catalog.py",
    "rmlog_read.py", "tests/probe_fdleak_rf6.c", "rmlog/rmlog_errors.h",
    "rmlog/_ac4_probe.c",
]

def md5_local(rel):
    p = os.path.join(LOCAL_SRC, rel)
    return hashlib.md5(open(p, "rb").read()).hexdigest()

b = Board()
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    rc, out, err = b.run("rm -rf /root/rmlog_test && mkdir -p /root/rmlog_test", timeout=30)
    print("prep rc=%d out=%r err=%r" % (rc, out, err), flush=True)
    b.put_dir(LOCAL_SRC, REMOTE)
    print("UPLOAD_DONE", flush=True)
    # 本地 md5 清单
    local_map = {rel: md5_local(rel) for rel in KEYFILES}
    with open(os.path.join(OUT, "local_md5.txt"), "w", encoding="utf-8") as fh:
        for rel in KEYFILES:
            fh.write("%s  %s\n" % (local_map[rel], rel))
    # 板端 md5
    remote_cmd = "cd /root/rmlog_test/src && md5sum " + " ".join(KEYFILES)
    rc, out, err = b.run(remote_cmd, timeout=60)
    with open(os.path.join(OUT, "remote_md5.txt"), "w", encoding="utf-8") as fh:
        fh.write("rc=%d\n%s\n[stderr]\n%s\n" % (rc, out, err))
    print("REMOTE_MD5 rc=%d" % rc, flush=True)
    print(out, flush=True)
    if err.strip():
        print("[stderr]", err, flush=True)
    # 逐项比对
    remote_map = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            remote_map[parts[1]] = parts[0]
    all_match = True
    for rel in KEYFILES:
        lm, rm = local_map[rel], remote_map.get(rel)
        ok = (lm == rm)
        if not ok:
            all_match = False
        print("%s  %s  local=%s remote=%s" % ("MATCH" if ok else "DIFF", rel, lm, rm), flush=True)
    print("ALL_MATCH=%s" % all_match, flush=True)
finally:
    b.close()
