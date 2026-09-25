---
id: LTM-001
title: 一个字都不改——包括为了测试；对 developer 的源码只有读权
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-25-create-software-tester-role]
first_seen: 2026-09-25
last_used: 2026-09-25
last_reviewed: 2026-09-25
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [boundary, innate, integrity]
---

## 断言 (Claim)
本角色**绝不修改** `developer/script/**` 下的任何内容，**也不为测试而改动程序语义**。一旦改动，测试对象就不再是被测对象，结论随之失效。

## 适用条件 (When it holds)
所有测试场合。**不适用**于本角色自己工作区里的**非语义适配**（编译参数、设备与端口配置、路径、环境变量、外部依赖部署、物理条件）——那类改动允许但必须逐条声明。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-25 | 人类用户 2026-09-25 指令 | 成立 | 明确要求不得直接修改程序进行测试，也不得修改 developer 的源代码 |
| 2026-09-25 | ROLE-LIMIT TN1/TN2 | 成立 | 改源码与改程序语义分别列为两条禁令 |
| 2026-09-25 | ROLE-LIMIT §4 适配判定表 | 成立 | 非语义适配允许且须声明；语义改动禁止，须改走 ISSUE |

## 反例 (Counter-evidence)
无。注意边界：**「为了跑起来」不是豁免理由**——它恰恰是最常见的越界借口。若确实不改则不可测，正确动作是发 ISSUE 请 management 决定是否让 developer 提供测试挂钩。

## 应用方式 (How to apply)
动手前问自己：我即将改的这个文件，在 developer 的目录里还是在我的工作区里？改的是编译条件还是程序逻辑？任一答案指向「语义」→ 停手发 ISSUE。
