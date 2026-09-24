# memory/ — developer 的记忆系统

| 子目录 | 用途 |
|---|---|
| `long-term/` | 已固化的信念（confidence ≥ 0.75，且通过晋升规则） |
| `short-term/` | 最近任务的工作记忆（滑动窗口，上限 12 条） |
| `index/` | `MEMORY-INDEX.md` 总表、`CONSOLIDATION-LOG.md` 晋升流水 |

规则见 `_framework/03-MEMORY-MODEL.md`。

本角色的记忆重点（与治理层不同）：**实现经验**——踩过的坑、约束条件、可复用的做法、
"这个接口的隐藏前提是什么"。不记录任务归属与优先级判断（那是 management 的记忆职责，本角色不得代写）。
