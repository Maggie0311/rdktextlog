---
id: LTM-005
title: 记忆分层是状态而非等级：短期是候选，长期是已验证信念，未验证经验不得入长期
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap, _framework/03-MEMORY-MODEL, _framework/00-ARCHITECTURE]
first_seen: 2026-02-14
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [memory, innate, anti-pollution]
---

## 断言 (Claim)
长期与短期记忆不是"重要/不重要"的等级，而是**验证状态**：短期=候选经验，长期=通过置信度与多源证据检验后的信念。未经验证的经验进入长期即构成记忆污染（违规 V5）。

## 适用条件 (When it holds)
任何需要跨任务复用经验的角色。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-14 | 记忆模型 §1 | 成立 | 明确"两者不是等级，而是状态" |
| 2026-02-14 | 晋升规则 §4.3 | 成立 | 5 条同时满足才可晋升 |
| 2026-02-14 | 违规项 V5 | 成立 | 记忆污染单列 |

## 反例 (Counter-evidence)
来自 `_framework/` 根规范或 role-limit 的强制约束可 `confidence=1.00` 直接入长期——这是"本能"而非"经验"，不违反本断言。

## 应用方式 (How to apply)
任何写入 `long-term/` 的动作前，逐条核对 §4.3 的 5 个条件；缺一即拒绝晋升，改留短时记忆。
