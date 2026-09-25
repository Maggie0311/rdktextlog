# memory/ — management 的记忆系统

| 子目录 | 用途 |
|---|---|
| `long-term/` | 已固化的信念（confidence ≥ 0.75，且通过晋升规则） |
| `short-term/` | 最近任务的工作记忆（滑动窗口，上限 12 条） |
| `index/` | `MEMORY-INDEX.md` 总表、`CONSOLIDATION-LOG.md` 晋升流水 |

**记忆规则（本节即全部要求，无需查阅他处）**

- 文件命名：长期 `LTM-<NNN>-<slug>.md`、短期 `STM-<NNN>-<slug>.md`；**一条一个文件**，原子化
- front matter 必填：`id / title / layer / status / confidence / evidence_count / success_count / failure_count / source_tasks / first_seen / last_used / last_reviewed / salience / decay_rate / tags`（短期再用 `promoted_to` 代替 `promoted_from`）
- 置信度初始值：单一任务观察 **0.30**；踩坑并复盘 **0.40**（`salience: high`）；来自强制约束的"本能"条目 **1.00** 并直接入长期
- 置信度更新：应用成功 **+0.10**；失败或不适用 **−0.15**（须补写"适用条件"）；被独立确认 **+0.15**；被有证据地反驳 **−0.25**；闲置一轮 **−decay_rate**（高显著性减半）
- 区间语义：0.00–0.29 假设（只可写短期，**禁止**据此做不可逆决策）/ 0.30–0.59 候选 / 0.60–0.79 可信（可入长期但状态为 `candidate`）/ 0.80–1.00 信念
- **晋升到长期须同时满足 5 条**：① `confidence ≥ 0.75`；② `evidence_count ≥ 3` 且来自 **≥2 个不同任务**；③ 至少 1 次**主动应用并成功**；④ 至少 1 次被**另一方角色或审计独立确认**；⑤ 长期中无冲突条目
- 衰减与遗忘：`confidence < 0.45` → `dormant`；`< 0.25` 或闲置 > 20 轮 → 移出长期（记 `forgot`）；高显著性条目衰减减半且永不自动删除
- 短期容量 **上限 12 条**，超出时丢弃 `confidence` 最低且 `salience: low` 者
- 读取姿势：先看 `index/MEMORY-INDEX.md` 总表；默认依据仅限 `status: active` 且 `confidence ≥ 0.60`；用到某条须更新其 `last_used` 与计数
- 禁止：把单次观察当信念；修改历史证据表（只能追加）；无证据提高他人条目置信度

本角色的记忆重点（与专家角色不同）：**调度经验**——哪类任务该派给谁、哪种拆解粒度不返工、哪些阻塞模式会重复出现。
不记录业务技术结论（那是专家角色的记忆职责，本角色不得代写）。
