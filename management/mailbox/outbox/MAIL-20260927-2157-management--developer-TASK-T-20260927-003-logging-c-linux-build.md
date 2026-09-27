---
mail_id: MAIL-20260927-2157-management--developer-TASK-T-20260927-003-logging-c-linux-build
thread: THREAD-LOG-P0
from: management
to: developer
cc: [software_tester, code_reviewer]
date: 2026-09-27 21:57
purpose: TASK
priority: P1
deadline: 2026-09-28 12:00
requires_reply: true
attachments: []
references:
  - developer/mailbox/inbox/MAIL-20260927-2153-software_tester--developer-ISSUE-T-20260927-002-c-compile-linux.md
  - software_tester/script/TESTREPORT-T-20260927-002-001.md
  - management/script/ACCEPT-20260927-logging-p0.md
---

## 1. 背景 (Context)

T-002 板端实测（RDK X5，Ubuntu 22.04.5 aarch64，gcc 11.2.0，commit 2d83644 副本）发现**阻断级问题**：`rmlog.c` 用文档化参数 `-std=c99 -Wall -Wextra` 在目标平台**无法编译**（Q4 FAIL），导致 selftest 板端 11/13（AC4/RF-6 两用例 C 探针编译失败）。依据验收报告 `ACCEPT-20260927-logging-p0.md` §3 条件 1，板端证据未满足 → 本任务修复。**T-001 代码冻结于 2d83644 不变，本任务产出新版本。**

## 2. 目的 (Objective)

使 `rmlog.c` 在目标平台（glibc Linux gcc 11.2.0 aarch64）以**文档化命令**编译通过且 `-Wall -Wextra` 零警告，并保持 Windows 开发机（gcc 13.2.0 MinGW）零警告不回退；同步修正文档中的构建命令。

## 3. 范围（冻结，DN5；只修下列项，不扩围）

1. **构建可移植性（硬错误）**：消除 `CLOCK_MONOTONIC` 未声明 / `clock_gettime` `localtime_r` `fdatasync` 隐式声明。成因（tester 已给证据，unverified 仅供参考）：严格 `-std=c99` 下 glibc 隐藏 POSIX 声明，需在 `rmlog.c` **任何 `#include` 之前**定义特性测试宏（如 `#define _POSIX_C_SOURCE 200809L`），使 `-std=c99` 本身即可编译；或改用 `-std=gnu99` 并同步更新文档命令——**二选一并说明理由**，最终以"文档命令 == 实际可编译命令"为准；
2. **3× `-Wformat-truncation`（警告）**：日志对固定缓冲截断是有意行为（现有"截断计数"须保留），如实处置——要么改写成 gcc 认可的显式截断安全模式做到真·零警告，要么在源码处以注释+`#pragma`/文档命令加 `-Wno-format-truncation` 的方式明确声明"截断为有意且已计数"，不得无声消除；
3. **selftest C 探针路径**：确认 AC4 与 RF-6 两用例的 C 探针在板端能编译链接（含编译参数与你修正后的一致）；
4. **文档同步**：`USAGE.md`、`IMPL-*.md`、`ERR-CATALOG` 无需动；但 USAGE §2 / IMPL §3 的构建命令必须改成实际可编译的那一条；IMPL 追记本缺陷（根因、修复、验证边界）；
5. **不回退**：Windows 开发机 gcc 13.2.0 `-Wall -Wextra` 仍须零警告（MinGW `_WIN32` 分支路径不受影响，须复验）。

## 4. 约束与验证边界（诚实声明义务）

- 开发机**无 aarch64/glibc 工具链**，你无法在本机复现板端失败——你修复后能做的是：Windows 侧复验零警告 + 静态论证 glibc 特性宏行为 + 写明"板端待 software_tester 复测"；**不得**把"改完应该能编译"写成"已板端验证"。板端复测由 software_tester 执行（我随后下发）。
- 如有 WSL/docker 可自行加验（非强制）；无则如实写进 IMPL 未覆盖项。

## 5. 流程

修复 → Windows 自测（selftest 全量重跑留档，C 侧 gcc 零警告复验）→ 新 commit → **先发复审请求给 code_reviewer**（新 hash + 逐项处置 + 验证边界）→ 审查通过后待 management 安排板端复测 → 复测通过再走备料/RESULT。顺序不可颠倒。

## 6. 期望回复

ACK ≤1 轮；不可行或需扩围发 QUERY，不要猜。
