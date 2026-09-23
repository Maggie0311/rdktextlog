# MEMORY-INDEX — framework_admin (R-001) 记忆总表

> 更新规则：每次晋升/降级/遗忘/新增后同步本表。读取记忆时**先看本表**。
> 生成时间: 2026-02-14

## 长期记忆 (long-term)

| ID | 标题 | 状态 | 置信度 | 证据数 | 显著性 | 最近使用 | 文件 |
|---|---|---|---|---|---|---|---|
| LTM-001 | 角色边界用负向清单定义，正向清单只作补充 | active | 1.00 | 3 | high | 2026-02-14 | `long-term/LTM-001-boundary-as-negative-space.md` |
| LTM-002 | 每个动作/产物有且仅有一个主责角色 | active | 1.00 | 3 | high | 2026-02-14 | `long-term/LTM-002-single-owner.md` |
| LTM-003 | 跨角色协作只能经邮箱留痕 | active | 1.00 | 3 | high | 2026-02-14 | `long-term/LTM-003-cross-role-via-mailbox.md` |
| LTM-004 | 接口即契约，变更须先 NOTIFY 并给兼容期 | active | 0.85 | 2 | medium | 2026-02-14 | `long-term/LTM-004-interface-freeze.md` |
| LTM-005 | 记忆分层是状态而非等级，未验证经验不得入长期 | active | 1.00 | 3 | high | 2026-02-14 | `long-term/LTM-005-memory-is-state-not-rank.md` |
| LTM-006 | 框架初始发布只算 1 个证据源，置信度封顶 0.85 | active | 0.80 | 2 | high | 2026-02-14 | `long-term/LTM-006-bootstrap-confidence.md` |

**统计**：active 6 条；candidate 0；dormant 0；deprecated 0。

## 短期记忆 (short-term) — 容量上限 12

| ID | 标题 | 状态 | 置信度 | 证据数 | 最近使用 | 晋升还差什么 |
|---|---|---|---|---|---|---|
| STM-001 | 七目录必须连同逐目录写入规则一起交付 | candidate | 0.35 | 1 | 2026-02-14 | 需在创建下一个角色时验证；置信度需 +0.40，证据需 ≥3 且跨 2 任务 |
| STM-002 | 架构管理员最大失焦风险是被拉去做业务产出 | candidate | 0.40 | 1 | 2026-02-14 | 需 2 次真实越界压力场景；需 1 次独立确认 |
| STM-003 | 邮件元数据不全将使协作时间线不可重建 | candidate | 0.35 | 1 | 2026-02-14 | 需 ≥10 封真实邮件后做时间线重建实验 |

**统计**：3 / 12 条，剩余容量 9。

## 读取建议

1. 默认依据：`status: active` 且 `confidence >= 0.60`（当前为 LTM-001~006 全部）。
2. 仅作提示、需重新验证：所有 STM 条目与 `candidate` 状态条目。
3. LTM-004 虽为 active，但证据仅来自设计期，**应用于真实接口变更后必须复核**。

## 待办（记忆层面）

- [ ] 用户口令："创建多个角色分工" -> 触发 STM-001 的验证（含"边界正交性自检"）
- [ ] 出现第一封真实邮件后复核 STM-003
- [ ] 出现第一次越界压力后复核 STM-002
- [ ] 首个角色创建后，对本角色全部 LTM 做一次再巩固复核（更新 last_reviewed）
