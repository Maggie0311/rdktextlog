/* probe_fdleak_r5.c — code_reviewer 独立验证件（R5 复审, REVIEW-T-20260926-001-rf6-2d83644）
 *
 * 目的: 对 commit 2d83644 的 rmlog.c 独立复核 RF-6 修复 —— close 后按需重开
 *       路径（rmlog__open_locked 的 g_path 复用分支）句柄数是否恒定。
 * 口径: 与 reviewer 上轮 W5（probe_fdleak_r4.c）同构 —— GetProcessHandleCount
 *       定量, 双组隔离变量:
 *         reopen 组: rmlog_open(显式目录) 后 1 条 emit + rmlog_close, 循环 N 轮
 *                    （每轮恰走一次 rmlog__open_locked 按需重开, RF-6 触发面）;
 *         fast 组:   常驻 fd 连续 N 条 emit, 零重开（对照组, 应恒定）;
 *         null 组:   rmlog_open(NULL)->close 循环 N/2 轮（rmlog_open(NULL) 入口
 *                    独立定量; 进程内已有 g_path, 走 rmlog__open_locked 复用
 *                    分支 —— 缺省裁决分支由 probe_null_r5.c 以全新进程覆盖）。
 *       注: rmlog_open(NULL) 的落点为缺省目录 /userdata/rmlog（库的缺省裁决）,
 *       故 null 组不产生本探针目录内的落盘行; 其打开成功与否以返回值判定。
 * 预期: 修复后（2d83644）delta 全 0; 修复前（a675c8d）reopen 组 delta=N（1:1）。
 * 用法: probe_fdleak_r5.exe <rounds> <reopen_dir> <fast_dir>
 */
#include "rmlog.h"
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

static long hcount(void)
{
    DWORD n = 0;
    GetProcessHandleCount(GetCurrentProcess(), &n);
    return (long)n;
}

static long count_lines(const char *path)
{
    FILE *f = fopen(path, "rb");
    long n = 0;
    char buf[4096];
    if (!f) return -1;
    while (fgets(buf, sizeof(buf), f) != NULL) n++;
    fclose(f);
    return n;
}

int main(int argc, char **argv)
{
    long rounds, i;
    long b_re, a_re, b_fa, a_fa, b_nu, a_nu;
    long l_re, l_fa;
    const char *re_dir, *fa_dir;
    char p[1024];

    if (argc < 4) {
        fprintf(stderr, "usage: probe_fdleak_r5 <rounds> <reopen_dir> <fast_dir>\n");
        return 2;
    }
    rounds = atol(argv[1]);
    re_dir = argv[2];
    fa_dir = argv[3];
    if (rounds <= 0) return 2;

    /* ---- reopen 组: 每轮 emit -> close, 每轮恰走一次按需重开 ---- */
    if (rmlog_open(re_dir) != 0) { fprintf(stderr, "open(re) failed\n"); return 2; }
    rmlog_close();                 /* 保证第一轮 emit 即走重开路径 */
    b_re = hcount();
    for (i = 0; i < rounds; i++) {
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "r5 reopen round %ld", i);
        rmlog_close();
    }
    a_re = hcount();

    /* ---- fast 组: 常驻 fd 连续 emit, 零重开（对照） ---- */
    if (rmlog_open(fa_dir) != 0) { fprintf(stderr, "open(fa) failed\n"); return 2; }
    b_fa = hcount();
    for (i = 0; i < rounds; i++) {
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "r5 fast emit %ld", i);
    }
    a_fa = hcount();
    rmlog_close();

    /* ---- null 组: rmlog_open(NULL)->close 循环（rmlog_open(NULL) 入口独立定量;
     *      落点为缺省目录 /userdata/rmlog, 无本目录落盘行, 以返回值判定成败） ---- */
    b_nu = hcount();
    for (i = 0; i < rounds / 2; i++) {
        if (rmlog_open(NULL) != 0) { fprintf(stderr, "open(NULL) failed at %ld\n", i); return 2; }
        rmlog_close();
    }
    a_nu = hcount();

    /* ---- 落盘自检: reopen/fast 两组各 N 行（落点漂移则行数不足） ---- */
    snprintf(p, sizeof(p), "%s/rmlog.log", re_dir);
    l_re = count_lines(p);
    snprintf(p, sizeof(p), "%s/rmlog.log", fa_dir);
    l_fa = count_lines(p);

    printf("R5_PROBE rounds=%ld reopen:base=%ld after=%ld delta=%ld fast:base=%ld after=%ld delta=%ld null:base=%ld after=%ld delta=%ld lines=%ld/%ld\n",
           rounds,
           b_re, a_re, a_re - b_re,
           b_fa, a_fa, a_fa - b_fa,
           b_nu, a_nu, a_nu - b_nu,
           l_re, l_fa);

    if (l_re < rounds || l_fa < rounds) {
        fprintf(stderr, "self-check failed: lines reopen=%ld fast=%ld (expect >= %ld each)\n",
                l_re, l_fa, rounds);
        return 2;
    }
    if (a_re - b_re >= 10 || a_fa - b_fa >= 10 || a_nu - b_nu >= 10) {
        fprintf(stderr, "R5 LEAK REGRESSION: handle count grew (reopen/fast/null)\n");
        return 3;
    }
    return 0;
}
