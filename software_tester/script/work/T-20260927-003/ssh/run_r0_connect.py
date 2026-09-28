# -*- coding: utf-8 -*-
"""T-003 复测步骤 0: 连通性 + 板端环境自证（与上轮同法，地址已轮换）。"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board, HOST as board_HOST

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "board_output")
os.makedirs(OUT, exist_ok=True)

CMDS = [
    ("connect_banner", "echo SSH_CONNECT_OK; hostname; date '+%F %T %z'"),
    ("uname", "uname -a"),
    ("os_release", "cat /etc/os-release | head -3"),
    ("python3", "python3 --version"),
    ("gcc", "gcc --version | head -1"),
    ("old_workdir", "ls -ld /root/rmlog_test 2>&1; ls /root/rmlog_test 2>&1"),
]

b = Board()
log = []
try:
    t0 = time.time()
    b.connect()
    print("CONNECT_OK elapsed=%.1fs" % (time.time() - t0), flush=True)
    log.append("CONNECT_OK host=%s" % board_HOST)
    for name, cmd in CMDS:
        rc, out, err = b.run(cmd, timeout=60)
        block = "=== %s (rc=%d) ===\n%s" % (name, rc, out)
        if err.strip():
            block += "[stderr]\n%s" % err
        log.append(block)
        print(block, flush=True)
finally:
    b.close()
with open(os.path.join(OUT, "r0_connect_env.txt"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(log) + "\n")
print("R0_DONE", flush=True)
