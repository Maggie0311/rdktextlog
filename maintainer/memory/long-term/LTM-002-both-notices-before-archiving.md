---
id: LTM-002
title: 先齐备再归档：management 的验收许可与两封合格确认通知，三份缺一不可
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
归档需**三份要件齐备**：① `management` 的 **`accepted` 验收结论（归档许可）**；② `developer` 的合格确认通知；③ `software_tester` 的合格确认通知。三者 **commit hash 必须一致**；缺哪份就向哪方发 QUERY。

## 适用条件 (When it holds)
所有归档启动前。**不适用**于墓碑记录（那记录的是未采用或被验收驳回的版本，不需要三份要件）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | 人类用户 2026-09-26 指令 | 成立 | 要求让 developer 和 software_tester 确定合格后通知 maintainer |
| 2026-09-26 | **委托层选项确认** | 成立 | 明确选择「**必须先经 management 验收通过才归档**」，故许可要件由 management 提供 |
| 2026-09-26 | ROLE-LIMIT K1/KN11 | 成立 | 三份要件缺一即不得归档 |
| 2026-09-26 | PRINCIPLES KP2 | 成立 | 归档意味着宣布合格，不可替他人宣布 |

## 反例 (Counter-evidence)
无。若两封通知的 commit hash **不一致**，说明归档对象不明确——此时应发 QUERY 让双方对齐，**不得**自行选择其一。

## 应用方式 (How to apply)
归档第一步：把**三份**要件的 `mail_id` 与 commit hash 并列抄进版本卡；任一份缺失或不一致就停下问人，**不得先归档后补**。

---

> **修订记录（2026-09-26，委托层选项确认）**：见 `DECISION-20260926-009`。本条结论已按委托层选择更新。
