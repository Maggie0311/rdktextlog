---
id: LTM-004
title: 级别门槛是双向的：无场景不得定高，有场景不得定低
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-23-create-code-reviewer-role]
first_seen: 2026-09-23
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [severity, innate, calibration]
---

## 断言 (Claim)
给不出「输入/状态 X → 后果 Y」的具体场景，级别**不得高于 MINOR**；找不到条款依据，**不得高于 NIT**；范围外只能 `INFO`。反方向同样成立：能给出崩溃/数据损坏/功能错误的场景，就**不得**降级为 MINOR。

## 适用条件 (When it holds)
所有定级。**不适用**于 `unverified`（那是不确定状态，不是级别）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | SEVERITY.md §2 | 成立 | 门槛表为硬性条款 |
| 2026-09-23 | ROLE-LIMIT RN7 | 成立 | 风格偏好最多 NIT；无依据不得要求返工 |
| 2026-09-23 | PRINCIPLES RP6 | 成立 | 级别是要求他人返工的唯一凭据，虚高会透支可信度 |

## 反例 (Counter-evidence)
无。两个方向的失效都要防：门槛只用来防「虚高」时，就会变成「和稀泥式降级」——那也是瞒报（RN8）。

## 应用方式 (How to apply)
定级时按 SEVERITY §3 的三问顺序走一遍，并把复现场景写进发现项；写不出场景就降级，写得出来就别降。
