# REVIEW-T-20261001-logging-v3-d77d36c

| 字段 | 值 |
|---|---|
| 审查 ID | REVIEW-T-20261001-logging-v3-d77d36c |
| 关联 task_id | T-20261001-logging-v3（复审任务号 T-20261002-013-logging-v3-rereview） |
| 审查请求来源 | management（TASK 邮件 MAIL-20261002-1045-management--code_reviewer-TASK-T-20261002-013-logging-v3-rereview） |
| 被审 commit | `d77d36c8535cdcb55249e400b56205254e50d299`（短 hash: `d77d36c`） |
| 审查时间 | 2026-10-02 15:27 |
| 审查人 | code_reviewer (R-004) |
| 结论 | **PASS** |

## 1. 被审对象

- 复审基准：来源 commit `d77d36c`（feature/logging-v3 tip），在 `8ce5162` 之上追加 2 提交：
  - `20bd40f` fix(logging-v3): harden daemon capture and communication metrics
  - `d77d36c` fix(logging-v3): close dmesg race and document snapshot retention
- 复审范围（增量，`git diff --stat 8ce5162..d77d36c -- developer/script` 恰 9 文件、149+/16-，与处置说明一致、无超范围改动）：

| 文件 | 变更点 | 对应发现项 |
|---|---|---|
| `developer/script/rmlog/blackbox.py` | 新增 `max_snapshots` 保留上限 + `_prune_snapshots` | F-01 |
| `developer/script/rmlog/daemon.py` | 新增 `sd_notify` + 心跳 + `HeartbeatWatchdog` 接线 | F-02 |
| `developer/script/systemd/rmlog-demo.service` | 增 `WatchdogSec=2` | F-02 |
| `developer/script/rmlog/monitors.py` | `DmesgMonitor` 终止子进程+启动竞态；`CommStats` 滑动窗口错误率 | F-03、F-06 |
| `developer/script/rmlog/crash.py` | 遗言后恢复 `SIG_DFL` + re-raise 保留 core dump | F-04 |
| `developer/script/rmlog/gen_code.py` | schema banner 文件名替换两处 | F-05 |
| `developer/script/shared/rmlog_schema.h` | 头注释 `rmlog_errors.h`→`rmlog_schema.h` | F-05 |
| `developer/script/IMPL-T-20261001-logging-v3.md` | 增量修复说明 + 板端未验证项诚实标注 | F-01~F-06 |
| `developer/script/tests/test_v3_smoke.py` | 增 max_snapshots / CommStats / Dmesg 竞态用例 | 回归 |

## 2. 覆盖声明

| 文件 / 模块 | 覆盖方式 | 说明 |
|---|---|---|
| `rmlog/blackbox.py`（F-01） | 全查 + 实测 | 逐行读 `__init__`/`_prune_snapshots`/`snapshot`；smoke 用例实测 limited(2)/unlimited(0) |
| `rmlog/daemon.py` + `systemd/rmlog-demo.service`（F-02） | 全查 + 静态推演 | 逐行读 `sd_notify`/心跳循环/`HeartbeatWatchdog`；接线推演 WatchdogSec=2 > 心跳 0.5s |
| `rmlog/monitors.py`（F-03/F-06） | 全查 + 实测 | 逐行读 `DmesgMonitor.run/stop/_terminate_process`、`CommStats.failure`；smoke 用真实阻塞子进程覆盖竞态 |
| `rmlog/crash.py`（F-04） | 全查 + signal-safe 推演 | 逐行读 handler；`os.write`/`signal.signal`(sigaction)/`os.kill`(kill)/`os.getpid` 均为 async-signal-safe |
| `rmlog/gen_code.py` + `shared/rmlog_schema.h`（F-05） | 全查 + 生成一致性实测 | 读渲染替换逻辑；gen_consistency 探针逐字节一致、banner 无 `rmlog_errors.h` 残留 |
| 回归兼容面（`writer.py`/`async_writer.py`/`__init__.py`/`catalog.py`/`code_map.py`） | 全查（只读核对未改动） | `git diff --stat` 证明均不在增量内，接口/24 码冻结未动 |
| 板端 dmesg/sysfs/systemd watchdog/core_pattern | **不查（原因：无板端，环境事实待板端）** | 见 §5 未确定项 |

- **未覆盖部分及原因**：板端实装事实（dmesg/sysfs 真实字段、systemd watchdog 实重启、`ulimit`/`kernel.core_pattern` 的 core dump 配置）本角色无板端，属 software_tester/板端复测范畴，如实标注 `unverified`，不冒充已验证。
- 本次执行的实际验证动作及证据（**均为独立实跑，留档于验证区 `code_reviewer/script/verify-T-20261002-013-d77d36c/`**）：
  1. `python -m rmlog.selftest` → **13/13 PASS exit 0**（`selftest-v3-d77d36c.log`）。
  2. C 侧 `gcc -std=c99 -Wall -Wextra` 编译 `rmlog.c` → **零告警**（`gcc-rmlog-d77d36c.log`，空输出）。
  3. C 侧 `gcc` 编译 `shared/rmlog_schema.h` → **零告警**（`gcc-schema-d77d36c.log`，空输出）。
  4. 生成一致性探针 → `schema_identical=True`、`header_identical=True`、`schema_has_rmlog_errors_h_ref=False`（`gen_consistency-d77d36c.log`）。
  5. schema 探针 → `len=24 domains=5 bit_comm004=0x223004 code=E-COMM-004`（`schema_probe-run.log`）。
  6. `python tests/test_v2_smoke.py` → **V2 SMOKE PASS**（`accepted=1 dropped=9`）；`python tests/test_v3_smoke.py` → **V3 SMOKE PASS**（`smoke-d77d36c.log`）。

> **验证分两段完成说明（如实）**：selftest / gcc×2 / gen_consistency / schema_probe 五项在上一会话轮已实跑并留档（本会话只核对其日志结果，未重跑）；`test_v2_smoke` / `test_v3_smoke` 两项本会话补跑（上一会话轮无此留档），因 DSH 沙箱阻断 `tempfile.mkdtemp` 目录内写（已知环境问题，探针已复证 `os.mkdir(name,0o700)` 目录被判不可读、0o777 正常），用验证区 shim `run_smoke_shim.py`（仅把 mkdtemp 目录 mode 放宽为 0o777 并把临时区重定向到验证区，不改测试语义与断言）重跑通过，此环境问题**非代码缺陷**。以 r13 留档日志为准。

## 3. 应用标准清单

- 通用清单：CHECKLIST-COMMON v1.0（GEN-08 并发 / GEN-13 吞异常 / GEN-15 资源释放 / GEN-17 资源上限 / GEN-19 接口破坏 / GEN-26 过期注释 / GEN-31~34 可复现与诚实标注）
- 语言清单：CHECKLIST-PYTHON v1.0（PY-09 过宽异常 / PY-12 资源释放 / PY-14 线程安全 / PY-17 线程 join / PY-28 subprocess 注入 / PY-33 断言有效）；CHECKLIST-C v1.0（C-22 信号安全函数 / C-24 句柄关闭）——C 侧仅复核生成头零告警，未改 C 逻辑
- **用户自定义标准**：无（`standard/user/` 下无 `USER-*.md`，仅 `USER-TEMPLATE.md` 模板）
- 项目契约：`developer/script/CODE-STYLE.md` §2.5（错误码跨端接口单一来源）、§4.4（时间戳双轨）、§5（自测工作区约定）；`IMPL-T-20261001-logging-v3.md` 增量修复说明

## 4. 发现项（上轮 F-01~F-06 逐条核销）

> 复审只审增量：逐条回应上轮 F-01~F-06（已修复/未修复/申诉），并报告是否有新发现项。

### F-01 [MINOR] 黑匣子快照保留上限 + `max_snapshots=0` 语义文档化 —— **已核销**
- **位置**：`developer/script/rmlog/blackbox.py:19-44`、`:115`；`developer/script/IMPL-T-20261001-logging-v3.md:19-20`
- **现象（首轮）**：黑匣子快照文件错误风暴下磁盘无限累积，无保留上限。
- **核销验证**：`BlackBox.__init__` 增 `max_snapshots=16`，`max_snapshots < 0` 抛 `ValueError`，docstring 明写 `max_snapshots=0` 表示不淘汰（无限保留）；`_prune_snapshots()`（`:31-44`）在 `max_snapshots==0` 时直接返回，否则按文件名排序后 `os.unlink` 最旧 `names[:-max_snapshots]` 个，失败仅吞 `OSError` 留下磁盘事实；`snapshot()` 在 `os.replace(temp, final)` 后调用 `_prune_snapshots()`（`:115`）。smoke 实测 `max_snapshots=2` 写 3 次剩 2、`max_snapshots=0` 写 3 次剩 3。IMPL 如实写"设为 0 表示不淘汰、无限保留，使用者需自行规划磁盘"。
- **依据条款**：GEN-17（资源上限）、GEN-13（吞异常但保留可观察事实，属合理降级）
- **级别**：MINOR（上轮）→ 核销
- **观察（不计级，不要求返工）**：淘汰顺序按文件名字典序近似"最旧"（文件名 = `wallsec-monotonic_ns-pid-seq`），墙钟回拨（NTP）的极端情形可能错序；但保留上限的 AC 目标是"封顶磁盘"而非精确时序，此近似不影响封顶正确性。记录为透明度备注。

### F-02 [MINOR] daemon 心跳 + systemd WatchdogSec + sd_notify 接线 —— **已核销（板端实装仍待验证）**
- **位置**：`developer/script/rmlog/daemon.py:19-34`（sd_notify）、`:48-49`（watchdog 启动）、`:59-64`（心跳循环与停止）；`developer/script/systemd/rmlog-demo.service:7`；`developer/script/rmlog/monitors.py:53-80`（HeartbeatWatchdog）
- **现象（首轮）**：心跳看门狗与 systemd WatchdogSec 未接线，daemon 无周期 `sd_notify WATCHDOG=1`、service 模板无 `WatchdogSec`。
- **核销验证**：`sd_notify()` 处理 `NOTIFY_SOCKET`（含 abstract socket `@`→`\0`），无 socket 时静默返回 False；`HeartbeatWatchdog(runtime, timeout=1.5, interval=0.1)` 在进入主循环前 `start()`，主循环 `while not stop.wait(0.5): runtime.heartbeat("main"); sd_notify("WATCHDOG=1")`，启动后 `sd_notify("READY=1")`，finally 里 `watchdog.stop(); sd_notify("STOPPING=1")`。service 模板增 `WatchdogSec=2`。接线推演成立：心跳周期 0.5s < WatchdogSec 2s，`WATCHDOG=1` 有充足余量；`HeartbeatWatchdog` 读 `heartbeat_main` age > 1500ms 时发 `E-FSM-003`（应用层看门狗）与 systemd 重启（systemd 看门狗）双层兜底。IMPL §6 如实标注板端未验证。
- **依据条款**：GEN-15（线程释放：`watchdog.stop()` join）、GEN-08（`_heartbeat` 有锁保护）
- **级别**：MINOR（上轮）→ 核销（代码接线完成；板端实装 = unverified，见 §5）

### F-03 [MINOR] dmesg 监听停止子进程泄漏 + 启动竞态 —— **已核销**
- **位置**：`developer/script/rmlog/monitors.py:88-144`（`DmesgMonitor.__init__/_terminate_process/run/stop`）
- **现象（首轮）**：`DmesgMonitor.stop()` 只设事件，阻塞的 `dmesg --follow` 子进程不被 terminate/kill，线程泄漏；stop 与启动存在竞态窗口。
- **核销验证**：增 `_proc` + `_proc_lock`；`_terminate_process()`（`:94-107`）terminate→wait(1s)→超时则 kill→wait，重复调用安全（吞 `TimeoutExpired/OSError/ValueError`）。`run()`（`:109-137`）`proc=None` 初始化，锁内写 `_proc` 并读 `stop_during_start`，若启动期间已被 stop 则立即终止返回；`finally` 终止进程并锁内清空 `_proc`。`stop()`（`:139-144`）设事件 + 锁内取 `_proc` 并终止。竞态闭合：无论 stop 发生在启动前/启动中/启动后，子进程都被终止等待，无泄漏。smoke 用真实阻塞子进程（`time.sleep(30)`）覆盖启动竞态，断言 `not thread.is_alive()`。
- **依据条款**：GEN-15（子进程资源释放）、GEN-08（启动竞态）、PY-17（线程 join）
- **级别**：MINOR（上轮）→ 核销

### F-04 [MINOR] crash 遗言后恢复默认信号 + re-raise 保留 core dump（signal-safe）—— **已核销**
- **位置**：`developer/script/rmlog/crash.py:40-48`
- **现象（首轮）**：crash 钩子写遗言后 `os._exit(128+sig)`，直接退出不产生 core dump，违背 REQ P0#2"留 coredump"。
- **核销验证**：handler 改为 `finally` 中 `signal.signal(signum, signal.SIG_DFL)` 后 `os.kill(os.getpid(), signum)`。signal-safe 推演：遗言写入只用 `os.write`（预打开 fd、消息字节在安装期预格式化）；恢复与重抛用 `signal.signal`（=sigaction，POSIX async-signal-safe）、`os.kill`（=kill，安全）、`os.getpid`（安全）。对 SIGABRT/SIGBUS/SIGFPE/SIGSEGV 恢复默认动作 = core dump（是否真正落 core 仍取决于板端 `ulimit`/`kernel.core_pattern`，注释已如实说明）。Python 层无法保证 handler 完整 POSIX async-signal-safe 语义的局限，注释诚实披露（GEN-33）。
- **依据条款**：C-22（信号安全函数，参照适用 Python `os.*` 系统调用映射）
- **级别**：MINOR（上轮）→ 核销

### F-05 [NIT] 共享头注释更正 —— **已核销**
- **位置**：`developer/script/shared/rmlog_schema.h:2`；`developer/script/rmlog/gen_code.py:147-148`
- **现象（首轮）**：schema 头 banner 误写 `rmlog_errors.h`，文件名与注释不一致。
- **核销验证**：banner 改为 `rmlog_schema.h`；`gen_code.write_schema` 渲染时同时替换 `rmlog_errors.h`→`rmlog_schema.h` 与 `RMLOG_ERRORS_H`→`RMLOG_SCHEMA_H`（宏名同步）。gen_consistency 探针实测 `schema_identical=True`、`header_identical=True`、`schema_has_rmlog_errors_h_ref=False`，生成物与生成器渲染逐字节一致，无残留。
- **依据条款**：GEN-26（注释与代码一致）
- **级别**：NIT（上轮）→ 核销

### F-06 [NIT] 通信错误率滑动窗口统计（替代"连续失败"）—— **已核销**
- **位置**：`developer/script/rmlog/monitors.py:10-50`（`CommStats`）；`developer/script/IMPL-T-20261001-logging-v3.md:22-23`
- **现象（首轮）**：CommStats 阈值用"连续失败数"，与 REQ"错误率"措辞未对齐。
- **核销验证**：`CommStats.__init__` 增 `rate_window=20`、`error_rate_threshold=0.5`，`_outcomes=deque(maxlen=rate_window)`；`success()` 追加 0、`failure()` 追加 1，`rate=sum/len`（`_outcomes` 至少 1，无除零）；三路判定：`interrupted = consecutive >= window`（唯一触发 `E-COMM-004`）、`rate_warning = len>=rate_window and rate>=threshold`（`E-COMM-003`）、`burst_warning = consecutive>=fail_threshold`（`E-COMM-003`）。注释明确区分"链路中断 vs 分散失败/短时突发噪声"；`error_rate` 以 `%.3f` 记入 attrs。IMPL 如实写"通信统计增加固定滑动窗口错误率，连续中断仍独立使用 E-COMM-004"。兼容性：`window`/`fail_threshold` 默认值与位置不变，新参数带默认值，既有调用方不受影响。smoke 实测 `distributed`（分散失败）`consecutive_failures==0` 且不误报中断。
- **依据条款**：GEN-19（不破坏既有调用方）、GEN-30（阈值参数语义清晰）
- **级别**：NIT（上轮）→ 核销

### 新发现项：无

逐行复核增量 9 文件（含 GEN-08 竞态、GEN-13 吞异常、GEN-15 资源释放、PY-09/PY-12/PY-17/PY-33），**未发现新的阻断级/严重级/一般级/提示级问题**。F-01 的"文件名排序近似淘汰"已在核销栏作为不计级观察记录，不构成返工项。

## 5. 未确定项（unverified）

| 项 | 缺什么信息 | 已尝试的获取方式 |
|---|---|---|
| 板端 dmesg/sysfs 真实字段 | 目标板 `dmesg --follow` 实际输出字段、sysfs 路径 | 本角色无板端；代码路径已静态核对，板端实测归 software_tester |
| systemd watchdog 实重启 | 目标板 systemd 版本对 `WatchdogSec`/`sd_notify` 的实际重启行为 | 同上 |
| core dump 配置 | 板端 `ulimit -c`、`/proc/sys/kernel/core_pattern` 是否真的允许落 core | 同上 |

> 上述三项为板端环境事实，`IMPL-T-20261001-logging-v3.md` §6 已诚实标注"尚未在 RDK X5 板端验证"。它们**不构成本轮代码结论**，PASS 门槛（覆盖声明/验证证据/零阻断零严重）不受影响；板端复测由 management 裁定投入。

## 6. 结论与理由

- 结论：**PASS**
- 门槛核对：
  - 覆盖声明：**完整**（增量 9 文件全查；板端环境事实显式标注 unverified，未冒充）
  - 实际验证证据：**有且充分**（selftest 13/13、gcc×2 零告警、gen_consistency 一致、schema 探针 24 码、smoke v2/v3 双 PASS，全部独立实跑留档）
  - 阻断级问题 **0** 个、严重级问题 **0** 个
- 上轮 4 一般（F-01~F-04）+ 2 提示（F-05/F-06）**全部核销**；零新发现项；回归兼容（`Writer.event`/`rmlog.event`/`AsyncWriter.emit`/24 错误码）冻结未动。
- **验收权声明**：本结论不构成验收；验收由 management 裁定（架构 §4.1）。本角色只回答"代码在标准下有没有问题"。

## 7. 声明

- 本次审查**未修改任何被审代码**（`developer/script/**` 全程只读；全部验证在 `code_reviewer/script/verify-T-20261002-013-d77d36c/` 独立副本进行）。
- 本报告对应的 commit hash 如发生变化，本报告即行失效，须再次审查（可只审增量）。
