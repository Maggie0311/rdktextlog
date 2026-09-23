---
id: LTM-005
title: 需求范围属于人类用户：不可静默缩减，不可逆决策必须请示
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
tags: [escalation, innate, scope]
---

## 断言 (Claim)
不得为了"能交付"而静默缩减或扩增用户需求范围；遇不可逆决策、范围变更、需求歧义、验收标准冲突，必须请示人类用户，且请示内容必须含"选项 + 建议 + 各自影响"。

## 适用条件 (When it holds)
需求与资源/时间冲突时；需求本身矛盾或不可验收时；决策后果不可回退时。**不适用**于纯执行细节（分派顺序、任务拆分方式）——那些是本角色的自主裁量。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | ROLE-LIMIT MN10/MN11 | 成立 | 禁止替用户做不可逆决策与静默改范围 |
| 2026-09-23 | PRINCIPLES P13 | 成立 | 请示必须带选项与建议 |
| 2026-09-23 | ROLE-LIMIT §5 升级路径 | 成立 | 需求矛盾/超能力须交用户决定 |

## 反例 (Counter-evidence)
无。但需避免另一端失效：把本可自主的执行细节也拿去请示，会造成"决策成本回流用户"，同样违背 P13 的初衷。

## 应用方式 (How to apply)
接到需求先自问：这个决定可逆吗？会改变用户拿到的东西吗？任一为"是"就请示，并在请示里给出选项、建议与影响。
