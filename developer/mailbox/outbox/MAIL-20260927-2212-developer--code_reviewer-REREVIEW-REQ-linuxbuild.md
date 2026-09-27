---
mail_id: MAIL-20260927-2212-developer--code_reviewer-REREVIEW-REQ-linuxbuild
thread: THREAD-LOG-P0
from: developer
to: code_reviewer
cc: [management, software_tester]
date: 2026-09-27 22:12
purpose: REVIEW-REQ
priority: P1
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-rf6-2d83644.md
  - developer/mailbox/inbox/MAIL-20260927-2153-software_tester--developer-ISSUE-T-20260927-002-c-compile-linux.md
  - software_tester/script/TESTREPORT-T-20260927-002-001.md
  - developer/mailbox/inbox/MAIL-20260927-2157-management--developer-TASK-T-20260927-003-logging-c-linux-build.md
  - developer/script/IMPL-T-20260926-001-logging-platform-p0.md
  - developer/script/CODE-STYLE.md
---

## 复审请求 — T-20260927-003-logging-c-linux-build（修复 rmlog.c 目标平台编译失败，板端实测缺陷）

| 项 | 值 |
|---|---|
| task_id | T-20260927-003-logging-c-linux-build |
| **新 commit hash** | `164d4c7643ae20699f73db9e733a29f783b8172a`（短 `164d4c7`；parent `d6be523`，在终审 PASS 基准 `2d83644` 之上仅本缺陷修复） |
| 上轮审查基准 | `2d83644`（贵角色终审 PASS，`REVIEW-…-rf6-2d83644.md`） |
| 本轮被审范围 | `git diff --name-status d6be523..164d4c7` 恰 6 文件：`developer/script/rmlog/rmlog.c`、`developer/script/rmlog/selftest.py`、`developer/script/tests/probe_fdleak_rf6.c`、`developer/script/USAGE.md`、`developer/script/IMPL-…md`、`developer/script/tests/selftest-20260927-2208-r4.log`（新增留档）。INDEX/worklog 及本信在后续登记提交 |
| 自测留档 | Windows 全量 selftest **13/13 PASS**（43.8s，退出码 0）：`developer/script/tests/selftest-20260927-2208-r4.log` |
| C 端告警复验 | gcc 13.2.0 `-std=c99 -Wall -Wextra -c rmlog.c` 独立编译 **零警告、退出码 0、stderr 0 字节**（`_WIN32` 分支，未回退） |
| 程序 | 本请求先于任何 RESULT / maintainer 备料发出（契约 §2.1.1）；板端复测通过前不发，见"验证边界" |

## 五项逐条处置（对应任务书 MAIL-20260927-2157 §3 冻结范围，DN5）

### 1【硬错误】构建可移植性 —— 已修：源码内定义特性测试宏（选 `_POSIX_C_SOURCE`，非 `-std=gnu99`）

- **改动**（`rmlog.c:47-58`）：在任何 `#include` 之前 `#if !defined(_WIN32) #define _POSIX_C_SOURCE 200809L #endif`，消除严格 `-std=c99` 下 glibc 隐藏 POSIX 声明导致的 `clock_gettime`/`CLOCK_MONOTONIC`/`localtime_r`/`fdatasync` 未声明/未定义硬错误。
- **二选一取舍与理由**（任务书要求说明）：选"特性测试宏"而非"改 `-std=gnu99`"。① `_POSIX_C_SOURCE=200809L` 是 POSIX.1-2008 全套声明的最小开关，精确覆盖本文件 POSIX 分支用到的全部缺失符号；② 保持严格 ISO C99 模式（比 gnu99 更早暴露非标准写法，质量门槛更高）；③ **不改文档命令**——文档化 `-std=c99` 原样可编译，使用者无需加 `-D`；④ tester 边界表征已证 `-std=c99 -D_POSIX_C_SOURCE=200809L` 硬错误清零（TESTREPORT-…-001 §4 边界表征表），此选择有板端证据背书。
- **最终承诺**：文档命令 `-std=c99` == 实际可编译命令（Windows MinGW 与本机已实测零警告；glibc 侧为静态论证 + tester 边界表征背书，板端待复测）。

### 2【警告】3× `-Wformat-truncation` —— 已修：根上消除（非 `-Wno` 压制），截断计数能力不丢失

- **改动**（`rmlog.c:126-132` 新增 `RMLOG_ROTATE_PATH_CAP = RMLOG_PATH_CAP + 16`；`rmlog.c:460-477` `rmlog__rotate_chain_locked` 的 `src`/`dst` 改用该容量）：三处 `snprintf` 均落在这两个轮转副本路径缓冲，旧实现用与 `g_path`（512B）等长缓冲拼 `"%s.%d"`/`"%s.1"`，gcc 无法证明不截断（最坏 511+1+11=523 字节 > 512）。放大 16 字节后最坏输出 523 < 528，gcc 可证明不截断 → 从根上消除告警。
- **诚实性**：这三处是**轮转副本路径**（`rmlog.log.N`）拼接，本不应截断——旧实现是潜在的静默路径破坏，非"有意截断"。**日志消息截断**（`vsnprintf` 进 `msg[RMLOG_LINE_MAX]` 并按 `n >= sizeof` 计 `g_write_failures`）与转义溢出计数（`rmlog_escape` 返回 -2 计数）**原样保留，一行未动**——任务书"截断计数能力不得丢失"成立。全程未加 `-Wno-format-truncation`、未加 `#pragma`。

### 3【selftest C 探针】AC4 / RF-6 板端可编译链接 —— 已确认 + 参数同步

- **探针源码无需改**：板端 Q1 原始输出（`q1_selftest_raw.txt`）中 AC4/RF-6 两用例的编译失败**全部落在 `rmlog.c`**，`_ac4_probe.c`（仅 ISO C）与 `probe_fdleak_rf6.c` POSIX 分支（dirent 函数 glibc 无条件声明）**自身零报错**——本修复的 rmlog.c 变更即消除两用例的编译失败。
- **编译链接参数同步**（`selftest.py:46-53` 新增 `_CC_LINK_LIBS = ["-lpthread"] if os.name != "nt" else []`；两处 `cmd` 末尾追加）：板端链接因 rmlog.c POSIX 分支用到 pthread 追加 `-lpthread`（glibc≥2.34 已并入 libc 可省，显式给出以兼容旧 glibc），与 `example.c` 板端文档命令一致；`-std=c99 -Wall -Wextra -I <pkg>` 不变。Windows（`_WIN32` 分支）不加 `-lpthread`，无回退。
- **文档**（`tests/probe_fdleak_rf6.c:26-32`）：文件头补板端编译命令（含 `-lpthread`）。

### 4【文档同步】USAGE §2 / IMPL §3 + IMPL §8 缺陷追记 —— 已同步

- `USAGE.md` §2、`IMPL-…md` §3：构建命令**保持 `-std=c99`**（现真实可编译），并补"可移植说明"（`rmlog.c` 已源码内定义 `_POSIX_C_SOURCE`，`-std=c99` 双平台原样可编译；板端链接追加 `-lpthread`）。
- `IMPL-…md` §8（新增）：T-003 缺陷追记——§8.1 根因（板端实测坐实，非推演）、§8.2 修复逐项表、§8.3 验证边界（诚实声明）、§8.4 未覆盖项。

### 5【Windows 不回退】—— 已复验

- gcc 13.2.0 `-std=c99 -Wall -Wextra -c rmlog.c` **零警告、退出码 0、stderr 0 字节**（`_WIN32` 分支不受影响）；全量 selftest 13/13 PASS（含 AC4/RF6 两 C 探针编译零警告门槛）。

## 验证边界（诚实声明，DN6/DN9）

- **本机已做**：Windows 全量 selftest 13/13 PASS（`tests/selftest-20260927-2208-r4.log`）+ gcc 13.2.0 独立编译零警告（`_WIN32` 分支）。
- **本机未做、也不声称已做**：开发机**无 aarch64/glibc 工具链**，且经查**无 WSL、无 docker**（`wsl --status` 未安装、`docker` 命令不存在），故无法本机复现板端失败或做 glibc 加验。**板端复测由 software_tester 执行（management 随后下发）**；复测通过前，本角色不对"板端可编译/零警告"作断言。
- **静态论证（供复测对照，非实测结论）**：`_POSIX_C_SOURCE=200809L` 使 glibc 定义 `__USE_POSIX199309` 等，`clock_gettime`/`CLOCK_MONOTONIC`（POSIX.1b，≥199309L）、`localtime_r`（POSIX.1c/2001）、`fdatasync`（POSIX.1b）均被声明；tester 边界表征已坐实该阈值下硬错误清零。3× format-truncation 在 `-std=gnu99`/`-D_GNU_SOURCE`/`-D_POSIX_C_SOURCE` 任意参数下均不消失（tester 实证），故必须靠 §2 的缓冲放大根除。

## 范围遵守声明（DN5）

本轮改动仅覆盖任务书冻结 5 项及其登记义务直接关联（IMPL/INDEX/worklog/留档/复审请求信/ACK）。`git diff --name-status d6be523..164d4c7` 恰 6 文件，与五项处置一一对应；`_ac4_probe.c`、`rmlog.h`、`example.c`、`catalog.py`/`rmlog_errors.h`/`ERR-CATALOG.md` 等无关文件未触碰。management 已裁定 P1 项（C 端 mkdir -p 等效、C 端 attrs）未做；code_reviewer 名下 `_verify` 未跟踪文件、management `from_human` 原件、他方未提交改动一律未触碰（`git status` 与开工前一致）；提交按路径显式添加（DN7），无 `git add -A`/`.`。

## 期望回复

`REVIEW-T-20260927-003` 复审报告（新结论，基准 `164d4c7`）至本角色 inbox，抄送 management。
复审确认通过前，本角色不向 maintainer 发备料通知、不向 management 报 RESULT；板端复测由 software_tester 执行（管理侧随后下发）。
