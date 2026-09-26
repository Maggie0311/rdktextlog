# -*- coding: utf-8 -*-
"""rmlog.worker — 多进程并发写压测工作进程（selftest 专用, AC5）。

任务: T-20260926-001-logging-platform-p0（REQ §4 P0-d / AC5）。

为什么是独立模块 + 子进程: 并发写安全的前提是**多个独立进程**各持 O_APPEND
句柄 —— 进程内线程模拟不了多进程 fd 与内核追加语义。selftest 用
subprocess 拉起 N 个本进程, 各写 M 条, 事后由 selftest 校验"无丢行、无交错半行"。

用法: python3 -m rmlog.worker <log_dir> <count> [max_bytes]
    每条事件 attrs 携带 wid(工作进程号=pid) 与 i(条目序号), 供事后按进程对账。
    正常退出码 0; 参数错误退出码 2。
"""

import os
import sys

from .writer import Writer


def main(argv):
    """工作进程入口: 建独立 Writer 连写 count 条 INFO 事件后退出。"""
    if len(argv) < 3:
        sys.stderr.write("usage: python3 -m rmlog.worker <log_dir> <count> [max_bytes]\n")
        return 2
    log_dir = argv[1]
    count = int(argv[2])
    # max_bytes 可选: 传小值可让多进程场景下也触发轮转（压测轮转竞争路径）
    max_bytes = int(argv[3]) if len(argv) > 3 else 8 * 1024 * 1024

    writer = Writer(log_dir=log_dir, max_bytes=max_bytes, keep=5)
    wid = os.getpid()
    for i in range(count):
        # 统一用 E-SYS-005(里程碑) 便于对账; 消息带 pid 交叉印证 wid
        ok = writer.event("E-SYS-005", "worker",
                          "worker %d event %d" % (wid, i),
                          attrs={"wid": wid, "i": i})
        if not ok:
            # 压测中写失败也如实上报（正常应为 0 失败）
            sys.stderr.write("worker %d: write failed at %d\n" % (wid, i))
            return 1
    writer.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
