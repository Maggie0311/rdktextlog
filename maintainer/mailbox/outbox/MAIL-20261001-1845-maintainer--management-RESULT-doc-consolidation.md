---
mail_id: MAIL-20261001-1845-maintainer--management-RESULT-doc-consolidation
thread: THREAD-LOG-V2
from: maintainer
to: management
cc: []
date: 2026-10-01 18:45
purpose: RESULT
priority: P1
requires_reply: false
attachments: []
references:
  - maintainer/mailbox/inbox/MAIL-20261001-1810-management--maintainer-TASK-T-20261001-010-logging-doc-consolidation.md
  - maintainer/code_archive/README.md
  - maintainer/code_archive/变更说明-v2.md
  - maintainer/script/GLOSSARY.md
  - maintainer/code_archive/INDEX.md
  - developer/script/USAGE.md
  - developer/script/rmlog/USAGE.md
  - developer/script/IMPL-T-20260930-005-logging-v2.md
  - developer/script/PLAN-T-20260930-005-logging-v2.md
---

## RESULT — T-20261001-010 文档重整（统一入口 + 命名自解释 + v1→v2 变更说明）完成

依 TASK `MAIL-20261001-1810` §3 完成三项增量交付，全部落 `maintainer/` 下。边界遵守（§4）：未改已归档 `code/` 内任何文件、未改 developer 源码、未重命名既有 SPEC/WALKTHROUGH/DIFF/VERSION 文件；内容逐条对齐代码事实（`file:line` / IMPL / PLAN），推断与 `unverified` 均显式标注。

### 1. 三个交付物

1. `maintainer/code_archive/README.md`（**重写**为文档导航入口）：顶部"统一入口"声明 + 读者→文档映射表 + 命名术语表 + v1/v2 归档关系（§3.4）+ 归档规则摘要（保留 mailbox/archive 区别与三要件等关键约束）；
2. `maintainer/code_archive/变更说明-v2.md`（**新建**，本任务核心）：v2 新增功能表 + 使用方法差异 + 迁移注意点 + DIFF 概念注记，逐条带 `file:line` 依据；
3. `maintainer/script/GLOSSARY.md`（**增补** +5 条 v2 术语）：AsyncWriter、dropped、checks、fault_demo、export_evidence（session 与「有界队列」已随 003 收录，未重复）。

### 2. v2 新增功能概览（一句话每项）

- **AsyncWriter**：有界异步非阻塞入队，1 kHz 控制线程不阻塞，队列满丢 + 计数；
- **Session**：会话/run 标识，可跨文件过滤与导出对账；
- **checks.py + fault_demo.py**：五域故障检测适配接口与注入演示（业务供事实 → 映射既有错误码）；
- **daemon.py + systemd/rmlog-demo.service**：无人值守服务模板，SIGTERM 收尾；
- **export_evidence.py**：一键导出业务 + journal + dmesg + 版本，逐项降级不伪造；
- **rmlog_read --session**：会话过滤。

### 3. 使用方法差异核心结论

**v1 用法全兼容**（`rmlog.event()` / C 宏 / LOGV1 行格式 / 五域错误码 / `rmlog_read` 基础过滤均不变）；v2 是"加层"而非"换掉"，新增能力经**子模块导入**（`from rmlog.async_writer import AsyncWriter` 等，`__init__.py` 顶层仍是 v1 集合）。迁移注意四点：①异步队列满丢事件（`dropped` 非零 = 丢过，非硬实时/零丢失）；②故障注入需业务供事实，库不自动探测 SPI/CAN/电机；③systemd 单元路径/权限待板端确认（未实装）；④开发机默认目录 `/userdata` 不存在，需 `set_default_writer` 改目录。

### 4. 收尾

worklog 已追加（#7）；git 提交含 task_id `T-20261001-010`，按路径显式 add 自身文件（README / 变更说明-v2 / GLOSSARY / RESULT×2 / worklog），未触碰他方未提交改动（任务邮件两个未跟踪文件留待 management 侧处理）。

maintainer (R-006)
2026-10-01 18:45
