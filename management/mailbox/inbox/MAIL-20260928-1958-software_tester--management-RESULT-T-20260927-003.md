---
mail_id: MAIL-20260928-1958-software_tester--management-RESULT-T-20260927-003
thread: THREAD-LOG-P0
from: software_tester
to: management
cc: [developer, code_reviewer]
date: 2026-09-28 19:58
purpose: RESULT
priority: P1
requires_reply: true
attachments: []
references:
  - software_tester/script/TESTREPORT-T-20260927-002-001.md
  - code_reviewer/script/REVIEW-T-20260927-003-164d4c7.md
  - software_tester/script/TESTREPORT-T-20260927-003-001.md
---

## RESULT — T-20260927-003-logging-c-linux-build（linux-build-fix 板端聚焦复测）

已完成 RDK X5 板端复测（聚焦 2+1 问）。报告：`software_tester/script/TESTREPORT-T-20260927-003-001.md`（冻结字段全）。**本 RESULT ≠ 验收。**

### 1. 被测对象

- commit：`164d4c7643ae20699f73db9e733a29f783b8172a`（`164d4c7`，linux-build-fix）。`git archive` 签出副本，本机 12 关键文件 blob 核对 MATCH，板端 md5 34/34 MATCH；未修改 developer 源码。
- 板端：RDK X5 aarch64 / Ubuntu 22.04.5 / gcc 11.2.0 / python3 3.10.12；SSH 地址已轮换为新 IPv6（连接成功）。

### 2. 复测三项结论（事实层）

| 问 | 结论 | 关键事实（对照上轮 T-002） |
|---|---|---|
| R-Q1 板端 selftest 13/13 | **PASS** | `SELFTEST PASS`，退出码 0，13/13（上轮 11/13）；上轮 FAIL 的 AC4 与 RF6 均 PASS——RF6 定量行 `reopen:base=6 after=6 delta=0 fast:base=7 after=7 delta=0 rounds=600 lines=600/600`（C 探针含 `-lpthread` 链接执行成功） |
| R-Q4 板端 `gcc -std=c99 -Wall -Wextra -c rmlog.c` | **PASS** | 退出码 **0** 且 stderr **0 字节**，.o 25544 字节产出（上轮退出码 1、stderr 2854 字节：CLOCK_MONOTONIC 硬错误 + 3× format-truncation）；本轮未追加任何编译参数，与上轮 FAIL 同口径 |
| R-Q3 多进程×轮转对账（UV-1 复确认，上轮同参） | **PASS，无回归** | combo 3×400 keep=20：写成功 1200 == 可见 1200，无半行/无全灭/无缺号；multi 2×300 与 solo 基线：无全灭、幸存连续后缀；三组全 OK，与上轮一致 |

### 3. 复现命令与原始输出

- 复现命令见报告 §4；原始输出留档 `software_tester/script/work/T-20260927-003/board_output/`（r0 连通自证 / remote_md5 / rq4 编译 / rq1 selftest 全文 / rq3 探针+对账 / rq3_logs.tar）。

### 4. 覆盖与未覆盖

- 本轮**聚焦复测**：未重复 Q2 全量平台核查（上轮已采集，平台未变更，仅地址轮换）。
- 未覆盖：clang（板端无）、断电/掉电恢复（UV-5）、C 端 flock 竞争轮转专测（UV-2，本轮由 selftest RF6 用例间接覆盖）、大压力/长时稳定性。

### 5. 备料与通知

- 因无阻断级问题，已按契约 §2.1.5 向 maintainer 发合格确认通知（HANDOFF，备料非许可）：`maintainer/mailbox/inbox/MAIL-20260928-1958-software_tester--maintainer-HANDOFF-T-20260927-003.md`。
- 本实测坐实 code_reviewer 复审报告 §6 UV-T003-1/2（板端可编译零告警 / 两 C 探针编译链接执行全链路）。

### 6. 声明

本 RESULT 只描述"在什么条件下观察到了什么"；验收归 management，静态审查归 code_reviewer。未修改 developer 源码；适配仅限非语义适配（逐条见报告 §3）。

software_tester (R-005)
2026-09-28 19:58
