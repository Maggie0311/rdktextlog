# -*- coding: utf-8 -*-
# Maintainer archive note (v001): source snapshot 3148fed; comments only.
"""T-20260930-005：可运行五域故障注入演示，供开发机和板端 smoke test 使用。"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rmlog.writer import Writer
from rmlog.checks import emit_check
from rmlog.session import Session

def main(argv=None):
    p = argparse.ArgumentParser(description="rmlog 五域故障注入")
    p.add_argument("directory")
    p.add_argument("--fail", choices=["init", "comm", "hw", "fsm", "sys"])
    a = p.parse_args(argv)
    w = Writer(log_dir=a.directory)
    session = Session("fault-demo")
    for kind in ("init", "comm", "hw", "fsm", "sys"):
        # 检测适配器保持纯业务接口；这里用会话绑定 writer 实际落盘。
        emit_check(session.wrap(w), kind, ok=(kind != a.fail), detail="injected=%s" % (kind == a.fail))
    if a.fail == "sys":
        w.write_failures += 0  # 保持演示不伪造 IO 失败；真实失败由 Writer 计数
    w.close()
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
