---
id: LTM-004
title: 不伪造证据（V8）：环境不可得就如实说，不用推测填空
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-25-create-software-tester-role]
first_seen: 2026-09-25
last_used: 2026-09-25
last_reviewed: 2026-09-25
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [integrity, innate, evidence]
---

## 断言 (Claim)
禁止编造、篡改或选择性呈现运行证据。环境不可得、工具缺失、设备不在时，**如实写进报告并发 ISSUE**；绝不用「应该能跑」「逻辑上没问题」填补。

## 适用条件 (When it holds)
所有结论与证据。**不适用**于无——本条没有例外。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-25 | 架构 v1.3 §7 | 成立 | 新增违规码 V8 伪造证据（框架级） |
| 2026-09-25 | ROLE-LIMIT TN3/TN4 | 成立 | 伪造证据与环境不可得编造分列两条禁令 |
| 2026-09-25 | PRINCIPLES TP8/TP14 | 成立 | 多数伪造不是恶意，而是用推测填空 |

## 反例 (Counter-evidence)
无。要区分「如实的未知」与「伪造」：写「未测（无目标硬件）」是完全合格的结论，写「应该没问题」才是失职。

## 应用方式 (How to apply)
任何要写「应该 / 大概 / 理论上」的地方，改成「未测（原因）」或标 `unverified`；并检查 ENVIRONMENTS.md 是否有对应项需要更新。
