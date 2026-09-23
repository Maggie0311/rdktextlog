# script/ — 产物与脚本

本角色产出的可复用资产。**本角色的产物是"项目级的编排产物"，不是业务交付物**：

| 产物 | 命名 | 说明 |
|---|---|---|
| 需求拆解书 | `REQ-<YYYYMMDD>-<slug>.md` | WBS：task_id / 主责角色 / AC / 依赖 |
| 全局进度台账 | `PROJECT-BOARD.md` | **唯一真相源**，字段冻结见 ROLE-LIMIT §4 |
| 验收报告 | `ACCEPT-<YYYYMMDD>-<slug>.md` | 逐条 AC 的结论 + 证据路径 |
| 产物登记 | `INDEX.md` | 本表 |

规范：命名 `<slug>.<ext>`，重大变更另存 `-v2` 不覆盖；**每个产物必须登记到 `INDEX.md`**。
