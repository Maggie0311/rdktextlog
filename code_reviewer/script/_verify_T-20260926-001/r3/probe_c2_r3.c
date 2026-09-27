/* probe_c2_r3.c — 复审 C 端专项探针（显式目录版, 验证区内自建）:
 * 1) rmlog_open(显式目录) → 4 级事件各一条 → rmlog_close 两次（幂等）→
 *    再次 RMLOG_I（F-8: close 后 emit 按需重开继续记录）→ flush → close;
 * 2) 轮转分支: 3200 条长消息（~750B/行）触发 RMLOG_MAX_BYTES=2MB 轮转;
 *    每 500 条插一条 FATAL（AC6 fdatasync/_commit 与轮转组合）;
 *    事件总量 2.4MB < 链容量(2MB x 6) → 无淘汰, 可全量对账;
 * 3) 退出前 rmlog_close 落盘 INFO（rmlog_close 的 fdatasync 路径）。
 */
#include "rmlog.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    int i;
    char msg[512];
    const char *dir = "probe_c_dir";

    if (rmlog_open(dir) != 0) {
        printf("open failed\n");
        return 2;
    }
    RMLOG_I("ctrl", RMLOG_CODE_INIT_000, "probe start state=%d", 1);
    RMLOG_W("pwr",  RMLOG_CODE_HW_005,   "probe warn v=%d", 22500);
    RMLOG_E("spi",  RMLOG_CODE_COMM_001, "probe error dev=%s", "/dev/spidev0.0");
    RMLOG_F("fsm",  RMLOG_CODE_FSM_004,  "probe fatal st=%d", 7);
    rmlog_close();
    rmlog_close();   /* 幂等 */
    RMLOG_I("ctrl", RMLOG_CODE_INIT_000, "after close emit continues (F-8)");
    rmlog_close();

    /* 轮转分支 */
    if (rmlog_open(dir) != 0) {
        printf("reopen failed\n");
        return 2;
    }
    for (i = 0; i < 3200; i++) {
        memset(msg, 'x', sizeof(msg) - 1);
        msg[sizeof(msg) - 1] = '\0';
        snprintf(msg, sizeof(msg), "long event %04d pad", i);
        RMLOG_I("probe", RMLOG_CODE_SYS_005, "%s", msg);
        if (i % 500 == 0) {
            RMLOG_F("probe", RMLOG_CODE_FSM_004, "fatal checkpoint %04d", i);
        }
    }
    rmlog_close();
    printf("probe2 done\n");
    return 0;
}
