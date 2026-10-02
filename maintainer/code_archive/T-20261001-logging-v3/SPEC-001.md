# SPEC-001 — T-20261001-logging-v3（来源 commit `d77d36c`）

> 说明：本文件 `file:line` 一律为**来源 commit `d77d36c` 行号**（归档带注版因补注行有偏移）。审查/测试对象以 d77d36c 为准，归档带注版见 `code/`。

## 1. 一句话定位

这是 rmlog 日志平台的 v3：在 v1（地基：行格式/错误码/多进程落盘）与 v2（异步/会话/自启/导出）之上，补齐"赛场自动记录 + 场下秒定位"上半层——黑匣子环形缓冲、崩溃遗言、dmesg/资源/通信监控、心跳看门狗、字符串+24bit 双轨错误码、Linux/STM32 公共头文件、日志统计 CLI。旧业务仍可继续调用 `rmlog.event(...)` / `Writer.event(...)` / `AsyncWriter.emit(...)`。

## 2. 结构总览（54 个 tracked 文件）

| 区域 | 职责 |
|---|---|
| `rmlog/blackbox.py` | P0 黑匣子环形缓冲 + ERROR/FATAL 自动 JSONL 快照 |
| `rmlog/crash.py` | P0 信号崩溃遗言钩子（写完遗言恢复 SIG_DFL 重抛保留 core） |
| `rmlog/monitors.py` | P1 通信统计 CommStats / 心跳看门狗 HeartbeatWatchdog / dmesg 监听 DmesgMonitor |
| `rmlog/resources.py` | P1 温度/电压/内存越限监控 ResourceMonitor |
| `rmlog/auto.py` | P0/P1 低打点运行时入口 LogRuntime |
| `rmlog/code_map.py` | P2 字符串码 ↔ 24bit bit 码双轨映射 |
| `rmlog/gen_code.py` | 单一来源生成器（catalog → `rmlog_errors.h` + `shared/rmlog_schema.h` + `ERR-CATALOG.md`） |
| `shared/rmlog_schema.h` | P2 生成物：Linux/STM32 共用错误码头文件（24 码） |
| `rmlog/daemon.py` + `systemd/rmlog-demo.service` | systemd 常驻入口（sd_notify + 心跳 + WatchdogSec 接线） |
| `rmlog_read.py` | 读端 CLI（parse/tail/filter/**stats**） |
| `tests/test_v3_smoke.py` | v3 开发机烟测；`tests/test_v2_smoke.py`、`rmlog/selftest.py` | 回归 |
| `rmlog/*.c`、`rmlog/*.h` | C 端协议与探针配套（本轮未改 C 逻辑） |

## 3. 各模块功能（事实）

- `BlackBox`（`rmlog/blackbox.py:16`）：`record` 追加内存样本，`snapshot` 原子写 JSONL 快照；`max_snapshots=0` 不淘汰无限保留，否则按文件名淘汰（`:31-44`）。
- `EmergencyWriter` + `install_signal_hooks`（`rmlog/crash.py:7`、`:30`）：handler 用 `os.write` 写遗言，`signal.signal(SIG_DFL)` + `os.kill` 重抛（`:40-48`）。
- `CommStats`（`rmlog/monitors.py:10`）：滑动窗口错误率；连续 `window` 次失败→`E-COMM-004`，分散失败/突发→`E-COMM-003`。
- `HeartbeatWatchdog`（`rmlog/monitors.py:53`）：喂狗超时→`E-FSM-003`。
- `DmesgMonitor`（`rmlog/monitors.py:83`）：真实 `dmesg --follow` 子进程，可疑行转 `E-COMM-002`（spi/can/i2c）/`E-HW-003`（其它）；stop 终止并等待子进程（`:94-137`）。
- `ResourceMonitor`（`rmlog/resources.py:10`）：读 sysfs/procfs，越限映射 `E-HW-002`/`E-HW-001`/`E-SYS-001`。
- `LogRuntime`（`rmlog/auto.py:16`）：`heartbeat`/`sample`/`emit` 统一入口；`emit` 的 ERROR/FATAL 后自动倒黑匣子快照（`:41-67`）。
- `code_map`（`rmlog/code_map.py:14`）：`encode`/`decode`/`hex_code`，24bit 布局 `domain(8)|level(4)|number(12)`（如 `E-COMM-004`=`0x223004`）。
- `gen_code.write_schema`（`rmlog/gen_code.py:140`）：生成 `shared/rmlog_schema.h`，banner 替换 `rmlog_errors.h`→`rmlog_schema.h`、`RMLOG_ERRORS_H`→`RMLOG_SCHEMA_H`（F-05）。
- `daemon.main`（`rmlog/daemon.py:37`）：`sd_notify`（`:19`）READY/WATCHDOG/STOPPING，主循环每 0.5s 喂狗（`:59-61`），`HeartbeatWatchdog(timeout=1.5, interval=0.1)`（`:48`）。

## 4. 关键流程

1. 业务经 `LogRuntime.sample/heartbeat` 持续喂黑匣子内存窗口；`emit` 写事件。
2. `emit` 遇到 ERROR/FATAL → `BlackBox.snapshot("error", code)` 原子落 JSONL 快照 + 补一条 `E-SYS-005`（`auto.py:56-64`）。
3. 崩溃：信号 handler 写 `CRASH|signal=N|pid=M` 遗言 → 恢复 SIG_DFL → 重抛（保留 core，取决于板端 ulimit/core_pattern）。
4. 常驻：daemon 启动 marker（`E-INIT-000` + git/power/session）→ `sd_notify(READY=1)` → 主循环 0.5s 喂狗 + `sd_notify(WATCHDOG=1)` → SIGTERM 后 `STOPPING=1` + `E-SYS-005` + `writer.close()`。
5. 场下：`rmlog_read.py filter/stats` 过滤或按码/级别统计频次。

## 5. 数据流与关键状态

黑匣子 `deque(maxlen=capacity)` 只存最近 N 条样本，不落盘；快照 `os.replace(temp, final)` 原子落名。`CommStats._outcomes=deque(maxlen=rate_window)` 存最近 success/failure 序列；`consecutive_failures` 独立计数。`ResourceMonitor`/`DmesgMonitor`/`HeartbeatWatchdog` 各自线程 + `threading.Event` 停止。`code_map` 把 24 码映射为 24bit 整数，高位保留为零。

## 6. 依赖与外部接口

仅 Python 标准库（`json`/`os`/`signal`/`socket`/`subprocess`/`threading`/`deque`/`tempfile`）。Linux 路径依赖 sysfs/procfs（`/sys/class/thermal/thermal_zone0/temp`、`/sys/class/power_supply/BAT0/voltage_now`、`/proc/meminfo`）、`dmesg --follow`、可选 `NOTIFY_SOCKET`。systemd 模板依赖 `/usr/bin/python3`、`/opt/rdk_x5_software/developer/script` 入口、`WatchdogSec=2`。C 端 `shared/rmlog_schema.h` 供 STM32/RT-Thread 下位机共用（生成物）。

## 7. 构建与运行方式（引用 developer 说明并核实）

在 `developer/script`（来源副本同于本版 `code/`）：

```bash
PYTHONPATH=. python3 -m rmlog.selftest        # 13/13 PASS（板端实测，TESTREPORT-T-20261002-014-001 §5.3）
PYTHONPATH=. python3 tests/test_v2_smoke.py   # V2 SMOKE PASS accepted=1 dropped=9
PYTHONPATH=. python3 tests/test_v3_smoke.py   # V3 SMOKE PASS bit-map blackbox monitors stats schema
python3 -m rmlog.gen_code                     # 生成 rmlog_errors.h + shared/rmlog_schema.h（24 码）
python3 rmlog_read.py stats <log>             # 统计 CLI（按错误码/级别频次）
gcc -std=c99 -Wall -Wextra -I rmlog -o /tmp/rmlog-example rmlog/example.c rmlog/rmlog.c -lpthread
```

daemon：`python3 -m rmlog.daemon <dir>`，SIGTERM 优雅收尾（板端 BQ5 实测退出码 0）。上述命令与结果由 HANDOFF、review 报告与 tester 板端报告共同记录。

## 8. 术语表

见 `maintainer/script/GLOSSARY.md`；本版增补：黑匣子（BlackBox）、环形缓冲、崩溃遗言、sd_notify、WatchdogSec、错误率滑动窗口、24bit 双轨码、资源监控、生成头（schema）等（见 GLOSSARY「版本收录记录」004 行）。

## 9. 已知关注点（只转述，不作质量裁定）

- review `REVIEW-T-20261001-logging-v3-d77d36c.md` **PASS**：上轮 F-01~F-06（黑匣子保留上限 / 心跳+WatchdogSec 接线 / dmesg 泄漏+竞态 / 遗言保留 core / schema banner / 错误率窗口）**全部核销**，零新发现项；回归兼容（`Writer.event`/`rmlog.event`/`AsyncWriter.emit`/24 码）冻结未动。
- 不计级观察（review 转述）：黑匣子淘汰按文件名字典序近似"最旧"，极端墙钟回拨（NTP）可能错序，但不影响"封顶磁盘"目标。
- tester `TESTREPORT-T-20261002-014-001` 未覆盖：systemd 实装 + WatchdogSec 实际重启、sd_notify 实际投递、压力/长时/断电持久化、真实硬件故障接入（真实 SPI/CAN/电压）、1 kHz 硬实时、板端 core dump 实际放开（`ulimit -c=0`、`core_pattern=core`）。

## 10. 未解疑问（unverified）

1. `unverified`：板端 systemd 实装后 `WatchdogSec=2` 是否真会重启 daemon（未安装服务，安全边界外）。
2. `unverified`：`sd_notify` 的 `READY=1`/`WATCHDOG=1`/`STOPPING=1` 是否真送达 systemd（临时目录无 `NOTIFY_SOCKET`，`sd_notify()` 静默返回 False）。
3. `unverified`：断电/掉电持久化、长时/压力稳定性、1 kHz 硬实时边界。
4. `unverified`：真实 SPI/CAN/电压等硬件故障能否提供与注入 provider 同形态的事实（`CommStats` 需通信层显式调 success/failure，不拦截驱动；`ResourceMonitor` 电压默认只读 BAT0，RDK X5 无 BAT0 会按设计跳过）。
5. `unverified`：板端 core dump 当前禁用（`ulimit -c=0`），崩溃遗言代码路径已测，但实际 core 文件生成需先放开 ulimit。
6. `unverified`：daemon 启动 marker 的 `power=unknown`（daemon.py 硬编码）与临时目录下 `git=unknown`（非 git 仓库走兜底）为被测程序默认值，其真实语义待 developer 澄清。

## 11. 事实层与推断层的分离声明

- **事实**：第 3~5 节对函数/类的描述均可由来源 commit `d77d36c` 的代码定位；第 7 节命令与结果、第 9 节 review/tester 结论均来自落盘报告（review `REVIEW-…-d77d36c.md`、tester `TESTREPORT-T-20261002-014-001.md`）。
- **推断**：仅第 1 节"一句话定位"对整体用途的概括，以及补注导读中对"设计意图"的措辞（已用"补注"标记，属解释而非代码事实）。
- 本文不宣称发布、整车交付或硬实时保证；未验证项一律标 `unverified`，不编造解释（KN6/KN13）。
