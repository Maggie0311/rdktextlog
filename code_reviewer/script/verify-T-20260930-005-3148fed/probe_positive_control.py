# -*- coding: utf-8 -*-
"""正向对照：不用 tempfile.mkdtemp，改用工作区内 os.makedirs 目录，
完整走 smoke 第 17-22 行的逻辑（AsyncWriter(maxsize=1) + emit 10 + close + 读回），
证明代码与测试逻辑本身正确，唯一变量是 mkdtemp+沙箱。"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from rmlog.writer import Writer
from rmlog.async_writer import AsyncWriter
from rmlog.session import Session
from rmlog.format import parse_line

def run_with(logdir_factory, label, rounds=20):
    fails = 0
    for _ in range(rounds):
        d = logdir_factory()
        try:
            w = Writer(log_dir=d)
            session = Session("smoke", session_id="smoke-fixed")
            a = AsyncWriter(w, maxsize=1, session=session)
            accepted = sum(a.emit("E-SYS-005", "test", "x") for _ in range(10))
            a.close(); a.close()
            events = [parse_line(x) for x in open(os.path.join(d, "rmlog.log"), encoding="utf8")]
            ok = (accepted >= 1 and a.dropped >= 1 and
                  any(e and e["attrs"].get("session") == "smoke-fixed" for e in events))
            if not ok:
                fails += 1
        except Exception as e:
            fails += 1
            print("  %s trial EXC: %r" % (label, e))
    print("%s: rounds=%d fails=%d" % (label, rounds, fails))
    return fails

# A) mkdtemp（预期：沙箱下全 FAIL）
f1 = run_with(lambda: tempfile.mkdtemp(prefix="posctl_a_"), "A mkdtemp", 10)

# B) os.makedirs 工作区目录（预期：全 PASS，证明代码正确）
seq = [0]
def makedirs_factory():
    seq[0] += 1
    d = os.path.join(ROOT, "_posctl_b", "d%03d" % seq[0])
    os.makedirs(d, exist_ok=True)
    return d
f2 = run_with(makedirs_factory, "B makedirs-ws", 10)

print("RESULT: mkdtemp_fails=%d makedirs_ws_fails=%d" % (f1, f2))
