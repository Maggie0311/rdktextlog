---
id: LTM-009
title: 墓碑也是资产：未采用或被否决的版本必须留记录，且不可删除
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
salience: medium
decay_rate: 0.05
promoted_from: innate
tags: [archive, innate, history]
---

## 断言 (Claim)
被否决或未采用的版本，在 `code_archive/_tombstones/` 留一条墓碑记录（版本、原因、当时依据）；**任何版本记录与墓碑都不得删除**。

## 适用条件 (When it holds)
出现未采用版本时；以及任何清理旧文件的冲动出现时。**不适用**于本角色自己的草稿。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | 人类用户 2026-09-26 指令 | 成立 | 要求满足长期维护需求、维护更改脉络 |
| 2026-09-26 | ROLE-LIMIT K7/KN9 | 成立 | 墓碑不删 |
| 2026-09-26 | PRINCIPLES KP4 | 成立 | 为什么没采用与采用了什么同样重要 |

## 反例 (Counter-evidence)
无。代价是目录会变大——但墓碑记录只是**文本**，不是产物副本，体积可控。

## 应用方式 (How to apply)
每次有版本被否决，立即补墓碑；定期检查 `_tombstones/` 与 `INDEX.md` 是否一致。
