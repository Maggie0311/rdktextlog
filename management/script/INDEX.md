# script/INDEX — management 产物登记表

> 规则：任何新增/重大变更的产物必须在此登记。重大变更另存 `-v2`，不覆盖。

| # | 产物 | 路径 | 类型 | 版本 | 创建日期 | 最近验证 | 消费者 |
|---|---|---|---|---|---|---|---|
| 1 | 需求拆解书（RDK X5 RoboMaster 文本日志系统） | `script/REQ-20260926-001-logging.md` | REQ | v1.1（§7.1 追加裁决记录） | 2026-09-26 | 2026-09-27 | 全体角色、人类用户 |
| 2 | 全局进度台账（唯一真相源） | `script/PROJECT-BOARD.md` | BOARD | v1（随任务流转持续更新） | 2026-09-26 | 2026-09-27 | 人类用户、全体角色 |
| 3 | 验收报告（T-001，accepted 有条件） | `script/ACCEPT-20260927-logging-p0.md` | ACCEPT | v1 | 2026-09-27 | 2026-09-27 | developer、maintainer、code_reviewer、software_tester、人类用户 |

**在产（进行中，完成后转入上表）**：

| 产物 | 用途 | 触发条件 | 当前状态 |
|---|---|---|---|
| `PLAN-20260926-req001-logging-p0.md`（位于 `plan/`） | 首个需求第一轮分派的编排计划 | 2026-09-26 受理 REQ-001 | done（分派/跟进/验收已完成；里程碑 M2 规划另立计划） |
| maintainer 归档包（SPEC/WALKTHROUGH/VERSION 等） | T-001 归档 | maintainer 依 ACCEPT + HANDOFF + 终审 PASS 三要件执行 | maintainer 侧待执行（已获归档许可） |
| 板端证据核验任务（software_tester） | 用户回贴板端自测输出后核验 | 用户回贴 | 待触发 |
