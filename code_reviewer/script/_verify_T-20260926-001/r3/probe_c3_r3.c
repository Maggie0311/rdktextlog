/* probe_c3_r3.c — C 端轮转分支探针（修正版: 显式填充保证行长约 690B）:
 * 4000 条长事件（≈2.76MB > 2MB → 触发约 2 次轮转）+ 每 500 条 FATAL（AC6 组合）。
 * 对账: seq 1..4008 连续无缺、无半行、rmlog.log.1/.2 存在、单文件 ≤ max+一行。
 */
#include "rmlog.h"
#include <stdio.h>
#include <string.h>

int main(void)
{
    int i;
    char msg[640];
    const char *dir = "probe_c3_dir";

    if (rmlog_open(dir) != 0) {
        printf("open failed\n");
        return 2;
    }
    for (i = 0; i < 4000; i++) {
        int pref = snprintf(msg, sizeof(msg), "long event %04d ", i);
        memset(msg + pref, 'x', sizeof(msg) - (size_t)pref - 1);
        msg[sizeof(msg) - 1] = '\0';
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "%s", msg);
        if (i % 500 == 0) {
            RMLOG_F("probe", RMLOG_CODE_FSM_004, "fatal checkpoint %04d", i);
        }
    }
    rmlog_close();
    printf("probe3 done\n");
    return 0;
}
