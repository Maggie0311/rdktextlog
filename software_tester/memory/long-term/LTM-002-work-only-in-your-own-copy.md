---
id: LTM-002
title: 只在自身工作区的副本里构建与运行
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
tags: [boundary, innate, workspace]
---

## 断言 (Claim)
一切构建、运行、烧录产出的中间物都发生在 `software_tester/script/work/<task_id>/` 的**副本**中；绝不在他方目录内构建或留下产物。

## 适用条件 (When it holds)
所有涉及构建或运行的场合。**不适用**于只读地查看源码（那是允许且必要的）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-25 | 架构 v1.2 §2.1 | 成立 | 不存在公共工作空间；每块区域有且仅有一个写入者 |
| 2026-09-25 | ROLE-LIMIT TN9 | 成立 | 禁止在原地构建 |
| 2026-09-25 | ROLE-LIMIT T2 | 成立 | 副本工作区是本角色的标准动作 |

## 反例 (Counter-evidence)
无。代价是需要在报告中记录副本来源（commit hash），这是必要成本而非冗余。

## 应用方式 (How to apply)
接到任务先建工作区目录并把被测 commit 的副本放进去；报告 §1 写清副本来源与路径。
