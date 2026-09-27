/* probe_fdleak2_r4.c — 泄漏源对照实验（reviewer 副本, r4）:
 * 模式 B（先跑, 避免 A 的累积影响基线）: open 一次 + emit 1000 条, 不 close
 *   —— emit 走 g_fd>=0 的 reopen_current 快路径, 不经过 rmlog__open_locked
 *   的 g_path 复用分支 → 期望 delta ≈ 0~2（环境噪声）。
 * 模式 A: emit→close × 500 —— 每轮走一次 g_path 复用重开（泄漏 1 个句柄）
 *   → 期望 delta ≈ 500（与轮数 1:1, 比例性证明）。
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
    const char *dir = "fdleak2_dir";
    long base, after;
    int i;

    if (rmlog_open(dir) != 0) {
        printf("OPENFAIL\n");
        return 2;
    }

    /* ---- 模式 B: 常驻 fd, 1000 条 emit, 不 close ---- */
    base = hcount();
    for (i = 0; i < 1000; i++) {
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "modeB fastpath %04d", i);
    }
    after = hcount();
    printf("MODE_B base=%ld after=%ld delta=%ld\n", base, after, after - base);

    /* ---- 模式 A: emit→close × 500（每轮一次 g_path 复用重开） ---- */
    base = hcount();
    for (i = 0; i < 500; i++) {
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "modeA reopen cycle %04d", i);
        rmlog_close();
    }
    after = hcount();
    printf("MODE_A base=%ld after=%ld delta=%ld\n", base, after, after - base);
    return 0;
}
