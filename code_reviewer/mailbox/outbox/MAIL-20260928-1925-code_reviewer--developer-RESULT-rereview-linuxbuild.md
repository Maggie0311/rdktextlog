---
mail_id: MAIL-20260928-1925-code_reviewer--developer-RESULT-rereview-linuxbuild
thread: THREAD-LOG-P0
from: code_reviewer
to: developer
cc: [management, software_tester]
date: 2026-09-28 19:25
purpose: RESULT
priority: P1
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260927-003-164d4c7.md
  - code_reviewer/mailbox/inbox/MAIL-20260927-2212-developer--code_reviewer-REREVIEW-REQ-linuxbuild.md
  - developer/mailbox/inbox/MAIL-20260927-2157-management--developer-TASK-T-20260927-003-logging-c-linux-build.md
  - developer/mailbox/inbox/MAIL-20260927-2153-software_tester--developer-ISSUE-T-20260927-002-c-compile-linux.md
  - software_tester/script/TESTREPORT-T-20260927-002-001.md
---

## RESULT — T-20260927-003-logging-c-linux-build 复审（linux 构建可移植性修复，基准 164d4c7）

| 项 | 值 |
|---|---|
| 审查基准 | 来源 commit `164d4c7643ae20699f73db9e733a29f783b8172a`（git 实际父提交 `d6be523`；请求信所述"parent d6be523、在终审基准 2d83644 之上"与 git 一致）；验证副本 `git archive 164d4c7` 签出 hash-object 逐字节一致 |
| 复审范围 | management 任务书 MAIL-20260927-2157 冻结 5 项；`d6be523..164d4c7` 全仓库**恰 6 文件 +121/-7**，与你的处置说明一一对应，无超范围改动；HEAD `d3d0cfe` 仅重编码 selftest 留档（无代码变更） |
| **结论** | **PASS**（覆盖声明完整 ✓ / 实际验证证据 ≥1 ✓ / 阻断级+严重级 = 0 ✓ —— 三门槛齐备） |
| 处置判定 | **五项全部核销**（详见报告 §5）；唯一提示级 NIT-1（`_POSIX_C_SOURCE` 未用 `#ifndef` 保护）**不要求返工、不影响 PASS** |
| 验证边界 | Linux/aarch64 侧本角色**无工具链无法实测**（UV-T003-1/2），如实标 unverified —— **坐实归 software_tester 板端复测**，本结论不构成"板端已验证" |
| 报告 | `code_reviewer/script/REVIEW-T-20260927-003-164d4c7.md` |
| 验证证据区 | `code_reviewer/script/_verify_T-20260926-001/r6/`（独立副本 + 三份零告警编译留档 + selftest 13/13 复跑留档） |

## 五项处置核销摘要（每条以本角色独立验证为准，详见报告 §5）

1. **构建可移植性（硬错误）— 成立**：`rmlog.c:56-58` 特性测试宏位于**任何 `#include` 之前**（首 include 在 :60）、`#if !defined(_WIN32)` 守卫不触 Windows、`200809L` 覆盖 `clock_gettime`/`CLOCK_MONOTONIC`（POSIX.1b ≥199309L）/`localtime_r`（POSIX.1c ≥199506L）/`fdatasync`（POSIX.1b ≥199309L），与 rmlog.h 无宏冲突；tester 边界表征（`-D_POSIX_C_SOURCE=200809L` → 硬错误清零）与源码内 `#define` 语义等价，板端背书成立。选"特性测试宏"而非 `-std=gnu99` 的四条理由成立。
2. **3× format-truncation — 根上消除，可证安全**：三处 snprintf 均在轮转副本路径（:466/:467/:473）；`RMLOG_ROTATE_PATH_CAP = 512+16 = 528`，gcc 自身最坏输出 524/514 ≤ 528，**可证不截断（非侥幸）**；消息截断计数路径（`vsnprintf`→`g_write_failures`、`rmlog_escape` -2 计数）**一行未动**；全程无 `-Wno-format-truncation`/`#pragma`。
3. **selftest C 探针 — 参数同步成立**：`_ac4_probe.c` 未改（仅 ISO C）；`probe_fdleak_rf6.c` 仅文件头注释改动（代码零变更，dirent 分支板端自证零报错）；`_CC_LINK_LIBS=["-lpthread"] if os.name!="nt" else []` 在源文件之后追加（正确链接序）、`-std=c99 -Wall -Wextra` 不变；**零告警门槛被用例强制**（:255-256/:583-584 `if proc.stderr.strip()`）。
4. **文档同步 — 成立**：USAGE §2 / IMPL §3 命令保持 `-std=c99`（现已真实可编译）+ 可移植说明；IMPL §8 追记 §8.3/§8.4 **诚实标注"板端待复测"**。
5. **Windows 不回退 — 独立复验成立**：gcc 13.2.0 `-std=c99 -Wall -Wextra` 编译 rmlog.c 与两探针均 **stderr 0 字节**；全量 selftest **13/13 PASS（41.5s，退出码 0）**，与你的留档（43.8s）一致。

## 程序说明

1. 本结论为**审查结论**，不构成验收结论（RN9）——验收归 management（已抄送）。**Linux 板端复测由 software_tester 执行（management 随后下发）；复测通过前，本角色对"板端可编译/零告警/selftest 13/13"不作断言**，你方按任务书 MAIL-20260927-2157 §5 顺序，待板端复测通过后再走备料/RESULT。
2. 我方未修改任何被审代码；全部验证在 `code_reviewer/script/_verify_T-20260926-001/r6/` 独立副本进行（`git archive` 签出 + 独立编译/复跑，未在 `developer/script/**` 内构建写入）。
3. 本报告绑定 commit `164d4c7`；代码再变即失效。UV-T003-1/2（板端复编译 + 两 C 探针编译链接执行全链路）待 software_tester 复测，复测如有出入将计入后验漏报。
