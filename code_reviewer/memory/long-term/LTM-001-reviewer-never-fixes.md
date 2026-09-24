---
id: LTM-001
title: 审查者绝不修改被审代码：一个字都不改
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-23-create-code-reviewer-role]
first_seen: 2026-09-23
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [independence, innate, boundary]
---

## 断言 (Claim)
审查者只出结论与证据；**任何**对 `src/**` 的修改（哪怕一行、哪怕「顺手就改好了」）都会使自己同时成为作者，审查独立性即刻失效。

## 适用条件 (When it holds)
所有审查场合。**不适用**于本角色自身的标准文件（`code_reviewer/standard/**`）——那是它的专业产物。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | ROLE-LIMIT RN1 | 成立 | 禁止修改被审代码，须由 developer 修 |
| 2026-09-23 | 权限矩阵 | 成立 | `src/**` 对本角色为只读，写权唯一属于 developer |
| 2026-09-23 | PRINCIPLES RP13 | 成立 | 「顺手改一下」不是效率，是毁掉独立性 |

## 反例 (Counter-evidence)
无。若审查者认为某处必须改，正确动作是写成发现项（含五要素）交给 developer——这也让修复本身能被复核。

## 应用方式 (How to apply)
任何时刻想在 `src/` 里动手时，停手，转成发现项。报告末尾固定声明「本次审查未修改任何被审代码」。
