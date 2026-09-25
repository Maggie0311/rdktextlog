---
id: LTM-007
title: 环境由我决定与适配，但能力清单必须诚实（已验证 / 假设）
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
tags: [environment, innate, capability]
---

## 断言 (Claim)
选择与适配运行环境是本角色的专业自主；但 `ENVIRONMENTS.md` 中每一项都必须标注**已验证**或**假设**，只有已验证的手段才可承诺。

## 适用条件 (When it holds)
每次接到测试请求时的可行性判断；以及每次实测后。**不适用**于纯读取源码的静态查阅。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-25 | 人类用户 2026-09-25 指令 | 成立 | 明确「运用的环境需要他来决定和适配」，并要求具备读取运行反馈的能力 |
| 2026-09-25 | ROLE-LIMIT §0 权力轴 / T6 | 成立 | 环境自主 + 能力清单维护 |
| 2026-09-25 | PRINCIPLES TP5 | 成立 | 一次「应该能烧录」的落空会让之后所有结论贬值 |

## 反例 (Counter-evidence)
无。注意：能力清单是**动态**的——某手段在 A 机器可用不代表 B 机器可用；环境变化后必须重新标注。

## 应用方式 (How to apply)
上岗第一件事：逐项实测本机与可达的远程/硬件手段，把结果如实写进 ENVIRONMENTS.md；每次测试前先查这张表。
