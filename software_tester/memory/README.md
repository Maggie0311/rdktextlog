# memory/ — software_tester 的记忆系统

| 子目录 | 用途 |
|---|---|
| `long-term/` | 已固化的信念（confidence ≥ 0.75，且通过晋升规则） |
| `short-term/` | 最近任务的工作记忆（滑动窗口，上限 12 条） |
| `index/` | `MEMORY-INDEX.md` 总表、`CONSOLIDATION-LOG.md` 晋升流水 |

规则见 `_framework/03-MEMORY-MODEL.md`。

本角色的记忆重点（与开发者、审查者都不同）：**运行环境的经验**——哪台机器/哪块板子怎么接、
哪种手段能采到哪类反馈、哪种失败模式会重复出现、哪些"看起来像缺陷"其实是环境导致的。
**注意**：环境能力清单是 `script/ENVIRONMENTS.md`（给全体看的公共资产），
`memory/` 是本角色**私有经验**，两者不得混放。
