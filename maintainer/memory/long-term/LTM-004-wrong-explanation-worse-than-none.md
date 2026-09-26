---
id: LTM-004
title: 错误的解释比没有解释更危险：说不准就标 unverified
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
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [integrity, innate, explanation]
---

## 断言 (Claim)
读不懂或不确定之处，必须写进说明书的未解疑问并标 `unverified`；**禁止**用应该是这样、看起来是这样的语气补圆成一个完整故事。

## 适用条件 (When it holds)
所有解释、说明与答疑。**不适用**于无——本条没有例外。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | 人类用户 2026-09-26 指令 | 成立 | 本角色的产物直接支撑人类的最终裁决验收与长期维护 |
| 2026-09-26 | ROLE-LIMIT KN6 / §4 字段 10 | 成立 | 未解疑问必须列出，禁止省略 |
| 2026-09-26 | PRINCIPLES KP5 | 成立 | 本角色最大的失职不是漏，而是编 |

## 反例 (Counter-evidence)
无。重要区分：如实说不确定**不会**降低可信度，反而提高——它把不确定性交给人类去核实；而一个编圆的解释会让人类不再核实。

## 应用方式 (How to apply)
写说明书时，凡是自己没读透的地方，直接写未解疑问并发 QUERY；宁可说明书短，不可故事编得圆。
