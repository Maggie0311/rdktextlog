---
id: LTM-007
title: 审查结论绑定 commit hash，代码一变结论即失效
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
tags: [process, innate, traceability]
---

## 断言 (Claim)
每份审查报告必须记录被审对象的 commit hash。报告出具后代码若发生变化，该报告**即行失效**，必须重新审查（可只审增量，但必须重新出结论并记录新 hash）。

## 适用条件 (When it holds)
所有审查报告。**不适用**于对未提交工作区的非正式讨论（那不构成审查结论，也不得被当作审查依据）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 架构 §4.1 第 6 条 | 成立 | 审查对象必须冻结 |
| 2026-09-23 | REVIEW-STANDARD §1/§3 | 成立 | 流程第 1 步固定 hash；复审只审增量但须重出结论 |
| 2026-09-23 | PRINCIPLES RP3 | 成立 | 没有 hash 的报告在争议时无法自证审的是哪一版 |

## 反例 (Counter-evidence)
无。实务上要小心「边审边改」：若发现 developer 在审查期间仍在提交，应停下并发 QUERY 要求冻结一个版本。

## 应用方式 (How to apply)
开工第一件事就是把 commit hash 抄进报告表头；复审时先核对 hash 是否变化，变化了就走增量复审流程。
