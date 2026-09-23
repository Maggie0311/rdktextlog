---
id: LTM-001
title: 角色边界必须用"绝不能做"的负向清单定义，正向清单只能作补充
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-02-14-bootstrap, _framework/00-ARCHITECTURE, _framework/05-CONVENTIONS]
first_seen: 2026-02-14
last_used: 2026-02-14
last_reviewed: 2026-02-14
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [boundary, design-principle, innate]
---

## 断言 (Claim)
给一个角色划边界时，**"绝不能做什么"清单是主约束，正向清单是次要的**；只写正向清单的契约在实践中必然被越界击穿。

## 适用条件 (When it holds)
- 适用于多方协作、职责需要互斥的场合。
- **不适用**于单角色、无协作的场合（此时负向清单无对象）。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-14 | 框架设计 T-2026-02-14-bootstrap | 成立 | `00-ARCHITECTURE.md` 冲突仲裁条款以 role-limit 文本为准 |
| 2026-02-14 | 本角色自约束 | 成立 | `ROLE-LIMIT.md` 中 N1–N10 占全文一半篇幅 |
| 2026-02-14 | 审计项设计 | 成立 | 违规 V1「越界」只能靠负向清单判定 |

## 反例 (Counter-evidence)
尚未发现。理论上若某角色的工作完全自我封闭、不与他方交互，则负向清单价值下降。

## 应用方式 (How to apply)
每创建/审查一个角色契约，先检查：是否存在一节明确写"绝不能做"，且每条都标注了"应由谁做"。缺失即打回。
