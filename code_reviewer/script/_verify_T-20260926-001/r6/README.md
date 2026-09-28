# r6 — T-20260927-003-logging-c-linux-build 复审（增量）验证留档

> 角色: code_reviewer (R-004) · 审查基准: commit `164d4c7`（T-003 linux-build-fix）
> 复审对象: `developer/script/` 在 `d6be523..164d4c7` 的 6 文件增量
> 验证日期: 2026-09-27 · 环境: Windows + gcc 13.2.0 (MinGW, C:\MinGW\bin\gcc.exe) + Python 3.14.7

## 1. 基准核对（W1）

- 用 `git archive 164d4c7 developer/script` 直接签出被审 commit 交付物到本目录（不经工作区），
  `git hash-object` 抽样核对：`rmlog.c`、`selftest.py`、`tests/probe_fdleak_rf6.c` 三件与 commit blob
  **逐字节一致**（match=True）。
- `git diff --name-only 164d4c7 HEAD`：被审代码/文档文件（rmlog.c / selftest.py / probe_fdleak_rf6.c /
  USAGE.md / IMPL-*.md）与 HEAD **零差异**（HEAD d3d0cfe 仅重编码 selftest 留档，无代码变更）。

## 2. Windows 侧零告警复验（W2，对应处置项 5「不回退」）

命令（`_WIN32` 分支，`-std=c99` 保持，无 `-lpthread`）：

| 对象 | 命令 | 退出码 | stderr 字节 |
|---|---|---|---|
| rmlog.c 独立编译 | `gcc -std=c99 -Wall -Wextra -c rmlog/rmlog.c` | 0 | **0**（`rmlog_warncheck.txt`） |
| AC4 探针 | `gcc -std=c99 -Wall -Wextra -I rmlog -o ac4_probe.exe rmlog/rmlog.c rmlog/_ac4_probe.c` | 0 | **0**（`probe_ac4_warncheck.txt`） |
| RF-6 探针 | `gcc -std=c99 -Wall -Wextra -I rmlog -o probe_fdleak_rf6.exe rmlog/rmlog.c tests/probe_fdleak_rf6.c` | 0 | **0**（`probe_rf6_warncheck.txt`） |

> 三个 `*_warncheck.txt` 均为捕获的 stderr（0 字节 = 零告警，与上轮 r5 留档同口径）。

## 3. 全量 selftest 独立复跑（W3）

命令：`python -m rmlog.selftest <r6>\work`（`*>` 重定向 → `selftest_r6.log`，随后转 UTF-8 无 BOM）

结果：**13/13 PASS，用时 41.5s，`__EXIT_CODE__=0`**（留档 `selftest_r6.log`）。
RF6 用例定量行：`RF6_PROBE reopen:base=50 after=50 delta=0 fast:base=51 after=51 delta=0 rounds=600 lines=600/600`。

## 4. 结论支撑

- 本目录三件 warncheck（0 字节）+ selftest_r6.log（13/13）+ 本 README 构成 Windows 侧独立复验证据。
- Linux/aarch64 侧（glibc gcc 11.2.0）**本角色无工具链，无法实测** —— 该侧为静态论证 + tester 板端边界表征
  （`q4_char_c99_POSIX.txt`：`-D_POSIX_C_SOURCE=200809L` → exit 0、仅余 3× format-truncation）背书，
  **坐实归 software_tester 板端复测**，本角色不下"已板端验证"断言。
