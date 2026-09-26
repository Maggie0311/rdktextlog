---
id: LTM-003
title: 补注只加注释行，绝不改代码——连顺手改个类型都不行
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
tags: [boundary, innate, readability]
---

## 断言 (Claim)
**就地补注**（注释直接加在归档代码文件上，**不另存第二份**）：只允许**新增**以注释符号开头的行；不得增删改任何代码行、字符串字面量、宏、编译指令、缩进与空行。补注前后 diff **必须只含新增注释行**，并记录**双指纹**（来源 commit + 补注前后 SHA-256）。

## 适用条件 (When it holds)
所有补注场合。**不适用**于在说明书中用文字讲解——那是文字，不受此限，且是必须改代码才能讲清时的正解。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | 人类用户 2026-09-26 指令 | 成立 | 要求在不修改源代码的情况下适当补充注释 |
| 2026-09-26 | ROLE-LIMIT KN3 / §4 补注判定表 | 成立 | 越界即违规 |
| 2026-09-26 | PRINCIPLES KP3 | 成立 | 动了代码行，它就不再是原产物的注释版 |

## 反例 (Counter-evidence)
无。边界情形：若某段代码必须改才能讲清（例如类型歧义导致误解），正确动作是**在说明书里用文字说明**并发 ISSUE，而不是替 developer 改。

## 应用方式 (How to apply)
补注完成后跑一次 diff 自检；只要 diff 里出现一行不以注释符号开头的新增内容，就**从来源重新复制并重做**（此时尚未冻结，可重来）。

---

> **修订记录（2026-09-26，委托层选项确认）**：见 `DECISION-20260926-009`。本条结论已按委托层选择更新。
