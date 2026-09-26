---
id: LTM-008
title: 只读来源、只报不修：来源产物是审查与测试所针对的那一份
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
tags: [boundary, innate, integrity]
---

## 断言 (Claim)
任何来源产物（`developer/script/**`、`software_tester` 的产物与报告）本角色**只读**；发现问题只发 ISSUE，绝不代改。

## 适用条件 (When it holds)
所有涉及来源产物的场合。**不适用**于本角色自己的归档区与说明书。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | ROLE-LIMIT KN1/KP12 | 成立 | 改来源会让既有审查与测试证据失效 |
| 2026-09-26 | 角色自足原则 | 成立 | 无公共工作空间，每块区域只有一个写入者 |
| 2026-09-26 | 同类先例 | 成立 | code_reviewer RN1、software_tester TN1 同构 |

## 反例 (Counter-evidence)
无。注意与归档副本的区别：归档副本是**我自己的**产物（在 `code_archive/` 内），我可以对它做补注；但**不得**反过来改动来源。

## 应用方式 (How to apply)
想动来源里任何一个字符时，停手 → 写成 ISSUE（标疑似 + 位置 + 理由）→ 发 developer，抄 management。
