---
id: LTM-006
title: 框架初始发布本身只算 1 个证据源，未经真实运行验证不得标高置信度
layer: long-term
status: active
confidence: 0.80
evidence_count: 2
success_count: 2
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap, _framework/03-MEMORY-MODEL §4.3]
first_seen: 2026-02-14
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.05
promoted_from: innate
tags: [memory, self-discipline, meta]
---

## 断言 (Claim)
由 framework_admin **一次性设计产出**的规范，其内部自洽性不构成多条独立证据。凡其结论依赖"未在真实角色运行中检验"的，置信度上限为 0.85，且在真实任务验证后方可上调。

## 适用条件 (When it holds)
规范/架构类产出，其正确性只能由**后续真实使用**证明，不能由"写得很顺"自证。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-14 | 记忆模型 §4.3 条件 2 | 成立 | 要求证据来自 ≥2 个不同任务 |
| 2026-02-14 | 本次自审 | 成立 | LTM-004 被主动压至 0.85 并留"待复核" |

## 反例 (Counter-evidence)
由用户直接下达的硬性需求（如"必须有七个目录"）不适用本上限，可直接 `confidence=1.00`。

## 应用方式 (How to apply)
每次给自己写长期记忆时，先问："这条结论有没有在任何一次真实任务里被事实验证过？" 没有 -> 封顶 0.85 并标记待复核。
