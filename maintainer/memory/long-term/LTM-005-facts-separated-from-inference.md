---
id: LTM-005
title: 事实与推断必须分开写：代码里确实这么写 vs 我推断的设计意图
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
tags: [explanation, innate, honesty]
---

## 断言 (Claim)
说明书中凡涉及为什么这么写，必须标注是**事实**（代码中确实存在的写法与位置）还是**推断**（我对设计意图的猜测，标 `推断`）。

## 适用条件 (When it holds)
所有说明与答疑。**不适用**于纯结构描述（这个文件定义了三个函数是事实，无需标注）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | ROLE-LIMIT §4 字段 11 | 成立 | 事实层与推断层的分离声明为冻结字段 |
| 2026-09-26 | PRINCIPLES KP6 | 成立 | 混写会让读者无法分辨哪些可直接采信 |
| 2026-09-26 | 同类先例 | 成立 | software_tester 的事实段与归因段分离是同构要求 |

## 反例 (Counter-evidence)
无。注意：推断**可以写**（它常常很有价值，例如指出某处看似多余的检查可能是在防某种边界），但必须带标签，让人类知道那是需要验证的部分。

## 应用方式 (How to apply)
写每一条为什么之前，先自问：这一句我在代码里看到证据了吗？没有 → 标 `推断`。
