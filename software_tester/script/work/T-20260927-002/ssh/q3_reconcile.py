# -*- coding: utf-8 -*-
"""q3_reconcile.py — 多进程×轮转逐 worker 对账工具（本角色测试工件，不改被测源码）。

用法: python3 q3_reconcile.py <dir> <workers> <per_worker> [dir2 workers2 per2 ...]
扫描 dir 下 rmlog.log 与 rmlog.log.* 全部文件，逐行解析，统计:
  写成功数(期望)、磁盘可见有效行、半行/残行数、每 worker 幸存数与缺号集、重复、文件数。
"""
import os, sys, re
sys.path.insert(0, "/root/rmlog_test/src")
from rmlog import format as fmt


def scan(d, workers, per):
    seen = {}   # (wid, i) -> filename
    halves = 0
    total_lines = 0
    files = []
    for f in sorted(os.listdir(d)):
        if not (f == "rmlog.log" or f.startswith("rmlog.log.")):
            continue
        files.append(f)
        with open(os.path.join(d, f), encoding="utf-8", errors="replace") as fh:
            for l in fh:
                s = l.rstrip("\r\n")
                if not s:
                    continue
                total_lines += 1
                ev = fmt.parse_line(s)
                if ev is None:
                    halves += 1
                    continue
                try:
                    wid = int(ev["attrs"]["wid"])
                    idx = int(ev["attrs"]["i"])
                except Exception:
                    # 无 wid/i attrs 的写入者（solo 基线）: 从 message 提取序号
                    m = re.search(r"solo line (\d+)", ev.get("message", ""))
                    if m:
                        wid = 0
                        idx = int(m.group(1))
                    else:
                        halves += 1
                        continue
                key = (wid, idx)
                if key in seen:
                    pass  # duplicate
                seen[key] = f
    expect = workers * per
    got = len(seen)
    by_wid = {}
    for (wid, idx) in seen:
        by_wid.setdefault(wid, set()).add(idx)
    print("=== DIR %s ===" % d)
    print("files=%d (%s)" % (len(files), files))
    print("expect_written=%d  visible=%d  halves=%d  total_lines=%d" % (expect, got, halves, total_lines))
    print("workers_with_survivors=%d/%d" % (len(by_wid), workers))
    all_contig = True
    for wid in sorted(by_wid):
        idxs = by_wid[wid]
        missing = sorted(set(range(per)) - idxs)
        lo, hi = min(idxs), max(idxs)
        interior = sorted(set(range(lo, hi + 1)) - idxs)  # 幸存区间内的洞 = 非淘汰性损失(F-1 症状)
        contig = (len(interior) == 0)
        all_contig = all_contig and contig
        print("  wid=%s surviving=%d range=[%d..%d] missing=%d interior_holes=%d %s%s"
              % (wid, len(idxs), lo, hi, len(missing), len(interior),
                 "CONTIGUOUS-SUFFIX" if contig else "HAS-INTERIOR-HOLES",
                 "" if len(interior) == 0 else (" %s" % interior[:8])))
    # 全灭检测
    full_extinct = (len(by_wid) < workers)
    # 结论分两级:
    #   A) 无淘汰场景(keep 足够): 要求可见==写成功 且 无半行 且 每 worker 0..per-1 全齐
    #   B) 有淘汰场景(keep 小): 要求无 worker 全灭 且 每 worker 幸存为连续后缀(无内部洞)
    no_eviction = (got == expect)
    ok = False
    if no_eviction:
        ok = (halves == 0) and (not full_extinct) and all(len(by_wid[w]) == per for w in by_wid)
        verdict = "OK(无静默销毁, 无淘汰全量对账)" if ok else "DEGRADED(残行/全灭/缺号)"
    else:
        ok = (halves == 0) and (not full_extinct) and all_contig
        verdict = "OK(无静默销毁: 无全灭且幸存为连续后缀, 缺失属正常轮转淘汰)" if ok else "DEGRADED(全灭或内部洞=F-1 症状)"
    print("RESULT %s: expect=%d visible=%d halves=%d survivors=%d/%d evicted=%d -> %s"
          % (os.path.basename(d), expect, got, halves, len(by_wid), workers, expect - got, verdict))
    print()


def main():
    args = sys.argv[1:]
    for i in range(0, len(args), 3):
        d = args[i]
        workers = int(args[i + 1])
        per = int(args[i + 2])
        scan(d, workers, per)


if __name__ == "__main__":
    main()
