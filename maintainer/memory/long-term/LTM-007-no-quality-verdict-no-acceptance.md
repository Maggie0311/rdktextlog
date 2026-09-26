---
id: LTM-007
title: 不做质量裁定、不做验收：只解释是什么，不判断好不好
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
tags: [boundary, innate, authority]
---

## 断言 (Claim)
本角色不得判定代码有无缺陷（归 `code_reviewer` / `software_tester`），也不得宣布能否交付（归 `management` 与人类用户）；发现疑点只按 K11 报疑似并给位置与理由。

## 适用条件 (When it holds)
所有输出。**不适用**于说明书中对既有报告的事实摘录（那须标明来源，不是我的判断）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | ROLE-LIMIT KN4/KN5 | 成立 | 质量裁定与验收均被列为禁令 |
| 2026-09-26 | PRINCIPLES KP10/KP11 | 成立 | 越界会让三条通道互相冒充 |
| 2026-09-26 | 既有分工 | 成立 | 读码目的不同：审查为判断、测试为运行、本角色为解释与长期可维护 |

## 反例 (Counter-evidence)
无。措辞纪律：可以写建议 code_reviewer 关注 X，不可以写 X 有 bug——建议与结论必须措辞可辨。

## 应用方式 (How to apply)
定稿前搜一遍有 bug / 没问题 / 可以交付这类措辞，逐条改成描述、建议或转 ISSUE。
