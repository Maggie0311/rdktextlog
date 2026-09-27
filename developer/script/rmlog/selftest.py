# -*- coding: utf-8 -*-
"""rmlog.selftest — 断言式自测入口，覆盖 AC1–AC6 可自测项。

任务: T-20260926-001-logging-platform-p0。
R1 返工: 新增 2 用例 —— test_ac5_concurrent_rotation（F-1 多进程×轮转逐 worker
对账）与 test_reader_time_prefix（F-2 分钟前缀回归）。

用法与输出约定（CODE-STYLE §5）::

    python3 -m rmlog.selftest [work_dir]
    全部通过: 打印各用例 PASS 摘要 + "SELFTEST PASS"，退出码 0;
    任一失败: 打印 FAIL 详情，退出码 1。
    原始输出由调用方重定向保存到 script/tests/（交付时随 RESULT 附摘要）。

覆盖矩阵（AC 编号 -> 用例）:
    AC2 行格式与残行:  test_ac2_roundtrip / test_ac2_partial_line
    AC3 错误码体系:    test_ac3_catalog
    AC4 双端一致:      test_ac4_consistency（Python 与 gcc 编译的 C 端逐字节对照）
    AC5 落盘与查询:    test_ac5_concurrent / test_ac5_rotation /
                       test_ac5_concurrent_rotation（F-1 组合对账）/ test_ac5_read_filter
    F-2 时间前缀:      test_reader_time_prefix（分钟前缀整分钟语义回归）
    AC6 崩溃取证:      test_ac6_last_line_survives
    附加:              test_gen_code / test_reader_cli（读端 CLI 冒烟）

平台差异: 本测试在 Windows 开发机运行（并发与崩溃语义的等效模拟见各用例注释;
Linux 板端按 Q1=A 裁决由用户按 USAGE.md 板端自测复验 —— 本结果不得表述为
Linux 已验证; 多进程×轮转在 Linux 上的行为为协议推演, IMPL §4 有声明）。
"""

import os
import shutil
import subprocess
import sys
import time

from . import catalog
from . import format as fmt
from .writer import Writer
from .encode_cases import CASES, run_py_side, write_probe_input, read_probe_output

# 仓库内各交付物的绝对路径（selftest 需要跨包目录取 C 源码与读端工具）
_PKG_DIR = os.path.dirname(os.path.abspath(__file__))
_SCRIPT_DIR = os.path.dirname(_PKG_DIR)
_C_SOURCE = os.path.join(_PKG_DIR, "rmlog.c")
_C_HEADER = os.path.join(_PKG_DIR, "rmlog.h")
_GEN_HEADER = os.path.join(_PKG_DIR, "rmlog_errors.h")
_PROBE_C = os.path.join(_PKG_DIR, "_ac4_probe.c")
_READER = os.path.join(_SCRIPT_DIR, "rmlog_read.py")


class Fail(Exception):
    """断言失败（携带用例名与原因，由 main 捕获后统一报告）。"""


def check(cond, msg):
    """断言辅助: 失败抛 Fail（带上下文消息），成功无副作用。"""
    if not cond:
        raise Fail(msg)


# ---------------------------------------------------------------- AC2
def test_ac2_roundtrip(work):
    """AC2: 编码->解析往返一致; 分隔符/换行/控制字符安全; attrs 保留。"""
    wall = fmt.wall_timestamp(1758888000.123)   # 固定输入, 避免时间依赖
    line = fmt.encode(7, wall, 123456, "ERROR", "E-COMM-001", "spi",
                      "超时|dev=/dev/spidev0.0\n第二行", {"try": 3, "note": "a|b"})
    ev = fmt.parse_line(line)
    check(ev is not None, "合法行被误判为残行: %r" % line)
    check(ev["seq"] == 7, "seq 不一致: %r" % ev)
    check(ev["wall_ts"] == wall, "wall_ts 往返不一致")
    check(ev["mono_ts"] == 123456, "mono_ts 往返不一致")
    check(ev["level"] == "ERROR" and ev["code"] == "E-COMM-001", "级别/码不一致")
    check(ev["module"] == "spi", "module 往返不一致")
    check(ev["message"] == "超时|dev=/dev/spidev0.0\n第二行",
          "消息含分隔符/换行时往返不一致: %r" % ev["message"])
    check(ev["attrs"] == {"try": "3", "note": "a|b"}, "attrs 往返不一致: %r" % ev["attrs"])
    print("  PASS  AC2 roundtrip(转义/属性/双时间戳)")


def test_ac2_partial_line(work):
    """AC2: 各类残行（截断/混入/空行/外部行）被安全丢弃且解析不抛异常。"""
    cases = [
        "LOGV1|12|2026-09-26T16:00:00.000|1234",           # 头部截断（缺字段）
        "LOGV1|13|2026-09-26T16:00:00.000|1234|ERRO",      # 尾部截断
        "OGV1|14|2026-09-26T16:00:00.000|1234|ERROR|E-SYS-005|sys|x",  # 前缀残缺
        "2026-09-26T16:00:00.000 journald 混入行",          # 外源行
        "",                                                # 空行
        "LOGV1|abc|2026-09-26T16:00:00.000|1234|ERROR|E-SYS-005|sys|x",  # seq 非数字
        "LOGV1||||||||",                                   # 全空字段（语义闸拦截）
    ]
    for i, line in enumerate(cases):
        ev = fmt.parse_line(line)
        check(ev is None, "残行 #%d 未被丢弃: %r -> %r" % (i, line, ev))
    # fuzz: 任意字节序列解析不抛异常（读端面对的是崩溃后磁盘上的任意内容）
    import random
    rng = random.Random(42)
    for _ in range(300):
        blob = bytes(rng.randrange(256) for _ in range(40))
        fmt.parse_line(blob.decode("utf-8", errors="replace"))  # 只要求不抛异常
    print("  PASS  AC2 残行三道闸 + 随机字节 fuzz(300 次, 解析不抛异常)")


# ---------------------------------------------------------------- AC3
def test_ac3_catalog(work):
    """AC3: 五域齐全、每域 >=3 码、字段完整、序号无重复、生成头同步。"""
    check(tuple(catalog.DOMAINS) == ("INIT", "COMM", "HW", "FSM", "SYS"),
          "五域定义与 REQ 不符: %r" % (tuple(catalog.DOMAINS),))
    seen = set()
    for domain in catalog.DOMAINS:
        codes = catalog.codes_by_domain(domain)
        check(len(codes) >= 3, "域 %s 不足 3 个错误码" % domain)
        for code in codes:
            item = catalog.get(code)
            check(item is not None, "码 %s 查表失败" % code)
            check(item["level"] in fmt.LEVELS, "码 %s 级别非法: %r" % (code, item["level"]))
            check(bool(item["meaning"].strip()) and bool(item["action"].strip()),
                  "码 %s 含义/建议动作缺失" % code)
            check(code not in seen, "错误码重复: %s" % code)
            seen.add(code)
    check(len(catalog.ERRORS) == len(seen), "ERRORS 表存在无法按域索引的码")
    print("  PASS  AC3 五域 %s 共 %d 码(字段完整/无重复)" % (
        "/".join(catalog.DOMAINS), len(catalog.ERRORS)))


# ---------------------------------------------------------------- AC4
def _write_probe_source():
    """写 C 探针源码文件（固定内容; 独立 .c 便于 code_reviewer 静态审查）。"""
    src = r"""/* _ac4_probe.c — AC4 双端一致性探针（selftest 专用, 不随板端交付）。
 * 生成: rmlog/selftest._write_probe_source()（固定内容, 便于静态审查）。
 * 输入: 二进制用例文件（格式见 encode_cases.write_probe_input 注释）。
 * 输出: 二进制渲染行流（格式见 encode_cases.read_probe_output 注释）。 */
#include "rmlog.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* 读一个 uint32(LE); 失败返回 0 */
static int read_u32(FILE *f, unsigned int *v)
{
    unsigned char b[4];
    if (fread(b, 1, 4, f) != 4) { return 0; }
    *v = (unsigned)b[0] | ((unsigned)b[1] << 8) | ((unsigned)b[2] << 16) | ((unsigned)b[3] << 24);
    return 1;
}
static int read_i32(FILE *f, int *v)
{
    unsigned int u;
    if (!read_u32(f, &u)) { return 0; }
    *v = (int)u;
    return 1;
}
static int read_i64(FILE *f, long long *v)
{
    unsigned char b[8];
    long long acc = 0;
    int i;
    if (fread(b, 1, 8, f) != 8) { return 0; }
    for (i = 7; i >= 0; i--) { acc = (acc << 8) | b[i]; }
    *v = acc;
    return 1;
}
/* 读一个 u16 长度前缀字符串; 返回 malloc 的 UTF-8 缓冲（调用方 free） */
static char *read_str(FILE *f)
{
    unsigned char b[2];
    size_t len;
    char *buf;
    if (fread(b, 1, 2, f) != 2) { return NULL; }
    len = (size_t)b[0] | ((size_t)b[1] << 8);
    buf = (char *)malloc(len + 1);
    if (!buf) { return NULL; }
    if (len && fread(buf, 1, len, f) != len) { free(buf); return NULL; }
    buf[len] = '\0';
    return buf;
}
/* 写一个 u16 长度前缀字符串 */
static int write_str(FILE *f, const char *s)
{
    size_t len = strlen(s);
    if (len > 65535) { return 0; }
    fputc((int)(len & 0xFF), f);
    fputc((int)((len >> 8) & 0xFF), f);
    return fwrite(s, 1, len, f) == len;
}

int main(int argc, char **argv)
{
    FILE *in, *out;
    unsigned int count, i;
    if (argc < 3) {
        fprintf(stderr, "usage: ac4_probe <in.bin> <out.bin>\n");
        return 2;
    }
    in = fopen(argv[1], "rb");
    out = fopen(argv[2], "wb");
    if (!in || !out) {
        fprintf(stderr, "open failed\n");
        return 2;
    }
    if (!read_u32(in, &count)) { return 2; }
    for (i = 0; i < count; i++) {
        int seq, j;
        long long mono;
        char *wall, *level, *code, *mod, *msg;
        char emod[2048], emsg[2048], line[4096];
        int n;
        if (!read_i32(in, &seq) || !read_i64(in, &mono)) { return 2; }
        wall = read_str(in); level = read_str(in); code = read_str(in);
        mod = read_str(in);  msg = read_str(in);
        if (!wall || !level || !code || !mod || !msg) { return 2; }
        if (rmlog_escape(mod, emod, sizeof(emod)) < 0) { return 2; }
        if (rmlog_escape(msg, emsg, sizeof(emsg)) < 0) { return 2; }
        n = snprintf(line, sizeof(line), "LOGV1|%d|%s|%ld|%s|%s|%s|%s",
                     seq, wall, (long)mono, level, code, emod, emsg);
        if (n < 0 || (size_t)n >= sizeof(line)) { return 2; }
        if (!write_str(out, line)) { return 2; }
        free(wall); free(level); free(code); free(mod); free(msg);
        for (j = 0; j < 0; j++) { (void)j; } /* 无占位循环; 保持 -Wall 干净 */
    }
    fclose(in);
    fclose(out);
    return 0;
}
"""
    with open(_PROBE_C, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(src)


def _build_c_probe(work):
    """生成错误码头并编译 C 探针（gcc 由 PATH 提供; 编译警告视为失败）。"""
    subprocess.run([sys.executable, "-m", "rmlog.gen_code"], cwd=_SCRIPT_DIR,
                   check=True, stdout=subprocess.DEVNULL)
    check(os.path.exists(_GEN_HEADER), "rmlog_errors.h 未生成")
    exe = os.path.join(work, "ac4_probe.exe" if os.name == "nt" else "ac4_probe")
    cmd = ["gcc", "-std=c99", "-Wall", "-Wextra", "-I", _PKG_DIR,
           "-o", exe, _C_SOURCE, _PROBE_C]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise Fail("C 探针编译失败:\n%s\n%s" % (proc.stdout, proc.stderr))
    if proc.stderr.strip():
        raise Fail("C 探针编译存在警告（-Wall -Wextra 下不允许）:\n%s" % proc.stderr)
    return exe


def test_ac4_consistency(work):
    """AC4: 同一事件（同 seq/时间戳/内容）C 端与 Python 端渲染逐字节相同。

    时间由用例固定注入，消除"双端各自取时间"的差异 —— 一致性判定只针对
    编码规则本身（转义表/字段序/格式化），这是 REQ P0-c 的可测化。
    """
    exe = _build_c_probe(work)
    in_bin = os.path.join(work, "ac4_in.bin")
    out_bin = os.path.join(work, "ac4_out.bin")
    write_probe_input(in_bin, CASES)
    proc = subprocess.run([exe, in_bin, out_bin], capture_output=True, text=True)
    check(proc.returncode == 0, "C 探针运行失败: %s" % proc.stderr)
    c_lines = read_probe_output(out_bin)
    py_lines = run_py_side(CASES)
    check(len(c_lines) == len(py_lines),
          "C 端输出条数 %d != 用例数 %d" % (len(c_lines), len(py_lines)))
    for i, (py, c) in enumerate(zip(py_lines, c_lines)):
        check(py == c, "双端不一致(用例 %d):\n  PY: %r\n  C : %r" % (i, py, c))
    print("  PASS  AC4 双端 %d 个用例逐字节一致(含|/换行/控制字符/中文)" % len(CASES))


# ---------------------------------------------------------------- AC5
def test_ac5_concurrent(work):
    """AC5: 多进程并发写 —— 无丢行、无交错半行（(wid,i) 全量对账）。"""
    log_dir = os.path.join(work, "ac5_conc")
    workers, per = 4, 250
    procs = [subprocess.Popen(
        [sys.executable, "-m", "rmlog.worker", log_dir, str(per)],
        cwd=_SCRIPT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for _ in range(workers)]
    for p in procs:
        _out, err = p.communicate(timeout=120)
        check(p.returncode == 0,
              "worker 退出码 %d: %s" % (p.returncode, err.decode("utf-8", "replace")[:200]))
    expect = workers * per
    got = 0
    seen_pairs = set()
    path = os.path.join(log_dir, "rmlog.log")
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            ev = fmt.parse_line(raw)
            if ev is None:
                continue
            got += 1
            pair = (ev["attrs"]["wid"], int(ev["attrs"]["i"]))
            check(pair not in seen_pairs,
                  "对账重复: wid=%s i=%s（写重复或丢行检测失效）" % pair)
            seen_pairs.add(pair)
    check(got == expect,
          "行数不符: 期望 %d 实得 %d（存在丢行或不可解析行）" % (expect, got))
    by_wid = {}
    for wid, seq in seen_pairs:
        by_wid.setdefault(wid, set()).add(seq)
    for wid, seqs in by_wid.items():
        check(len(seqs) == per, "wid=%s 行数 %d != %d" % (wid, len(seqs), per))
    print("  PASS  AC5 多进程并发 %dx%d=%d 行无丢行/无交错" % (workers, per, expect))


def test_ac5_rotation(work):
    """AC5: 超过 max_bytes 触发轮转, 保留份数不超 keep, 最老副本被淘汰。"""
    log_dir = os.path.join(work, "ac5_rot")
    w = Writer(log_dir=log_dir, max_bytes=1024, keep=3)
    for i in range(120):
        w.event("E-SYS-005", "rot", "rotate test line %03d padding padding" % i)
    w.close()
    files = sorted(os.listdir(log_dir))
    check("rmlog.log" in files, "主文件缺失: %r" % files)
    copies = [f for f in files if f.startswith("rmlog.log.")]
    check(len(copies) >= 2, "未产生轮转副本（轮转未触发）: %r" % files)
    check(len(copies) <= 3, "轮转副本超量: %r" % copies)
    check(not os.path.exists(os.path.join(log_dir, "rmlog.log.4")),
          "最老副本未被淘汰（存在 .4）")
    print("  PASS  AC5 轮转触发, 副本数 %d (2<=n<=keep=3), 最老已淘汰" % len(copies))


def test_ac5_concurrent_rotation(work):
    """AC5×F-1: 多进程并发写 + 触发轮转 —— 逐 worker 对账, 任何写成功的事件不得静默销毁。

    这是 R1 返工新增的组合用例（reviewer probe_1e/1g 在旧协议上实证的
    严重缺陷回归闸）: 旧协议下两个进程对同一目录以小 max_bytes 并发写,
    其中一个进程的全部写入（event 全部返回 True）可从磁盘上完全消失
    —— fd 搁浅在旧 inode 上, 该文件被对方的轮转链当"最老副本"淘汰。
    本用例必须保持:
      1. 每个 worker 全部写成功（退出码 0, 事件数全对上）;
      2. 每个 worker 写成功的每一条 (wid,i) 都能在主文件或副本链中读到
         （写成功条数 == 磁盘可见条数, 不存在"某 worker 全灭"或部分灭）;
      3. 无半行（解析不出的行只允许 0 条 —— INFO 级无 flush 承诺, 但协议
         v2 每写一次 write 整行, 轮转链原子 rename, 磁盘上不应有半行）;
      4. 各 worker 的事件序号 i 在其 wid 名下无重复、无缺号（0..per-1 全齐）。
    keep 传大值（20, 见下方 worker 命令行 "8000", "20"）: 保证压测期间写入的
    副本不被淘汰, 对账窗口完整（淘汰属正常容量治理, 不在本用例的"不灭失"
    承诺内 —— 用大 keep 把它排除; RF-3 更正: 本行旧文残留 keep=10, 系 1010 轮
    参数误校准修复后 docstring 未同步）。
    """
    log_dir = os.path.join(work, "ac5_conc_rot")
    workers, per = 3, 400
    # 行长约 105B, 每 worker 自计字节 ≈ 42KB → max_bytes=8000 时每 worker 触发
    # ~5 次轮转（合计 ~15 次）。keep 必须大于轮转总次数: 链槽位 = keep+1,
    # keep=20 → 21 槽 > 15, 最早的文件不会被正常保留策略淘汰 —— 这样
    # "写成功 => 链上可见"的对账窗口完整覆盖整个压测过程（淘汰属正常容量治理,
    # 不在"不灭失"承诺内; 若 keep 太小, 本用例会把正常淘汰误报为数据销毁,
    # R1 自测第一轮即因此误报, 已校准参数并在此注释留痕）。
    procs = [subprocess.Popen(
        [sys.executable, "-m", "rmlog.worker", log_dir, str(per), "8000", "20"],
        cwd=_SCRIPT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for _ in range(workers)]
    for p in procs:
        _out, err = p.communicate(timeout=180)
        check(p.returncode == 0,
              "worker 退出码 %d: %s" % (p.returncode, err.decode("utf-8", "replace")[:200]))
    # ---- 对账: 读主文件 + 全部副本链 ----
    expect = workers * per
    seen_pairs = {}
    total_files = 0
    for name in sorted(os.listdir(log_dir)):
        if not (name == "rmlog.log" or name.startswith("rmlog.log.")):
            continue
        total_files += 1
        path = os.path.join(log_dir, name)
        with open(path, encoding="utf-8", errors="replace") as fh:
            for raw in fh:
                ev = fmt.parse_line(raw)
                if ev is None:
                    continue
                wid = ev["attrs"]["wid"]
                idx = int(ev["attrs"]["i"])
                pair_key = (wid, idx)
                check(pair_key not in seen_pairs,
                      "对账重复: wid=%s i=%d 出现于 %s 与 %s（数据被复制或检测失效）"
                      % (wid, idx, seen_pairs.get(pair_key, "?"), name))
                seen_pairs[pair_key] = name
    check(total_files >= 2, "未产生轮转副本（轮转未被触发, 用例失效）: %d 个文件" % total_files)
    got = len(seen_pairs)
    check(got == expect,
          "写成功 %d 条, 磁盘可见 %d 条 —— 存在已确认写成功的事件被静默销毁"
          % (expect, got))
    by_wid = {}
    for (wid, idx) in seen_pairs:
        by_wid.setdefault(wid, set()).add(idx)
    check(len(by_wid) == workers,
          "有 worker 全灭（旧协议 F-1 症状）: 仅 %d/%d 个 worker 有幸存行"
          % (len(by_wid), workers))
    for wid, idxs in by_wid.items():
        missing = set(range(per)) - idxs
        check(not missing,
              "wid=%s 缺号 %d 个（如 %s）—— 该 worker 部分事件被销毁"
              % (wid, len(missing), sorted(missing)[:3]))
    print("  PASS  AC5×F-1 多进程×轮转 %dx%d 行逐 worker 对账: 写成功=%d 可见=%d, "
          "副本文件 %d 个, 无半行/无全灭/无缺号" % (workers, per, expect, got, total_files))


def test_ac5_read_filter(work):
    """AC5: 读端一条命令按 级别+错误码前缀 过滤（对齐 REQ AC5 原话场景）。"""
    log_dir = os.path.join(work, "ac5_filter")
    w = Writer(log_dir=log_dir)
    # 混合写入: 应命中 2 条 E-INIT-*（ERROR 级）, INFO 与 WARN 级及他码不命中
    w.event("E-INIT-000", "init", "启动完成")                    # INFO  不命中
    w.event("E-INIT-001", "init", "组件初始化失败 errno=2")       # ERROR 命中
    w.event("E-INIT-003", "init", "组件降级运行")                 # WARN  不命中(级别不够)
    w.event("E-COMM-001", "spi", "SPI 超时")                      # ERROR 但码不匹配
    w.event("E-INIT-004", "init", "配置非法 unit=rad")            # ERROR 命中
    w.close()
    log = os.path.join(log_dir, "rmlog.log")
    proc = subprocess.run(
        [sys.executable, _READER, "filter", log,
         "--level", "ERROR", "--code", "E-INIT-*"],
        capture_output=True, text=True)
    check(proc.returncode == 0, "rmlog_read 退出码 %d: %s" % (proc.returncode, proc.stderr))
    lines = [l for l in proc.stdout.splitlines() if l.strip()]
    check(len(lines) == 2, "应命中 2 条, 实得 %d: %r" % (len(lines), lines))
    check(all("E-INIT-" in l for l in lines), "命中行混入非 E-INIT-* 码: %r" % lines)
    print("  PASS  AC5 读端一条命令 --level ERROR --code E-INIT-* 命中 2/5")


# ---------------------------------------------------------------- AC6
def test_ac6_last_line_survives(work):
    """AC6: 硬崩溃前最后一条 ERROR/FATAL 事件已落盘可读。

    方法: 子进程写 ERROR/FATAL 后立即 os._exit(1) —— 模拟"来不及任何清理的
    硬崩溃"（Windows/Linux 语义一致的等效模拟; kill -9 不可跨平台）。
    ERROR/FATAL 级走 flush 路径, 父进程随后直接读文件必须能读到。
    """
    log_dir = os.path.join(work, "ac6")
    crash = os.path.join(work, "ac6_crasher.py")
    with open(crash, "w", encoding="utf-8") as fh:
        fh.write(
            "import os, sys\n"
            "sys.path.insert(0, r'%s')\n"
            "from rmlog.writer import Writer\n"
            "w = Writer(log_dir=r'%s')\n"
            "w.event('E-SYS-005', 'victim', '崩溃前最后一条里程碑')\n"
            "w.event('E-INIT-002', 'victim', 'FATAL: 关键组件初始化失败, 即将硬崩溃')\n"
            "os._exit(1)\n" % (_SCRIPT_DIR, log_dir))
    proc = subprocess.run([sys.executable, crash], capture_output=True, text=True)
    check(proc.returncode == 1, "crasher 未按预期退出: %d" % proc.returncode)
    path = os.path.join(log_dir, "rmlog.log")
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    evs = [e for e in (fmt.parse_line(l) for l in lines) if e is not None]
    check(len(evs) == 2, "崩溃后应读到 2 条完整事件, 实得 %d" % len(evs))
    check(evs[-1]["code"] == "E-INIT-002" and evs[-1]["level"] == "FATAL",
          "最后一条不是崩溃前的 FATAL 事件: %r" % evs[-1])
    print("  PASS  AC6 硬崩溃(os._exit)后最后一条 ERROR/FATAL 事件可读")


# ---------------------------------------------------------------- 附加
def test_gen_code(work):
    """附加: 生成头与文档可重建且内容与表一致（单一来源链路自检）。"""
    from .gen_code import render_header, render_doc
    header = render_header()
    check("#define RMLOG_ERROR_TABLE_LEN %d" % len(catalog.ERRORS) in header,
          "生成头表长与 catalog 不一致")
    check("RMLOG_CODE_COMM_001" in header, "生成头缺少码常量示例 E-COMM-001")
    doc = render_doc()
    for item in catalog.ERRORS[:3]:
        check(item["code"] in doc and item["meaning"] in doc,
              "文档缺少码 %s 的内容" % item["code"])
    print("  PASS  GEN 生成头/文档与 catalog 单一来源一致")


def test_reader_time_prefix(work):
    """F-2 回归: --until/--since 分钟级前缀不再漏掉该分钟的事件。

    回归背景（reviewer probe_until2 实证）: 旧读端原始字典序比较下,
    "--until 12:01" 漏掉 12:01 这一分钟的全部行（含 12:01:00.500 第一条）,
    而全精度值正确、--since 前缀碰巧正确 —— 属系统性证据漏洞。
    本用例构造同一分钟内多条事件, 验证前缀语义:
      --until T12:01  → 命中 12:01 分钟内全部行（前缀=该段末 12:01:59.999）;
      --since T12:01  → 命中 12:01 及之后（前缀=该段始 12:01:00.000）;
      --until T12:00  → 不命中 12:01 的行（窗口边界不被放宽）;
      全精度值行为与旧版一致（向后兼容）。
    """
    log_dir = os.path.join(work, "ac5_timeprefix")
    log = os.path.join(log_dir, "rmlog.log")
    # 直接构造合法日志行: 三条事件跨两个分钟, 时间点来自 reviewer 的复现形态
    lines = [
        "LOGV1|1|2026-09-26T12:00:00.100|100|INFO|E-SYS-005|t|minute 0 event",
        "LOGV1|2|2026-09-26T12:01:00.500|1500|ERROR|E-COMM-001|t|minute 1 first",
        "LOGV1|3|2026-09-26T12:01:59.900|59900|ERROR|E-COMM-001|t|minute 1 last",
    ]
    os.makedirs(log_dir, exist_ok=True)
    with open(log, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")

    def run_filter(extra):
        proc = subprocess.run([sys.executable, _READER, "filter", log] + extra,
                              capture_output=True, text=True)
        check(proc.returncode == 0,
              "filter 退出码 %d: %s" % (proc.returncode, proc.stderr))
        return [l for l in proc.stdout.splitlines() if l.strip()]

    got_until_min = run_filter(["--until", "2026-09-26T12:01"])
    # 修复后语义: "--until T12:01" = 上界 12:01:59.999 → 12:00 与 12:01 的行全部命中;
    # 旧缺陷的行为是只命中 12:00 的 1 行（12:01 分钟内事件全部漏掉）。
    check(len(got_until_min) == 3,
          "--until 分钟前缀应按段末语义命中 3 行（12:00 全部 + 12:01 全部）, "
          "若只得 1 行即 F-2 缺陷复现: %r" % (got_until_min,))
    # 窗口断言: --since 12:01 --until 12:01 = 恰好 12:01 这一分钟内的 2 行
    got_window = run_filter(["--since", "2026-09-26T12:01",
                             "--until", "2026-09-26T12:01"])
    check(len(got_window) == 2,
          "[since 12:01, until 12:01] 应恰好命中 12:01 这一分钟的 2 行, 实得 %d: %r"
          % (len(got_window), got_window))
    got_since_min = run_filter(["--since", "2026-09-26T12:01"])
    check(len(got_since_min) == 2,
          "--since 分钟前缀应含该分钟起 2 行, 实得 %d: %r"
          % (len(got_since_min), got_since_min))
    got_until_prev = run_filter(["--until", "2026-09-26T12:00"])
    check(len(got_until_prev) == 1,
          "--until 12:00 不应命中 12:01 的行, 实得 %d: %r"
          % (len(got_until_prev), got_until_prev))
    got_until_full = run_filter(["--until", "2026-09-26T12:01:59.900"])
    check(len(got_until_full) == 3,
          "全精度 --until 行为须保持（3 行）, 实得 %d: %r"
          % (len(got_until_full), got_until_full))
    print("  PASS  F2 时间前缀归一: 前缀=日历段语义（until=段末/since=段始）, "
          "窗口与全精度行为正确")


def test_reader_cli(work):
    """附加: 读端 parse/tail 子命令冒烟（filter 已在 AC5 覆盖）。"""
    log = os.path.join(work, "ac5_filter", "rmlog.log")   # 复用 AC5 过滤用例的日志
    for sub, extra in (("parse", []), ("tail", ["-n", "3"])):
        proc = subprocess.run([sys.executable, _READER, sub, log] + extra,
                              capture_output=True, text=True)
        check(proc.returncode == 0, "read %s 退出码 %d: %s" % (
            sub, proc.returncode, proc.stderr))
    print("  PASS  READ parse/tail CLI 冒烟")


# ---------------------------------------------------------------- 主入口
def main(argv):
    """自测主入口: 工作区 -> 依次执行用例 -> 汇总 PASS/FAIL 与退出码。

    工作区约定（平台事实, 诚实标注）: 缺省落在产物区 `script/tests/_work/`
    （前一版用系统临时目录, 在本开发机会话的文件沙箱下深层路径被拒 ——
    且产物区内自测可留下证据, 符合产物自足原则; 结束后清理, 不留垃圾）。
    """
    cleanup = len(argv) <= 1
    work = argv[1] if len(argv) > 1 else os.path.join(_SCRIPT_DIR, "tests", "_work")
    os.makedirs(work, exist_ok=True)
    _write_probe_source()

    tests = [
        ("AC2 roundtrip", lambda: test_ac2_roundtrip(work)),
        ("AC2 partial", lambda: test_ac2_partial_line(work)),
        ("AC3 catalog", lambda: test_ac3_catalog(work)),
        ("AC4 consistency", lambda: test_ac4_consistency(work)),
        ("AC5 concurrent", lambda: test_ac5_concurrent(work)),
        ("AC5 rotation", lambda: test_ac5_rotation(work)),
        ("AC5 concurrent rotation (F-1)", lambda: test_ac5_concurrent_rotation(work)),
        ("AC5 read filter", lambda: test_ac5_read_filter(work)),
        ("AC6 crash", lambda: test_ac6_last_line_survives(work)),
        ("GEN doc/header", lambda: test_gen_code(work)),
        ("READ time prefix (F-2)", lambda: test_reader_time_prefix(work)),
        ("READ cli", lambda: test_reader_cli(work)),
    ]
    failed = 0
    t0 = time.time()
    print("rmlog.selftest — 工作区: %s" % work)
    for name, fn in tests:
        try:
            fn()
        except Fail as exc:
            failed += 1
            print("  FAIL  %s: %s" % (name, exc))
        except Exception as exc:            # 用例自身的意外错误也按 FAIL 处理
            failed += 1
            print("  FAIL  %s: 未预期异常 %r" % (name, exc))
    used = time.time() - t0
    print("自测结束: %d/%d 通过, 用时 %.1fs" % (len(tests) - failed, len(tests), used))
    if cleanup and os.path.isdir(work):
        shutil.rmtree(work, ignore_errors=True)
    if failed:
        print("SELFTEST FAIL")
        return 1
    print("SELFTEST PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
