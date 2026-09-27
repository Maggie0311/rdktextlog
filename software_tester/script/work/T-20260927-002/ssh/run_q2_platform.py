# -*- coding: utf-8 -*-
"""Q2 平台核查：逐条执行并留档原始输出到 board_output/q2/。"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from board import Board

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "board_output", "q2")
os.makedirs(OUT, exist_ok=True)

CMDS = [
    ("os_release", "cat /etc/os-release"),
    ("uname", "uname -a; uname -m"),
    ("python3_version", "python3 --version; python3 -c 'import sys,platform; print(sys.version); print(platform.machine())'"),
    ("userdata", "ls -ld /userdata 2>&1; df -h /userdata 2>&1"),
    ("journal_dir", "ls -ld /var/log/journal 2>&1; ls /var/log/journal 2>&1"),
    ("journald_conf", "grep -vE '^\\s*#|^\\s*$' /etc/systemd/journald.conf 2>&1"),
    ("journald_enabled", "systemctl is-enabled systemd-journald 2>&1; systemctl is-active systemd-journald 2>&1"),
    ("rsyslog_active", "systemctl is-active rsyslog 2>&1; systemctl is-enabled rsyslog 2>&1"),
    ("rsyslog_proc", "ps -ef | grep -i [r]syslog 2>&1; ls -l /etc/rsyslog.conf /etc/rsyslog.d 2>&1"),
    ("coredumpctl", "which coredumpctl 2>&1; coredumpctl --version 2>&1"),
    ("core_pattern", "cat /proc/sys/kernel/core_pattern 2>&1"),
    ("coredump_active", "systemctl is-active systemd-coredump 2>&1; systemctl is-enabled systemd-coredump 2>&1"),
    ("dmesg_iso", "dmesg --time-format iso 2>&1 | head -8"),
    ("compilers", "which gcc clang cc 2>&1; gcc --version 2>&1 | head -2; clang --version 2>&1 | head -2"),
]

b = Board()
try:
    b.connect()
    print("CONNECT_OK", flush=True)
    for name, cmd in CMDS:
        rc, out, err = b.run(cmd, timeout=60)
        full = "=== CMD ===\n%s\n=== EXIT %d ===\n=== STDOUT ===\n%s\n=== STDERR ===\n%s\n" % (cmd, rc, out, err)
        with open(os.path.join(OUT, "%s.txt" % name), "w", encoding="utf-8") as fh:
            fh.write(full)
        # 打印精简视图
        print("=" * 60, flush=True)
        print("[%s] rc=%d" % (name, rc), flush=True)
        print(out, flush=True)
        if err.strip():
            print("[stderr]", err, flush=True)
finally:
    b.close()
print("Q2_DONE", flush=True)
