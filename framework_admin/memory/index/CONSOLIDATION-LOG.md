# CONSOLIDATION-LOG — framework_admin 记忆固化流水

> 只追加。记录每一次晋升 / 降级 / 遗忘 / 新增 / 破例。
> 格式：`[日期] <动作> <记忆ID> | 理由 | 证据 | 操作人`

| 日期 | 动作 | 记忆 ID | 理由 | 证据 | 操作人 |
|---|---|---|---|---|---|
| 2026-02-14 | innate | LTM-001 | 来自 `_framework/00-ARCHITECTURE §6` 与本角色 N 清单，属强制约束（本能），非经验 | 规范条款 | framework_admin |
| 2026-02-14 | innate | LTM-002 | 来自 `01-ROLE-REGISTRY` 边界正交性自检要求 | 规范条款 | framework_admin |
| 2026-02-14 | innate | LTM-003 | 来自 `02-MAILBOX-PROTOCOL §5` 硬性礼节 | 规范条款 | framework_admin |
| 2026-02-14 | innate | LTM-004 | 来自 `04-ROLE-CONTRACT-TEMPLATE §4` 接口冻结条款 | 规范条款 | framework_admin |
| 2026-02-14 | innate | LTM-005 | 来自 `03-MEMORY-MODEL §1` | 规范条款 | framework_admin |
| 2026-02-14 | innate | LTM-006 | 自我约束：对设计期结论实施置信度封顶，防止自证 | 自审 | framework_admin |
| 2026-02-14 | new-stm | STM-001 | 本次 bootstrap 任务的观察，尚未跨任务验证 | T-2026-02-14-bootstrap | framework_admin |
| 2026-02-14 | new-stm | STM-002 | 本次 bootstrap 任务的观察，尚需真实越界压力验证 | T-2026-02-14-bootstrap | framework_admin |
| 2026-02-14 | new-stm | STM-003 | 本次 bootstrap 任务的观察，需真实邮件流验证 | T-2026-02-14-bootstrap | framework_admin |
| 2026-09-23 | review | LTM-001~006 | 新角色创建后的**首次再巩固复核**：更新 `last_used/last_reviewed`；LTM-004 本轮属预防性应用，**不计证据**，维持 0.85 | T-2026-09-23-create-management-role | framework_admin |
| 2026-09-23 | reinforce | STM-001 | 在创建 R-002 时**主动应用并成功**（第 2 次证据）：31 文件骨架连同逐目录写入规则一次性交付 | T-2026-09-23-create-management-role | framework_admin |
| 2026-09-23 | reject-promotion | STM-001 | 晋升判定：`evidence_count=2 < 3` 且无独立确认，不满足 §4.3 条件 2 与条件 4 | T-2026-09-23-create-management-role | framework_admin |
| 2026-09-23 | new-stm | STM-004 | 本轮新观察：相邻角色的边界必须按"层"切分而非"级别"切分（6 项冲突面靠层切分全部裁定） | T-2026-09-23-create-management-role | framework_admin |
| 2026-09-23 | reinforce | STM-001 | 创建 R-003 时**第 3 次应用成功**（跨 2 个任务）：34 文件骨架连同写入规则交付，规格逐项核对无缺项。0.45 -> 0.55 | T-2026-09-23-create-developer-role | framework_admin |
| 2026-09-23 | reinforce | STM-004 | **跨任务复现成立**：7 项冲突面（含新增的"决定怎么写"）靠分层消解。0.35 -> 0.45。同时暴露适用前提：存在指挥关系时须再分 WHAT/WHEN 与 HOW | T-2026-09-23-create-developer-role | framework_admin |
| 2026-09-23 | new-stm | STM-005 | 本轮新观察：引入指挥链时必须写明可判定的服从范围，否则专家角色会退化为传声筒或以"同级"为由拒活 | T-2026-09-23-create-developer-role | framework_admin |
| 2026-09-23 | reject-promotion | STM-001 / STM-004 | 晋升判定：证据数与跨任务数已达标，但**均缺 §4.3 条件 4 的独立确认**（全部证据同源，本角色自产）。维持 candidate | T-2026-09-23-create-developer-role | framework_admin |
| 2026-09-23 | reinforce | STM-001 | 创建 R-004 时**第 4 次应用成功**（3 任务 / 4 证据）：46 文件骨架 + 10 份标准连同写入规则交付。0.55 -> 0.65 | T-2026-09-23-create-code-reviewer-role | framework_admin |
| 2026-09-23 | reinforce | STM-004 | **第 3 次跨任务复现**：审查权与验收权按"回答什么问题"分层切开。0.45 -> 0.55 | T-2026-09-23-create-code-reviewer-role | framework_admin |
| 2026-09-23 | reinforce | STM-005 | **第 2 次证据（跨任务复现）**，同时暴露需扩展：面对判断型角色时轴应换成 PROCESS vs VERDICT。0.35 -> 0.45 | T-2026-09-23-create-code-reviewer-role | framework_admin |
| 2026-09-23 | new-stm | STM-006 | 本轮新观察：判断型角色的独立性必须落在结论生成环节，且改变结论的唯一合法输入是证据 | T-2026-09-23-create-code-reviewer-role | framework_admin |
| 2026-09-23 | reject-promotion | STM-001 | 第 3 次晋升判定：证据充分（4 条 / 3 任务），但置信度 0.65 < 0.75 且**仍缺独立确认**。维持 candidate，缺口已收窄为两项 | T-2026-09-23-create-code-reviewer-role | framework_admin |
| 2026-09-24 | new-stm | STM-007 | **踩坑并复盘**（记忆模型 §4.1 第 2 条，confidence 0.40 / salience high）：我在角色目录之外自设 `src/` 产物区，与 `00-ARCHITECTURE §2` 对 `script/` 的定义相矛盾，由委托层指出并废止 | T-2026-09-24-fix-artifact-area | framework_admin |
| 2026-09-24 | invalidate | （设计结论） | 受 `DECISION-20260924-005` 影响：本角色名下**不再存在**任何以 `src/` 为前提的设计结论；相关表述已在规范与角色文本中清除，历史件保留但交叉引用替代件 | T-2026-09-24-fix-artifact-area | framework_admin |
| 2026-09-25 | innate | **LTM-007** | **委托层确立的原则**写入根规范 `00-ARCHITECTURE v1.2 §2.1`，属强制约束（本能），非经验。confidence 1.00 直入长期（记忆模型 §4.1 第 3 条） | 用户指令 + 规范条款 | framework_admin |
| 2026-09-25 | reinforce | STM-007 | 委托层将其确认为一般原则（**+0.15 独立确认**），0.40 -> 0.55；该条已上升为 LTM-007，**不再走 §4.3 晋升**，作为原则的来源保留 | T-2026-09-25-elevate-self-sufficiency | framework_admin |
| 2026-09-25 | reinforce | STM-001 | 创建 R-005 时**第 5 次应用成功**（4 任务 / 5 证据）：37 文件骨架 + 能力清单骨架。0.65 -> 0.75 | T-2026-09-25-create-software-tester-role | framework_admin |
| 2026-09-25 | reject-promotion | STM-001 | **第 4 次晋升判定：仍不晋升，但已满足 4/5 条件**（置信度 0.75 达标、5 证据、跨 4 任务、4 次主动应用）。唯一缺口是条件 4 的**独立确认**——本条自 2026-02-14 起全部由本角色自产自证 | T-2026-09-25-create-software-tester-role | framework_admin |
| 2026-09-25 | reinforce | STM-004 | **第 4 次跨任务复现**：与 R-004 邻接的新角色靠"产出物性质"（静态判断 vs 动态事实）切开。0.55 -> 0.65 | T-2026-09-25-create-software-tester-role | framework_admin |
| 2026-09-25 | new-stm | STM-008 | 本轮新观察：**能力型角色**（能力取决于外部条件而非自身判断）必须随角色交付"能力清单骨架 + 实测首任务"，否则"未标状态"会被读成"已具备"，最终以伪造结果（V8）形式爆掉 | T-2026-09-25-create-software-tester-role | framework_admin |

## 待处理晋升候选

**STM-001 已达标但卡在独立确认**：置信度 0.75、证据 5 条、跨 4 个任务、4 次主动应用成功——条件 1/2/3 全满足，唯一缺口是 §4.3 条件 4（**独立确认**）。
其余 7 条置信度均 < 0.75（最高 STM-004 的 0.65）。**STM-001 已充分满足条件 1、2、3**（证据 4 条 / 跨 3 任务 / 3 次主动应用成功），**缺口已收窄为两项**：置信度仍差 0.10，以及条件 4 的独立确认。按 P12，自产证据不可替代外部确认，故不晋升。

## 说明

本次为**引导（bootstrap）轮**：长期记忆全部以 `promoted_from: innate` 身份由强制规范直接注入，
这是记忆模型 §4.1 第 3 条例外（`_framework/` 强制约束 `confidence = 1.00` 直接入长期）。
自 STM-001~003 起，一切经验型记忆**必须**走 §4.3 的五条件晋升规则。
