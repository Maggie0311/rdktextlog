"""复审补跑留档：test_v2_smoke / test_v3_smoke 的沙箱 shim。

原因：Windows DSH 沙箱把 `tempfile.mkdtemp` 内部 `os.mkdir(name, 0o700)` 创建的
目录判为不可读（后续 os.listdir / 写入 / chmod 全部 WinError 5）。已探针确认：
0o777 目录与 0o600 文件均正常，仅 0o700 目录异常。故本 shim 仅替换 mkdtemp 的
目录 mode 为 0o777，并把临时区重定向到验证区工作目录；不修改任何被审代码或测试
文件，不改动其断言与语义。
"""
import os
import random
import sys
import tempfile

# 1) 临时区重定向到验证区（workspace-write），避免落到系统受限临时目录
TMP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp_smoke"))
os.makedirs(TMP_ROOT, mode=0o777, exist_ok=True)
tempfile.tempdir = TMP_ROOT


def _mkdtemp_relaxed(suffix=None, prefix=None, dir=None):
    """等价于 tempfile.mkdtemp，但以 mode=0o777 建目录（沙箱 shim）。"""
    if dir is None:
        dir = tempfile.gettempdir()
    prefix = prefix or "tmp"
    suffix = suffix or ""
    for _ in range(10000):
        name = os.path.join(dir, prefix + "%08x" % random.getrandbits(32) + suffix)
        try:
            os.mkdir(name, 0o777)
            return name
        except FileExistsError:
            continue
    raise FileExistsError("No usable temporary directory name found")


tempfile.mkdtemp = _mkdtemp_relaxed

# 2) 被测源指向验证区 d77d36c 副本（与上一轮 selftest 同一副本）
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "developer", "script"))
sys.path.insert(0, ROOT)

import runpy

fail = False
for test in ("test_v2_smoke", "test_v3_smoke"):
    print("===== %s =====" % test)
    try:
        runpy.run_path(os.path.join(ROOT, "tests", test + ".py"), run_name="__main__")
        print("%s PASS" % test)
    except SystemExit as e:
        code = e.code if e.code is not None else 0
        print("%s SystemExit(%r)" % (test, code))
        if code:
            fail = True
    except BaseException as e:
        import traceback
        traceback.print_exc()
        print("%s FAIL: %r" % (test, e))
        fail = True

print("SMOKE SHIM DONE fail=%s" % fail)
sys.exit(1 if fail else 0)
