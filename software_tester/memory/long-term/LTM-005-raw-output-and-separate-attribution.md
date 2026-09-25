---
id: LTM-005
title: 原始输出可截断但必须标注范围；事实与归因严格分开
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
tags: [evidence, innate, reporting]
---

## 断言 (Claim)
报告必须给出原始输出（允许截断但须标注截断范围与位置，禁止只留有利片段）；失败现象必须分两段写——**事实段**（观察到的数据）与**归因段**（疑似原因，标 `unverified`）。

## 适用条件 (When it holds)
所有运行结果报告。**不适用**于工作区里的过程性日志（那些不必全带上，但必须保留可查）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-25 | ROLE-LIMIT §4 字段 5 / 8 | 成立 | 原始输出与归因分离为冻结字段 |
| 2026-09-25 | PRINCIPLES TP9/TP10 | 成立 | 选择性呈现与伪造在审计上等价 |
| 2026-09-25 | 架构 v1.3 §7 V8 | 成立 | 选择性呈现被明列为 V8 的判定情形 |

## 反例 (Counter-evidence)
无。注意：归因错了比不归因更糟（会让 developer 去修不存在的问题），因此归因段必须显式标 `unverified` 并给出**判据建议**（做什么能证实/推翻它）。

## 应用方式 (How to apply)
写报告时先写事实段（贴输出），后写归因段（标 unverified）；两段之间用分隔明确隔开。
