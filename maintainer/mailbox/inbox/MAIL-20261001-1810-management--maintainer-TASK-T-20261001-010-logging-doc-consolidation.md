---
mail_id: MAIL-20261001-1810-management--maintainer-TASK-T-20261001-010-logging-doc-consolidation
thread: THREAD-LOG-V2
from: management
to: maintainer
cc: []
date: 2026-10-01 18:10
purpose: TASK
priority: P1
deadline: 2026-10-02 12:00
requires_reply: true
attachments: []
references:
  - maintainer/code_archive/README.md
  - maintainer/code_archive/INDEX.md
  - developer/script/USAGE.md
  - developer/script/rmlog/USAGE.md
  - maintainer/code_archive/T-20260926-001-logging-platform-p0/SPEC-001.md
  - maintainer/code_archive/T-20260930-005-logging-v2/SPEC-001.md
---

## 1. 背景 (Context)

人类用户对文档提出三点意见（2026-10-01，全部成立）：
1. 文档散落（`developer/script/` 与 `maintainer/code_archive/` 两处、v1/v2 两个 task 目录），没有统一入口；
2. 命名不自解释（SPEC/WALKTHROUGH/DIFF/USAGE/IMPL/PLAN 从文件名看不出"哪些是给我看的"）；
3. **没有一份文档回答"v2 相比 v1 新增了什么功能、使用方法有何不同"**（最关键缺口：v2 的 DIFF-001 写的是"首版"而非"v1→v2"）。

## 2. 目的 (Objective)

文档重整：统一入口、命名自解释、补齐 v1→v2 变更说明。**全部为增量新增/增强，不改动已归档 code/ 与既有文档内容。**

## 3. 交付（落 `maintainer/` 下）

### 3.1 重写 `maintainer/code_archive/README.md` 为「文档导航入口」
顶部醒目声明：**"所有给人看的文档统一在 maintainer 下；developer/script 里的是开发过程原始产物（源码 + 实现说明 IMPL + 代码风格 CODE-STYLE），最终以 maintainer 归档版为准。"** 并给出两张表：

- **读者 → 文档映射**（按"你是谁/想干什么 → 按顺序读什么"，路径精确到文件）：
  | 你是谁 / 想干什么 | 读什么（按顺序） |
  |---|---|
  | 电控队员，想上手用 | `developer/script/USAGE.md`(使用手册) → `code_archive/变更说明-v2.md`(v2 新功能/用法差异) |
  | 想理解它是什么、开发过程、为什么这样 | `T-20260930-005-logging-v2/SPEC-001.md`(说明书·总览) → `…/WALKTHROUGH-001.md`(走读) → `…/DIFF-001.md`(版本差异) |
  | 想改代码/接入开发 | `developer/script/rmlog/USAGE.md`(API 要点) → `…/WALKTHROUGH-001.md` → `developer/script/IMPL-T-20260930-005-logging-v2.md`(实现说明) |
- **命名术语表**（让文件名自解释）：
  `SPEC-001`=说明书（给人类看的总览与开发过程）｜`WALKTHROUGH-001`=逐模块代码走读（教学向）｜`DIFF-001`=版本差异｜`QUESTIONS-001`=读码前自查｜`USAGE.md`=使用手册（用户向）｜`IMPL-*.md`=实现说明（开发者向）｜`PLAN-*.md`=开发计划（开发者向）｜`VERSION-*.md`=归档版本卡（审计向）。

### 3.2 新建 `maintainer/code_archive/变更说明-v2.md`（本任务核心）
明确回答两问，内容务必与代码事实一致（引用 file:line 与 IMPL/PLAN）：
- **v2 相比 v1 新增了什么功能**（表格：功能 / 是什么 / 为什么加 / 对应文件）：
  `AsyncWriter`（有界异步非阻塞入队，1kHz 控制线程不阻塞，队列满丢+计数）、`Session`（会话/run 标识，可过滤/导出）、`checks.py`+`fault_demo.py`（五域故障检测适配接口与注入演示，业务供事实→映射错误码）、`daemon.py`+`systemd/rmlog-demo.service`（无人值守服务模板，SIGTERM 收尾）、`export_evidence.py`（一键导出业务+journal+dmesg+版本，逐项降级不伪造）、`rmlog_read --session`（会话过滤）。
- **使用方法是否有不同**：
  - 完全不变的：`rmlog.event()` / `RMLOG_I/W/E/F` 宏、LOGV1 行格式、五域错误码、`rmlog_read` 基础过滤——v1 用法全兼容；
  - 新增/推荐的用法：session 绑定、`AsyncWriter` 异步入队、`export_evidence` 导出、`--session` 过滤；
  - 迁移注意点：异步队列满会丢（`dropped` 计数，非零丢失承诺）；故障注入需业务提供事实（库不自动探测 SPI/CAN/电机）；systemd 单元路径/权限待板端确认（未实装）；开发机默认目录 `/userdata` 不存在，需 `set_default_writer` 改目录。
- 文末注明"本文件对应框架 DIFF（版本差异）概念，是 v1→v2 的完整差异；原 v2 归档的 DIFF-001 为 ChatGPT 按新任务写的'首版'，不含 v1→v2 对比，以此文为准"。

### 3.3 `maintainer/script/GLOSSARY.md` 增补 v2 新术语
`session`、`异步队列/AsyncWriter`、`dropped`、`checks`、`fault_demo`、`export_evidence`——人话解释 + 对应文件。

### 3.4 v1/v2 归档关系说明（并入导航 README）
v1=基线（`T-20260926-001-logging-platform-p0`，已归档 v001/v002）；v2=升级（`T-20260930-005-logging-v2`，已归档 v001/v002）；两者是两个 task 的两套归档，v2 为当前主线。

## 4. 边界

**只做增量新增/增强**：不改已归档 `code/` 内任何文件、不改 developer 源码、不重命名既有 SPEC/WALKTHROUGH/DIFF/VERSION 文件（命名澄清一律在导航表里做映射）。文档内容必须与代码事实一致，标注依据（file:line / IMPL / PLAN），不得编造。

## 5. 交付与收尾

RESULT → management（`management/mailbox/inbox/MAIL-20261001-HHMM-maintainer--management-RESULT-doc-consolidation.md` + outbox 副本）；worklog 追加；git 提交（先 status + diff --cached 核对，按路径显式 add 自己的文件，禁 -A/.，不触碰他方未提交改动，commit 含 task_id）。
