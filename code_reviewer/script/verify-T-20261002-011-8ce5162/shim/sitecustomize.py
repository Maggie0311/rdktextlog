"""测试环境垫片（code_reviewer 验证区专用，非被审代码）。

背景: Windows 沙箱下 tempfile.mkdtemp() 内部 os.mkdir(mode=0o700) 会把目录
建成 owner-only ACL, 随后 os.listdir 报 EACCES(WinError 5)。这是 DSH 文件
沙箱与被审代码无关的环境交互（selftest 走 os.makedirs 默认 0o777 不受影响,
故 13/13 通过）。本垫片仅把 0o700 放宽为 0o777, 不改任何被审代码/测试断言,
使 tests/test_v2_smoke.py 与 tests/test_v3_smoke.py 能在沙箱内原样运行。
"""
import os as _os

_orig_mkdir = _os.mkdir


def _mkdir(path, mode=0o777, *args, **kwargs):
    if mode == 0o700:
        mode = 0o777
    return _orig_mkdir(path, mode, *args, **kwargs)


_os.mkdir = _mkdir
