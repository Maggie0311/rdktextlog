---
id: LTM-004
title: 被下游依赖的接口即契约，变更须先 NOTIFY 并给兼容期
layer: long-term
status: active
confidence: 0.85
evidence_count: 2
success_count: 2
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap, _framework/04-ROLE-CONTRACT-TEMPLATE]
first_seen: 2026-02-14
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: medium
decay_rate: 0.05
promoted_from: innate
tags: [interface, process, innate]
---

## 断言 (Claim)
一旦某输出被下游消费，其字段/路径/格式即成为契约：变更前必须发 NOTIFY、给兼容期、升版本；禁止静默变更。

## 适用条件 (When it holds)
存在 ≥1 个下游消费者时。无消费者的内部文件可自由改。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-14 | 契约模板 §4 接口冻结 | 成立 | 模板内建该条款 |
| 2026-02-14 | 本角色输出契约 | 成立 | `_framework/` 字段变更需 NOTIFY |

## 反例 (Counter-evidence)
证据数仅 2 条且均来自同一轮设计工作，尚未经真实协作验证。**待一次真实接口变更任务后复核，方可升至 0.95。**

（2026-09-23 复核记录，T-2026-09-23-create-management-role：本轮为 R-002 定义了 `task_id` 格式与台账字段并声明"出生即冻结"，
属**预防性应用**，**不是**一次真实的接口变更处理，故**不新增证据、不上调置信度**，维持 0.85 待复核。依据 LTM-006。）

## 应用方式 (How to apply)
定义任何输出契约时，同时写明：谁消费、变更通知对象、兼容期长度。
