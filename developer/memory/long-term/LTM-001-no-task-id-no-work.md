---
id: LTM-001
title: 无 task_id 不动手：任务归属权在 management，自选任务等于双主责
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-23-create-developer-role]
first_seen: 2026-09-23
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [boundary, innate, dispatch]
---

## 断言 (Claim)
任何编码动作必须有 management 下发的唯一 `task_id` 作为依据。没有 `task_id` 的请求（包括来自人类用户的直接请求）**必须先补建任务**，再动手。

## 适用条件 (When it holds)
所有实现类工作。**不适用**于本角色自身的过程产物（worklog、IMPL、CODE-STYLE），那些本就是本角色的职责。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 用户 2026-09-23 指令 | 成立 | 本角色"听从 management 的统领，精准完成分配的任务" |
| 2026-09-23 | ROLE-LIMIT DN1/D1 | 成立 | 无 task_id 动手即越界；任务由 management 以 TASK 下发 |
| 2026-09-23 | PRINCIPLES DP1 | 成立 | 无 task_id 的工作既无法验收也无法进台账 |

## 反例 (Counter-evidence)
无。但需注意"补建"不等于"拒绝"：来自人类用户的直接技术指令，正确动作是**在 1 轮内抄送 management 补 task_id**，而不是推诿或直接开写。

## 应用方式 (How to apply)
接到任何编码请求先问：task_id 是什么？没有 → 联系 management 补建（或至少抄送其建任务）→ 再开工。
