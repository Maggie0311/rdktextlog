---
mail_id: MAIL-20260927-2153-software_tester--management-RESULT-T-20260927-002
thread: THREAD-LOG-P0
from: software_tester
to: management
cc: [developer, code_reviewer]
date: 2026-09-27 21:53
purpose: RESULT
priority: P1
deadline: 2026-09-27 23:59
requires_reply: true
attachments: []
references:
  - MAIL-20260927-1600-management--software_tester-TASK-T-20260927-002-logging-boardtest-ssh
  - software_tester/script/TESTPLAN-T-20260927-002.md
  - software_tester/script/TESTREPORT-T-20260927-002-001.md
---

## RESULT — T-20260927-002-logging-boardtest-ssh（板端 SSH 实测）

已完成 RDK X5 板端 SSH 实测。报告：`software_tester/script/TESTREPORT-T-20260927-002-001.md`（冻结字段全）。**本 RESULT ≠ 验收。**

### 1. 被测对象

- commit：`2d8364400c9a7afc0e8210ba247799d2bfe9bc34`（`2d83644`），经 `git archive` 签出副本，本机与板端 md5 逐文件核对一致；未修改 developer 源码。

### 2. 四个问题结论（事实层）

| Q | 结论 | 关键事实 |
|---|---|---|
| Q1 板端 selftest 13/13 | **FAIL（11/13）** | `SELFTEST FAIL`，退出码 1；AC4 consistency 与 C fdleak(RF-6) 两用例因 **C 探针编译失败**而 FAIL，其余 11 用例 PASS（含 AC5×F-1 3×400=1200 逐 worker 对账 PASS） |
| Q2 平台核查 | **已采集（事实）** | python3 3.10.12；`/userdata` 存在；journald 持久化目录 `/var/log/journal` 存在（Storage 默认 auto）；rsyslog active+enabled；**coredumpctl/systemd-coredump 不可用**（`core_pattern=core`）；`dmesg --time-format iso` 可用（ISO 时间戳） |
| Q3 多进程×轮转无静默销毁 | **PASS** | solo/multi/combo 三组逐 worker 对账：无 worker 全灭、幸存为连续后缀（无内部洞）、无半行；combo(keep=20) 写成功 1200==可见 1200 |
| Q4 板端 gcc/clang 编译 rmlog.c 零警告 | **FAIL** | `gcc -std=c99 -Wall -Wextra -c rmlog.c` → 退出码 1，`CLOCK_MONOTONIC` 未声明（硬错误）+ 隐式声明 ×3 + `-Wformat-truncation` ×3；clang 不存在；即使 `-std=gnu99`/`-D_GNU_SOURCE`/`-D_POSIX_C_SOURCE` 消除硬错误，仍有 3 处 `-Wformat-truncation` 警告 |

### 3. 复现命令与原始输出

- 复现命令见 `TESTREPORT-T-20260927-002-001.md` §4。
- 原始输出留档：`software_tester/script/work/T-20260927-002/board_output/`（q1/q2/q3/q4 全部 raw + `q3_logs.tar`）。

### 4. 需 management 裁量 / 需 developer 处理

- **C 端在目标平台（aarch64 Linux gcc 11.2.0）无法以文档化参数 `-std=c99 -Wall -Wextra` 编译**（UV-3 实测为 FAIL；开发机 gcc 13.2.0 零警告不能代表 Linux 目标平台）。已另行发 ISSUE 给 developer（抄 management）附现象+证据+复现步骤，归因标 unverified。
- 因发现阻断级问题（C 端目标平台不可编译 → AC1/AC4/Q4 板端证据不成立），**未向 maintainer 发 HANDOFF**（契约 §2.1.5）。
- 其余板端结论：Python 端 11 用例板端 PASS（含 AC5×F-1 多进程×轮转，UV-1 Python 侧已落成实测）；Q3 无静默销毁。

### 5. 声明

本 RESULT 只描述"在什么条件下观察到了什么"；验收归 management，静态审查归 code_reviewer。未修改 developer 源码；适配仅限非语义适配（传输/路径/编译参数/测试工件，逐条见报告 §3）。

software_tester (R-005)
2026-09-27 21:53
