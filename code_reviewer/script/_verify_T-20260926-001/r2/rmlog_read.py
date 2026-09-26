# -*- coding: utf-8 -*-
"""rmlog_read — rmlog 读端工具: parse / tail / filter（REQ §4 P0-e）。

任务: T-20260926-001-logging-platform-p0。

比赛日"一条命令定位"示例（详见 USAGE.md §5）::

    python3 rmlog_read.py filter ./rmlog.log --level ERROR --code E-INIT-*
    python3 rmlog_read.py tail ./rmlog.log -n 20 --follow

子命令:
    parse   逐行解析并 pretty 打印（检查行格式/残行丢弃是否生效）
    tail    看最后 N 条（--follow 持续跟踪, 类 tail -f）
    filter  按级别/错误码/时间窗过滤 —— 场下定位的主力入口

残行策略（AC2）: 每行先过 rmlog.format.parse_line 三道闸（前缀/字段数/语义）,
不合法的行**丢弃并计数**, 结束时把丢弃数打到 stderr —— 比赛取证时必须
知道"有多少行没能读出来", 这是证据链诚实性的一部分。
"""

import argparse
import os
import sys
import time

# 允许脚本被直接执行（python3 rmlog_read.py ...）也可作为模块导入:
# 把脚本所在目录加入 sys.path, 保证 `from rmlog import ...` 在两种方式下都成立。
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rmlog.format import parse_line, level_rank  # noqa: E402


def iter_events(paths):
    """逐行解析多个日志文件（含轮转副本）, 产出 (行号, 事件或 None, 原始行)。

    为什么不预读全文件: 比赛日志可达数十万行, tail/filter 都应流式处理,
    内存占用与文件大小解耦。
    """
    for path in paths:
        if not os.path.exists(path):
            sys.stderr.write("rmlog_read: 文件不存在: %s\n" % path)
            continue
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for lineno, raw in enumerate(fh, 1):
                ev = parse_line(raw)
                yield lineno, ev, raw.rstrip("\r\n")


def cmd_parse(args):
    """parse 子命令: pretty 打印每个合法事件; 残行以 [DROP] 标注（默认显示）。"""
    dropped = 0
    for lineno, ev, raw in iter_events([args.file]):
        if ev is None:
            dropped += 1
            if not args.quiet:
                print("  [DROP] L%-6d %s" % (lineno, raw[:80]))
            continue
        attrs = ("  " + " ".join("%s=%s" % kv for kv in sorted(ev["attrs"].items()))
                 if ev["attrs"] else "")
        print("L%-6d #%s %s (%s) [%s] %s %s: %s%s" % (
            lineno, ev["seq"], ev["wall_ts"], ev["mono_ts"], ev["level"],
            ev["code"], ev["module"], ev["message"], attrs))
    _summary(dropped)
    return 0


def cmd_tail(args):
    """tail 子命令: 输出最后 N 条; --follow 每秒轮询新行（类 tail -f）。

    follow 用"记住已读字节数 + 增量读"实现, 不依赖 inotify（板端探测 least
    surprise: 轮询在 Linux/Windows 行为一致, P0 不引入平台分支）。
    """
    path = args.file
    if args.follow:
        offset = 0
        if os.path.exists(path):
            offset = os.path.getsize(path)
            _tail_print(path, args.number)
        try:
            while True:
                if os.path.exists(path):
                    size = os.path.getsize(path)
                    if size < offset:      # 轮转/重建: 文件变小, 从头读新文件
                        offset = 0
                    if size > offset:
                        with open(path, "r", encoding="utf-8", errors="replace") as fh:
                            fh.seek(offset)
                            for raw in fh:
                                ev = parse_line(raw)
                                if ev is not None:
                                    _print_event(ev)
                        offset = size
                time.sleep(1.0)
        except KeyboardInterrupt:
            return 0
    else:
        return _tail_print(path, args.number)


def _tail_print(path, n):
    """非 follow 的 tail: 全量流式读, 仅打印最后 n 条合法事件。"""
    window = []
    dropped = 0
    for _, ev, _raw in iter_events([path]):
        if ev is None:
            dropped += 1
            continue
        window.append(ev)
        if len(window) > n:
            window.pop(0)
    for ev in window:
        _print_event(ev)
    _summary(dropped)
    return 0


def _print_event(ev):
    """单条事件的默认人读格式（tail/filter 共用; parse 用更详细的版式）。"""
    attrs = ("  " + " ".join("%s=%s" % kv for kv in sorted(ev["attrs"].items()))
             if ev["attrs"] else "")
    print("%s [%s] %s %s: %s%s" % (
        ev["wall_ts"], ev["level"], ev["code"], ev["module"], ev["message"], attrs))


def _summary(dropped):
    """把残行丢弃数打到 stderr —— stdout 保持纯事件流, 可安全重定向/管道。"""
    if dropped:
        sys.stderr.write("rmlog_read: 丢弃残行/非法行 %d 条\n" % dropped)


def cmd_filter(args):
    """filter 子命令: 级别（不低于）/错误码（前缀通配）/时间窗三组条件 AND 组合。

    时间窗基于墙上时间戳的字符串比较: 行格式 v1 的 wall_ts 是定宽 ISO8601,
    字典序即时间序, 无需解析成 datetime —— 既快又避免时区二次解释。
    """
    code_prefix = None
    if args.code:
        # --code 支持 E-INIT-* 形式的前缀通配（REQ AC5 原话就是这种用法）
        code_prefix = args.code[:-1] if args.code.endswith("*") else args.code
    dropped = 0
    matched = 0
    for _, ev, _raw in iter_events([args.file]):
        if ev is None:
            dropped += 1
            continue
        if args.level and level_rank(ev["level"]) < level_rank(args.level):
            continue
        if code_prefix is not None and not ev["code"].startswith(code_prefix):
            continue
        if args.since and ev["wall_ts"] < args.since:
            continue
        if args.until and ev["wall_ts"] > args.until:
            continue
        _print_event(ev)
        matched += 1
    _summary(dropped)
    sys.stderr.write("rmlog_read: 命中 %d 条\n" % matched)
    return 0


def build_parser():
    """参数解析器（三个子命令共用一套残行统计行为）。"""
    p = argparse.ArgumentParser(
        prog="rmlog_read.py",
        description="rmlog 读端工具: parse / tail / filter（行格式 v1）")
    sub = p.add_subparsers(dest="cmd", required=True)

    pp = sub.add_parser("parse", help="逐行解析并 pretty 打印（含残行标注）")
    pp.add_argument("file")
    pp.add_argument("--quiet", action="store_true", help="不打印残行原文")

    tp = sub.add_parser("tail", help="看最后 N 条; --follow 持续跟踪")
    tp.add_argument("file")
    tp.add_argument("-n", "--number", type=int, default=20)
    tp.add_argument("--follow", action="store_true")

    fp = sub.add_parser("filter", help="按级别/错误码/时间窗过滤（场下定位主力）")
    fp.add_argument("file")
    fp.add_argument("--level", choices=["INFO", "WARN", "ERROR", "FATAL"],
                    help="只看不低于该级别的行")
    fp.add_argument("--code", help="错误码, 支持前缀通配（如 E-INIT-*）")
    fp.add_argument("--since", help="起始墙上时间（含）, 如 2026-09-26T16:00")
    fp.add_argument("--until", help="结束墙上时间（含）")
    return p


def main(argv):
    """CLI 入口: 子命令分发。"""
    args = build_parser().parse_args(argv)
    if args.cmd == "parse":
        return cmd_parse(args)
    if args.cmd == "tail":
        return cmd_tail(args)
    return cmd_filter(args)


if __name__ == "__main__":
    # argv[0] 是脚本自身路径, 切掉后 argparse 才能拿到真正的子命令
    sys.exit(main(sys.argv[1:]))
