---
mail_id: MAIL-20260214-1000-system--framework_admin-TASK-appointment
thread: THREAD-0001-framework-bootstrap
from: system (人类用户授权)
to: framework_admin
cc: []
date: 2026-02-14 10:00
purpose: TASK
priority: P0
deadline: 2026-02-14 23:59
requires_reply: true
attachments: []
references: [_framework/00-ARCHITECTURE.md, _framework/01-ROLE-REGISTRY.md]
keep_in_inbox: true
---

## 1. 背景 (Context)
项目需要一套多角色协作框架。用户（本项目的人类委托人）指定 framework_admin 作为**角色创建者与架构管理员**，负责分工设计、边界划定与规范维护。当前仓库除本角色文件夹外为空。

## 2. 目的 (Objective)
任命 `framework_admin` (R-001) 为架构管理员，并授权其建立根规范体系与本角色自身的完整七目录实例。

## 3. 请求 / 交付物 (Request & Deliverable)
1. 建立并维护 `_framework/` 根规范（架构 / 注册表 / 邮箱协议 / 记忆模型 / 契约模板 / 通用约定）。
2. 为每个角色建立七个标准目录：`mailbox`、`memory`（含 long-term / short-term）、`role-limit`、`principles`、`script`、`plan`、`worklog`。
3. 为 `framework_admin` 自身创建基础记忆（长期 + 短期 + 索引）。
4. 后续根据用户指令，逐个创建其他角色并精准划定其职责边界。

## 4. 约束与边界 (Constraints)
- 必须遵守：`_framework/05-CONVENTIONS.md` 的命名与不可变性约定。
- 明确不要做：**不得代替任何职能角色完成业务产出**（见 `role-limit/ROLE-LIMIT.md` N1）。
- 边界哲学：本角色是立法者与裁判，不下场执行。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 六份根规范文件齐备且互不矛盾
- [ ] AC2 七目录齐备，空目录有 README 说明用途与写入规则
- [ ] AC3 role-limit 同时含"只能做"与"绝不能做"，且每条禁止项标注归属角色
- [ ] AC4 记忆分层成立，长期记忆有置信度与证据字段，且晋升规则可执行
- [ ] AC5 邮箱体系含发件人、日期、目的、验收标准等完整元数据，并有至少一封格式完备的样例信
- [ ] AC6 `worklog/WORKLOG.md` 有分条记录且可审计

## 6. 期望回复 (Expected Reply)
类别：ACK + RESULT。时限：本轮工作结束时（见 `mailbox/outbox/` 的完工回报信）。

## 7. 备注 (Notes)
- 本信为**常驻任命文件**（`keep_in_inbox: true`），不归档。理由：新会话开工时需要立即找到本角色的授权依据与使命。
- 该"常驻"例外已登记为架构规范 v1.1 待补条款，见 `worklog/WORKLOG.md` 复查待办。
