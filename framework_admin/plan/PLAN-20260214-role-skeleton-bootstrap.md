# PLAN-20260214-role-skeleton-bootstrap

| 字段 | 值 |
|---|---|
| 计划 ID | PLAN-20260214-role-skeleton-bootstrap |
| 角色 | framework_admin |
| 关联邮件 | 无（由人类用户直接下达，非邮箱任务） |
| 创建时间 | 2026-02-14 |
| 状态 | done |

## 1. 目标 (Objective)
建立多角色协作框架的**根规范**与 framework_admin 角色自身的**七目录实例**，使得后续任何新角色都能被快速、无歧义地创建。

可验收判据：给定 `_framework/` + 一个角色目录，一个零上下文的执行者能据此独立开工，且不越界。

## 2. 约束 (Constraints)
- 来自 role-limit 的硬边界：本角色只做架构与边界，不做任何业务产出（N1）。
- 来自用户口述的硬需求：每个角色必须含 mailbox / memory / role-limit / principles / script / plan / worklog 七项。
- mailbox 必须自成体系：来信人、日期、目的等元数据齐全。
- memory 必须分 long-term / short-term，且长期记忆由短期沉淀、需反复检验后升华（仿动物记忆）。
- 资源约束：单会话完成，不引入外部依赖。

## 3. 记忆依据 (Memory Basis)

| 记忆 ID | 层 | 置信度 | 本计划如何用 |
|---|---|---|---|
| LTM-001 | long-term | 1.00 | 先写 N 清单再写 A 清单，确定 role-limit 结构 |
| LTM-002 | long-term | 1.00 | 注册表加入正交性自检；明确"唯一主责" |
| LTM-003 | long-term | 1.00 | 跨角色通道只走邮箱；不直接改他人文件 |
| LTM-005 | long-term | 1.00 | 设计晋升/遗忘/防污染机制 |
| LTM-006 | long-term | 0.80 | 对设计期结论实施置信度封顶 |

（本轮为引导轮，short-term 记忆在收工时新写，不参与规划。）

## 4. 专业方法 (Method)
采用**先规范后实例**的顺序：根规范先行，角色实例作为规范的第一份样例。
理由（P10 规范性递减 + P7 契约先冻结）：根规范一旦有角色依赖就冻结，因此必须在创建任何角色**之前**定稿，避免"边做边改规范"导致角色各自漂移。

采用**负向优先**（P1）：所有角色契约模板都以"绝不能做"为主约束块。

## 5. 步骤 (Steps)

| # | 步骤 | 输入 | 输出 | 状态 |
|---|---|---|---|---|
| 1 | 建立标准目录骨架 | 用户需求 | 七个角色子目录 + `_framework/` | done |
| 2 | 编写根规范 00–05 | 需求拆解 | 六份根规范文件 | done |
| 3 | 编写 5 份模板 + 13 份目录 README | 根规范 | 模板与占位说明 | done |
| 4 | 编写本角色 role-limit | 根规范 | `role-limit/ROLE-LIMIT.md` | done |
| 5 | 编写本角色 principles | 边界哲学 | `principles/PRINCIPLES.md` | done |
| 6 | 初始化双层记忆 + 索引 + 流水 | 记忆模型 | 6 条 LTM + 3 条 STM + 2 份索引 | done |
| 7 | 下发任命信（自任命样例） | 注册表 | `mailbox/inbox/WELCOME-framework_admin.md` | done |
| 8 | 撰写并发送首封协议通知邮件 | 邮箱协议 | `mailbox/outbox/MAIL-...RFC...` | done |
| 9 | 写工作日志 | 全过程 | `worklog/WORKLOG.md` | done |
| 10 | 自审并记录 | 全部产物 | `_framework/decisions/DECISION-...` | done |

## 6. 接口与依赖 (Interfaces)

| 依赖方 | 需要什么 | 何时需要 | 已发邮件 |
|---|---|---|---|
| （未来）全部角色 | `_framework/` 根规范 + 模板 | 创建时 | MAIL-20260214-...-NOTIFY-rfc-framework-v1 |

当前无外部角色，故无真实跨角色依赖；该邮件以"存档样例"形式发出，供后续角色读取。

## 7. 风险与回滚 (Risk & Rollback)

| 风险 | 概率 | 影响 | 缓解 | 回滚动作 |
|---|---|---|---|---|
| 规范过度设计，实际用不上 | 中 | 中 | 每条规范都写"判定方法/审计项"，无判定方法的不写 | 出 v2 精简版，保留旧版 |
| 目录结构后期被证明不够用 | 中 | 高 | 七目录为**最小集**，允许角色自建子目录，禁止删除七目录 | 追加目录，不重构 |
| 记忆规则太复杂导致角色不执行 | 中 | 高 | 给出可复制模板 + 明确阈值数字 | 简化晋升条件至 3 条 |
| 本角色越界做业务 | 中 | 高 | N1 + P18 破例留痕 | 记录破例并回退 |

## 8. 验收 (Acceptance)
- [x] `_framework/` 六份根规范齐备
- [x] 七目录齐备且每目录有 README 说明用途
- [x] role-limit 含 A1–A12 与 N1–N10
- [x] principles 含可操作准则，非口号
- [x] memory 双层 + 索引 + 固化流水
- [x] 存在至少一封格式完备的邮件样例
- [x] worklog 分条记录
- [ ] 由一个真实新角色验证本框架可用（**待下一轮任务，对应 STM-001 的验证**）

## 9. 收工检查 (Exit Checklist)
- [x] 产物已落 `script/`（含 `script/INDEX.md`）
- [x] worklog 已记录
- [x] mailbox 已闭环（inbox 无滞留 + 交付邮件已入 outbox）
- [x] short-term 记忆已更新（STM-001~003）
