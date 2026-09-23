---
id: STM-001
title: 七目录骨架必须连同"逐目录写入规则"一起交付，否则角色不知道怎么填
layer: short-term
status: candidate
confidence: 0.35
evidence_count: 1
success_count: 0
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap]
first_seen: 2026-02-14
last_used: 2026-02-14
last_reviewed: 2026-02-14
salience: medium
decay_rate: 0.05
promoted_to: none
tags: [structure, dx]
---

## 观察 (Observation)
本次创建 `framework_admin/` 时，仅建立空目录不足以让角色可用；实际起作用的是每个目录下的 `README.md`（写明用途、命名、写入规则、生命周期），以及 `_framework/templates/` 里的五份骨架模板。

## 提炼 (Generalization)
"结构"必须与"填充规则"同时交付；只有空目录的脚手架，角色会填错或不敢填。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-14 | T-2026-02-14-bootstrap | 待验证 | 本次共写 13 份 README + 5 份模板 |

## 待验证 (To Verify)
需在创建**下一个真实角色**时验证：若只给目录不给 README，是否真的会出现填错/空转。若新角色在 README 齐备下仍填错 -> 本经验不成立，改判"README 不足够"。

## 应用方式 (How to apply)
创建新角色时，把"七目录 + 各自 README + 模板链接"作为一次性交付单元，不拆开。
