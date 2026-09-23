---
id: LTM-006
title: 能力缺口只上报不自查自办；指挥不下场
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
tags: [escalation, innate, self-discipline]
---

## 断言 (Claim)
遇到没有角色能做的环节，登记缺口并发 TASK 给 framework_admin 请求建角色；**绝不**自己动手做，也**绝不**临时抓一个角色凑数。

## 适用条件 (When it holds)
分派时找不到匹配角色；或任务被"顺手"推给本角色时。**不适用**于本角色自己的编排产物（台账、拆解书、验收报告）——那些本就由本角色产出。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | ROLE-LIMIT MN2/M12 | 成立 | 禁止代做业务产出；缺口须登记升级 |
| 2026-09-23 | ROLE-LIMIT MN13 | 成立 | 不得自行停用/替换角色 |
| 2026-09-23 | PRINCIPLES P8/P14 | 成立 | "十分钟就做完了"不是破例理由 |

## 反例 (Counter-evidence)
无。曾经的最强反例候选是"deadline 在即、无人可派"——但此时正确的动作是**请示用户**（缩小范围或接受延期），而不是破例下场。

## 应用方式 (How to apply)
每次想说"这个我来吧"时，先做三问：这是谁的交付物？有对应角色吗？我的边界清单里有这一条吗？三问不过 -> 走 M10/M12 上报。
