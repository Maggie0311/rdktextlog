---
id: LTM-008
title: 手段要恰当：能回答问题的前提下，选最轻的一种
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
salience: medium
decay_rate: 0.05
promoted_from: innate
tags: [method, innate, efficiency]
---

## 断言 (Claim)
在本机直跑、远程机运行、烧录到目标板、物理测量等手段之间，**选能回答该问题的最轻手段**；手段的「重」不等于结论的「强」。

## 适用条件 (When it holds)
每次选择测试手段。**不适用**于问题本身就依赖特定平台时（例如验证目标板时序，就必须上目标板）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-25 | 人类用户 2026-09-25 指令 | 成立 | 要求「通过一定且恰当的手段」测试，且「如果有必要测试的话」 |
| 2026-09-25 | PRINCIPLES TP6 | 成立 | 手段只在与问题匹配时才有价值 |
| 2026-09-25 | ROLE-LIMIT T5 | 成立 | 多角度测试仅在有必要且有判定标准时进行 |

## 反例 (Counter-evidence)
无。但「轻」不是目的：若问题只能由目标平台回答，就必须上目标平台，不得因省事而用本机近似替代。

## 应用方式 (How to apply)
选择手段时先写一句理由：「用 X 手段，因为它能回答 Y，且无需 Z 的代价」。写不出理由就说明手段选错了。
