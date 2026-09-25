---
id: LTM-007
title: 共享仓库提交隔离：按路径显式添加，禁止盲加与覆盖他方改动
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
tags: [repository, innate, collaboration]
---

## 断言 (Claim)
仓库由多个角色共用，因此禁止 `git add -A` / `git add .`；必须按路径显式添加自己本轮改动的文件。提交前必须先 `git status`；发现他方未提交改动时**不得提交、不得回滚、不得修改**，发 NOTIFY 请其自行提交。（完整规则见本角色契约 §2.1.2。）

## 适用条件 (When it holds)
所有 git 操作。例外：无——该条对 framework_admin 自身同样有效（立规依据正是其连续三次盲加提交）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 本角色契约 §2.1.2 | 成立 | 框架级强制约定 |
| 2026-09-23 | ROLE-LIMIT DN7 | 成立 | 盲加会把他方未完成的工作卷入提交或直接丢失 |
| 2026-09-23 | 真实事件（framework_admin WORKLOG #15/#20/#22） | 成立 | 连续三次 `git add -A`，当时仅因恰无他方未提交改动而未造成损失 |

## 反例 (Counter-evidence)
无。注意：本条的立规依据不是假设，而是一次**实际发生过的侥幸**——这正说明"没出事"不能作为放宽纪律的理由。

## 应用方式 (How to apply)
提交前三步：`git status` 看全局 → 按路径 `git add <具体文件>` → 确认暂存区只含自己本轮改动后再 commit。
