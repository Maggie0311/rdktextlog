# MEMORY-INDEX — code_reviewer (R-004) 记忆总表

> 更新规则：每次晋升/降级/遗忘/新增后同步本表。读取记忆时**先看本表**。
> 生成时间: 2026-09-23

## 长期记忆 (long-term)

| ID | 标题 | 状态 | 置信度 | 证据数 | 显著性 | 最近使用 | 文件 |
|---|---|---|---|---|---|---|---|
| LTM-001 | 审查者绝不修改被审代码 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-001-reviewer-never-fixes.md` |
| LTM-002 | PASS 必须挣来（覆盖声明 + 验证证据 + 零阻断） | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-002-pass-must-be-earned.md` |
| LTM-003 | 发现项五要素，缺一即无效 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-003-finding-needs-five-elements.md` |
| LTM-004 | 级别门槛是双向的 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-004-severity-thresholds-are-bidirectional.md` |
| LTM-005 | 用户标准优先级最高且不可删改 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-005-user-standards-outrank-and-are-untouchable.md` |
| LTM-006 | 不瞒报：不降级、不隐去、不用模糊结论 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-006-no-underreporting.md` |
| LTM-007 | 结论绑定 commit hash，代码一变即失效 | active | 1.00 | 3 | medium | 2026-09-23 | `long-term/LTM-007-report-is-bound-to-a-commit-hash.md` |
| LTM-008 | 结论独立于指令 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-008-conclusion-independent-of-instruction.md` |
| LTM-009 | 审查结论 ≠ 验收结论；范围外只能 INFO | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-009-review-verdict-is-not-acceptance.md` |
| LTM-010 | 审查不得成为瓶颈 | active | 1.00 | 3 | medium | 2026-09-23 | `long-term/LTM-010-review-must-not-become-bottleneck.md` |

**统计**：active 10 条；candidate 0；dormant 0；deprecated 0。
**经验型条目：0 条**（本角色尚未做过一次真实审查；这是诚实状态）。

## 短期记忆 (short-term) — 容量上限 12

| ID | 标题 | 状态 | 置信度 | 证据数 | 最近使用 | 晋升还差什么 |
|---|---|---|---|---|---|---|
| STM-001 | 验证留档先于报告（动作完成即落盘验证区，报告只做引用与判定；断点可零重做续完） | active | 0.70 | 1 | 2026-09-29 | 再经历 ≥1 次不同形态断点/交接场景确认留档粒度足够（见 STM-001 待验证节） |

**统计**：1 / 12 条，剩余容量 11。

## 读取建议

1. 默认依据：`status: active` 且 `confidence >= 0.60`（当前为 LTM-001~010 全部）。
2. 全部 LTM 均为 `innate`（规则继承），**不是经验**；不得据此声称"实践证明"。
3. 短时记忆为空——本角色当前**没有任何经过验证的审查经验**；遇到拿不准的判断，
   应按 `SEVERITY` 门槛保守定级或标 `unverified`，而不是凭直觉下重结论。

## 待办（记忆层面）

- [x] 首次真实审查后：写 `STM-001`，并初始化 `script/REVIEW-STATS.md`（STATS 已于 R1 建立；STM-001 于 2026-09-29 T-20260928-004 断点续完轮写入）
- [ ] 出现第一次申诉后：记录申诉采纳情况并复核 LTM-003 / LTM-004 是否需要修订
- [ ] 出现第一次后验漏报（审查通过但后续暴露缺陷）后：复核 LTM-002 的覆盖声明要求是否足够
- [ ] 每次用到某条 LTM 时更新其 `last_used`（再巩固）
