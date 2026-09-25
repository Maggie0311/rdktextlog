---
id: LTM-003
title: 派活与协作必须落邮箱，未落邮箱即不存在
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-23-create-management-role]
first_seen: 2026-09-23
last_used: 2026-09-23
last_reviewed: 2026-09-23
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [communication, innate, audit]
---

## 断言 (Claim)
任务分派、进度问询、催办、打回、验收结论，必须形成 `mailbox/outbox/` 中的一封信；对话渠道中口头达成的安排不构成任务，也不构成进度。

## 适用条件 (When it holds)
所有跨角色交互。例外：与人类用户的沟通可走对话渠道，但**结论仍需在 1 轮内补一封邮件或台账记录留痕**（架构 §5.6）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-23 | 本角色契约 MN6 与 §2 通信义务 | 成立 | "结论留痕"为硬性要求 |
| 2026-09-23 | ROLE-LIMIT MN6 | 成立 | 禁止口头/隐式派活 |
| 2026-09-23 | PRINCIPLES P5 | 成立 | 台账证据只认邮件与文件路径 |

## 反例 (Counter-evidence)
无。注意：邮箱是**正式通道**，不是唯一沟通方式——讨论可以在对话里进行，但结论必须回流邮箱。

## 应用方式 (How to apply)
每次分派后自问：outbox 里有这封信吗？没有就补发。审计时只要发现台账里有"assigned"而 outbox 无信，即判为断链（V4）。
