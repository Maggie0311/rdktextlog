---
id: STM-003
title: 邮件元数据不全会导致三个月后无法重建协作时间线
layer: short-term
status: candidate
confidence: 0.35
evidence_count: 1
success_count: 0
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap]
first_seen: 2026-02-14
last_used: 2026-02-14
last_reviewed: 2026-02-14
salience: medium
decay_rate: 0.05
promoted_to: none
tags: [communication, metadata]
---

## 观察 (Observation)
邮箱协议最终固定了 12 个必填 front matter 字段（mail_id/thread/from/to/cc/date/purpose/priority/deadline/requires_reply/attachments/references）与 7 段正文结构。刻意加入 `thread` 与 `references` 是为了让**后续任何一封信都能反推出完整协作链路**。

## 提炼 (Generalization)
邮件的价值一半在内容、一半在元数据；缺失 `thread` 或 `references` 的邮件在归档后等同于孤立噪声。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-14 | T-2026-02-14-bootstrap | 待验证 | 尚无真实邮件流可供检验 |

## 待验证 (To Verify)
在产生 ≥10 封真实邮件后，尝试只凭邮箱重建一条完整任务时间线。若失败 -> 元数据字段不足，需补字段并升协议版本。

## 应用方式 (How to apply)
发信前逐字段核对；审计时对缺 `thread` 或 `references` 的邮件记提醒。
