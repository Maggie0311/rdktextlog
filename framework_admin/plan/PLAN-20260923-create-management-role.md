# PLAN-20260923-create-management-role

| 字段 | 值 |
|---|---|
| 计划 ID | PLAN-20260923-create-management-role |
| 角色 | framework_admin (R-001) |
| 关联邮件 | 无（人类用户直接下达，非邮箱任务） |
| 创建时间 | 2026-09-23 21:00 |
| 状态 | done |

## 1. 目标 (Objective)
在**不与既有角色 R-001 产生边界重叠、也不留工作流真空**的前提下，创建 R-002 `management` 的完整角色实例。

可验收判据：给定 `management/` 目录，一个零上下文执行者能据此独立开工且不越界；且 `management` 的"只能做"集合与 `framework_admin` 的"只能做"集合**交集为空**。

## 2. 约束 (Constraints)
- 来自 role-limit 的硬边界：本角色只做角色定义/边界/规范/任命（A1、A2、A5、A6），**不代做业务产出**（N1）；不写他方 `memory/script/worklog/outbox`（N2/N3）。
- 来自用户口述的硬需求：R-002 与 R-001 **平行同级**；统领项目全局；统一拆解/计划/分派；主动沟通进度与任务分配；领导其他 AI；把环节路由给最合适的专家角色；整体检查验收；掌握真实进度；关键问题与人类用户交互。
- 来自用户口述的**硬禁止**：R-002 **没有创建角色的能力**，建角色权唯一属于 framework_admin。
- 来自 `_framework/05-CONVENTIONS.md` 的命名与不可变性约定。
- 资源约束：单会话完成，不引入外部依赖。

## 3. 记忆依据 (Memory Basis)

| 记忆 ID | 层 | 置信度 | 本计划如何用 |
|---|---|---|---|
| LTM-001 | long-term | 1.00 | 契约先写 MN 禁止清单，再写 M 允许清单 |
| LTM-002 | long-term | 1.00 | 冲突面逐项指定唯一主责（本次核心） |
| LTM-003 | long-term | 1.00 | 任命与后续协作全部落邮箱 |
| LTM-005 | long-term | 1.00 | R-002 记忆初始化只用 innate 注入，经验留空 |
| LTM-006 | long-term | 0.80 | 对本轮设计结论同样封顶，不因"写得很顺"抬高 |
| STM-001 | short-term | 0.35 | **本轮即其验证场景**：交付骨架时必须连同逐目录写入规则 |

## 4. 专业方法 (Method)
先做**冲突面枚举**（列出可能同时落在两个角色"只能做"里的动作），逐项裁定唯一主责，**然后**才写契约文本（P2 单一主责 + P4 职责正交）。

切分轴选取：不按"谁更高级"切，而按**层**切——`framework_admin` 管"谁能做什么"（元层/静态），`management` 管"这次谁做什么"（执行层/动态）。理由（P10）：层与层的变更频率不同，按层切分比对等切分更稳定。

## 5. 步骤 (Steps)

| # | 步骤 | 输入 | 输出 | 状态 |
|---|---|---|---|---|
| 1 | 冲突面枚举与唯一主责裁定 | 用户需求 + R-001 契约 | 裁定表（6 项） | done |
| 2 | 注册表登记 R-002 | 裁定结果 | `01-ROLE-REGISTRY.md` 新行 | done |
| 3 | 建立七目录与全部骨架文件 | 骨架规格 §1 | `management/` 25 个文件 | done |
| 4 | 编写四段式 ROLE-LIMIT | 裁定表 | `role-limit/ROLE-LIMIT.md` | done |
| 5 | 编写 PRINCIPLES（≥8 条可操作） | 边界哲学 | `principles/PRINCIPLES.md` | done |
| 6 | 初始化双层记忆 + 索引 + 流水 | 记忆模型 §4.1 | 6 LTM + STM-000 + 2 索引 | done |
| 7 | 投递任命信 + 首个任务 | 契约 | `management/mailbox/inbox/WELCOME-management.md` | done |
| 8 | 两两正交性与流程覆盖复核 | 双方契约 | 裁定记录入 `_framework/decisions/` | done |
| 9 | 回填本角色 `script/INDEX.md` 与自审 | 全部产物 | INDEX 更新 + AUDIT-LOG R2 | done |
| 10 | 更新自身 worklog / 记忆 / git 提交 | 全过程 | WORKLOG #16+ + STM 更新 | done |

## 6. 接口与依赖 (Interfaces)

| 依赖方 | 需要什么 | 何时需要 | 已发邮件 |
|---|---|---|---|
| management (R-002) | 契约 + 任命信 + 根规范 | 生效即需要 | `MAIL-20260923-2100-framework_admin--management-TASK-appointment` |
| 人类用户 | 完工回报 | 本轮结束 | `MAIL-20260923-2130-framework_admin--system-RESULT-management-role-created` |
| 未来角色 | R-002 定义的 task_id 格式与台账字段 | 第一个业务角色出现时 | 未发（届时须升级为根约定，见 LTM-004） |

## 7. 风险与回滚 (Risk & Rollback)

| 风险 | 概率 | 影响 | 缓解 | 回滚动作 |
|---|---|---|---|---|
| R-002 管理权膨胀为架构权（变成第二个 admin） | 中 | 高 | MN1 + MN12 + 权限矩阵明示"新建角色无权限" | 撤回契约并出 v2 |
| 两角色在"派活/验收/对接用户"三处重叠 | 中 | 高 | 步骤 1 的裁定表逐项指定唯一主责 | 重裁并修订双方契约 |
| R-002 亲自下场做业务（失去验收独立性） | 中 | 高 | MN2 + P8"指挥不下场" + 升级路径第 6 条 | 破例留痕并回退 |
| 手工创建 25 个文件出现遗漏（G2） | 中 | 中 | 建后逐项对照 `script/role-skeleton-spec.md §1` 复核 | 补齐缺项 |

## 8. 验收 (Acceptance)
- [x] 注册表新增 R-002 一行
- [x] 七目录齐备且每目录有 README 写入规则
- [x] ROLE-LIMIT 四段写满，MN 每条标注"应由谁做"
- [x] PRINCIPLES ≥8 条且可操作，含注意力焦点表与自检清单
- [x] 记忆初始化（LTM-000 + 6 条 innate LTM + STM-000 + 索引 + 流水）
- [x] inbox 存有任命信（含 purpose/priority/deadline/AC）
- [x] 与 R-001 的"只能做"交集为空、合并覆盖全部工作流环节（执行环节真空已登记为 G4）
- [x] worklog 追加记录 + git 提交

## 9. 收工检查 (Exit Checklist)
- [x] 产物已落 `script/` 并登记 `script/INDEX.md`
- [x] worklog 已记录
- [x] mailbox 已闭环（无滞留；任命信为常驻件）
- [x] short-term 记忆已更新（STM-001 加固 + 新增 STM-004）
