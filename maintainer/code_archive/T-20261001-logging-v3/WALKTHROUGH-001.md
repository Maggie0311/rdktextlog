# WALKTHROUGH-001 — T-20261001-logging-v3（来源 commit `d77d36c`）

> 教学向走读：先讲"每块在做什么"，再讲"关键函数"，最后串"数据流"。行号均为来源 commit `d77d36c` 行号。建议按 P0 → P1 → P2 的顺序读。

## 0. 读前地图

v3 是在 v1/v2 之上的"加层"，不是重写。业务侧最关心的三个新入口：

1. **黑匣子**（`blackbox.py`）：运行时滚动存最近几秒高频样本，出错才落盘——"飞行记录仪"。
2. **崩溃遗言**（`crash.py`）：进程被信号打死前，写最后一行 + 尽量保留 core dump。
3. **自动运行时**（`auto.py` 的 `LogRuntime`）：把日志、黑匣子、会话属性合成一个入口，业务不再逐处拼上下文。

## 1. `blackbox.py` — 黑匣子环形缓冲（P0）

- **职责**：只在内存里保存最近 `capacity` 条结构化样本，正常不碰磁盘；ERROR/FATAL 时才把当前窗口原子写成一个 JSONL 快照。
- **关键函数**：
  - `record(kind, **values)`（`:83`）：`mono_ms` + `kind` + 业务字段，`deque.append`。高频、无盘 IO。
  - `snapshot(reason, code)`（`:94`）：锁内取窗口副本 → `mkstemp` 临时文件写 header+rows → `fsync` → `os.replace` 原子落名 → `_prune_snapshots()`。
  - `_prune_snapshots()`（`:31`）：`max_snapshots==0` 不淘汰；否则按文件名排序 `unlink` 最旧 `names[:-max_snapshots]`。
  - `_safe_value`（`:55`）：把任意对象（dict/list/set/bytes/自定义对象）降级成 JSON 可序列化值，保证取证路径不抛异常。
- **数据流**：`record` → 内存 `samples` deque → `snapshot` → `blackbox-<wallsec>-<mono_ns>-<pid>-<seq>.jsonl`。

## 2. `crash.py` — 崩溃遗言（P0）

- **职责**：给 SIGABRT/SIGBUS/SIGFPE/SIGSEGV 装 handler，崩溃前写一行 `CRASH|signal=N|pid=M`。
- **关键点**：`EmergencyWriter.__init__`（`:10`）在**安装期**预打开 fd；`messages` 在**安装期**预格式化（`:36`）；handler（`:40`）只 `os.write` + `signal.signal(SIG_DFL)` + `os.kill` 重抛。所有"重活"都不在信号上下文里做。
- **为何重抛而不是 `os._exit`**：恢复默认动作再重抛同信号，才能让内核走"默认动作 = core dump"路径（是否真落 core 仍看板端 ulimit/core_pattern）。

## 3. `monitors.py` — 三条自动捕获线（P1）

- **`CommStats`**（`:10`）：通信层显式调 `success()`/`failure()`。`_outcomes=deque(maxlen=rate_window)` 存 0/1 序列算错误率；三路判定（`:38-41`）——`interrupted`（连续 `window` 次失败→`E-COMM-004`）、`rate_warning`（窗口满且错误率≥阈值→`E-COMM-003`）、`burst_warning`（连续 `fail_threshold` 次→`E-COMM-003`）。区分"链路真断"与"噪声"。
- **`HeartbeatWatchdog`**（`:53`）：独立线程每 `interval` 读 `runtime.health_attrs()` 的心跳 age，超过 `timeout` 发 `E-FSM-003`（应用层看门狗）；systemd 层由服务文件 `WatchdogSec` 兜底重启。
- **`DmesgMonitor`**（`:83`）：真实 `dmesg --follow --time-format iso` 子进程，`PATTERN` 命中的行映射 `E-COMM-002`/`E-HW-003`。`run()`（`:109`）处理"启动中已被 stop"的竞态；`_terminate_process`（`:94`）terminate→wait→kill→wait，重复调用安全。`source` 可注入（测试不依赖 dmesg）。

## 4. `resources.py` — 资源越限监控（P1）

- **职责**：周期读温度/电压/内存，越限映射到既有 24 码。
- **`_linux_values`**（`:29`）：读 `thermal_zone0/temp`（m°C）、`BAT0/voltage_now`（µV→mV）、`/proc/meminfo MemAvailable`（kB）。读不到就跳过（不报错）。
- **`check_once`**（`:48`）：采样后 `temp_mdeg>85000→E-HW-002`、`voltage_mv<14000→E-HW-001`、`memory_available_kb<32768→E-SYS-001`。

## 5. `auto.py` — 低打点运行时 `LogRuntime`（P0/P1）

- **职责**：业务侧的单一入口，把 `heartbeat`/`sample`/`emit` 组合起来。
- **`emit`**（`:41`）：写事件后，若 effective level 是 ERROR/FATAL → `blackbox.snapshot("error", code)` → 成功则补 `E-SYS-005`（带 `path`），失败则 `blackbox_failures += 1`。这样"出错自动留现场"对业务透明。
- **`health_attrs`**（`:69`）：返回各心跳的 age_ms，供看门狗读。

## 6. `code_map.py` + `gen_code.py` + `shared/rmlog_schema.h` — 双轨码与公共头（P2）

- **`code_map`**（`:10`）：`DOMAIN_IDS`（INIT=0x21…SYS=0x25）、`LEVEL_IDS`（INFO=1…FATAL=4）；`encode`（`:14`）= `(domain<<16)|(level<<12)|number`；`decode`（`:26`）反查；`hex_code` 给 `0x%06X`。字符串码仍是日志主显示，bit 码用于跨端紧凑传输。
- **`gen_code`**（`:65` `render_header`、`:140` `write_schema`）：单一来源 catalog.py → 生成 `rmlog_errors.h`（C 端）与 `shared/rmlog_schema.h`（Linux/STM32 共用），每码带 `RMLOG_CODE_*`/`RMLOG_LVL_*`/`RMLOG_BIT_*` 三宏。
- **`shared/rmlog_schema.h`**：生成物（24 码 + 级别 + bit 宏 + 码表 + 五域），与 `rmlog_errors.h` 同源，仅 banner/guard 不同。

## 7. `daemon.py` + `systemd/rmlog-demo.service` — 常驻与看门狗（P1）

- **`sd_notify`**（`:19`）：读 `NOTIFY_SOCKET`，abstract socket `@`→`\0`，`send` 后返回 True；无 socket 静默 False。
- **`main`**（`:37`）：装 SIGTERM/SIGINT → `AsyncWriter` + `LogRuntime` + `install_signal_hooks` + `HeartbeatWatchdog(timeout=1.5, interval=0.1)` → 启动 marker → `READY=1` → 主循环 `while not stop.wait(0.5): heartbeat + WATCHDOG=1` → finally `watchdog.stop() + STOPPING=1 + E-SYS-005 + writer.close()`。
- **服务模板**：`WatchdogSec=2`（`:7`），心跳 0.5s < 2s，留有余量；`Restart=on-failure`。

## 8. `rmlog_read.py` — 统计 CLI（P2）

- **`cmd_stats`**（`:239`）：按错误码/级别统计频次，`总事件` + `级别` + `code\tcount` + 残行计数，用于场下快速定位。

## 9. 一条数据贯穿（端到端）

业务 `LogRuntime.heartbeat("main")` → 黑匣子内存样本；`emit("E-COMM-004", ...)` → 落 LOGV1 行 + 黑匣子快照 `E-SYS-005`；若期间崩溃 → `crash.py` 写遗言；daemon 主循环喂狗 + `sd_notify`；场下 `rmlog_read.py stats` 统计频次 → `filter` 定位 → 倒黑匣子快照回放错误前窗口。
