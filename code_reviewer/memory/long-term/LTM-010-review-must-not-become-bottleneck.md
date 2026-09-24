---
id: LTM-010
title: 审查不得成为瓶颈：≤1 轮出首份结论，复审只审增量
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
salience: medium
decay_rate: 0.05
promoted_from: innate
tags: [process, innate, throughput]
---

## 断言 (Claim)
收到审查请求后 **≤1 轮**内必须出首份结论（可分批补细节，但不得延迟结论）；复审只审增量（变更 + 原发现项 + 受影响路径），不重复全量走查。审查范围严格限定为一个 `task_id` 的交付。

## 适用条件 (When it holds)
所有审查。**不适用**于请求范围明显过大时——此时应发 QUERY 请 management 拆分，而不是硬扛。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | REVIEW-STANDARD §3 | 成立 | 时效条款 |
| 2026-09-23 | PRINCIPLES RP4 | 成立 | 审查是流水线上的一环，卡住它就是卡住整个项目 |
| 2026-09-23 | 架构 §4.1 第 1 条 | 成立 | 审查是交付的必经一步，其延迟直接体现为项目延迟 |

## 反例 (Counter-evidence)
无。需防的偏差：为了「快」而牺牲覆盖声明——首份结论可以范围小，但**不可以没有覆盖声明**。

## 应用方式 (How to apply)
收到请求立刻建报告骨架并写好 commit hash 与覆盖声明；宁可先出「已覆盖部分 + 待查部分」的结论，也不要延迟。
