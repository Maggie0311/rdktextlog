# -*- coding: utf-8 -*-
"""全量 smoke 主体正向对照：把 tempfile.mkdtemp 替换为工作区内 os.makedirs 目录，
跑 test_v2_smoke.main() 的完整 17-30 行逻辑（含 fault_demo / export_evidence / 轮转）。
预期：全部 PASS —— 证明 smoke 唯一失败点是 mkdtemp+沙箱，其余逻辑全对。"""
import os
import sys
import tempfile

VERIFY = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(VERIFY, "tests")
sys.path.insert(0, TESTS)

_counter = [0]
def fake_mkdtemp(prefix="t"):
    _counter[0] += 1
    d = os.path.join(VERIFY, "_smoke_full", "%s%04d" % (prefix, _counter[0]))
    os.makedirs(d, exist_ok=True)
    return d

# 在调用 main() 前替换模块属性（main 内部按 tempfile.mkdtemp 属性查找，会命中补丁）
tempfile.mkdtemp = fake_mkdtemp

import test_v2_smoke as smoke

print("RUN full smoke body with mkdtemp -> workspace makedirs ...")
smoke.main()
print("FULL SMOKE BODY PASS")
