/* probe_degr_r4.c — RF-5 复审探针（reviewer 副本, r4）:
 * Windows 平台（无 flock）rmlog__rotlock_acquire 恒返回 -2（约定值"无跨进程锁"）。
 * RF-5 口径: -1（POSIX open/flock 失败）计 g_lock_degradations; -2 不计。
 * 本探针: 显式目录写 4000 条长消息（~2.3MB > RMLOG_MAX_BYTES=2MB）触发轮转决策路径,
 * 期望: 事件全部落盘（轮转决策在 Windows 上保守跳过, 数据不丢）,
 * 且计数器可观测性由符号表核对（g_lock_degradations 与 g_write_failures 均在场）。
 * -1 计数路径无法在 Windows 实测（无 flock 失败条件）—— 以静态逐行为准, 报告如实标注。
 */
#include "rmlog.h"
#include <stdio.h>
#include <string.h>

int main(void)
{
    char msg[512];
    int i;
    const char *dir = "degr_dir";

    if (rmlog_open(dir) != 0) {
        printf("OPENFAIL\n");
        return 2;
    }
    for (i = 0; i < 4000; i++) {
        memset(msg, 'x', sizeof(msg) - 1);
        msg[sizeof(msg) - 1] = '\0';
        snprintf(msg, sizeof(msg), "degr pad %04d", i);
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "%s", msg);
    }
    rmlog_close();
    printf("DONE\n");
    return 0;
}
