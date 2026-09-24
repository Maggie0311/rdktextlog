# memory/ — code_reviewer 的记忆系统

| 子目录 | 用途 |
|---|---|
| `long-term/` | 已固化的信念（confidence ≥ 0.75，且通过晋升规则） |
| `short-term/` | 最近任务的工作记忆（滑动窗口，上限 12 条） |
| `index/` | `MEMORY-INDEX.md` 总表、`CONSOLIDATION-LOG.md` 晋升流水 |

规则见 `_framework/03-MEMORY-MODEL.md`。

本角色的记忆重点（与开发者不同）：**审查经验**——哪类缺陷容易漏、哪类判断容易被申诉推翻、哪种表述能减少往返。
**注意**：本角色的 `standard/` 是给所有人看的**公共标准**，而 `memory/` 是它自己的**私有经验**，两者不得混放。
