# memory/ — framework_admin 的记忆系统

| 子目录 | 用途 |
|---|---|
| `long-term/` | 已固化的信念（confidence ≥ 0.75，且通过晋升规则） |
| `short-term/` | 最近任务的工作记忆（滑动窗口，上限 12 条） |
| `index/` | `MEMORY-INDEX.md` 总表、`CONSOLIDATION-LOG.md` 晋升流水 |

规则见 `_framework/03-MEMORY-MODEL.md`。
