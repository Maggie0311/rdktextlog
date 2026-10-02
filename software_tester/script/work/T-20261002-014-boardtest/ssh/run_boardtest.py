# -*- coding: utf-8 -*-
"""run_boardtest.py — T-20261002-014 v3 板端实测 BQ1~BQ5（事实采集）。

按任务书 §4 序列执行，每步 stdout/stderr/退出码 分离落盘到 raw/，同时打印到本机 stdout。
全部活动仅在板端 /tmp 下（/tmp/rmlog-v3-test）。BQ4 只读，BQ5 不装 systemd 服务、不改 /etc。
"""
import os
import sys
import time
import hashlib
import tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                      # work/T-20261002-014-boardtest
RAW = os.path.join(BASE, "raw")
SRC = os.path.join(BASE, "src", "developer", "script")
os.makedirs(RAW, exist_ok=True)

sys.path.insert(0, HERE)
sys.path.insert(0, r"D:\rdk_x5_software\software_tester\script\work\T-20260927-002\pylib")
from board import Board  # noqa: E402

IDENTITY_CMD = (
    "hostname; cat /proc/device-tree/model; uname -a; uname -m; "
    "cat /etc/os-release; python3 --version; gcc --version | head -1; ls -ld /userdata"
)

KEYFILES = [
    "rmlog/selftest.py", "rmlog/writer.py", "rmlog/rmlog.c",
    "rmlog/monitors.py", "rmlog/resources.py", "rmlog/daemon.py",
    "rmlog/auto.py", "tests/test_v2_smoke.py", "tests/test_v3_smoke.py",
]

REMOTE = "/tmp/rmlog-v3-test"


def md5_local(rel):
    return hashlib.md5(open(os.path.join(SRC, rel), "rb").read()).hexdigest()


def save(name, text):
    path = os.path.join(RAW, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def fmt_step(title):
    return "\n" + "=" * 78 + "\n" + title + "\n" + "=" * 78


def main():
    log = []
    b = Board()
    try:
        host = b.connect()
        line = "CONNECT_OK host=%s" % host
        print(line, flush=True)
        log.append(line)

        # ---------------- 步骤 1: 身份与环境核查 ----------------
        sec = fmt_step("STEP 1 身份与环境核查 (identity/environment)")
        print(sec, flush=True)
        rc, out, err = b.run(IDENTITY_CMD + "; echo __EXIT__=$?", timeout=60)
        body = ("CMD: %s\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n" % (IDENTITY_CMD, rc, out, err))
        save("01_identity.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 2: 上传代码 ----------------
        sec = fmt_step("STEP 2 上传 developer/script (d77d36c) -> %s" % REMOTE)
        print(sec, flush=True)
        tmp_tar = os.path.join(BASE, "_upload_src.tar")
        with tarfile.open(tmp_tar, "w") as tf:
            for name in sorted(os.listdir(SRC)):
                tf.add(os.path.join(SRC, name), arcname=name)
        upload_txt = []
        upload_txt.append("local source dir: %s" % SRC)
        upload_txt.append("tar size bytes: %d" % os.path.getsize(tmp_tar))
        try:
            rc, out, err = b.run(
                "rm -rf %s /tmp/_upload.tar && mkdir -p %s" % (REMOTE, REMOTE), timeout=30)
            upload_txt.append("[prep] rc=%d out=%r err=%r" % (rc, out, err))
            b.put(tmp_tar, "/tmp/_upload.tar")
            rc, out, err = b.run(
                "tar -xf /tmp/_upload.tar -C %s && rm -f /tmp/_upload.tar "
                "&& echo UPLOAD_OK && cd %s && find . -type f | sort && echo FILES=$(find . -type f | wc -l)"
                % (REMOTE, REMOTE), timeout=60)
            upload_txt.append("[extract] rc=%d\n[stdout]\n%s\n[stderr]\n%s" % (rc, out, err))
            # md5 核对关键文件
            local_map = {rel: md5_local(rel) for rel in KEYFILES}
            rc2, out2, err2 = b.run(
                "cd %s && md5sum %s" % (REMOTE, " ".join(KEYFILES)), timeout=60)
            upload_txt.append("[remote md5sum] rc=%d\n[stdout]\n%s\n[stderr]\n%s" % (rc2, out2, err2))
            remote_map = {}
            for ln in out2.splitlines():
                p = ln.split()
                if len(p) >= 2:
                    remote_map[p[1]] = p[0]
            for rel in KEYFILES:
                lm, rm = local_map[rel], remote_map.get(rel)
                upload_txt.append("%s  %s  local=%s remote=%s" % (
                    "MATCH" if lm == rm else "DIFF", rel, lm, rm))
            # 上传两个测试辅助脚本（非 developer 源码，仅测试驱动）
            for helper in ("bq3_monitors.py", "bq5_daemon.sh"):
                b.put(os.path.join(HERE, helper), "%s/%s" % (REMOTE, helper))
            rc3, out3, err3 = b.run("cd %s && ls -l bq3_monitors.py bq5_daemon.sh" % REMOTE, timeout=30)
            upload_txt.append("[helpers] rc=%d\n%s\n[stderr]\n%s" % (rc3, out3, err3))
        finally:
            try:
                os.remove(tmp_tar)
            except Exception:  # noqa: BLE001
                pass
        body = "\n".join(upload_txt) + "\n"
        save("02_upload.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 3: BQ1 selftest ----------------
        sec = fmt_step("STEP 3 BQ1 selftest (python3 -m rmlog.selftest)")
        print(sec, flush=True)
        t0 = time.time()
        rc, out, err = b.run(
            "cd %s && PYTHONPATH=. python3 -m rmlog.selftest" % REMOTE, timeout=500)
        used = time.time() - t0
        body = ("CMD: cd %s && PYTHONPATH=. python3 -m rmlog.selftest\n"
                "elapsed=%.1fs\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n"
                % (REMOTE, used, rc, out, err))
        save("03_bq1_selftest.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 4: BQ2 v2 smoke ----------------
        sec = fmt_step("STEP 4 BQ2 v2 smoke (tests/test_v2_smoke.py)")
        print(sec, flush=True)
        t0 = time.time()
        rc, out, err = b.run(
            "cd %s && PYTHONPATH=. python3 tests/test_v2_smoke.py" % REMOTE, timeout=300)
        used = time.time() - t0
        body = ("CMD: cd %s && PYTHONPATH=. python3 tests/test_v2_smoke.py\n"
                "elapsed=%.1fs\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n"
                % (REMOTE, used, rc, out, err))
        save("04_bq2_v2_smoke.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 5: BQ2 v3 smoke ----------------
        sec = fmt_step("STEP 5 BQ2 v3 smoke (tests/test_v3_smoke.py)")
        print(sec, flush=True)
        t0 = time.time()
        rc, out, err = b.run(
            "cd %s && PYTHONPATH=. python3 tests/test_v3_smoke.py" % REMOTE, timeout=300)
        used = time.time() - t0
        body = ("CMD: cd %s && PYTHONPATH=. python3 tests/test_v3_smoke.py\n"
                "elapsed=%.1fs\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n"
                % (REMOTE, used, rc, out, err))
        save("05_bq2_v3_smoke.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 6: BQ3 monitors ----------------
        sec = fmt_step("STEP 6 BQ3 v3 监控层读真实 dmesg/sysfs/procfs")
        print(sec, flush=True)
        t0 = time.time()
        rc, out, err = b.run(
            "cd %s && PYTHONPATH=. python3 bq3_monitors.py" % REMOTE, timeout=120)
        used = time.time() - t0
        body = ("CMD: cd %s && PYTHONPATH=. python3 bq3_monitors.py\n"
                "elapsed=%.1fs\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n"
                % (REMOTE, used, rc, out, err))
        save("06_bq3_monitors.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 7: BQ4 core 配置（只读） ----------------
        sec = fmt_step("STEP 7 BQ4 ulimit -c / core_pattern (只读)")
        print(sec, flush=True)
        cmd = "ulimit -c; echo '--- core_pattern ---'; cat /proc/sys/kernel/core_pattern; echo '--- core_uses_pid ---'; cat /proc/sys/kernel/core_uses_pid"
        rc, out, err = b.run(cmd, timeout=30)
        body = ("CMD: %s\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n" % (cmd, rc, out, err))
        save("07_bq4_core_config.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 8: BQ5 daemon ----------------
        sec = fmt_step("STEP 8 BQ5 daemon 心跳 + SIGTERM 收尾")
        print(sec, flush=True)
        t0 = time.time()
        rc, out, err = b.run("bash %s/bq5_daemon.sh" % REMOTE, timeout=120)
        used = time.time() - t0
        body = ("CMD: bash %s/bq5_daemon.sh\n"
                "elapsed=%.1fs\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n"
                % (REMOTE, used, rc, out, err))
        save("08_bq5_daemon.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 汇总 ----------------
        with open(os.path.join(RAW, "SUMMARY.txt"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(log))
        print(fmt_step("ALL DONE. raw output in %s" % RAW), flush=True)
    finally:
        b.close()


if __name__ == "__main__":
    main()
