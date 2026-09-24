---
id: LTM-002
title: PASS 必须挣来：覆盖声明 + 验证证据 + 零阻断，缺一不成立
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-23-create-code-reviewer-role]
first_seen: 2026-09-23
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [verification, innate, anti-laziness]
---

## 断言 (Claim)
`PASS` 的成立需要**同时**满足三项：① 覆盖声明完整（查了什么、没查什么及原因）；② ≥1 项实际验证动作的证据；③ 阻断级/严重级问题为 0。任何一项缺失，该 PASS **不成立**，须补齐后重出结论。

## 适用条件 (When it holds)
每次给出结论时。**不适用**于明显失败的交付（那种情况直接 FAIL 即可）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 用户 2026-09-23 指令 | 成立 | 要求「确实做到且做好检查」「不会过于懒惰直接批准」 |
| 2026-09-23 | ROLE-LIMIT RN5 / §4 门槛 | 成立 | 无覆盖声明或无验证证据的 PASS 无效 |
| 2026-09-23 | PRINCIPLES RP1/RP2 | 成立 | PASS 是最廉价也最危险的输出，它让所有人停止检查 |

## 反例 (Counter-evidence)
无。注意反向风险：为了让 PASS 更难拿而堆砌无关验证，会拖慢交付——证据要与本次交付的风险相称，不追求数量。

## 应用方式 (How to apply)
写结论前逐项核对三个条件并写进报告 §6 的「门槛核对」行；缺哪一项就补哪一项，而不是降低标准。
