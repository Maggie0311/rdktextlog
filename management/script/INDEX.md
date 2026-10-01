# script/INDEX — management 产物登记表

> 规则：任何新增/重大变更的产物必须在此登记。重大变更另存 `-v2`，不覆盖。

| # | 产物 | 路径 | 类型 | 版本 | 创建日期 | 最近验证 | 消费者 |
|---|---|---|---|---|---|---|---|
| 1 | 需求拆解书（RDK X5 RoboMaster 文本日志系统） | `script/REQ-20260926-001-logging.md` | REQ | v1.1（§7.1 追加裁决记录） | 2026-09-26 | 2026-09-27 | 全体角色、人类用户 |
| 2 | 全局进度台账（唯一真相源） | `script/PROJECT-BOARD.md` | BOARD | v1（随任务流转持续更新） | 2026-09-26 | 2026-10-01 | 人类用户、全体角色 |
| 3 | 验收报告（T-001，accepted） | `script/ACCEPT-20260927-logging-p0.md` | ACCEPT | v3（v2 板端证据 / v3 v2 收口追记） | 2026-09-27 | 2026-10-01 | developer、maintainer、code_reviewer、software_tester、人类用户 |
| 4 | v2 验收报告 | `script/ACCEPT-20261001-logging-v2.md` | ACCEPT | v1 | 2026-10-01 | 2026-10-01 | 全体角色、人类用户 |
| 5 | logging 下一版开发规划（v3 路线图，融合两方案） | `script/REQ-20261001-logging-v3-roadmap.md` | REQ/ROADMAP | v1 | 2026-10-01 | 2026-10-01 | 人类用户、全体角色 |

**在产（进行中，完成后转入上表）**：

| 产物 | 用途 | 触发条件 | 当前状态 |
|---|---|---|---|
| M2 立项（logging 下一版任务拆解） | 依 v3 路线图 P0–P3 拆成可验收任务并派发 | 人类用户启动"开始 M2/下一版" | 待触发（路线图已立：REQ-20261001-logging-v3-roadmap.md） |
