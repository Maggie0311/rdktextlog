---
id: LTM-003
title: 发现项必须五要素齐全，缺一即无效
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
tags: [evidence, innate, anti-false-positive]
---

## 断言 (Claim)
每条发现项必须含：位置（`file:line`）/ 现象 / **复现路径或推演链** / **依据条款** / 严重级别 + 建议。缺任何一项，该条**不得进入结论**；developer 也可据此直接拒绝该条。

## 适用条件 (When it holds)
所有发现项。**不适用**于 `INFO` 级范围外提示（可只写位置与现象）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 用户 2026-09-23 指令 | 成立 | 要求「不会误报」「不会过度要求本不存在的错误」 |
| 2026-09-23 | ROLE-LIMIT RN6 / §4 | 成立 | 五要素缺一即无效 |
| 2026-09-23 | REVIEW-STANDARD §4 | 成立 | 五要素同时是 developer 的申诉依据 |

## 反例 (Counter-evidence)
无。需注意「依据条款」一栏的诚实性：找不到条款时不能编一条凑数，应按 SEVERITY 门槛降为 NIT 或不写。

## 应用方式 (How to apply)
每条草稿先补五要素；补不齐就问自己：这是发现，还是印象？
