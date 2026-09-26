---
id: LTM-006
title: 解释必须可定位：给出 file:line，让人能自己核实
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
tags: [explanation, innate, verifiability]
---

## 断言 (Claim)
任何关于某功能在哪实现、某行为由谁触发的说明，必须给出 `file:line`；不可定位的说明不得作为结论写入说明书。

## 适用条件 (When it holds)
所有指向具体实现的说明。**不适用**于整体定位类描述（如这是一个串口采集程序）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | ROLE-LIMIT §4 字段 3 | 成立 | 关键函数须给 file:line |
| 2026-09-26 | PRINCIPLES KP7 | 成立 | 可定位的说明能被人自己核实 |
| 2026-09-26 | 人类用户诉求 | 成立 | 用户要据此审查代码与长期维护 |

## 反例 (Counter-evidence)
无。行号会随版本变化——因此**说明书必须与归档版本绑定**（说明书写在 `code_archive/<task_id>/` 内，版本号对应），不得跨版本复用。

## 应用方式 (How to apply)
每条涉及实现的说明后面附位置；找不到位置时，说明自己没读懂 → 走 LTM-004（标 unverified）。
