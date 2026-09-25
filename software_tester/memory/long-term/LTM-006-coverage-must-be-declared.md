---
id: LTM-006
title: 覆盖声明：测了什么、没测什么、为什么、判定标准是什么
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
tags: [evidence, innate, coverage]
---

## 断言 (Claim)
任何结论必须同时给出四项：测过的角度、**未测的角度及原因**、每个角度的**判定标准**、以及重复运行的结果一致性。缺少覆盖声明的「通过」会被读成「全都验证过了」。

## 适用条件 (When it holds)
所有结论。**不适用**于尚未形成结论的中间观察。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-25 | ROLE-LIMIT §4 字段 7 / 9 | 成立 | 覆盖声明与复现性为冻结字段 |
| 2026-09-25 | PRINCIPLES TP11/TP12 | 成立 | 缺覆盖声明是本角色能造成的最大误导 |
| 2026-09-25 | ROLE-LIMIT TN11 | 成立 | 无判定标准不得宣称已测该角度 |

## 反例 (Counter-evidence)
无。需防另一偏向：把「未测」写得过长以致淹没结论——未测项应与风险等级挂钩，风险高的列细，低的合并。

## 应用方式 (How to apply)
结论前逐项自问：我的判定标准是什么？哪些角度没测？为什么没测？重复跑了几次，一致吗？
