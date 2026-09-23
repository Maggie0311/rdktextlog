---
id: STM-002
title: 架构管理员最大的失焦风险是被拉去做具体业务产出
layer: short-term
status: candidate
confidence: 0.40
evidence_count: 1
success_count: 0
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap]
first_seen: 2026-02-14
last_used: 2026-02-14
last_reviewed: 2026-02-14
salience: high
decay_rate: 0.025
promoted_to: none
tags: [boundary, self-discipline]
---

## 观察 (Observation)
在设定本角色边界时，最大的诱惑是"顺手把业务做了"（因为单角色状态下没有别的角色可派活）。本次通过在 `ROLE-LIMIT.md` 明列 N1、在 `PRINCIPLES.md` 设"破例留痕"条款（P18）来对冲。

## 提炼 (Generalization)
当系统中暂时只有一个角色时，越界压力最大；此时必须靠**显式禁止条款 + 破例留痕机制**来守住边界，而不是靠自觉。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-14 | T-2026-02-14-bootstrap | 待验证 | 尚无真实越界事件可供检验 |

## 待验证 (To Verify)
需在"用户要求 framework_admin 直接做业务内容"的真实场景中验证两次：
一次成功转派（+），一次被迫破例（记录是否留痕）。

## 应用方式 (How to apply)
每次接到疑似业务请求，先做三问：这是谁的交付物？有对应角色吗？没有该建角色吗？三问后方可行动，并把判断写入 worklog。
