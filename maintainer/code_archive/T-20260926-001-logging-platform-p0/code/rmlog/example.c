/* （maintainer 补注：C 接口最小使用示例，也是 USAGE §2 快速体验与 IMPL §3 复现命令编译的对象。
 * 要点：错误码一律用生成头的 RMLOG_CODE_* 常量（不要裸写字符串）；板端链接在命令尾追加 -lpthread。）
 */
/*
 * example.c — rmlog C 接口最小使用示例（随 P0 交付, 供自测与业务接入参考）。
 *
 * 任务: T-20260926-001-logging-platform-p0（REQ §4 P0-c）。
 *
 * 演示内容:
 * 1. rmlog_open 显式目录（跨平台演示的关键: Windows 开发机没有 /userdata,
 *    所以示例从 argv[1] 取目录; 板端可省略参数走默认裁决 /userdata/rmlog）;
 * 2. 四个级别的宏族各记一条, 错误码一律用生成头文件的 RMLOG_CODE_* 常量;
 * 3. 结束前 rmlog_close 落盘缓冲并退出。
 *
 * 编译（开发机自测）:
 *     gcc -std=c99 -Wall -Wextra -o example.exe example.c rmlog.c
 * 板端（X5, 交叉或本机 gcc）:
 *     gcc -std=c99 -Wall -Wextra -o example example.c rmlog.c -lpthread
 * 运行:
 *     ./example <日志目录>       # 如 ./example ./demo_log
 */
#include "rmlog.h"
#include <stdio.h>

int main(int argc, char **argv)
{
    const char *dir = (argc > 1) ? argv[1] : NULL;

    if (rmlog_open(dir) != 0) {
        fprintf(stderr, "rmlog_open failed (dir=%s)\n", dir ? dir : "(default)");
        return 1;
    }
    printf("rmlog log file: %s\n", rmlog_path() ? rmlog_path() : "(unknown)");

    /* 四级各一条: 级别宏 + 生成常量, 与 Python 端 rmlog.event(...) 一一对应 */
    RMLOG_I("ctrl", RMLOG_CODE_INIT_000, "上电自检完成, 进入待机 state=%d", 1);
    RMLOG_W("pwr",  RMLOG_CODE_HW_005,   "电池电压接近下限 v=%dmV", 22500);
    RMLOG_E("spi",  RMLOG_CODE_COMM_001, "SPI 传输超时 dev=/dev/spidev0.0 retry=%d", 3);
    RMLOG_F("fsm",  RMLOG_CODE_FSM_004,  "状态机进入未定义状态 st=%d", 7);

    rmlog_close();
    return 0;
}
