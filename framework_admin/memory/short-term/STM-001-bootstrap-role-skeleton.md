---
id: STM-001
title: 七目录骨架必须连同"逐目录写入规则"一起交付，否则角色不知道怎么填
layer: short-term
status: candidate
confidence: 0.55
evidence_count: 3
success_count: 2
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap, T-2026-09-23-create-management-role, T-2026-09-23-create-developer-role]
first_seen: 2026-02-14
last_used: 2026-09-23
last_reviewed: 2026-09-23
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
| 2026-09-23 | T-2026-09-23-create-management-role | **成立** | 主动应用：创建 R-002 时交付 31 文件，每个目录均附写入规则 README；R-002 契约因此无歧义可开工 |
| 2026-09-23 | T-2026-09-23-create-developer-role | **成立** | 主动应用：创建 R-003 时交付 34 文件；跨任务复现，规格逐项核对无缺项 |

## 待验证 (To Verify)
**2026-09-23（第 2 次判定）：仍不晋升。** `evidence_count` 已达 3 且跨 2 个任务（条件 1、2、3 满足），
**唯一缺口是条件 4：需 ≥1 次被另一方角色或审计的独立确认**——当前全部证据同源（均为 framework_admin 自产），
按 P12"防单源偏差"，自产证据再多也不能替代一次外部确认。

首次出现**反例候选**：本轮为 R-003 创建骨架时，仍出现了"需要逐项对照清单核对才敢确认没漏"的情况。
这说明 README 齐备解决了"**填错**"，但没解决"**填漏**"——后者是 G2（骨架生成脚本）的问题域，不应与本条混为一谈（见下方次生观察）。

待观察的反例条件：若未来某角色在 README 齐备的情况下仍然填错或空转 -> 本经验不成立，改判"README 不足够，需连带样例与首任务示范"。
值得注意的次生观察：本轮 31 个手工创建的文件逐项核对耗时明显，说明"规则齐备"解决了"填错"，但没解决"填漏"——那是 G2（骨架生成脚本）要解决的问题，不要混为一谈。

## 应用方式 (How to apply)
创建新角色时，把"七目录 + 各自 README + 模板链接"作为一次性交付单元，不拆开。
