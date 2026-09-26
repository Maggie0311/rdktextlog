---
id: LTM-001
title: 归档即冻结：归档件的原产物字节永不可变，要变只能是新版本
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
tags: [archive, innate, integrity]
---

## 断言 (Claim)
写入 `code_archive/<task_id>/original/` 的产物**永不修改**；任何变动一律作为**新版本**（版本号递增）归档。

## 适用条件 (When it holds)
所有归档场合。**不适用**于带注副本（`annotated/`）——那是我生成的新产物，不是归档件。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-26 | 人类用户 2026-09-26 指令 | 成立 | 要求对各任务的代码各版本进行归档，支撑长期维护 |
| 2026-09-26 | ROLE-LIMIT KN2 | 成立 | 可变的归档等于没有归档 |
| 2026-09-26 | PRINCIPLES KP1 | 成立 | 归档的全部价值在于它当时就是这个样子 |

## 反例 (Counter-evidence)
无。注意区分：**冻结不等于不能修正错误**——若归档时抄错了文件，应在版本卡中记录更正说明并**重新归档为新版本**，而不是偷偷改旧件。

## 应用方式 (How to apply)
每次要对 code_archive 里已有文件动手前，先问：这是**新增版本**还是**修改旧件**？后者一律禁止。
