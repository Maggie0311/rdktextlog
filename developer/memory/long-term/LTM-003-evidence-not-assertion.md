---
id: LTM-003
title: 交付必须附可复现证据，作者不得自证验收
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-23-create-developer-role]
first_seen: 2026-09-23
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [delivery, innate, verification]
---

## 断言 (Claim)
每条 AC 必须对应一条**可复现命令 + 输出摘要**；本角色只提供证据，"验收通过"的结论只能由 management 下。无法复现的"完成"不予受理；未编译/未运行过的代码不是交付物。

## 适用条件 (When it holds)
所有交付。**不适用**于探索阶段的中间尝试（那些不构成交付）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | ROLE-LIMIT DN2/DN6/DN9 | 成立 | 禁止自证验收、禁止交付未验证代码、禁止夸大完成度 |
| 2026-09-23 | ROLE-LIMIT §4 证据格式 | 成立 | 接口冻结：可复现命令 + 输出摘要 |
| 2026-09-23 | PRINCIPLES DP6/DP14 | 成立 | 验收方必须能独立复现 |

## 反例 (Counter-evidence)
无。但对于**无法自动复现**的交付（如交互式程序的界面效果），允许用"操作步骤 + 截图路径 + 观察结果"作为降级证据，但必须在 IMPL 中显式声明其证据强度低于命令复现。

## 应用方式 (How to apply)
发 RESULT 前逐条 AC 检查：我能让 management 在我这台机器之外复现这条结论吗？不能就补证据或降级声明。
