# MEMORY-INDEX — maintainer (R-006) 记忆总表

> 生成时间: 2026-09-26

## 长期记忆 (long-term)

| ID | 标题 | 状态 | 置信度 | 证据数 | 显著性 | 最近使用 | 文件 |
|---|---|---|---|---|---|---|---|
| LTM-001 | 归档即冻结：归档件字节永不可变 | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-001-archive-means-frozen.md` |
| LTM-002 | 先齐备再归档：两封合格确认通知缺一不可 | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-002-both-notices-before-archiving.md` |
| LTM-003 | 补注只加注释行，绝不改代码 | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-003-annotate-comments-only.md` |
| **LTM-004** | **错误的解释比没有解释更危险：说不准就标 unverified** | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-004-wrong-explanation-worse-than-none.md` |
| LTM-005 | 事实与推断必须分开写 | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-005-facts-separated-from-inference.md` |
| LTM-006 | 解释必须可定位（file:line） | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-006-explanations-must-be-locatable.md` |
| LTM-007 | 不做质量裁定、不做验收 | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-007-no-quality-verdict-no-acceptance.md` |
| LTM-008 | 只读来源、只报不修 | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-008-read-only-sources-report-dont-fix.md` |
| LTM-009 | 墓碑也是资产，版本不可删 | active | 1.00 | 3 | medium | 2026-09-26 | `long-term/LTM-009-tombstones-are-assets.md` |
| LTM-010 | code_archive 与 mailbox/archive 不混用 | active | 1.00 | 3 | medium | 2026-09-26 | `long-term/LTM-010-code-archive-is-not-mail-archive.md` |
| LTM-011 | 答疑等于承诺：先读后答 | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-011-answering-is-a-commitment.md` |

**统计**：active 11 条；candidate 0。**经验型条目：0 条**（尚未归档过任何产物；诚实状态）。

## 短期记忆 (short-term) — 容量上限 12

| ID | 标题 | 状态 | 置信度 | 证据数 | 最近使用 | 晋升还差什么 |
|---|---|---|---|---|---|---|
| — | （空） | — | — | — | — | 需先有真实归档任务，禁止硬凑 |

**统计**：0 / 12 条，剩余容量 12。

## 读取建议

1. 默认依据：`status: active` 且 `confidence ≥ 0.60`（当前为 LTM-001~011 全部）。
2. 全部 LTM 均为 `innate`（规则继承），**不是经验**；不得据此声称"实践证明"。
3. **特别提醒**：`LTM-004` 是本角色的核心风险条款——它约束的不是"我说什么"，而是"我**不**说什么"。

## 待办（记忆层面）

- [ ] 首次真实归档后：写 `STM-001`；检验说明书是否真的让人只看它就理解了代码结构
- [ ] 出现第一次**解释错误**（被用户或 developer 纠正）后：立即写 STM，并复核 `LTM-004/005`
- [ ] 出现第一次答疑高峰（用户连续追问）后：分析哪类问题最常被问，考虑把它写进说明书标准节
- [ ] 每次用到某条 LTM 时更新其 `last_used`
