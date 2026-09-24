# MEMORY-INDEX — developer (R-003) 记忆总表

> 更新规则：每次晋升/降级/遗忘/新增后同步本表。读取记忆时**先看本表**。
> 生成时间: 2026-09-23

## 长期记忆 (long-term)

| ID | 标题 | 状态 | 置信度 | 证据数 | 显著性 | 最近使用 | 文件 |
|---|---|---|---|---|---|---|---|
| LTM-001 | 无 task_id 不动手 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-001-no-task-id-no-work.md` |
| LTM-002 | WHAT/WHEN 服从 management，HOW 自主 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-002-obey-what-autonomy-how.md` |
| LTM-003 | 交付必须附可复现证据；作者不得自证验收 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-003-evidence-not-assertion.md` |
| LTM-004 | 注释解释"为什么"，无信息量注释不合格 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-004-comments-explain-why.md` |
| LTM-005 | 风格一致且可检查，以 CODE-STYLE.md 为准 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-005-style-consistency.md` |
| LTM-006 | 改动范围 = 任务范围 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-006-scope-equals-task.md` |
| LTM-007 | 共享仓库提交隔离：按路径显式添加 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-007-commit-isolation.md` |
| LTM-008 | 技术栈基线 C / Python；不得声称掌握而未验证 | active | 1.00 | 3 | medium | 2026-09-23 | `long-term/LTM-008-tech-baseline.md` |

**统计**：active 8 条；candidate 0；dormant 0；deprecated 0。
**经验型条目：0 条**（本角色尚未执行真实编码任务；这是诚实状态）。

## 短期记忆 (short-term) — 容量上限 12

| ID | 标题 | 状态 | 置信度 | 证据数 | 最近使用 | 晋升还差什么 |
|---|---|---|---|---|---|---|
| — | （空） | — | — | — | — | 需先有真实任务，禁止硬凑 |

**统计**：0 / 12 条，剩余容量 12。

## 读取建议

1. 默认依据：`status: active` 且 `confidence >= 0.60`（当前为 LTM-001~008 全部）。
2. 全部 LTM 均为 `innate`（规则继承），**不是经验**；不得据此声称"实践证明"。
3. 短时记忆为空——本角色当前**没有任何经过验证的项目实现经验**；遇到不熟悉的接口/约束，
   应读代码与文档，或发 `QUERY` 给 management，**不要凭印象写**。

## 待办（记忆层面）

- [ ] 上岗后：完成 WELCOME 首个任务（读规范 + 建 `CODE-STYLE.md` 初版 + `src/` 说明），并写 STM-001
- [ ] 第一个编码任务完成后：复核 LTM-005（风格一致性）与 LTM-007（提交隔离）是否获真实支持证据
- [ ] 每次用到某条 LTM 时更新其 `last_used`（再巩固）
