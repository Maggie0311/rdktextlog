# MEMORY-INDEX — management (R-002) 记忆总表

> 更新规则：每次晋升/降级/遗忘/新增后同步本表。读取记忆时**先看本表**。
> 生成时间: 2026-09-23 · **2026-09-26 新增**：LTM-007（人类输入文件通道，依 `DECISION-20260926-011` 以 innate 注入）

## 长期记忆 (long-term)

| ID | 标题 | 状态 | 置信度 | 证据数 | 显著性 | 最近使用 | 文件 |
|---|---|---|---|---|---|---|---|
| LTM-001 | 编排权不含角色定义权，建角色只能由 framework_admin 执行 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-001-orchestrate-not-define.md` |
| LTM-002 | 每个任务有且仅有一个主责角色，禁止双主责 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-002-single-owner-per-task.md` |
| LTM-003 | 派活与协作必须落邮箱，未落邮箱即不存在 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-003-assignment-must-be-mailed.md` |
| LTM-004 | 进度唯一真相源是 PROJECT-BOARD，口头进度不算数 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-004-board-is-single-truth.md` |
| LTM-005 | 需求不可静默缩减；不可逆决策与范围变更必须请示人类用户 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-005-scope-belongs-to-user.md` |
| LTM-006 | 能力缺口只上报不自查自办；指挥不下场 | active | 1.00 | 3 | high | 2026-09-23 | `long-term/LTM-006-escalate-not-improvise.md` |
| **LTM-007** | **人类投放的文件是一手依据：只读、登记、以路径引用，绝不改动** | active | 1.00 | 3 | high | 2026-09-26 | `long-term/LTM-007-human-files-are-input-evidence.md` |

**统计**：active 7 条；candidate 0；dormant 0；deprecated 0。
**经验型条目：0 条**（本角色尚未执行真实调度任务；这是诚实状态）。

## 短期记忆 (short-term) — 容量上限 12

| ID | 标题 | 状态 | 置信度 | 证据数 | 最近使用 | 晋升还差什么 |
|---|---|---|---|---|---|---|
| — | （空） | — | — | — | — | 需先有真实任务，禁止硬凑 |

**统计**：0 / 12 条，剩余容量 12。

## 读取建议

1. 默认依据：`status: active` 且 `confidence >= 0.60`（当前为 LTM-001~007 全部）。
2. 全部 LTM 均为 `innate`（强制约束），不是经验；**不得**据此声称"实践证明"。
3. 短时记忆为空——本角色当前**没有任何经过验证的调度经验**，遇到边界判断应发 QUERY 给 framework_admin，而不是凭感觉。

## 待办（记忆层面）

- [ ] 上岗后：完成 WELCOME 首个任务（读规范 + 建 PROJECT-BOARD 骨架），并写 STM-001
- [ ] **每次开工先扫 `from_human/`**（人类可能在你不在时投放文件）——与 `INTAKE-LOG.md` 对比，未登记的立即处理
- [ ] 首个需求分派完成后：复核 LTM-004 是否获真实支持证据
- [ ] 发生第一次打回返工后：把"拆解粒度"经验写成 STM
- [ ] 每次用到某条 LTM 时更新其 `last_used`（再巩固）
