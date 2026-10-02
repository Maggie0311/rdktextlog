# REVIEW-T-20261001-logging-v3-8ce5162

| 字段 | 值 |
|---|---|
| 审查 ID | REVIEW-T-20261001-logging-v3-8ce5162 |
| 关联 task_id | T-20261002-011-logging-v3-review |
| 审查请求来源 | management（TASK 邮件 MAIL-20261002-0958） |
| 被审 commit | `8ce5162eda11c802eb0e6616d7baca1f6fce95a`（短 `8ce5162`） |
| 审查时间 | 2026-10-02 10:04~10:40（基准核对 + 逐文件静态审查 + 独立实跑 + 留档） |
| 审查人 | code_reviewer (R-004) |
| 结论 | **CONDITIONAL**（阻断/严重 = 0；存在 4 一般级 + 2 提示级，逐条列出后续可处理项） |

---

## 1. 被审对象

- task_id: `T-20261002-011-logging-v3-review`
- commit hash: `8ce5162eda11c802eb0e6616d7baca1f6fce95a`（短 `8ce5162`；feature/logging-v3 tip）
- 审查基准: **来源 commit 8ce5162**（ROLE-LIMIT §2.1.1 第 6 条）。工作树当前为 master（旧状态），故以 `git archive 8ce5162 developer/script` 签出副本到本角色验证区 `code_reviewer/script/verify-T-20261002-011-8ce5162/` 审查，**未碰工作树**。
- 基准核对（git 实证）:
  - `git log --oneline feature/logging-v2..feature/logging-v3` = **恰 3 提交**（`5640987`→`ed90fca`→`8ce5162`），基于 v2 tip `fd8423c`（`git show -s %H %P` 父提交 = `ed90fca...`）✓
  - `git diff --stat feature/logging-v2...feature/logging-v3 -- developer/script` = **15 文件 +828/-7**，与任务书"15 文件 +828/-7"一致 ✓
- 变更文件清单（与任务书范围一致，无超范围）:

| 文件 | 状态 |
|---|---|
| `rmlog/blackbox.py` | 新增（+102） |
| `rmlog/crash.py` | 新增（+54） |
| `rmlog/monitors.py` | 新增（+98） |
| `rmlog/resources.py` | 新增（+79） |
| `rmlog/auto.py` | 新增（+81） |
| `rmlog/code_map.py` | 新增（+40） |
| `shared/rmlog_schema.h` | 新增（+153，生成物） |
| `tests/test_v3_smoke.py` | 新增（+79） |
| `IMPL-T-20261001-logging-v3.md` | 新增（+52） |
| `rmlog/daemon.py` | 修改（+18/-6） |
| `rmlog/gen_code.py` | 修改（+20） |
| `rmlog/rmlog_errors.h` | 修改（+25，生成物） |
| `rmlog/__init__.py` | 修改（+5/-2） |
| `rmlog_read.py` | 修改（+23，stats CLI） |
| `README.md` | 修改（+6） |

- 兼容性核对（v1/v2 接口冻结）: `writer.py`/`async_writer.py`/`session.py`/`catalog.py`/`format.py`/`rmlog.c`/`rmlog.h` **均不在 v3 diff 中**（零变更）。逐项静态核对：`Writer.event(code, module, message, level=None, attrs=None)`（writer.py:241）不变、模块级 `rmlog.event(...)`（writer.py:518）不变、`AsyncWriter.emit(code, module, message, level=None, attrs=None)`（async_writer.py:27）不变、catalog.ERRORS 仍为 **24 码**（5+5+5+4+5）。`__init__.py` 仅新增导出 `encode_code/decode_code/hex_code` 与版本号 0.1.0→0.2.0，纯增量无破坏。

---

## 2. 覆盖声明

| 文件 / 模块 | 覆盖方式 | 说明 |
|---|---|---|
| `blackbox.py` | 全查 + 实跑 | 环形缓冲并发（threading.Lock）、内存上界（deque maxlen=capacity）、快照序列化、错误路径刷出/临时文件清理逐一核对；test_v3_smoke 覆盖 snapshot 两次不同路径/opaque/deep 对象降级 |
| `crash.py` | 全查 + 实跑 | handler 只做 `os.write`（预打开 fd）+ `os._exit`，不触锁/print/分配（messages 预计算）；test_v3_smoke 覆盖 EmergencyWriter 落盘 |
| `monitors.py` | 全查 + 实跑 | CommStats/HeartbeatWatchdog/DmesgMonitor 生命周期与阈值判定；test_v3_smoke 覆盖 comm 阈值与 dmesg 注入转码 |
| `resources.py` | 全查 + 实跑 | sysfs/procfs 容错（文件不存在/权限不足→None→跳过）、越限阈值；test_v3_smoke 覆盖注入越限值与 provider 抛异常 |
| `auto.py`（LogRuntime） | 全查 + 实跑 | 编排接线（blackbox 接好、crash/monitors 未接，见 F-02/F-03）、初始化顺序、emit 错误路径 |
| `code_map.py` | 全查 + 实跑 | 24 码 encode→decode 全量往返 + 唯一性 + 与 C 头 RMLOG_BIT_* 逐码一致（见 §4-V6） |
| `gen_code.py` + `shared/rmlog_schema.h` + `rmlog_errors.h` | 全查 + 实跑 | 单源生成一致性：重新生成后与 commit 逐字节一致（§4-V7）；C 头自足性 gcc 实编（§4-V5） |
| `daemon.py` | 全查 | 启动 marker + 崩溃钩子接线；心跳看门狗接线缺失（F-02） |
| `rmlog_read.py`（stats CLI） | 全查 + 实跑 | cmd_stats 计数/级别统计；test_v3_smoke 覆盖 stats 输出 |
| `__init__.py` / `README.md` / `IMPL-*.md` | 全查 | 兼容性、诚实边界核对 |
| 兼容面（writer/async_writer/session/catalog/format/rmlog.c/h） | 静态核对（未逐行重审） | 均不在 v3 diff，仅核对公开签名/24 码未变 |

- **未覆盖部分及原因**:
  1. **板端 dmesg/sysfs 真实字段与权限** — 本角色无 X5 板端，`DmesgMonitor` 真实 `dmesg --follow` 与 `ResourceMonitor._linux_values` 的 `/sys/class/thermal/thermal_zone0/temp`、`/sys/class/power_supply/BAT0/voltage_now` 字段未实测（注入接口已测）。标 unverified。
  2. **systemd/core 策略** — `kernel.core_pattern`、`ulimit -c`、systemd `WatchdogSec` 兜底重启为板端 OS 配置，本角色未板端实测。标 unverified。
  3. **STM32 实测** — 仅静态论证 `shared/rmlog_schema.h` C99 自足 + host gcc `-std=c99 -Wall -Wextra -pedantic` 编译通过；STM32/RT-Thread 工具链实编未做。标 unverified。
  4. **电源状态探测** — daemon.py 启动 marker 的 `power` 字段硬编码 `"unknown"`（未探测 sysfs），属 P2#8"补电源状态"的占位实现。

- 本次执行的实际验证动作及证据（详见 §4）: selftest 13/13、test_v2_smoke、test_v3_smoke、gcc 编译 rmlog.c 与共享头、24 码双轨全量核对、生成物逐字节一致性。

---

## 3. 应用标准清单

- 通用清单: `CHECKLIST-COMMON.md` v1.0（GEN-01/02/03/05/06/07/08/10/11/13/15/17/18/19/21/25/26/31/33/34）
- 语言清单: `CHECKLIST-PYTHON.md` v1.0（PY-01/02/03/05/09/10/11/12/14/17/18/19/22/24/27/30/32/33）、`CHECKLIST-C.md` v1.0（C-01/08/09/10/16/22/23/27/28/29/30）
- **用户自定义标准: 无**（`code_reviewer/standard/user/` 下仅有 `README.md` 与 `USER-TEMPLATE.md`，无用户实际写入的标准）
- 项目契约: `developer/script/CODE-STYLE.md`（§1 仅标准库/§2 文件头四要素/§4 可靠性约定/§5 自测约定）、`management/script/REQ-20261001-logging-v3-roadmap.md`（P0–P2）

---

## 4. 验证动作与证据（本角色独立实跑，验证区 `code_reviewer/script/verify-T-20261002-011-8ce5162/`）

> 环境: Windows 开发机，Python 3.14.7 / gcc 13.2.0 (MinGW)。被审代码取自 `git archive 8ce5162 developer/script`（未碰工作树）。三项 Python 测试均以 `PYTHONPATH=<验证区>/developer/script` 运行。

| # | 动作 | 结果（退出码） | 在盘证据 |
|---|---|---|---|
| V1 | `python -m rmlog.selftest` | **13/13 PASS**，用时 37.6s，`EXIT=0`（含 AC3 24 码、AC4 双端逐字节、AC5 多进程×轮转、GEN 生成一致、RF6 句柄守恒） | `selftest-v3-8ce5162.log` |
| V2 | `python tests/test_v2_smoke.py` | **V2 SMOKE PASS accepted=1 dropped=9**，`EXIT=0` | `test_v2_smoke-8ce5162.log` |
| V3 | `python tests/test_v3_smoke.py` | **V3 SMOKE PASS bit-map blackbox monitors stats schema**，`EXIT=0` | `test_v3_smoke-8ce5162.log` |
| V4 | `gcc -std=c99 -Wall -Wextra -I rmlog -c rmlog/rmlog.c` | **退出码 0，零告警** | `gcc-rmlog-8ce5162.log` |
| V5 | `gcc -std=c99 -Wall -Wextra -pedantic -I . schema_probe.c`（include `shared/rmlog_schema.h`） | **退出码 0，零告警**；运行输出 `len=24 domains=5 bit_comm004=0x223004 code=E-COMM-004` | `gcc-schema-8ce5162.log`、`schema_probe.c` |
| V6 | 24 码双轨全量核对脚本（encode→decode 往返 + 唯一性 + 与 C 头 RMLOG_BIT_* 逐码比对） | `codes=24 unique_bits=24`，`E-COMM-004 -> 0x223004`，未知码 `-> None`，**BAD: none** | 本节记录（脚本内联） |
| V7 | 重新生成 `rmlog_errors.h` 与 `shared/rmlog_schema.h` 后与 commit 逐字节对比 | **IDENTICAL**（单一来源生成一致） | 本节记录 |

- **沙箱工作区说明（诚实记录）**: V2/V3 首次运行失败，根因是 `tempfile.mkdtemp()` 内部 `os.mkdir(mode=0o700)` 在 Windows 文件沙箱下生成 owner-only ACL，随后 `os.listdir` 报 `EACCES`（WinError 5）——**属 DSH 沙箱环境交互，非被审代码缺陷**（selftest 走 `os.makedirs` 默认 0o777 不受影响，故 V1 直接通过）。本角色以验证区内 `shim/sitecustomize.py`（仅将 `os.mkdir` 的 0o700 放宽为 0o777）垫片后原样重跑 V2/V3 通过，**未修改任何被审代码/测试断言**。垫片留存 `shim/sitecustomize.py`。

---

## 5. 发现项

### F-01 [MINOR] 黑匣子快照文件数量无保留上限，错误风暴下磁盘可无限累积
- **位置**: `blackbox.py:84-96`（`snapshot()` 每次 ERROR/FATAL 生成一个 `blackbox-*.jsonl`，无轮转/清理/数量上限）
- **现象**: 内存环形缓冲有界（`deque(maxlen=capacity)`），但**磁盘快照文件份数无上界**——每触发一次 ERROR/FATAL 就永久新增一个快照文件，长跑或错误风暴下可无限累积直至占满存储（进而诱发 E-SYS-002 落盘失败）。
- **复现路径/推演链**: 业务侧持续 emit ERROR（如传感器持续异常）→ `auto.py:56-57` 每次触发 `snapshot("error", code)` → 每份快照写最多 `capacity`(默认 2000) 行 → 快照文件数随时间线性增长，无任何保留/清理策略。对比 `writer.py` 有 `max_bytes×keep` 轮转治理，黑匣子快照无对应治理。
- **依据条款**: GEN-17（资源上限是否被考虑——无限累积的缓存/日志）
- **级别**: MINOR
- **建议**: 为 `blackbox-*.jsonl` 增加保留份数上限（如与日志轮转 `keep` 对齐），超限淘汰最旧快照。

### F-02 [MINOR] 心跳看门狗与 systemd WatchdogSec 未接线（REQ P1#4"systemd 兜底重启"未实现）
- **位置**: `daemon.py:36-40`（主循环 `while not stop.wait(1.0): pass` 不喂狗、不 `sd_notify`）、`systemd/rmlog-demo.service:5-13`（无 `WatchdogSec=`）
- **现象**: REQ P1#4"看门狗心跳 + systemd WatchdogSec —— 主循环喂狗，超时自动记 FSM 卡死；systemd 兜底重启"仅交付了 `HeartbeatWatchdog` 类（`monitors.py:37-64`，已单测）与 `LogRuntime.heartbeat/health_attrs`，但 daemon 主循环不调用 `runtime.heartbeat()`、不启动 HeartbeatWatchdog、不 `sd_notify`；服务文件未设 `WatchdogSec`。因此"主循环卡死→自动记 FSM-003→systemd 兜底重启"整条链路未接线（`Restart=on-failure` 只在进程退出时生效，卡死不触发）。
- **复现路径/推演链**: 主循环卡死（不退出）→ 无心跳喂狗、无 sd_notify → systemd 无 WatchdogSec 无法识别卡死 → 服务既不记 FSM-003 也不被重启。IMPL"已知边界 #2"已诚实标注"systemd watchdog 真实字段和权限尚未在 X5 上验证"，但本项是**代码层未接线**（非仅板端未验证）。
- **依据条款**: GEN-01（实现是否逐条满足 AC）、REQ P1#4
- **级别**: MINOR
- **建议**: 明确 P1#4 systemd 半条是否属本轮范围；若属，则 daemon 主循环喂狗 + 服务文件 `WatchdogSec=` + `sd_notify`（或确认交由业务循环接线）。

### F-03 [MINOR] DmesgMonitor.stop() 无法终止阻塞中的 `dmesg --follow` 子进程
- **位置**: `monitors.py:86`（`for line in source` 阻塞读管道）、`monitors.py:94-95`（`proc.terminate()` 仅在 for 循环退出后的 finally）、`monitors.py:97-98`（`stop()` 只置事件）
- **现象**: 真实 `dmesg --follow` 路径（`source=None`）下，`run()` 阻塞在管道 readline；`stop()` 只 `self._stop.set()`，但 `_stop` 检查在循环体内（拿到新行之后）。若内核无新行，`run()` 永不返回，`proc.terminate()` 永不执行 → 子进程/线程在关停时泄漏（且无 `proc.wait()`，终止后可能成僵尸）。
- **复现路径/推演链**: `source=None` → `dmesg --follow` 启动 → 某时刻无新内核行 → 调用 `stop()` → 线程仍阻塞于 readline → 关停挂起/泄漏。当前无真实接线（仅 test_v3_smoke 以有限 list 注入、正常耗尽退出），属**潜伏**问题。
- **依据条款**: GEN-15/GEN-17、PY-17（线程/进程是否在所有路径被 shutdown/join）
- **级别**: MINOR
- **建议**: `stop()` 主动 `proc.terminate()`（并 `wait()`），或 `run()` 用带超时的读/把 `proc` 生命周期纳入 `stop()` 管理。

### F-04 [MINOR] crash 钩子 `os._exit` 主动抑制默认 core dump（REQ P0#2"留 coredump"半条未达成）
- **位置**: `crash.py:40-47`（handler 内 `os._exit(128 + signum)`）
- **现象**: 捕获 SIGSEGV/SIGABRT 后写遗言，随即 `os._exit(128+signum)` 以退出码终止**而非重抛信号**，使信号 disposition 停留在"自定义 handler"，内核**不再产生默认 core dump**——`kernel.core_pattern`/`ulimit -c` 板端配置也救不回来（信号已被 handler 吞掉）。REQ P0#2"写遗言 + 留 coredump"仅达成前半。IMPL"已知边界 #1"已披露"不能替代内核 core dump"，但未点出"`_exit` 而非 re-raise 会主动吞掉默认 core"这一可修复的代码细节。
- **复现路径/推演链**: 业务 SIGSEGV → handler 写 `crash-<pid>.log` 遗言 → `os._exit(139)` → 进程以退出码 139 终止、**无 core 文件**。对照：若写完遗言后 `signal.signal(signum, SIG_DFL)` + `os.kill(os.getpid(), signum)` 重抛，则按系统配置产生 core。
- **依据条款**: REQ P0#2、GEN-01
- **级别**: MINOR
- **建议**: 遗言写完后恢复默认 disposition 并重抛信号以保留默认 core（或明确由 management 裁决"coredump 由板端另配、handler 只留遗言"并修正 IMPL 表述）。

### F-05 [NIT] shared/rmlog_schema.h 文件头注释仍写"rmlog_errors.h"
- **位置**: `shared/rmlog_schema.h:2`（注释 `* rmlog_errors.h — ...`）、`gen_code.py:147`（`write_schema` 用 `.replace("RMLOG_ERRORS_H", "RMLOG_SCHEMA_H")` 只改 include guard 未改注释）
- **现象**: schema 生成物注释文件名与实际文件名（`rmlog_schema.h`）不一致（含顶部 banner 与"任务"注释沿用 rmlog_errors 文案）。
- **复现路径/推演链**: 直接读 `shared/rmlog_schema.h` 第 2 行即见。不影响编译（V5 零告警）。
- **依据条款**: GEN-26（注释与代码/文件名一致）
- **级别**: NIT
- **建议**: `write_schema` 用独立的 banner（或同步替换文件名文案），保持生成物注释与文件名一致。

### F-06 [NIT] CommStats 触发阈值为"连续失败数"而非"错误率"
- **位置**: `monitors.py:29-31`（`if self.consecutive_failures >= self.fail_threshold`）
- **现象**: REQ P1#5 措辞"通信错误率统计"，实现以**连续失败数**触发（`failed/total` 仅写入黑匣子样本 `sample("comm",...)`，不参与阈值）。连续失败阈值用于判"链路丢失"是合理设计，但与"错误率"措辞存在偏差。
- **复现路径/推演链**: 30 次调用中 3 次失败但**分散**（不连续）→ `consecutive_failures` 被 success 清零 → 不触发 E-COMM-003/004，即便失败率 10% 已超直觉阈值。属语义措辞差异，非功能错误。
- **依据条款**: GEN-21（公开接口行为与文档/需求一致）、REQ P1#5
- **级别**: NIT
- **建议**: 统一措辞（如 REQ 改为"连续失败阈值"或实现补失败率阈值），消除需求-实现表述偏差。

---

## 6. 未确定项（unverified）

| 项 | 缺什么信息 | 已尝试的获取方式 |
|---|---|---|
| UV-1 板端 dmesg/sysfs 真实字段与权限 | X5 上 `/sys/class/thermal/thermal_zone0/temp`、`/sys/class/power_supply/BAT0/voltage_now` 是否存在/可读、`dmesg --follow` 是否需要 root | 本角色无板端；注入接口已单测（test_v3_smoke），真实字段待 software_tester 板端任务 |
| UV-2 systemd/core 策略 | `WatchdogSec`/`sd_notify` 兜底重启、`kernel.core_pattern`/`ulimit -c` core 落点 | 板端 OS 配置，本角色未实测；代码层"未接线/抑制 core"已作为 F-02/F-04 静态判定 |
| UV-3 STM32 实测 | RT-Thread/STM32 工具链实编 `shared/rmlog_schema.h`（仅 host gcc C99 -pedantic 论证自足） | 无 STM32 工具链；静态论证 + host gcc 编译通过 |

---

## 7. 结论与理由

### 结论: **CONDITIONAL**

**门槛核对**（ROLE-LIMIT §4）:
- 覆盖声明: **完整**（§2，逐文件标注查法 + 4 项未覆盖及原因）✓
- 实际验证证据: **≥1 项**（§4 V1~V7 独立实跑，全部落盘验证区）✓
- 阻断级(BLOCKER)/严重级(MAJOR)问题数: **0** ✓
- 存在一般级(MINOR) 4 项 + 提示级(NIT) 2 项 → 依"仅存在一般级/提示级问题，且逐条列出后续可处理项"判 **CONDITIONAL**。

**判定说明**:
1. 双轨映射正确性（重点⑥）：24 码 encode→decode 全量往返、24 bit 值唯一无碰撞、`E-COMM-004↔0x223004` 成立、Python `encode()` 与 C 头 `RMLOG_BIT_*` 逐码一致（V6）；生成物与生成器渲染逻辑逐字节一致（V7）；`shared/rmlog_schema.h` C99 自足、无 Python 依赖（V5，host gcc -pedantic 零告警）。
2. 黑匣子并发/内存上界（重点①）：环形缓冲有界（`deque(maxlen=capacity)`）+ `threading.Lock` 保护 + 快照临时文件异常清理正确（`UnboundLocalError` 已兜底），唯磁盘快照份数无上限（F-01）。
3. 崩溃钩子（重点②）：handler 只做 `os.write`+`os._exit`、不触锁/print/分配（messages 安装期预计算），遗言落盘已单测；但 `_exit` 抑制默认 core（F-04）。
4. 兼容性（重点⑤）：`Writer.event`/`rmlog.event`/`AsyncWriter.emit`/24 码均不变，`__init__.py` 纯增量导出。
5. 本轮**未发现阻断级/严重级问题**；F-01~F-06 为一般级/提示级，逐条列出后续可处理项（见 §5 建议），是否返工/何时处理由 management 裁量（RN10）。

- **验收权声明**：本结论不构成验收；验收由 management 裁定（架构 §4.1，RN9）。

---

## 8. 声明

1. 本次审查**未修改任何被审代码**：全部验证在 `code_reviewer/script/verify-T-20261002-011-8ce5162/` 的 `git archive` 独立副本上进行，`developer/script/**` 全程只读；test_v3_smoke 重生成的 rmlog_errors.h/schema 仅落于验证区副本内，未触碰工作树。
2. 本报告对应的 commit hash 如发生变化，本报告即行失效，须重新审查（可只审增量）。
3. 本结论**只受证据影响**；外部 ChatGPT"静态审查 PASS"未采信，本报告为我方第一份独立审查，全部发现项以本角色独立静态核对 + 实跑为准。
4. 结论字段自检：被审对象（§1）/覆盖声明（§2）/应用标准清单（§3，用户标准=无）/发现项五要素（§5 F-01~F-06）/未确定项（§6）/结论+门槛核对（§7）/声明（本节）齐全。
