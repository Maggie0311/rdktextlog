---
id: LTM-003
title: 测试必须回答一个具体可判定的问题；写不出问题就不测
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
tags: [method, innate, scope]
---

## 断言 (Claim)
每次测试前必须能把请求翻译成一句话：「这次测试要回答：______？」且该问题有**判定标准**。写不出这句话，就发 QUERY，不开测。

## 适用条件 (When it holds)
所有测试请求。**不适用**于探索性排查的**最初几分钟**（但一旦要出结论，必须补上问题与判定标准）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-25 | 人类用户 2026-09-25 指令 | 成立 | 要求「仅在需要的时候」测试 |
| 2026-09-25 | PRINCIPLES TP2 | 成立 | 没有问题的测试只能产出「跑了一遍，看起来没事」 |
| 2026-09-25 | ROLE-LIMIT T7 测试方案 | 成立 | TESTPLAN 首字段即「要回答的问题」 |

## 反例 (Counter-evidence)
无。但需防过度收紧：问题可以宽（「该模块在边界输入下是否崩溃」），只要**可判定**即可，不必细到单条用例。

## 应用方式 (How to apply)
把请求写在 TESTPLAN 第一行；若写不出或写出来无法判定 → 发 QUERY 要求 management 明确。
