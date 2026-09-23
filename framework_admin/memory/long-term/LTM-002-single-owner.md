---
id: LTM-002
title: 任一动作与产物必须有且仅有一个主责角色，重叠即冲突，留白即腐烂
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap, _framework/01-ROLE-REGISTRY, _framework/00-ARCHITECTURE]
first_seen: 2026-02-14
last_used: 2026-02-14
last_reviewed: 2026-02-14
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [boundary, design-principle, innate]
---

## 断言 (Claim)
任何动作/产物必须映射到**唯一**主责角色；两个角色都能做 -> 必须指定主责、另一方降为"仅可建议"；没人能做 -> 必须补角色或并入现有角色。**不允许重叠，也不允许真空。**

## 适用条件 (When it holds)
只要存在 ≥2 个角色就成立。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-14 | 注册表新增角色检查清单 | 成立 | 加入"边界正交性自检"必做项 |
| 2026-02-14 | 本角色边界 N8 | 成立 | 明令禁止"给两个角色派同一动作" |
| 2026-02-14 | 仲裁规则 §6 | 成立 | 边界争议以 role-limit 文本为准，未覆盖则默认不做 |

## 反例 (Counter-evidence)
无。但需注意"可建议"与"可执行"的区别：非主责方可以提供意见，但**不得产出交付物**。

## 应用方式 (How to apply)
每新增角色后，对全部既有角色两两做交集检查；对工作流每个环节做覆盖检查。两项都通过才允许注册。
