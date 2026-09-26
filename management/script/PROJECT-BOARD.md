# PROJECT-BOARD — 全局进度台账（唯一真相源）

> 维护者：`management` (R-002)。字段冻结见 `role-limit/ROLE-LIMIT.md §4`。
> 状态取值：`pending / assigned / in-progress / blocked / submitted / accepted / rejected / cancelled`。

| task_id | thread | 主责角色 | 状态 | 依赖 | 路由理由 | 计划完成 | 最近更新 | 证据/交付物路径 | 验收结论 |
|---|---|---|---|---|---|---|---|---|---|
| T-20260926-001-logging-platform-p0 | THREAD-LOG-P0 | developer | assigned | 无（前置已由人类完成：镜像/WiFi/rt_patch） | 唯一主责=developer：产出是源码+实现说明，命中 D1–D5/D7（其 ROLE-LIMIT §1）；management 不写码（MN2）；审查由 code_reviewer 在交付门必经（R-004 CR1）；实机测试是否进行待 Q1 裁决后定（R-005 T1） | 2026-09-27 | 2026-09-26 16:20 | 需求依据：`management/script/REQ-20260926-001-logging.md`；任务书：`developer/mailbox/inbox/MAIL-20260926-1620-management--developer-TASK-T-20260926-001-logging-platform-p0.md` | — |

## 里程碑（对应 `from_human/开发节奏规划.docx` 阶段）

| 里程碑 | 内容 | 对应任务 | 状态 |
|---|---|---|---|
| M1：初步文本日志平台可用 | rmlog 记得到/落得下/查得出 + 场下使用方法 | T-20260926-001 | in-flight |
| M2：比赛可用（阶段一收口） | 自启动/黑匣子/快照包/与节拍线程和SPI模块对接 | 待立（T-001 验收后） | pending |
| M3：稳定高性能（对应规划阶段三） | 性能优化/长跑验证/从机日志回传/CI | 远期 | pending |
