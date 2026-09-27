/* probe_fdleak_r4.c — RF-1 复审 handle 泄漏决定性测量探针（reviewer 副本, r4）:
 * rmlog__open_locked(a675c8d) 在 g_path 已有值分支内 open 一次(rmlog.c:164),
 * 函数尾部又无条件 open 一次(rmlog.c:175) —— 首个 fd 从未 close。
 * 静态确认之外, 用 GetProcessHandleCount 动态定量:
 *   先 warm up（建立 g_path）, 再做 1000 轮 "emit → close" 循环;
 *   每轮 emit 走一次 g_path 复用重开（泄漏 1 个文件句柄）, close 只关第二个 fd。
 * 预期（若泄漏成立）: after - base ≈ 1000;
 * 若无泄漏: after - base ≈ 0~2（环境噪声）。
 */
#include "rmlog.h"
#include <stdio.h>
#include <windows.h>

static long hcount(void)
{
    DWORD c = 0;
    if (!GetProcessHandleCount(GetCurrentProcess(), &c)) {
        return -1;
    }
    return (long)c;
}

int main(void)
{
    const char *dir = "fdleak_dir";
    long base, after;
    int i;

    if (rmlog_open(dir) != 0) {
        printf("OPENFAIL\n");
        return 2;
    }
    RMLOG_I("probe", RMLOG_CODE_INIT_000, "warmup establish g_path");
    rmlog_close();

    base = hcount();
    for (i = 0; i < 1000; i++) {
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "leak cycle %04d", i);
        rmlog_close();
    }
    after = hcount();
    printf("HANDLES base=%ld after=%ld delta=%ld\n", base, after, after - base);
    return 0;
}
