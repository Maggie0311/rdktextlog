---
id: LTM-002
title: 先齐备再归档：developer 与 software_tester 两封合格确认通知缺一不可
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
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [trigger, innate, boundary]
---

## 断言 (Claim)
只有同时具备 `developer` 与 `software_tester` 的**合格确认通知**（含同一 `task_id` 与 **commit hash**），才可启动归档；缺哪封就向哪方发 QUERY。

## 适用条件 (When it holds)
所有归档启动前。**不适用**于墓碑记录（那记录的是未采用的版本，不需要合格确认）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | 人类用户 2026-09-26 指令 | 成立 | 要求让 developer 和 software_tester 确定合格后通知 maintainer |
| 2026-09-26 | ROLE-LIMIT K1/KN11 | 成立 | 缺任一封即不得归档 |
| 2026-09-26 | PRINCIPLES KP2 | 成立 | 归档意味着宣布合格，不可替他人宣布 |

## 反例 (Counter-evidence)
无。若两封通知的 commit hash **不一致**，说明归档对象不明确——此时应发 QUERY 让双方对齐，**不得**自行选择其一。

## 应用方式 (How to apply)
归档第一步：把两封通知的 `mail_id` 与 commit hash 并列抄进版本卡；不一致就停下问人。
