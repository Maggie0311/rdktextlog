/* probe_rf1_r4.c — RF-1 复审功能探针（reviewer 副本, r4）:
 * 显式目录 open → 2 条事件 → close×2（幂等）→ 再 emit 2 条 → close;
 * 对账: rf1_dir/rmlog.log 恰 4 行, seq ∈ {1,2,3,4} —— close 后那条(seq=3)
 * 必须落回显式目录（RF-1 修复点）, 且不得出现任何轮转副本（未触发轮转）。
 * （r3 版 probe_c2 曾在旧代码上实证 close 后事件丢失 —— 本探针为其同构复验。） */
#include "rmlog.h"
#include <stdio.h>

int main(void)
{
    const char *dir = "rf1_dir";

    if (rmlog_open(dir) != 0) {
        printf("OPENFAIL\n");
        return 2;
    }
    RMLOG_I("ctrl", RMLOG_CODE_INIT_000, "rf1 before close seq1");
    RMLOG_W("pwr",  RMLOG_CODE_HW_005,   "rf1 before close seq2");
    rmlog_close();
    rmlog_close();   /* 幂等 */
    RMLOG_E("spi",  RMLOG_CODE_COMM_001, "rf1 after close seq3 (RF-1 reopen target)");
    RMLOG_F("fsm",  RMLOG_CODE_FSM_004,  "rf1 after close seq4");
    rmlog_close();
    printf("DONE\n");
    return 0;
}
