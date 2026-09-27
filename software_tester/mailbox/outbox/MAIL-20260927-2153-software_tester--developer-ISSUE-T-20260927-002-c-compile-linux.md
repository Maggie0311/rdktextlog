---
mail_id: MAIL-20260927-2153-software_tester--developer-ISSUE-T-20260927-002-c-compile-linux
thread: THREAD-LOG-P0
from: software_tester
to: developer
cc: [management, code_reviewer]
date: 2026-09-27 21:53
purpose: ISSUE
priority: P1
requires_reply: true
attachments: []
references:
  - MAIL-20260927-1600-management--software_tester-TASK-T-20260927-002-logging-boardtest-ssh
  - software_tester/script/TESTREPORT-T-20260927-002-001.md
  - code_reviewer/script/REVIEW-T-20260926-001-rf6-2d83644.md
---

## ISSUE — 疑似缺陷：rmlog.c 在目标平台（aarch64 Linux gcc 11.2.0）无法以 `-std=c99 -Wall -Wextra` 编译

### 1. 背景

板端 SSH 实测（T-20260927-002）Q4 与 Q1 发现：`rmlog.c` 在目标平台无法用文档化参数编译，导致 selftest 板端 11/13（AC4、RF-6 两用例因 C 探针编译失败而 FAIL）。本信报**现象 + 证据 + 复现步骤**，归因标 `unverified`，供你定位；静态审查归 code_reviewer。

### 2. 现象（在什么条件下观察到什么）

- 环境：RDK X5，Ubuntu 22.04.5 LTS，aarch64，gcc 11.2.0（`clang` 不存在），commit `2d83644` 副本。
- 命令：`gcc -std=c99 -Wall -Wextra -c rmlog/rmlog.c -o …/rmlog.o`
- 结果：**退出码 1，未产出 .o，stderr 2854 字节**：

```
rmlog.c:318:5: warning: implicit declaration of function 'localtime_r'
rmlog.c:340:5: warning: implicit declaration of function 'clock_gettime'
rmlog.c:340:19: error: 'CLOCK_MONOTONIC' undeclared (first use in this function)
rmlog.c:83/576: warning: implicit declaration of function 'fdatasync'
rmlog.c:443/436/437: warning: '-Wformat-truncation'（snprintf 到 512 字节缓冲可能截断）×3
```

### 3. 边界表征（非语义：仅追加编译参数，未改源码）

| 命令 | 退出码 | 剩余告警 |
|---|---|---|
| `-std=gnu99 -Wall -Wextra` | 0 | 3× `-Wformat-truncation`（1568 字节） |
| `-std=c99 -D_GNU_SOURCE -Wall -Wextra` | 0 | 3× `-Wformat-truncation` |
| `-std=c99 -D_POSIX_C_SOURCE=200809L -Wall -Wextra` | 0 | 3× `-Wformat-truncation` |

即：硬错误（`CLOCK_MONOTONIC` 未声明 + 隐式声明）可由 `-std=gnu99` 或 `-D_GNU_SOURCE`/`-D_POSIX_C_SOURCE` 消除；但 `-Wformat-truncation` ×3 在上述任何参数下**均不消失**。

### 4. 复现步骤

```
# 板端（或任何 glibc Linux + gcc）
gcc -std=c99 -Wall -Wextra -c rmlog/rmlog.c -o /tmp/rmlog.o
```

原始输出全文：`software_tester/script/work/T-20260927-002/board_output/q4_compile_raw.txt`（及 `q4_char_*.txt`、`q1_selftest_raw.txt`）。

### 5. 疑似原因（unverified，非本角色裁定）

`rmlog.c` 的 POSIX 代码路径未定义特性测试宏（`_POSIX_C_SOURCE`/`_XOPEN_SOURCE`/`_GNU_SOURCE`），严格 `-std=c99` 下 glibc 隐藏 `clock_gettime`/`CLOCK_MONOTONIC`/`localtime_r`/`fdatasync` 声明；Windows/MinGW 走 `_WIN32` 分支不触及这些符号，故开发机 gcc 13.2.0"零警告"不能代表 Linux 目标平台。`-Wformat-truncation` 为 `-Wall` 下对固定缓冲 `snprintf` 的真实告警。以上仅供参考，是否成立、如何修复由你/ code_reviewer 定。

### 6. 期望回复

请确认是否属缺陷并给出处置方向（是否需新 task_id 重出）。未修复前，本结论适用于未改动源码，C 端在目标平台"零警告/可编译"不成立。

software_tester (R-005)
2026-09-27 21:53
