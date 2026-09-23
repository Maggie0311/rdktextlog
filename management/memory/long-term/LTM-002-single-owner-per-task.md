---
id: LTM-002
title: 每个 task_id 有且仅有一个主责角色，禁止双主责
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
tags: [dispatch, innate, boundary]
---

## 断言 (Claim)
任何 `task_id` 必须映射到**唯一**主责角色；跨角色工作必须拆成多个各自主责的子任务并用显式依赖串联，禁止"两人共同负责"。

## 适用条件 (When it holds)
存在 ≥2 个角色的任何分派场合。**不适用**于同一角色内部的自组织（那是该角色自己的事）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | ROLE-LIMIT MN5 | 成立 | 禁止把同一动作派给两个角色 |
| 2026-09-23 | ROLE-LIMIT §6 DoD | 成立 | 每个 task_id 的唯一主责是验收前置条件 |
| 2026-09-23 | PRINCIPLES P2 | 成立 | "共同负责"在实践中等于"没人负责" |

## 反例 (Counter-evidence)
无。但需区分"主责"与"可建议"：非主责角色可以提供意见，**不得**产出交付物，也不得据此计入其工作量。

## 应用方式 (How to apply)
分派前逐条检查：这个 task_id 的主责是谁？该动作是否落在它的"只能做"清单里？两个问题都答得出，才发 TASK。
