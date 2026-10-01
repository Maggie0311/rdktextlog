# -*- coding: utf-8 -*-
"""最小探针：复现并定位 test_v2_smoke.py 在 Windows 3.14 开发机上的
FileNotFoundError(rmlog.log)。不依赖被审代码，只直接驱动 Writer+AsyncWriter。

对每次试验记录：close 返回值 / 线程存活 / 各类计数器 / 立即读 vs sleep 后读。
"""
import os
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from rmlog.writer import Writer
from rmlog.async_writer import AsyncWriter
from rmlog.session import Session


def one_trial(idx, n=10, maxsize=1, immediate_read=True):
    d = tempfile.mkdtemp(prefix="probe_race_")
    w = Writer(log_dir=d)
    session = Session("smoke", session_id="smoke-fixed")
    a = AsyncWriter(w, maxsize=maxsize, session=session)
    accepted = 0
    for _ in range(n):
        if a.emit("E-SYS-005", "test", "x"):
            accepted += 1
    ret1 = a.close()
    alive1 = a._thread.is_alive()
    a.close()
    alive2 = a._thread.is_alive()
    path = os.path.join(d, "rmlog.log")
    exists_imm = os.path.exists(path)
    size_imm = os.path.getsize(path) if exists_imm else -1
    exists_sleep = None
    size_sleep = None
    if not immediate_read:
        time.sleep(0.5)
    exists_sleep = os.path.exists(path)
    size_sleep = os.path.getsize(path) if exists_sleep else -1
    time.sleep(0.3)  # 额外给 daemon 线程任何残留动作的时间
    exists_final = os.path.exists(path)
    size_final = os.path.getsize(path) if exists_final else -1
    return dict(
        idx=idx, accepted=accepted, dropped=a.dropped,
        ret1=ret1, alive1=alive1, alive2=alive2,
        worker_fail=a.worker_failures, write_fail=a.write_failures,
        w_write_fail=w.write_failures, w_lock_deg=w.lock_degradations,
        w_last_error=w.last_error,
        exists_imm=exists_imm, size_imm=size_imm,
        exists_sleep=exists_sleep, size_sleep=size_sleep,
        exists_final=exists_final, size_final=size_final,
    )


def main():
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    imm = os.environ.get("PROBE_IMM", "1") == "1"
    fails = []
    print("PROBE smoke-race  rounds=%d immediate_read=%s" % (rounds, imm))
    for i in range(rounds):
        r = one_trial(i, n=10, maxsize=1, immediate_read=imm)
        bad = (not r["exists_imm"]) or (not r["exists_final"]) or r["worker_fail"] > 0
        if bad:
            fails.append(r)
        print(("[%02d] accepted=%d dropped=%d ret1=%s alive1=%s alive2=%s "
               "worker_fail=%d write_fail=%d w_write_fail=%d w_lock_deg=%d "
               "last_err=%s imm=%s(%d) sleep=%s(%d) final=%s(%d) %s") % (
                i, r["accepted"], r["dropped"], r["ret1"], r["alive1"], r["alive2"],
                r["worker_fail"], r["write_fail"], r["w_write_fail"], r["w_lock_deg"],
                r["w_last_error"], r["exists_imm"], r["size_imm"],
                r["exists_sleep"], r["size_sleep"],
                r["exists_final"], r["size_final"],
                "  <<< FAIL" if bad else ""))
    print("SUMMARY: rounds=%d fails=%d" % (rounds, len(fails)))
    if fails:
        print("FAIL TRIALS:")
        for r in fails:
            print("  idx=%d accepted=%d dropped=%d worker_fail=%d write_fail=%d "
                  "w_write_fail=%d w_lock_deg=%d last_err=%s imm=%s(%d) final=%s(%d)" % (
                      r["idx"], r["accepted"], r["dropped"], r["worker_fail"],
                      r["write_fail"], r["w_write_fail"], r["w_lock_deg"],
                      r["w_last_error"], r["exists_imm"], r["size_imm"],
                      r["exists_final"], r["size_final"]))


if __name__ == "__main__":
    main()
