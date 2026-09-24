---
id: LTM-005
title: 用户自定义标准优先级最高且不可删改，每次审查必须列出应用情况
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
tags: [user-interface, innate, priority]
---

## 断言 (Claim)
`standard/user/USER-*.md` 是**人类用户的意志**，优先级高于项目契约与本角色自己的清单；本角色**不得删除、修改或降低**其级别，只能发 ISSUE 建议。每次审查**必须**在报告中列出本次实际应用的用户标准（无则写「无」）。

## 适用条件 (When it holds)
每次审查。**不适用**于用户尚未写入任何标准的时期（此时写「无」，但不得省略该字段）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 用户 2026-09-23 指令 | 成立 | 要求留出用户自定义标准接口，方便人类用户以后添加检查点 |
| 2026-09-23 | ROLE-LIMIT RN4 / 权限矩阵 | 成立 | `standard/user/USER-*.md` 对本角色只读 |
| 2026-09-23 | standard/README §2 | 成立 | 优先级表：用户标准 > 项目契约 > 本角色清单 > 根规范 |

## 反例 (Counter-evidence)
无。若用户标准与项目契约冲突，以用户标准为准 **同时** 发 ISSUE 给 framework_admin 记 DECISION——执行与留痕两件事都要做。

## 应用方式 (How to apply)
审查第 1 步先扫 `standard/user/`；报告「应用标准清单」里逐条列出；发现项凡相关必引用户编号。
