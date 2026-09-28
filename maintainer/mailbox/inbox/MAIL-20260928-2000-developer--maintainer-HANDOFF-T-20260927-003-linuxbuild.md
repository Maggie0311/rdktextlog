---
mail_id: MAIL-20260928-2000-developer--maintainer-HANDOFF-T-20260927-003-linuxbuild
thread: THREAD-LOG-P0
from: developer
to: maintainer
date: 2026-09-28 20:00
purpose: HANDOFF
priority: P1
requires_reply: false
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260927-003-164d4c7.md
  - software_tester/script/TESTREPORT-T-20260927-003-001.md
  - management/script/ACCEPT-20260927-logging-p0.md
  - maintainer/mailbox/inbox/MAIL-20260927-1505-developer--maintainer-HANDOFF-T-20260926-001.md
  - developer/script/IMPL-T-20260926-001-logging-platform-p0.md
  - developer/script/INDEX.md
---

## 合格确认通知（备料，补发）— T-20260927-003-logging-c-linux-build

**本信是对 2026-09-27 那封覆盖 R3=`2d83644` 的 HANDOFF（MAIL-20260927-1505-developer--maintainer-HANDOFF-T-20260926-001.md）的补发/取代件**：该信发出后，板端首测发现 C 端目标平台编译失败（T-002），management 裁定开 T-003 修复，交付 R4=`164d4c7`（复审 PASS）并经板端复测全绿，management 验收报告 ACCEPT-20260927-logging-p0.md 已升格 **accepted（v2，归档版本指向 `164d4c7`）**。按契约 §2.1.5 补发针对 164d4c7 的合格确认通知，使三份要件（developer HANDOFF / reviewer+tester 报告 / management 许可）commit hash 一致，供你归档备料。**本通知自发出起取代 2026-09-27 那封 HANDOFF 成为当前有效备料，旧信仅留档备查。**

### 1. task_id

`T-20260927-003-logging-c-linux-build`（归属主交付 `T-20260926-001-logging-platform-p0` 的 **R4 版本**；任务书 MAIL-20260927-2157）

### 2. commit hash

**`164d4c7643ae20699f73db9e733a29f783b8172a`（短 `164d4c7`）** —— T-003 linux-build-fix 交付提交（R4 终版，审查与板端复测基准）。

- 全链：R0=`f3331b0` → R1=`45eeb04` → R2=`a675c8d` → R3=`2d83644` → **R4=`164d4c7`**
- `164d4c7` = `2d83644` + linux-build-fix：仅 **6 文件 +121/-7**（`rmlog/rmlog.c` 源码内 `_POSIX_C_SOURCE 200809L`、轮转副本路径缓冲放大根除 3×format-truncation、两 C 探针非 Windows 追加 `-lpthread`、selftest/文档同步、IMPL §8 追记与 selftest 留档）
- 代码再变则本通知与复审/复测结论同时失效。

### 3. 产物路径清单（全部位于 `developer/script/`）

| 路径 | 内容 |
|---|---|
| `developer/script/rmlog/` | Python 组件（catalog/format/writer/worker/gen_code/selftest）+ C 接口（`rmlog.h` / **`rmlog.c`（R4：顶部 `_POSIX_C_SOURCE 200809L`）** / 生成物 `rmlog_errors.h` / `example.c` / `_ac4_probe.c`） |
| `developer/script/rmlog_read.py` | 读端工具（parse/tail/filter，时间前缀归一） |
| `developer/script/USAGE.md` | 场下使用方法（§2/§3 已补可移植说明与板端自测清单） |
| `developer/script/ERR-CATALOG.md` | 错误码文档（生成物） |
| `developer/script/IMPL-T-20260926-001-logging-platform-p0.md` | 实现说明（**§8 为 T-003 缺陷追记**：根因/修复/验证边界） |
| `developer/script/INDEX.md` | 交付单元登记（R0–R4 hash 链，#5 行已登记 R4=164d4c7） |

### 4. 构建方式

- **Python 侧**：`cd developer/script && python3 -m rmlog.selftest`
- **C 侧**：`gcc -std=c99 -Wall -Wextra`（`rmlog/rmlog.c` 顶部已含 `_POSIX_C_SOURCE 200809L`，无需额外编译参数；**板端 aarch64 glibc 与开发机双端零警告**——板端实测 stderr 0 字节，开发机 gcc 13.2.0 复验同零警告）

### 5. 自测证据

- **开发机全量 selftest 13/13 PASS**（43.8s，退出码 0）：留档 `developer/script/tests/selftest-20260927-2208-r4.log`。
- **板端复测 13/13 全 PASS**：`software_tester/script/TESTREPORT-T-20260927-003-001.md`（上轮 11/13 → 本轮 13/13，含 AC4、RF6 两 C 探针用例，`-lpthread` 链接执行成功、RF6 delta=0）。
- 板端 `gcc -std=c99 -Wall -Wextra -c rmlog/rmlog.c` 退出码 0 且 **stderr 0 字节**（上轮硬错误 + 3×format-truncation 全消）；多进程×轮转同参对账无回归。

### 6. IMPL 与审查报告路径

- 实现说明（T-003 缺陷追记）：`developer/script/IMPL-T-20260926-001-logging-platform-p0.md` §8
- T-003 复审报告（**PASS，绑定 164d4c7**）：`code_reviewer/script/REVIEW-T-20260927-003-164d4c7.md`
- 板端复测报告（**全绿**）：`software_tester/script/TESTREPORT-T-20260927-003-001.md`
- 审查链全貌见 management 验收报告 §"审查依据"（五份，末位即上述 164d4c7 复审）。

### 7. 声明

**本通知是备料不是许可。** 归档以 management 的 accepted 验收结论为准：`management/script/ACCEPT-20260927-logging-p0.md`（v2，归档版本指向 `164d4c7`）。届时请核对 management 验收记录、本通知与 reviewer/tester 报告三者的 commit hash 一致（均应为 `164d4c7`）。**本通知取代本人 2026-09-27 发出的覆盖 `2d83644` 的 HANDOFF（MAIL-20260927-1505）成为当前有效备料**；`2d83644` 不再是归档版本。

developer (R-003)
2026-09-28 20:00
