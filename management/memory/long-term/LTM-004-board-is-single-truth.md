---
id: LTM-004
title: 进度唯一真相源是 PROJECT-BOARD，口头进度与记忆中的进度都不算数
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-23-create-management-role]
first_seen: 2026-09-23
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [progress, innate, auditability]
---

## 断言 (Claim)
项目进度的唯一权威记录是 `script/PROJECT-BOARD.md`；任何状态变更必须带**证据路径或邮件 ID**。没有证据的状态更新一律不接受。

## 适用条件 (When it holds)
任何进度判断、汇报、验收前置。**不适用**于角色内部的工作进度（那是它自己 worklog 的职责）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | ROLE-LIMIT M4/§4 | 成立 | 台账为唯一真相源，字段冻结 |
| 2026-09-23 | PRINCIPLES P5/P9 | 成立 | 只认可带证据路径的状态 |
| 2026-09-23 | ROLE-LIMIT §6 DoD | 成立 | 台账须与真实邮件流一致 |

## 反例 (Counter-evidence)
尚无真实运行验证（本角色未开工）。需警惕：台账本身可能变成"自我安慰的文档"——若台账状态与 outbox 邮件流不一致，以邮件流为准并立即修正台账。

## 应用方式 (How to apply)
每次收到"已完成"的说法，先要证据路径；拿到后再更新台账。汇报人类用户前，先核对台账与邮件流是否一致。
