# -*- coding: utf-8 -*-
"""T-003 复测步骤 1: 重建板端工作目录 /root/rmlog_test/（仅自建目录，不动系统配置），
上传 164d4c7 副本，逐文件 md5 核对。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "board_output")
os.makedirs(OUT, exist_ok=True)
SRC = os.path.join(BASE, "src", "developer", "script")

b = Board()
log = []
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    log.append("CONNECT_OK host=2409:893d:5175:915b:84d8:86d7:ff02:f8da")

    # 1) 重建板端工作目录（清空重建，避免旧版残留干扰）
    rc, out, err = b.run(
        "rm -rf /root/rmlog_test/src /root/rmlog_test/work /root/rmlog_test/q3 && "
        "mkdir -p /root/rmlog_test/src /root/rmlog_test/work && echo REBUILD_OK",
        timeout=60)
    log.append("=== rebuild (rc=%d) ===\n%s" % (rc, out + err))
    print(out, err, flush=True)
    if "REBUILD_OK" not in out:
        raise RuntimeError("rebuild failed")

    # 2) 上传副本
    out2 = b.put_dir(SRC, "/root/rmlog_test/src")
    log.append("=== upload ===\n%s" % out2)
    print("UPLOAD_OK", flush=True)

    # 3) 板端 md5 清单
    rc3, out3, err3 = b.run(
        "cd /root/rmlog_test/src/developer/script && "
        "find . -type f ! -name 'local_md5_manifest.txt' ! -path '*__pycache__*' -print0 | "
        "sort -z | xargs -0 md5sum", timeout=120)
    log.append("=== remote md5 (rc=%d) ===\n%s" % (rc3, out3))
    with open(os.path.join(OUT, "remote_md5.txt"), "w", encoding="utf-8") as fh:
        fh.write(out3)
    if err3.strip():
        log.append("[remote stderr]\n%s" % err3)
        print("[remote stderr]", err3, flush=True)
finally:
    b.close()
with open(os.path.join(OUT, "r1_upload_log.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(log) + "\n")
print("R1_DONE", flush=True)
