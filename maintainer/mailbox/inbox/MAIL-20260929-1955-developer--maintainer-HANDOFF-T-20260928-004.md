---
mail_id: MAIL-20260929-1955-developer--maintainer-HANDOFF-T-20260928-004
thread: THREAD-LOG-P0
from: developer
to: maintainer
cc: [management, code_reviewer]
date: 2026-09-29 19:55
purpose: HANDOFF
priority: P1
deadline: ""
requires_reply: false
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260928-004-08f6ce8.md
  - developer/mailbox/inbox/MAIL-20260929-1945-code_reviewer--developer-RESULT-T-20260928-004.md
  - developer/mailbox/inbox/MAIL-20260928-2133-management--developer-TASK-T-20260928-004-usage-rewrite.md
  - developer/script/IMPL-T-20260926-001-logging-platform-p0.md
  - developer/script/USAGE.md
  - developer/script/INDEX.md
  - maintainer/mailbox/inbox/MAIL-20260929-1955-developer--maintainer-QUERY-v002-handoff.md
---

## 合格确认通知（备料）— T-20260928-004-usage-rewrite（归档版本 002 备料）

收件确认：文档专项复审已 **PASS，零发现项**。依据 reviewer RESULT 信 MAIL-20260929-1945 与报告 `code_reviewer/script/REVIEW-T-20260928-004-08f6ce8.md`，按 management 任务书 MAIL-20260928-2133 §4 流程向你发本备料通知，供**归档版本 002** 备料使用。

> **归档形态口径说明**：版本 001（164d4c7）已归档冻结，本次仅两文档变更；本信按**全套重发**形态书写，增量归档还是整套重归以我对你的 QUERY（MAIL-20260929-1955-developer--maintainer-QUERY-v002-handoff，与本信同时发出）的答复为准。

### 1. task_id

`T-20260928-004-usage-rewrite`（USAGE.md 重构为用户优先手册，版本 002）

### 2. commit hash

- **本任务交付（复审与自测基准）：`08f6ce840d3bdbbeb2df2c20fcba0b4e54fe25a3`**（短 `08f6ce8`）
- **性质：`08f6ce8` = 归档版本 001（`164d4c7`）+ 纯文档重构**——`git diff --name-only df6cd42..08f6ce8` 全仓库**恰 2 文件**（`developer/script/USAGE.md` +418/−129 行区间、`developer/script/IMPL-T-20260926-001-logging-platform-p0.md` §9 追记），合计 +338/−129；**代码零变更**——`.py/.c/.h/ERR-CATALOG/CODE-STYLE` 冻结面 diff 为 0 文件（reviewer 报告 git 实证同口径）。
- hash 链连续：R0=`f3331b0` → R1=`45eeb04` → R2=`a675c8d` → R3=`2d83644` → R4=`164d4c7`（归档版本 001）→ **本任务=`08f6ce8`（归档版本 002 候选）**，无分叉。
- 文档再变则本通知与复审结论同时失效（须再次复审，可只审增量）。

### 3. 产物路径清单（本次变更恰 2 文件；其余产物与版本 001 归档件完全相同）

| 路径 | 本次变更 |
|---|---|
| `developer/script/USAGE.md` | **全文重写**为用户优先手册：§1 快速上手（Python 2 行 / C 3 行含编译命令）→ §2 日常使用 → §3 比赛日操作流 → §4 与系统日志的关系 → §5 FAQ 与故障排查（Q1~Q9）→ §6 部署（降级为一次性配置附录）→ §7 手册-代码对应关系表（一致性维护锚点）；**删除过时的「板端自测步骤（用户执行）」章节**及全部 Q1=A 回贴表述，板端事实改为一句话引用 TESTREPORT-T-20260927-003-001 实测结论 |
| `developer/script/IMPL-T-20260926-001-logging-platform-p0.md` | **§9 追记**（原 §1~§8 一字未动）：任务缘由 / 冻结 5 项改动清单（§9.1）/ 示例实跑核对证据（§9.2）/ 验证边界与已知风险（§9.3） |
| 其余（`rmlog/`、`rmlog_read.py`、`ERR-CATALOG.md`、`CODE-STYLE.md`、`INDEX.md`、`tests/` 等） | **零变更**（行为面冻结：行格式、错误码、默认路径 /userdata/rmlog/、轮转参数均未动） |

### 4. 构建方式（与版本 001 完全不变）

- **Python 侧**：`cd developer/script && python -m rmlog.selftest`
- **C 侧**：`gcc -std=c99 -Wall -Wextra -I rmlog -o <输出> rmlog\example.c rmlog\rmlog.c`
- 本次零代码变更，上述命令、依赖与版本 001 一字不差；手册中面向用户的全部命令已按实际行为逐一实跑核对（见下条）。

### 5. 自测证据

- **全量 selftest 13/13 PASS**（零代码变更回归证据）：本任务轮 `python -m rmlog.selftest tests\_work` 13/13、21.1s、退出码 0（IMPL §9.2 记录）；reviewer 独立复跑 **13/13 PASS 两次**（r7 留档 `selftest_r7.log`），与声明同口径。
- **示例实跑核对表（IMPL §9.2，2026-09-28 21:49~21:55，Windows/gcc 13.2.0/Python 3.14.7）**：Python 快速上手 2 行、C example 编译零告警+运行落盘、读端三命令、时间窗整分钟语义、残行 DROP、轮转文件族、通配符拒绝、默认目录构造期报错——逐项真实执行并记录输出摘要。
- **reviewer 独立抽查复核（复审报告 §4，V1~V5）**：文档原样命令实跑（快速上手/读端全链路 stdout-stderr 分离/轮转族/行为面回归）全部与手册表述一致，**"文档-实际行为一致性"成立**；8 件组件副本 blob 全 MATCH 08f6ce8。

### 6. IMPL 与审查报告路径

- 实现说明（本轮增量）：`developer/script/IMPL-T-20260926-001-logging-platform-p0.md` **§9**（§1~§8 为版本 001 既有内容）
- 审查报告：`code_reviewer/script/REVIEW-T-20260928-004-08f6ce8.md`（文档专项复审，**PASS，零发现项，绑定 08f6ce8**；验证证据区 `code_reviewer/script/_verify_T-20260926-001/r7/`）
- 任务依据：management 任务书 `developer/mailbox/inbox/MAIL-20260928-2133-management--developer-TASK-T-20260928-004-usage-rewrite.md`（冻结 5 项，reviewer 报告 §5 全部核销）
- 交付登记：`developer/script/INDEX.md`（#6 行登记 08f6ce8）

### 7. 声明

**本通知是备料不是许可。** 归档以 management 的 accepted 验收结论为准；届时请核对 management 验收记录、本通知与 reviewer 复审报告三者的 commit hash 一致（均应为 `08f6ce8`）。验收前如文档再变，本通知自动失效。归档形态（整套 v002 还是仅增量补件）以 QUERY 答复口径为准；software_tester 侧本任务无新增报告（纯文档、零代码行为变更，其 TESTREPORT-T-20260927-003-001 板端结论被本版手册引用并注明出处，仍归版本 001 链）。

developer (R-003)
2026-09-29 19:55
