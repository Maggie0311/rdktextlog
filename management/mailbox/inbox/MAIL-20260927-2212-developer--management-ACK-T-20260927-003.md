---
mail_id: MAIL-20260927-2212-developer--management-ACK-T-20260927-003
thread: THREAD-LOG-P0
from: developer
to: management
cc: [software_tester, code_reviewer]
date: 2026-09-27 22:12
purpose: ACK
priority: P1
requires_reply: false
attachments: []
references:
  - developer/mailbox/inbox/MAIL-20260927-2157-management--developer-TASK-T-20260927-003-logging-c-linux-build.md
  - developer/mailbox/inbox/MAIL-20260927-2153-software_tester--developer-ISSUE-T-20260927-002-c-compile-linux.md
---

## ACK — T-20260927-003-logging-c-linux-build（修复 rmlog.c 目标平台编译失败）

收到任务书，确认范围（冻结 5 项，DN5 不扩围）与验证边界（本机无 aarch64/glibc 工具链且无 WSL/docker，板端复测待 software_tester）。本轮修复已完成：

- 修复 commit：`164d4c7`（含 task_id 与 linux-build-fix）。
- 五项处置摘要：① `rmlog.c` 任何 `#include` 前按平台 `#define _POSIX_C_SOURCE 200809L`（选特性宏而非 `-std=gnu99`，理由见复审请求信）；② 轮转副本路径缓冲 `RMLOG_ROTATE_PATH_CAP = RMLOG_PATH_CAP + 16` 根除 3× `-Wformat-truncation`（非 `-Wno` 压制，日志消息截断计数能力原样保留）；③ selftest 两 C 探针（AC4/RF6）非 Windows 追加 `-lpthread` 保证板端可链接；④ USAGE §2 / IMPL §3 补可移植说明 + IMPL §8 缺陷追记（根因/修复/验证边界）；⑤ Windows gcc 13.2.0 零警告复验不回退。
- 自测证据：Windows 全量 selftest 13/13 PASS（留档 `tests/selftest-20260927-2208-r4.log`）+ gcc `-std=c99 -Wall -Wextra -c rmlog.c` 零警告（stderr 0 字节）。
- 已按顺序**先发复审请求**给 code_reviewer（`MAIL-20260927-2212-developer--code_reviewer-REREVIEW-REQ-linuxbuild.md`）。

本轮**不发 RESULT、不发 maintainer 备料**：待复审通过 + software_tester 板端复测通过后再走备料/RESULT。板端复测任务待你下发。
