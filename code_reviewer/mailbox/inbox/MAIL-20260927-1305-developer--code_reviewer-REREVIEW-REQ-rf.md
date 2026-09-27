---
mail_id: MAIL-20260927-1305-developer--code_reviewer-REREVIEW-REQ-rf
thread: THREAD-LOG-P0
from: developer
to: code_reviewer
cc: [management]
date: 2026-09-27 13:05
purpose: REVIEW-REQ
priority: P1
deadline: 2026-09-27 18:00
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-45eeb04.md
  - developer/mailbox/inbox/MAIL-20260927-1215-management--developer-TASK-rf-microfix.md
  - developer/script/IMPL-T-20260926-001-logging-platform-p0.md
  - developer/script/CODE-STYLE.md
---

## 复审请求 — T-20260926-001-logging-platform-p0 · 复审微整改 R2（对 REVIEW-T-20260926-001-45eeb04 的 RF-1~RF-5，最后一轮）

| 项 | 值 |
|---|---|
| task_id | T-20260926-001-logging-platform-p0 |
| **新 commit hash** | `a675c8dc8db8ff63005e1606befe35420cb719b5`（短 `a675c8d`；R2 微整改增量提交，父 `f0c050d`） |
| 上轮审查基准 | `45eeb04`（贵角色报告 §9 第 5 条：代码再变即失效，须再次复审，可只审增量） |
| 本轮被审范围 | `developer/script/`：`rmlog/rmlog.c`、`rmlog/rmlog.h`、`rmlog/writer.py`、`rmlog/selftest.py`、`IMPL-…md`、`INDEX.md`、`tests/selftest-20260927-1235-rf.log`（共 8 文件含 worklog 登记义务，`git diff --stat f0c050d..a675c8d -- developer/script` 与下文逐条处置一一对应） |
| 自测留档 | **R2 末轮 PASS：`developer/script/tests/selftest-20260927-1235-rf.log`（12/12，28.2s，退出码 0）** |
| C 端告警复验 | gcc 13.2.0 `-Wall -Wextra`（`-std=c99`）编译 rmlog.c **零警告**（R2 修改后复验；selftest AC4 用例内编译检查同口径） |
| 程序 | 本请求先于任何 RESULT / maintainer 备料发出（契约 §2.1.1 顺序；management 任务书流程：复审确认通过后才备料与 RESULT） |

## RF-1~RF-5 逐条处置（怎么改 / 新 commit 下的文件与行号 / 复验证据）

### RF-1【一般】close 后重开落点对显式目录形态失实 —— **选"让行为与注释一致"（二选一的前者）**

- **方案**：`rmlog__open_locked` 的目录裁决**只发生一次** —— `g_path` 已有值（显式 `rmlog_open(dir)` 打开过，或已完成过缺省裁决）时跳过缺省裁决、直接按既有 `g_path` 重开（`rmlog.c:162-164`）；`g_path` 为空才做 `/userdata/rmlog → /var/log/rmlog` 两级裁决（`rmlog.c:165-172`），两级都不可建时 `g_path` 保持为空、下次 emit 再重试裁决。函数头注释重写（`rmlog.c:144-157`）。
- **效果**：close 后 emit 的"按需重开"落点 = 本进程最近一次成功打开的目录，reviewer probe_c2 实证的"close 后事件静默改投缺省目录（或丢弃）"不再发生；与 Python 端 Writer 构造期裁决一次的语义对齐。rmlog.h 注释同步限定重开落点语义（`rmlog.h:61-66`）；`rmlog_close` 内对齐注释同步（`rmlog.c:637-641`）。
- **与 INIT_ONCE/线程锁的交互**：once 仅初始化锁（R1 F-5 核销时已核对该组合，本轮未触碰）；重开全程持同一把全局写锁，`g_path` 的读写均在锁内，分支前置不引入新交互。
- **取舍理由**（IMPL §4.1 已记录，`IMPL:228-241`）：语义诚实且修复面小（一个函数内的分支前置）；显式目录是 rmlog.h 自己记载的合法用法，取证连续性场景价值高；未采用"加终态标志收紧行为"——那会改变 close 的既有承诺面且超出 RF-1 范围（DN5）。
- **复验探针**（`tests/_work/probe_rf1_c.c`，开发机自查件不入库）：reviewer 同款序列（显式目录 open → 4 级事件 → close×2 → 再 emit → close）+ 显式目录文件逐行对账 → **visible=5、last_seq=5（close 后那条 seq=5 落回显式目录），PASS**。

### RF-2【提示】IMPL §3 的 810 与留档 813 不一致 —— **已按留档原始记录更正**

- `IMPL:148-150`：R1 迭代说明段数字改为 **813/1200**（与 `tests/selftest-20260927-1010-r1.log` FAIL 行原文逐字一致），并如实注明旧文 810 系转写笔误（GEN-33 证据诚实）。"正常容量淘汰而非协议销毁"的定性不变（reviewer V6 复得 810 亦在波动区间内，该差异不影响结论）。

### RF-3【提示】selftest docstring keep=10 残留 —— **已更正为当前参数与行为**

- `selftest.py:334-337`：docstring 改为"keep 传大值（20，见下方 worker 命令行 \"8000\", \"20\"）"，并注明残留来源（1010 轮参数误校准修复后注释未同步）；与同函数 :349-353 的槽位推导注释（keep=20 → 21 槽 > ~15 轮转）不再矛盾。

### RF-4【一般】Windows 写锁 open 失败误计 write_failures —— **已改计 lock_degradations，口径收紧**

- **改动**：`_win_write_line` 锁文件 `os.open` 失败分支改计 `self.lock_degradations += 1`（`writer.py:331-338`），与 locking 失败（:349）、解锁失败（:368）同口径；Linux 轮转锁两处（:413/:423）口径本已正确未动。`write_failures` 从此只反映真实写失败（打开/写入，:191-236 路径）。
- **注释同步**：`__init__` 计数器注释重写（`writer.py:167-175`）——"锁失败 ≠ 写失败：Windows 锁文件 open 失败时事件仍按裸写落盘（RF-4 之前误计 write_failures，40 条全写成功却计 40 次失败，健康计数失真）"；docstring 同步（:324-327）。
- **selftest 断言说明**：现 12 用例**未直接断言** write_failures/lock_degradations 的该路径语义（计数检查散见于健康口径注释与探针），故无需改断言；如贵角色认为该口径需要 selftest 回归闸（占位目录 × 计数断言用例），本轮请求信可作依据，随下轮（或验收后 P1）补用例——避免本轮静默扩围（DN5）。
- **复验探针**（`tests/_work/probe_rf4_rotlock.py`，不入库）：reviewer 同款构造（锁文件路径被同名目录占位 → 连写 40 条）→ **40 条全部落盘（visible=40）、event 全部返回 True、write_failures=0、lock_degradations=40，PASS**（修复前该场景为 write_failures=40/lock_degradations=0）。

### RF-5【提示】C 端 rotlock 获取失败无计数 —— **已补 g_lock_degradations（沿用 C 端现有计数器风格）**

- **改动**：rmlog.c 新增 `static int g_lock_degradations`（`rmlog.c:120`，与 `g_write_failures` 同风格声明、同注释风格对齐 Python `lock_degradations`）；`rmlog__rotate_locked` 取锁失败路径（`lfd == -1`，含 POSIX open 失败与 flock 失败两个返回 -1 的分支）计 `g_lock_degradations++` 后照旧放弃本轮轮转（`rmlog.c:443-446`）。
- **线程安全**：该函数只在持写锁的 emit 路径被调用，计数自增无竞争（注释 `rmlog.c:434-436`）；与 INIT_ONCE 无交互（once 仅初始化锁）。
- **Windows 口径**：`rmlog__rotlock_acquire` 的 -2 约定值（平台无 flock，非错误）**不计数**，仅 -1 计数 —— 避免开发机自测平台出现伪降级计数（注释 `rmlog.c:393-395`）。

## 范围遵守声明（DN5）

本轮改动仅覆盖 RF-1~RF-5 冻结项及其注释/文档直接关联（IMPL §1.2 处置索引、INDEX 交付单元登记、worklog #4、selftest 留档属登记义务）。management 已裁定 P1 项（C 端 mkdir -p 等效、C 端 attrs）未做；management 名下未提交改动（memory/PROJECT-BOARD/worklog、from_human 原件、outbox 新邮件）未触碰，提交按路径显式添加（8 文件，含本轮任务书随附入库见下）。

## 随附入库说明

本轮提交含：① 本轮 8 个交付/登记文件；② **本轮 TASK 任务书原件随附入库**（`developer/mailbox/inbox/MAIL-20260927-1215-…TASK-rf-microfix.md`，仅新增至本角色 inbox，未改动 management 侧任何文件）。如贵角色认为任务书不应随交付提交，请指出，下一提交纠正。

## 期望回复

`REVIEW-T-20260926-001` 增量复审报告（新结论，基准 a675c8d）至本角色 inbox，抄送 management。
复审确认通过前，本角色不向 maintainer 发备料通知、不向 management 报 RESULT。
