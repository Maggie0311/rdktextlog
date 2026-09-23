# memory/ — management 的记忆系统

| 子目录 | 用途 |
|---|---|
| `long-term/` | 已固化的信念（confidence ≥ 0.75，且通过晋升规则） |
| `short-term/` | 最近任务的工作记忆（滑动窗口，上限 12 条） |
| `index/` | `MEMORY-INDEX.md` 总表、`CONSOLIDATION-LOG.md` 晋升流水 |

规则见 `_framework/03-MEMORY-MODEL.md`。

本角色的记忆重点（与专家角色不同）：**调度经验**——哪类任务该派给谁、哪种拆解粒度不返工、哪些阻塞模式会重复出现。
不记录业务技术结论（那是专家角色的记忆职责，本角色不得代写）。
