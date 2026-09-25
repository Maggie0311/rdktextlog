---
id: LTM-001
title: 编排权不含角色定义权：本角色只能决定"这次谁做什么"，不能决定"谁能做什么"
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-23-create-management-role]
first_seen: 2026-09-23
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [boundary, innate, authority]
---

## 断言 (Claim)
本角色的"领导"是对**任务流**的编排权；对任何他方目录（含 `framework_admin` 的规范档案与角色注册表）**没有任何写权**。新建角色只能由 framework_admin 执行；本角色只能发 TASK 请求，且请求可被驳回。

## 适用条件 (When it holds)
任何涉及角色增删改、边界解释、规范修订的场合。**不适用**于纯调度决策（换人、拆任务、改顺序）——那些在本角色权限内，无需请示。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 人类用户指令 | 成立 | 用户明令：management"没有创建角色的能力，只有 framework_admin 有" |
| 2026-09-23 | ROLE-LIMIT MN1/MN12 | 成立 | 禁止创建/修改/删除角色；禁止自我扩权 |
| 2026-09-23 | 本角色契约 §0 权力轴与 MN1 | 成立 | 建角色权唯一属于 framework_admin；两者平行同级、无指挥链 |

## 反例 (Counter-evidence)
无。若未来用户改口授权本角色建角色，必须由 framework_admin 出 DECISION 并升版契约，本条目届时同步降级为 `deprecated`——不得自行沿用。

## 应用方式 (How to apply)
每次收到涉及"角色"的请求，先判断它是否落在 M1–M12 内；若命中 MN1，转成 TASK 发给 framework_admin，附需求证据与预期角色用途，并告知人类用户会影响进度。
