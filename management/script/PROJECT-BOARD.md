# PROJECT-BOARD — 全局进度台账（唯一真相源）

> 维护者：`management` (R-002)。字段冻结见 `role-limit/ROLE-LIMIT.md §4`。
> 状态取值：`pending / assigned / in-progress / blocked / submitted / accepted / rejected / cancelled`。

| task_id | thread | 主责角色 | 状态 | 依赖 | 路由理由 | 计划完成 | 最近更新 | 证据/交付物路径 | 验收结论 |
|---|---|---|---|---|---|---|---|---|---|
| T-20260926-001-logging-platform-p0 | THREAD-LOG-P0 | developer | submitted | 无（前置已由人类完成：镜像/WiFi/rt_patch） | 唯一主责=developer；审查门必经；角色由 management 会话以 subagent 上岗，只采信落盘证据；全链：R0 f3331b0（首轮 CONDITIONAL，2 严重）→裁定 AC5 含多进程×轮转→FAIL→R1 45eeb04（复审 PASS）→R2 a675c8d（RF 复审 FAIL，拦截修复引入的 RF-6 句柄泄漏）→R3 **2d83644（终审 PASS，三重口径核销，零新发现）**；developer 备料 maintainer（HANDOFF 1505）+最终 RESULT（1505）；**management 验收 accepted（有条件）**：板端 AC1/AC8 证据经 Q1 修订（A→B，DECISION MAIL-20260927-1525）改由 software_tester SSH 实测出具，矛盾项将降级 rejected | 2026-09-27 15:10 | 2026-09-27 15:25 | 验收报告 `management/script/ACCEPT-20260927-logging-p0.md`；审查链：REVIEW-…-{f3331b0,45eeb04,rf-a675c8d,rf6-2d83644}.md；交付终版 2d83644（7d1adc2=收尾提交）；信件 HANDOFF/RESULT MAIL-20260927-1505 | **accepted（有条件）** |
| T-20260927-002-logging-boardtest-ssh | THREAD-LOG-P0 | software_tester | pending | T-001（被测对象=commit 2d83644）；待人类用户提供 SSH 访问信息 | 唯一主责=software_tester（命中其 ROLE-LIMIT T1–T8/T12：运行环境适配与事实采集）；测试问题清单：AC1 板端可运行（selftest 13/13）、AC8 平台核查探测命令、UV-1 Linux 多进程×轮转实测、UV-3 板端 gcc 编译；安全边界=仅板端自建工作目录活动、不改系统配置、源码仅用副本 | 待 SSH 信息到位后 4 小时内出 TESTPLAN，测试当日出 TESTREPORT | 2026-09-27 15:25 | 裁决修订：`management/mailbox/outbox/MAIL-20260927-1525-management-decision-req001-q1-amend-b.md`；TASK 待凭据到位后下发 | — |

## 里程碑（对应 `from_human/开发节奏规划.docx` 阶段）

| 里程碑 | 内容 | 对应任务 | 状态 |
|---|---|---|---|
| M1：初步文本日志平台可用 | rmlog 记得到/落得下/查得出 + 场下使用方法 | T-20260926-001 | in-flight |
| M2：比赛可用（阶段一收口） | 自启动/黑匣子/快照包/与节拍线程和SPI模块对接 | 待立（T-001 验收后） | pending |
| M3：稳定高性能（对应规划阶段三） | 性能优化/长跑验证/从机日志回传/CI | 远期 | pending |
