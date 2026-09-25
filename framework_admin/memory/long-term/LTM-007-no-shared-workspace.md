---
id: LTM-007
title: 角色没有公共工作空间：每块区域有且仅有一个写入者，跨角色流转只经邮箱
layer: long-term
status: active
confidence: 1.00
evidence_count: 3
success_count: 3
failure_count: 0
source_tasks: [T-2026-09-24-fix-artifact-area, T-2026-09-25-elevate-self-sufficiency, _framework/00-ARCHITECTURE §2.1]
first_seen: 2026-09-24
last_used: 2026-09-25
last_reviewed: 2026-09-25
salience: high
decay_rate: 0.025
promoted_from: innate
tags: [architecture, boundary, innate, design-principle]
---

## 断言 (Claim)
本框架**不存在公共工作空间**：每个角色的全部产物都落在**该角色自己的目录**内（主要是 `script/`），
交付给他方经**邮件**完成（路径 + commit hash + 可选打包件）。
**每一块区域有且仅有一个写入者**；任何"多个角色都能写"的目录都是**违规设计**。
判据可当场回答：指着任意区域问"**这块有几个写入者？**"——答案 ≥2 即为违规。

## 适用条件 (When it holds)
任何涉及目录归属、产物存放、交付流转的设计与决策。

**不适用（重要，防止过度适用）**：**只读访问他方产物是允许且必要的**——审查、验收、审计都要读他方目录。
本条禁止的是**跨角色写入**，不是只读。
另：`_framework/` 由 framework_admin 独占、各角色目录由其本人独占，**各有唯一写入者**，不属公共区。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-09-24 | T-2026-09-24-fix-artifact-area | 成立 | 委托层指出 `src/` 共享产物区不必要；`DECISION-20260924-005` 废止，零迁移 |
| 2026-09-25 | T-2026-09-25-elevate-self-sufficiency | 成立 | 委托层将该判断确立为**一般原则**；写入根规范 `00-ARCHITECTURE v1.2 §2.1` |
| 2026-09-25 | 全仓自足性专项核查 | 成立 | 4 个角色 + `_framework/` 全部为单主区，**不存在多主共享区**（`AUDIT-LOG` R6） |

## 反例 (Counter-evidence)
暂无实例。理论反例条件：若出现**外部工具链强制**要求某个共享目录（例如某构建系统硬性要求固定的源码根），
且无法用配置或链接解决——此时应先由 framework_admin 出 DECISION 记录该**外部约束**，
**不得凭预想提前设立**。

## 应用方式 (How to apply)
1. 任何"新增顶层目录 / 共享区"的提案，先问"这块有几个写入者"；≥2 即否决，改为并入某角色目录。
2. 设计角色时，其产物区就是它自己的 `script/`；不要为"项目"另建共享区。
3. 交付一律走邮箱；需要他方改动 → 发 `ISSUE` / `TASK`，不直接写。
4. 审计时把"是否存在多主区"作为**固定检查项**（做法见 `AUDIT-LOG` R6）。
