/* （maintainer 补注：RF-6 句柄泄漏回归探针，selftest 第 10 用例编译执行。双组隔离变量：
 * reopen 组（每轮 emit→close，恰走一次 rmlog__open_locked 按需重开 = RF-6 泄漏触发面）与
 * fast 组（常驻 fd 零重开，对照）。判定口径 = 进程句柄数增量 <10；另有落盘自检（行数≥轮数）
 * 防"跑完但没写"的空洞通过。修复前后对照数据在 tests/probe_fdleak_rf6_before_after.log。）
 */
/* probe_fdleak_rf6.c — RF-6 句柄泄漏回归探针（T-20260926-001-logging-platform-p0）。
 *
 * 用途（R3 终轮微修复, 复审报告 REVIEW-T-20260926-001-rf-a675c8d §6 RF-6 的回归闸）:
 *   定量检测 C 端 rmlog 的"emit→close 循环重开"路径是否泄漏文件句柄。
 *
 * 回归背景:
 *   R2（commit a675c8d）的 RF-1 修复实现残留旧结构 —— rmlog__open_locked 各分支
 *   先 open 一次、函数尾部又无条件第二次 open, 首个 fd 从未 close 即被覆盖:
 *   每次按需重开泄漏 1 个文件句柄。修复前本探针 1000 轮 emit→close 实测
 *   delta=+1000（1:1 精确泄漏; 对照快路径 delta=0, 500 轮 +498 比例性成立,
 *   原始数据见同目录 probe_fdleak_rf6_before_after.log）; 修复后 delta 恒定。
 *
 * 覆盖的两条路径（隔离变量 = 是否经 rmlog__open_locked 按需重开）:
 *   1) reopen 组: rmlog_open(显式目录) 后, 每轮 1 条 INFO 事件 + rmlog_close ——
 *      每轮 emit 都因 fd 已关而走一次 rmlog__open_locked 的 g_path 复用重开
 *      （RF-6 的主要触发面, rmlog.h 记载的合法用法）; 显式目录保证落点固定,
 *      不触达缺省目录裁决（开发机为 Windows, 缺省目录 /userdata 系板端路径）。
 *   2) fast 组: 常驻 fd 连续 1000 条 INFO 事件, 全程零次重开 —— 泄漏若存在,
 *      只会出现在 1) 的重开路径上, 2) 应恒定。
 *
 * 判定: 进程句柄数增量（GetProcessHandleCount, Windows; POSIX 等效为描述符计数）
 *   每组 < 10 视为无泄漏。泄漏形态是 1:1 线性增长（修复前 +1000）, 与恒定基线
 *   相差三个数量级, 阈值放宽 10 仅用于排除 CRT/探针自身的非日志句柄抖动。
 *   探针退出码: 0=两组均无泄漏; 3=任一组超阈值。
 *
 * 用法: probe_fdleak_rf6 <轮数> <reopen日志目录> <fast日志目录>
 * 编译（开发机 MinGW, _WIN32 分支无 pthread）:
 *   gcc -std=c99 -Wall -Wextra -I rmlog -o probe_fdleak_rf6.exe rmlog/rmlog.c tests/probe_fdleak_rf6.c
 * 编译（板端 Linux; rmlog.c 已源码内定义 _POSIX_C_SOURCE 使 -std=c99 可编译,
 *   POSIX 分支用到 pthread 故追加 -lpthread —— glibc≥2.34 已并入 libc 可省,
 *   显式给出以兼容旧 glibc）:
 *   gcc -std=c99 -Wall -Wextra -I rmlog -o probe_fdleak_rf6 rmlog/rmlog.c tests/probe_fdleak_rf6.c -lpthread
 * （selftest 用例 RF6 以同口径编译并自动执行本探针。）
 */
#include "rmlog.h"
#include <stdio.h>
#include <stdlib.h>

#if defined(_WIN32)
#include <windows.h>
static long probe_handle_count(void)
{
    DWORD n = 0;
    GetProcessHandleCount(GetCurrentProcess(), &n);
    return (long)n;
}
#else
/* POSIX 等效口径: 打开描述符计数（/proc/self/fd 目录项数, Linux）。
 * 板端 X5/Linux 上同样可跑, 口径与 Windows 侧的"进程句柄数"语义对齐。 */
#include <dirent.h>
static long probe_handle_count(void)
{
    DIR *d = opendir("/proc/self/fd");
    long n = 0;
    struct dirent *e;
    if (!d) {
        return -1;              /* 非 Linux/proc 不可用时调用方按失败处理 */
    }
    while ((e = readdir(d)) != NULL) {
        n++;                    /* 含 "." 与 "..", 只作相对比较基线, 无碍 */
    }
    closedir(d);
    return n;
}
#endif

/* 数一个文本文件的行数（探针自检用: 防止"探针跑完但什么都没写"的空洞通过） */
static long probe_count_lines(const char *path)
{
    FILE *f = fopen(path, "rb");
    long n = 0;
    char buf[4096];
    if (!f) {
        return -1;
    }
    while (fgets(buf, sizeof(buf), f) != NULL) {
        n++;
    }
    fclose(f);
    return n;
}

int main(int argc, char **argv)
{
    long rounds, base_reopen, after_reopen, base_fast, after_fast;
    long lines_reopen, lines_fast;
    long i;
    const char *reopen_dir, *fast_dir;

    if (argc < 4) {
        fprintf(stderr, "usage: probe_fdleak_rf6 <rounds> <reopen_dir> <fast_dir>\n");
        return 2;
    }
    rounds = atol(argv[1]);
    reopen_dir = argv[2];
    fast_dir = argv[3];
    if (rounds <= 0) {
        fprintf(stderr, "rounds must be positive\n");
        return 2;
    }

    /* ---- 1) reopen 组: 每轮 emit(1 条) → close, 每轮恰走一次按需重开 ---- */
    if (rmlog_open(reopen_dir) != 0) {
        fprintf(stderr, "rmlog_open(%s) failed\n", reopen_dir);
        return 2;
    }
    rmlog_close();              /* 先关一次: 保证第一轮 emit 即走重开路径 */
    base_reopen = probe_handle_count();
    for (i = 0; i < rounds; i++) {
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "rf6 reopen round %ld", i);
        rmlog_close();
    }
    after_reopen = probe_handle_count();

    /* ---- 2) fast 组: 常驻 fd 连续 emit, 全程零次重开（对照） ---- */
    if (rmlog_open(fast_dir) != 0) {
        fprintf(stderr, "rmlog_open(%s) failed\n", fast_dir);
        return 2;
    }
    base_fast = probe_handle_count();
    for (i = 0; i < rounds; i++) {
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "rf6 fast emit %ld", i);
    }
    after_fast = probe_handle_count();
    rmlog_close();

    /* ---- 自检: 事件确实落盘（每组各 rounds 行）, 排除空洞通过 ---- */
    {
        char p[1024];
        snprintf(p, sizeof(p), "%s/rmlog.log", reopen_dir);
        lines_reopen = probe_count_lines(p);
        snprintf(p, sizeof(p), "%s/rmlog.log", fast_dir);
        lines_fast = probe_count_lines(p);
    }
    if (lines_reopen < rounds || lines_fast < rounds) {
        fprintf(stderr, "probe self-check failed: lines reopen=%ld fast=%ld (expect >= %ld each)\n",
                lines_reopen, lines_fast, rounds);
        return 2;
    }

    printf("RF6_PROBE reopen:base=%ld after=%ld delta=%ld fast:base=%ld after=%ld delta=%ld rounds=%ld lines=%ld/%ld\n",
           base_reopen, after_reopen, after_reopen - base_reopen,
           base_fast, after_fast, after_fast - base_fast,
           rounds, lines_reopen, lines_fast);

    if (after_reopen - base_reopen >= 10 || after_fast - base_fast >= 10) {
        fprintf(stderr, "RF-6 REGRESSION: handle count grew with reopen rounds (leak present)\n");
        return 3;
    }
    return 0;
}
