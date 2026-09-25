# memory/ — developer 的记忆系统

| 子目录 | 用途 |
|---|---|
| `long-term/` | 已固化的信念（confidence ≥ 0.75，且通过晋升规则） |
| `short-term/` | 最近任务的工作记忆（滑动窗口，上限 12 条） |
| `index/` | `MEMORY-INDEX.md` 总表、`CONSOLIDATION-LOG.md` 晋升流水 |

**记忆规则（本节即全部要求，无需查阅他处）**

- 文件命名：长期 `LTM-<NNN>-<slug>.md`、短期 `STM-<NNN>-<slug>.md`；**一条一个文件**
- front matter 必填：`id / title / layer / status / confidence / evidence_count / success_count / failure_count / source_tasks / first_seen / last_used / last_reviewed / salience / decay_rate / tags`
- 置信度初始值：单一任务观察 **0.30**；踩坑并复盘 **0.40**（`salience: high`）；来自强制约束的"本能"条目 **1.00** 直接入长期
- 更新：应用成功 **+0.10**；失败/不适用 **−0.15**；被独立确认 **+0.15**；被有证据反驳 **−0.25**；闲置一轮 **−decay_rate**（高显著性减半）
- 区间：0.00–0.29 假设（只可写短期）/ 0.30–0.59 候选 / 0.60–0.79 可信（长期须为 `candidate`）/ 0.80–1.00 信念
- **晋升 5 条件（须同时满足）**：① `confidence ≥ 0.75`；② `evidence_count ≥ 3` 且来自 ≥2 个不同任务；③ 至少 1 次主动应用成功；④ 至少 1 次被另一方角色或审计**独立确认**；⑤ 长期中无冲突条目
- 衰减：`< 0.45` → `dormant`；`< 0.25` 或闲置 > 20 轮 → 移出长期；高显著性永不自动删除
- 短期**上限 12 条**；读取先看 `index/MEMORY-INDEX.md`，默认依据仅限 `active` 且 `confidence ≥ 0.60`
- 禁止：单次观察当信念；修改历史证据表（只能追加）

本角色的记忆重点（与治理层不同）：**实现经验**——踩过的坑、约束条件、可复用的做法、
"这个接口的隐藏前提是什么"。不记录任务归属与优先级判断（那是 management 的记忆职责，本角色不得代写）。
