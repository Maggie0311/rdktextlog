/* probe_c_r3.c — 复审 C 端专项探针（验证区内自建, 不触碰被审代码）:
 * 1) example 同构: 4 级事件各一条 → 落盘 4 行;
 * 2) F-8 行为核实: rmlog_close() 后再次 RMLOG_I → 按需重开继续记录（非无操作）;
 * 3) AC6 组合: FATAL 先落盘再返回（fdatasync/_commit 路径不崩溃）;
 * 4) rmlog_close 幂等（重复 close 安全）。
 * 编译: gcc -std=c99 -Wall -Wextra -I <pkg>/rmlog -o probe_c_r3.exe probe_c_r3.c <pkg>/rmlog/rmlog.c
 */
#include "rmlog.h"
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    RMLOG_I("ctrl", RMLOG_CODE_INIT_000, "probe start state=%d", 1);
    RMLOG_W("pwr",  RMLOG_CODE_HW_005,   "probe warn v=%d", 22500);
    RMLOG_E("spi",  RMLOG_CODE_COMM_001, "probe error dev=%s", "/dev/spidev0.0");
    RMLOG_F("fsm",  RMLOG_CODE_FSM_004,  "probe fatal st=%d", 7);
    rmlog_close();
    rmlog_close();   /* 幂等 */
    RMLOG_I("ctrl", RMLOG_CODE_INIT_000, "after close emit continues (F-8 behavior)");
    rmlog_flush();
    rmlog_close();
    printf("probe done, path=%s\n", rmlog_path() ? rmlog_path() : "(null after close)");
    return 0;
}
