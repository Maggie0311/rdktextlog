# T-20261001-logging-v3：相对 v2 的变更说明

## 1. 范围与兼容性

本提交从 `feature/logging-v2` 加层实现路线图 P0–P3 的第一份可测实现，保留
v2 的 `Writer`、`AsyncWriter`、`Session`、行格式和 24 个字符串错误码。旧业务
仍可继续调用 `rmlog.event(...)`、`Writer.event(...)`、C 端 `RMLOG_*` 宏。
本提交未进行 RDK X5 板端测试；以下证据仅代表开发机 Python/host gcc。

## 2. 相对 v2 的新增能力

| 路线图 | 交付 |
|---|---|
| P0 | `blackbox.py` 环形高频样本（底盘/IMU/状态机/心跳/通信/电压/温度/日志统计）；ERROR/FATAL 自动快照；`crash.py` 信号遗言钩子 |
| P1 | `CommStats` 通信失败率阈值、`HeartbeatWatchdog`、可注入 `DmesgMonitor`、`ResourceMonitor` |
| P2 | `code_map.py` 字符串+24-bit bit 双轨；`gen_code.py` 自动生成 Linux/STM32 公共 `shared/rmlog_schema.h`；启动 marker 增补 git/session/power 字段；读端 `stats` |
| P3 基础 | 模块均为标准库、可注入数据源、黑匣子窗口容量可配置，具备长跑测试的接口边界 |

外部复核后的增量修复：黑匣子支持 `max_snapshots` 保留上限；daemon 启动看门狗、
主循环 heartbeat 与可选 `sd_notify`；dmesg stop 会终止并等待子进程；崩溃遗言
写完恢复 `SIG_DFL` 后重抛；公共 schema banner 与文件名一致；通信统计增加固定
滑动窗口错误率，连续中断仍独立使用 `E-COMM-004`。

### bit 编码冻结

```
24 bit: [domain 8 bit][level 4 bit][number 12 bit]
domain: INIT=0x21, COMM=0x22, HW=0x23, FSM=0x24, SYS=0x25
level : INFO=1, WARN=2, ERROR=3, FATAL=4
```

例如 `E-COMM-004` 为 `0x223004`。字符串码仍是日志主显示值，bit 码用于 STM32
帧或紧凑传输；未知/临时代码不会破坏旧文本日志。

## 3. 构建与自测

在仓库根目录执行：

```bash
PYTHONPATH=developer/script python3 developer/script/tests/test_v3_smoke.py
PYTHONPATH=developer/script python3 -m rmlog.selftest
gcc -std=c99 -Wall -Wextra -I developer/script/rmlog \
  -o /tmp/rmlog-example developer/script/rmlog/example.c \
  developer/script/rmlog/rmlog.c -lpthread
```

v3 smoke 将验证双轨码、黑匣子快照、通信/资源/dmesg 捕获、统计 CLI 和公共头
生成；旧 selftest 应保持 13/13。板端安装后再按 `USAGE.md` 的 systemd 流程验证。

## 4. 已知边界与未实现项

1. Python 信号钩子能留下遗言和黑匣子，但不能替代 Linux 内核 core dump；板端需另行配置 core 文件落点。
2. dmesg、sysfs、systemd watchdog 的真实字段和权限尚未在 X5 上验证；监视器提供注入接口以便先做单元测试。
3. 黑匣子数据字段是开放的，当前默认建议字段由业务调用 `sample()` 提供；本提交不臆造底盘/IMU 数据源。
4. `CommStats` 统计器需要通信层显式调用 success/failure；它不拦截 SPI/CAN 驱动。
5. P3 的长期压力、SPI 从机日志回传和 CI 矩阵不在本次主机实现中。
6. systemd WatchdogSec、sd_notify、dmesg 权限和 core dump 行为尚未在 RDK X5 板端验证；
   它们依赖目标板的 systemd、`ulimit` 与 `kernel.core_pattern` 配置。
