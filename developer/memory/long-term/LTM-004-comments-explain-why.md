---
id: LTM-004
title: 注释必须解释"为什么"；无信息量注释视为不合格
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
tags: [quality, innate, maintainability]
---

## 断言 (Claim)
详细注释的正确含义是**详细解释意图、原因、约束与坑**，不是把代码逐行翻译成中文。`i++; // i 加一` 这类注释属于不合格交付。默认注释语言为中文。

## 适用条件 (When it holds)
所有源码文件。**不适用**于自解释性极强的代码（如简单的 getter），此时不写注释优于写噪音注释。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 用户 2026-09-23 指令 | 成立 | "有详细的中文注释"是用户硬需求 |
| 2026-09-23 | ROLE-LIMIT D2/DN8 | 成立 | 注释覆盖文件头/函数头/非显然逻辑；噪音注释不合格 |
| 2026-09-23 | PRINCIPLES DP7 | 成立 | 写前先问：这段注释是否解释了代码本身表达不了的东西 |

## 反例 (Counter-evidence)
无。但需防止过度注释：把显而易见的赋值语句逐行注释同样增加维护成本，方向相反而已。判断标准始终是"是否补充了代码表达不了的信息"。

## 应用方式 (How to apply)
每写一处注释先自问三点：为什么这么做？为什么不是另一种做法？这里的隐含前提是什么？答不出来就不写。
