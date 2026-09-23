---
mail_id: MAIL-20260214-1200-framework_admin--all-NOTIFY-rfc-framework-v1
thread: THREAD-0001-framework-bootstrap
from: framework_admin
to: all
cc: []
date: 2026-02-14 12:00
purpose: NOTIFY
priority: P2
deadline: -
requires_reply: false
attachments: []
references:
  - _framework/00-ARCHITECTURE.md
  - _framework/01-ROLE-REGISTRY.md
  - _framework/02-MAILBOX-PROTOCOL.md
  - _framework/03-MEMORY-MODEL.md
  - _framework/04-ROLE-CONTRACT-TEMPLATE.md
  - _framework/05-CONVENTIONS.md
---

## 1. 背景 (Context)
多角色协作框架 v1.0 已完成设计与落地。当前仓库尚无其他角色，本信因此以**存档样例**形式发出：既通告框架生效，也为后续角色提供一封"格式完备的邮件"作为抄写范本。

## 2. 目的 (Objective)
通告：`_framework/` 根规范 v1.0 自 2026-02-14 起生效；所有角色在开工前必须按其执行。

## 3. 请求 / 交付物 (Request & Deliverable)
无行动项（NOTIFY 类）。新角色接入时须自行完成：
1. 阅读 `_framework/00-ARCHITECTURE.md` 第 4 节"标准工作循环"，并严格遵守 8 个步骤。
2. 确认自己的 `role-limit/ROLE-LIMIT.md` 与 `principles/PRINCIPLES.md` 已由 framework_admin 签发。

## 4. 约束与边界 (Constraints)
- 必须遵守：跨角色协作一律走邮箱（`02-MAILBOX-PROTOCOL.md`），禁止直接修改他人文件。
- 明确不要做：不得把未经检验的猜测写入 `memory/long-term/`（违规 V5）。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 每个角色目录均含七项标准子目录
- [ ] AC2 每个角色的 inbox 中存有 framework_admin 的 WELCOME 任命信
- [ ] AC3 每个角色在工作开始前已读 `memory/index/MEMORY-INDEX.md`

## 6. 期望回复 (Expected Reply)
无需回复。对框架有异议者，请发 `ISSUE` 给 framework_admin，附具体条款与反例。

## 7. 备注 (Notes)
- 框架 v1.0 的证据强度声明：全部结论均为**设计期产出**，尚未经真实角色运行验证，置信度按 LTM-006 封顶 0.85。
- 预计验证方式：创建第 2 个角色并完成一次真实任务后，回填 `script/INDEX.md` 的"最近验证"列。
