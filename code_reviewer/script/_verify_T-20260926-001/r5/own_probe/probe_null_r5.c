/* probe_null_r5.c — code_reviewer 独立验证件（R5 复审）: rmlog_open(NULL) 三分支定量。
 *
 * 配合修改副本编译（宏替换仅发生在本角色验证区内的副本, 不触碰被审区）:
 *   mode=default  : 副本 A（RMLOG_DEFAULT_DIR → 本验证区目录）→ 期望 open(NULL)=0,
 *                   事件落缺省目录, 句柄 delta=0 —— 覆盖分支①（缺省目录可用）;
 *   mode=fallback : 副本 B（DEFAULT→Q:/bogus 不可建, FALLBACK → 本验证区目录）
 *                   → 期望 open(NULL)=0, 事件落回退目录, delta=0 —— 覆盖分支②;
 *   mode=failboth : 副本 C（DEFAULT/FALLBACK → Q:/bogus* 均不可建）→ 期望
 *                   open(NULL)=-1, g_path 保持空 —— 覆盖分支③（两级皆败）。
 *   另: 未修改副本在本机沙箱下 /userdata 与 /var/log 均不可建, 已自然复现分支③
 *   返回 -1（见运行留档 probe_null_run.log）。
 * 口径: GetProcessHandleCount。用法: probe_null_r5.exe <default|fallback|failboth>
 */
#include "rmlog.h"
#include <stdio.h>
#include <string.h>
#include <windows.h>

/* 本角色验证区内落盘检查点（避免经命令行 -D 传引号字符串） */
#define R5_NULLRUN "D:/rdk_x5_software/code_reviewer/script/_verify_T-20260926-001/r5/own_probe/nullrun"

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
    long b, a, l;
    int ret;
    const char *mode = (argc > 1) ? argv[1] : "default";
    const char *chk;

    if (strcmp(mode, "default") == 0) {
        chk = R5_NULLRUN "/rmlog.log";
    } else if (strcmp(mode, "fallback") == 0) {
        chk = R5_NULLRUN "/rmlog.log";
    } else {
        chk = NULL;
    }

    b = hcount();
    ret = rmlog_open(NULL);
    if (ret == 0) {
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "r5 null-default open (%s)", mode);
    }
    a = hcount();
    printf("R5_NULL mode=%s ret=%d base=%ld after=%ld delta=%ld", mode, ret, b, a, a - b);
    if (chk) {
        l = count_lines(chk);
        printf(" lines=%ld", l);
        if (l < 1) {
            fprintf(stderr, "\nself-check failed: no line landed in expected default dir\n");
            return 2;
        }
    } else if (ret == 0) {
        fprintf(stderr, "\nself-check failed: failboth mode unexpectedly opened\n");
        return 2;
    }
    printf("\n");
    return 0;
}
