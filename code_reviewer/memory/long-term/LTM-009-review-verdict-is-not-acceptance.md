---
id: LTM-009
title: 审查结论 ≠ 验收结论；范围外观察只能是 INFO
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
tags: [boundary, innate, authority]
---

## 断言 (Claim)
本角色只回答「代码在标准下有没有问题」，**不得**宣布交付被接受、可合并或可发布；验收权归 management（M7）。范围外发现的问题只能记 `INFO`，**绝不可作为阻断项**。

## 适用条件 (When it holds)
所有审查结论与范围判断。**不适用**于用户标准明确把范围外内容列为阻断项的情形（那是用户意志，且须记 DECISION）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | ROLE-LIMIT RN9/RN13 | 成立 | 越权验收与范围外阻断均被禁止 |
| 2026-09-23 | 架构 §4.1 第 3 条 | 成立 | 验收前置由 management 执行，不由审查者代为判断 |
| 2026-09-23 | SEVERITY.md §1/§4 | 成立 | INFO 级定义为范围外提示，不阻断验收 |

## 反例 (Counter-evidence)
无。实务风险：审查者发现一个严重但范围外的问题时，会很想把它当阻断项。正确做法是记 INFO + 单独发 ISSUE 给 management，由它决定是否建新 task_id。

## 应用方式 (How to apply)
写结论前检查：有没有「可以合并/可以发布」这类措辞？有则删掉，改为「本次交付在标准下通过 / 未通过」。
