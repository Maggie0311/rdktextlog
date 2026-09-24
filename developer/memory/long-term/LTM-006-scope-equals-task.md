---
id: LTM-006
title: 改动范围必须等于任务范围，禁止静默扩张
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
salience: medium
decay_rate: 0.05
promoted_from: innate
tags: [scope, innate, discipline]
---

## 断言 (Claim)
任务途中发现的任何其他问题（既有缺陷、可优化点、风格不一致），只**记录并发 ISSUE**，不得顺手修改。改动范围与任务范围不一致时，验收方无法判断风险，回退也会连带丢掉无关改动。

## 适用条件 (When it holds)
所有实现类任务。例外：若不改动会导致本任务无法完成（如依赖的既有函数有致命 bug），必须先发 ISSUE 取得新的 `task_id` 再改。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | ROLE-LIMIT DN5 | 成立 | 静默扩张 = 交付了未约定的东西 |
| 2026-09-23 | PRINCIPLES DP2 | 成立 | 发现项写入 IMPL，不顺手改 |
| 2026-09-23 | ROLE-LIMIT §6 DoD | 成立 | 改动范围 = 任务范围是完成判定的硬项 |

## 反例 (Counter-evidence)
无。但要区分"扩张"与"必要的技术前置"：为完成本任务而必须的最小改动属于任务范围，判断标准是"不做它，本任务的 AC 能否达成"。

## 应用方式 (How to apply)
交付前跑一遍 `git diff --stat`，逐个文件自问：这个文件为什么出现在这次改动里？答不上来的就撤出。
