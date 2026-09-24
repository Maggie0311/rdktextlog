---
id: LTM-005
title: 风格必须一致且可被检查，以 CODE-STYLE.md 为准
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
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [quality, innate, interface]
---

## 断言 (Claim)
同一项目内不得混用多种代码风格；风格基线写在本角色维护的 `developer/script/CODE-STYLE.md`，且该文件被 management 用作验收依据之一（一经引用即成为契约，变更须先 NOTIFY 并给兼容期）。

## 适用条件 (When it holds)
所有源码。**不适用**于第三方库与生成代码（那些遵循其自身风格）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 用户 2026-09-23 指令 | 成立 | "代码风格规范"是用户硬需求 |
| 2026-09-23 | ROLE-LIMIT D3/§4 | 成立 | 风格内容由本角色定；CODE-STYLE.md 被引用后冻结 |
| 2026-09-23 | PRINCIPLES DP8 | 成立 | 风格的价值在于一致性，不在于完美 |

## 反例 (Counter-evidence)
无。注意边界：**规定"必须有且一致"是 framework_admin 的职责，规定"具体用什么风格"是本角色的专业职责**（ROLE-LIMIT §0 权力轴）；不要把后者的决定权上交。

## 应用方式 (How to apply)
写代码前先看 CODE-STYLE.md；若项目尚无该文件，先建它（可先给最小可用版本），再写第一行代码。
