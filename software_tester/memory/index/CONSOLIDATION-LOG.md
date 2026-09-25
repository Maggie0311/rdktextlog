# CONSOLIDATION-LOG — software_tester 记忆固化流水

> 只追加。记录每一次晋升 / 降级 / 遗忘 / 新增 / 破例。
> 格式：`[日期] <动作> <记忆ID> | 理由 | 证据 | 操作人`

| 日期 | 动作 | 记忆 ID | 理由 | 证据 | 操作人 |
|---|---|---|---|---|---|
| 2026-09-25 | innate | LTM-001 | 用户明令不得修改程序与源码；属强制约束（本能） | 用户指令 + TN1/TN2 | framework_admin |
| 2026-09-25 | innate | LTM-002 | 来自架构 v1.2 §2.1 与 TN9 | 规范条款 | framework_admin |
| 2026-09-25 | innate | LTM-003 | 来自用户"仅在需要的时候"与 TP2 | 用户指令 + 规范条款 | framework_admin |
| 2026-09-25 | innate | LTM-004 | 来自架构 v1.3 §7 **V8** 与 TN3/TN4 | 根规范条款 | framework_admin |
| 2026-09-25 | innate | LTM-005 | 来自 §4 冻结字段 5/8 与 TP9/TP10 | 规范条款 | framework_admin |
| 2026-09-25 | innate | LTM-006 | 来自 §4 冻结字段 7/9 与 TP11/TP12 | 规范条款 | framework_admin |
| 2026-09-25 | innate | LTM-007 | 来自用户"环境由他决定与适配" + T6 + TP5 | 用户指令 + 规范条款 | framework_admin |
| 2026-09-25 | innate | LTM-008 | 来自用户"恰当的手段" + TP6 | 用户指令 + 规范条款 | framework_admin |
| 2026-09-25 | innate | LTM-009 | 来自 TN5/TN6 与 §4 结论边界 | 规范条款 | framework_admin |
| 2026-09-25 | innate | LTM-010 | 来自 §0 权力轴与架构 v1.3 §7 V8 | 规范条款 | framework_admin |

## 待处理晋升候选

无。短期记忆为空（0 条），不存在晋升候选。

## 说明

本角色为**新建角色（引导）**：长期记忆全部以 `promoted_from: innate` 由强制约束直接注入（依据见 `memory/README.md` 的置信度初始值条款）。
自 STM-001 起，一切经验型记忆**必须**走 §4.3 的五条件晋升规则，不得绕过。

> 审计提示（framework_admin）：本角色的核心能力（能否真实运行被测程序、能否采到运行反馈）**至今未经任何实测**——
> `script/ENVIRONMENTS.md` 现阶段**全部条目标为"假设"**。这是缺口 **G7**，必须由其上岗首任务实测回填。
> 在此之前，任何"可以测试/可以烧录"的承诺都不成立（LTM-006：契约≠证据）。
