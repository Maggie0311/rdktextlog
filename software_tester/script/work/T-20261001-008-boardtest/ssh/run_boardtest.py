# -*- coding: utf-8 -*-
"""run_boardtest.py — T-20261001-008 v2 板端自测 + 五域故障注入（事实采集）。

按任务书 §4 五步序列执行，每步 stdout/stderr/退出码 分离落盘到 raw/，
同时打印到本机 stdout。全部活动仅在板端 /tmp 下（/tmp/rmlog-v2、/tmp/rmlog-fault-*）。
"""
import os, sys, time, hashlib, tarfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)                      # work/T-20261001-008-boardtest
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

KEYFILES = ["rmlog/selftest.py", "rmlog/writer.py", "rmlog/rmlog.c",
            "rmlog/fault_demo.py", "tests/test_v2_smoke.py", "rmlog_read.py"]


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
    log = []  # 汇总文本
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
        sec = fmt_step("STEP 2 上传 developer/script (d2e1081) -> /tmp/rmlog-v2")
        print(sec, flush=True)
        tmp_tar = os.path.join(BASE, "_upload_src.tar")
        with tarfile.open(tmp_tar, "w") as tf:
            for name in sorted(os.listdir(SRC)):
                tf.add(os.path.join(SRC, name), arcname=name)
        upload_txt = []
        upload_txt.append("local source dir: %s" % SRC)
        upload_txt.append("tar size bytes: %d" % os.path.getsize(tmp_tar))
        try:
            rc, out, err = b.run("rm -rf /tmp/rmlog-v2 /tmp/_upload.tar && mkdir -p /tmp/rmlog-v2", timeout=30)
            upload_txt.append("[prep] rc=%d out=%r err=%r" % (rc, out, err))
            b.put(tmp_tar, "/tmp/_upload.tar")
            rc, out, err = b.run(
                "tar -xf /tmp/_upload.tar -C /tmp/rmlog-v2 && rm -f /tmp/_upload.tar "
                "&& echo UPLOAD_OK && cd /tmp/rmlog-v2 && find . -type f | sort && echo FILES=$(find . -type f | wc -l)",
                timeout=60)
            upload_txt.append("[extract] rc=%d\n[stdout]\n%s\n[stderr]\n%s" % (rc, out, err))
            # md5 核对关键文件
            local_map = {rel: md5_local(rel) for rel in KEYFILES}
            rc2, out2, err2 = b.run(
                "cd /tmp/rmlog-v2 && md5sum " + " ".join(KEYFILES), timeout=60)
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
        finally:
            try:
                os.remove(tmp_tar)
            except Exception:  # noqa: BLE001
                pass
        body = "\n".join(upload_txt) + "\n"
        save("02_upload.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 3: selftest ----------------
        sec = fmt_step("STEP 3 selftest (python3 -m rmlog.selftest)")
        print(sec, flush=True)
        t0 = time.time()
        rc, out, err = b.run(
            "cd /tmp/rmlog-v2 && PYTHONPATH=. python3 -m rmlog.selftest", timeout=500)
        used = time.time() - t0
        body = ("CMD: cd /tmp/rmlog-v2 && PYTHONPATH=. python3 -m rmlog.selftest\n"
                "elapsed=%.1fs\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n" % (used, rc, out, err))
        save("03_selftest.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 4: smoke ----------------
        sec = fmt_step("STEP 4 smoke (python3 tests/test_v2_smoke.py)")
        print(sec, flush=True)
        t0 = time.time()
        rc, out, err = b.run(
            "cd /tmp/rmlog-v2 && PYTHONPATH=. python3 tests/test_v2_smoke.py", timeout=300)
        used = time.time() - t0
        body = ("CMD: cd /tmp/rmlog-v2 && PYTHONPATH=. python3 tests/test_v2_smoke.py\n"
                "elapsed=%.1fs\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n" % (used, rc, out, err))
        save("04_smoke.txt", body)
        print(body, flush=True)
        log.append(body)

        # ---------------- 步骤 5: 五域故障注入 ----------------
        for kind in ("init", "comm", "hw", "fsm", "sys"):
            sec = fmt_step("STEP 5 故障注入 kind=%s" % kind)
            print(sec, flush=True)
            d = "/tmp/rmlog-fault-%s" % kind
            cmd = ("rm -rf %s; mkdir -p %s; cd /tmp/rmlog-v2 && "
                   "PYTHONPATH=. python3 rmlog/fault_demo.py %s --fail %s" % (d, d, d, kind))
            rc, out, err = b.run(cmd, timeout=60)
            # 列出该域生成的日志文件与关键内容
            rc2, out2, err2 = b.run(
                "echo '--- files ---'; find %s -type f | sort; "
                "echo '--- content ---'; for f in $(find %s -type f | sort); do "
                "echo \"===== $f =====\"; cat \"$f\"; done" % (d, d), timeout=60)
            body = ("CMD: %s\n\n[exit] %d\n\n[stdout]\n%s\n\n[stderr]\n%s\n\n"
                    "[日志文件与内容] rc=%d\n%s\n[stderr]\n%s\n"
                    % (cmd, rc, out, err, rc2, out2, err2))
            save("05_fault_%s.txt" % kind, body)
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
