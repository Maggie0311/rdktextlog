---
mail_id: MAIL-20260925-2335-framework_admin--system-RESULT-self-sufficiency-elevated
thread: THREAD-0007-self-sufficiency-principle
from: framework_admin
to: system (人类用户)
cc: [management, developer, code_reviewer]
date: 2026-09-25 23:35
purpose: RESULT
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - _framework/00-ARCHITECTURE.md
  - framework_admin/principles/PRINCIPLES.md
  - framework_admin/memory/long-term/LTM-007-no-shared-workspace.md
  - framework_admin/script/role-skeleton-spec.md
  - framework_admin/_framework/01-ROLE-REGISTRY.md
  - framework_admin/_framework/decisions/AUDIT-LOG.md
---

## 1. 背景 (Context)
你指出：角色没有公共工作空间，各自产物存在自身文件系统内，经邮件系统发给其他角色；
要求我更新**工作记忆与方法**，并在**以后建角色**时注意。

## 2. 目的 (Objective)
回报：该原则已从"上一轮的一次更正"提升为**根规范级不变量**，并已写入我的方法与记忆、写入建角色的检查清单。

## 3. 认同与升级

我认同，并且认为你的表述比我上一轮的处理更准确：

| | 我上一轮做的 | 你这次给的 |
|---|---|---|
| 性质 | **补漏**（废止一个具体目录） | **一般性原则**（不变量） |
| 表述 | "与框架自身定义冲突，故废止 `src/`" | "**角色没有公共工作空间**" |
| 后果 | 只解决这一次 | 约束**下一次**新增目录 / 设计角色时的决策 |

真正的失败不是"选错了目录"，而是**设立了多主共享区**——它让"这块归谁"无法再用目录回答，
从而必然产生并发写、互相覆盖与责任不清。所以正确的固化形式是**不变量**：

> **每一块区域有且仅有一个写入者；不存在公共工作空间。**
> 判据（可当场回答）：指着任意区域问"**这块有几个写入者？**"——≥2 即为违规设计。

## 4. 已完成的更新

| 层 | 变更 |
|---|---|
| **根规范** | `00-ARCHITECTURE.md` **v1.1 → v1.2**：新增 **§2.1 角色自足原则（No Shared Workspace）**（5 条 + 理由 + 历史依据）；§7 补注"授权界定"——**不存在"公共区"这一豁免路径** |
| **我的方法** | `principles/PRINCIPLES.md` **v1.1**：新增 **P19 角色自足**（本组最高优先级，含"我自己的历史错误"注记）；专业检查清单增第 7 问 |
| **我的记忆** | 新增 **`LTM-007`**（innate，confidence 1.00，依据根规范 §2.1）；加固 `STM-007`（+0.15 独立确认 → 0.55），并注明其已上升为原则、**不再走 §4.3 晋升**，作为该原则的"来源"保留 |
| **建角色检查清单** | `01-ROLE-REGISTRY.md` 与 `script/role-skeleton-spec.md` **各增 2 项**：自足性检查、写入者唯一性检查；骨架规格 §1 目录清单后加自足性说明 |
| **审计** | `AUDIT-LOG` **R6**：把"是否存在多主区"立为**固定检查项**（首轮执行结果：`framework_admin/**`、`management/**`、`developer/**`、`code_reviewer/**`、`_framework/**` 写入者均为 1，**0 个多主区**） |
| **通告** | `MAIL-20260925-2320` 已投递 management / developer / code_reviewer |

## 5. 一处刻意的边界说明（防止我被自己"过度适用"）

原则中显式写明：**受限的是"写"，不是"读"。** 审查、验收、审计**必须**读取他方产物，属正常且必要；
`_framework/` 与各角色目录**各有唯一写入者**，因此是**单主区**，不是公共区。
——把"只读访问"也当成违规，是这条原则最可能的误用方向，所以我在条款里前置堵住。

## 6. 关于"注入记忆"

各角色需要把本条记入**自己的**记忆。这一条我**只发信告知、不代写**——依据 `ROLE-LIMIT` N2：
记忆必须由经历者本人沉淀，否则置信度失真。**我不给自己开例外**（我自己这一条是写进我自己的记忆的）。

## 7. 验收 (Acceptance)
- [x] 根规范 §2.1 可判定、有理由、有例外说明（"几个写入者"是路径判断，不是口号）
- [x] 我的方法与记忆已更新（P19 / LTM-007 / STM-007 加固）
- [x] **建角色检查清单两处**均已加入自足性与写入者唯一性检查——"以后建角色"不会再漏
- [x] 审计固定项已设立并完成首轮核查（0 个多主区）
- [x] 通告已投递全体；明确要求各角色自行更新记忆
- [x] 按 `05-CONVENTIONS v1.2 §7.2` 显式路径提交 git

## 8. 期望回复 (Expected Reply)
无需回复。下一个角色被创建时，你会在其契约与检查记录中看到**自足性检查**的执行结果；
若将来确实出现**外部工具链强制**的共享目录需求，我会先出 DECISION 记录该外部约束，
**不会凭预想提前设立**（`DECISION-20260924-005 §6` 已记录该重议条件）。
