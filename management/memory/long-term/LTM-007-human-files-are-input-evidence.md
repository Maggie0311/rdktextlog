---
id: LTM-007
title: 人类投放的文件是需求的一手依据：只读、登记、以路径引用，绝不改动
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-26-human-input-channel]
first_seen: 2026-09-26
last_used: 2026-09-26
last_reviewed: 2026-09-26
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [input, boundary, innate]
---

## 断言 (Claim)
`from_human/` 中的文件是**人类用户交给我的一手依据**。我对它们：
**只读**（不改名、不移动、不删除、不减内容）、**必登记**（处理后在 `from_human/INTAKE-LOG.md` 追加一行）、
**以路径引用**（在需求拆解书里写路径，不复制内容）——因为**原件才是权威**，复制会产生"抄错了"的版本。

## 适用条件 (When it holds)
每次接活与每次拆解需求时。

**不适用**（防止过度适用）：我可以**新增**自己的文件（例如我自己的阅读笔记）到 `from_human/` 之外的地方；
若确需整理人类文件，**只能请人类用户决定**，不能自行改名或移动。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | 人类用户 2026-09-26 指令 | 成立 | 要求留一个人给 management 传输文件的入口，便于沟通工作目标时给出具体文件参考 |
| 2026-09-26 | 本角色契约 MN14 与权限矩阵 | 成立 | 明确只读例外 + 禁止改动 |
| 2026-09-26 | 本角色契约 §3.1 开工前置 | 成立 | 每次开工必须扫描并登记未处理文件 |

## 反例 (Counter-evidence)
无。注意边界情形：若人类投放的文件**与需求矛盾**，正确动作是**发 QUERY 问人**，而不是"按我理解的版本执行"
或者"顺手把文件改成一致"。

## 应用方式 (How to apply)
1. 开工第一件事之一：扫 `from_human/`，与 `INTAKE-LOG.md` 对比，处理未登记文件；
2. 处理后在 `INTAKE-LOG.md` 追加一行（文件 / 收到日期 / 用在哪个需求或任务 / 备注）；
3. 需求拆解时**写路径引用**该文件；读不懂或矛盾就发 QUERY，**不猜**；
4. 永远不碰原件——包括"重命名更整齐"这种看起来无害的动作。
