---
id: LTM-010
title: code_archive 归档代码产物，mailbox/archive 归档邮件——两者不得混用
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-26-create-maintainer-role]
first_seen: 2026-09-26
last_used: 2026-09-26
last_reviewed: 2026-09-26
salience: medium
decay_rate: 0.05
promoted_from: innate
tags: [archive, innate, discipline]
---

## 断言 (Claim)
`code_archive/<task_id>/`（按版本组织）只放代码产物与其说明书；`mailbox/archive/YYYY-MM/`（按时间组织）只放邮件。两者不得互相存放。

## 适用条件 (When it holds)
所有归档动作。**不适用**于两处各自的 README。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | 人类用户 2026-09-26 指令 | 成立 | 明确要求注意和 mailbox 的 archive 区分开 |
| 2026-09-26 | ROLE-LIMIT KN10 | 成立 | 混放会让两类检索同时失效 |
| 2026-09-26 | PRINCIPLES KP13 | 成立 | 检索维度不同（时间 vs 版本） |

## 反例 (Counter-evidence)
无。若某封邮件对归档有决定性作用（例如两方确认通知），正确做法是在**版本卡里引用其 mail_id**，而不是把邮件复制进 code_archive。

## 应用方式 (How to apply)
归档前确认目标目录：`code_archive/` 收代码，`mailbox/archive/` 收邮件；引用关系用路径与 mail_id 表达。
