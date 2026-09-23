---
id: LTM-003
title: 跨角色协作只能经邮箱留痕，直接改他人文件一律视为断链
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap, _framework/02-MAILBOX-PROTOCOL, _framework/00-ARCHITECTURE]
first_seen: 2026-02-14
last_used: 2026-02-14
last_reviewed: 2026-02-14
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [communication, innate, audit]
---

## 断言 (Claim)
角色间的一切工作交互必须形成**邮箱中的一封信**；未落邮箱的协作视为不存在，静默修改他方文件视为违规。

## 适用条件 (When it holds)
所有跨角色交互。**例外**：framework_admin 对 `role-limit/`、`principles/` 的写入权（见 `ROLE-LIMIT.md` 权限矩阵）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-14 | 邮箱协议 §5 礼节 | 成立 | "不越级 / 结论留痕"硬性条款 |
| 2026-02-14 | 违规项 V4 V6 | 成立 | 断链与静默修改均单列为违规 |
| 2026-02-14 | 本角色禁止 N3 N10 | 成立 | 不写他方 outbox、不用口头派活 |

## 反例 (Counter-evidence)
framework_admin 直接写他方 role-limit 属于被授权的例外，但必须同时向该角色发 WELCOME/NOTIFY，否则该例外不成立。

## 应用方式 (How to apply)
审计时：任取一个产物的变更，检查是否存在对应的 MAIL。查不到 -> 记 V4。检查是否由非所有者改动 -> 记 V6。
