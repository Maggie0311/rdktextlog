# PROJECT-BOARD — 全局进度台账（唯一真相源）

> 维护者：`management` (R-002)。字段冻结见 `role-limit/ROLE-LIMIT.md §4`。
> 状态取值：`pending / assigned / in-progress / blocked / submitted / accepted / rejected / cancelled`。

| task_id | thread | 主责角色 | 状态 | 依赖 | 路由理由 | 计划完成 | 最近更新 | 证据/交付物路径 | 验收结论 |
|---|---|---|---|---|---|---|---|---|---|
| T-20260926-001-logging-platform-p0 | THREAD-LOG-P0 | developer | submitted | 无（前置已由人类完成：镜像/WiFi/rt_patch） | 唯一主责=developer；审查门必经；角色由 management 会话以 subagent 上岗，只采信落盘证据；全链：R0 f3331b0（首轮 CONDITIONAL，2 严重）→裁定 AC5 含多进程×轮转→FAIL→R1 45eeb04（复审 PASS）→R2 a675c8d（RF 复审 FAIL，拦截修复引入的 RF-6 句柄泄漏）→R3 **2d83644（终审 PASS，三重口径核销，零新发现）**；management 验收 accepted（有条件）；**板端实测（T-002）发现条件未满足：C 端目标平台不可编译（Q4 FAIL）+ selftest 11/13（Q1）→ 开 T-003 修复，归档冻结** | 2026-09-27 15:10 | 2026-09-27 21:57 | 验收报告 `management/script/ACCEPT-20260927-logging-p0.md`；审查链：REVIEW-…-{f3331b0,45eeb04,rf-a675c8d,rf6-2d83644}.md；交付终版 2d83644；板端证据 TESTREPORT-T-20260927-002-001.md | **accepted（有条件，板端 C 构建项未满足→T-003）** |
| T-20260927-002-logging-boardtest-ssh | THREAD-LOG-P0 | software_tester | completed | T-001（被测对象=commit 2d83644）；SSH 凭据已由人类用户提供 | 唯一主责=software_tester；板端 IPv6 直连实测；Q1 selftest 11/13 FAIL（AC4/RF-6 因 C 探针编译失败）、Q2 平台核查已采集（python3 3.10.12；/userdata 存在；journald 持久化；rsyslog active；coredumpctl 不可用；dmesg ISO 可用）、Q3 Linux 多进程×轮转 PASS（1200==1200 无静默销毁）、Q4 板端 gcc 编译 rmlog.c FAIL（CLOCK_MONOTONIC 未声明+3×format-truncation）；发现阻断级问题未发 HANDOFF（契约 §2.1.5） | 2026-09-27 23:59 | 2026-09-27 21:53 | TESTREPORT-T-20260927-002-001.md / TESTPLAN-T-20260927-002.md；RESULT MAIL-20260927-2153；ISSUE MAIL-20260927-2153（→developer）；commit 8970849 | 报告已出（含阻断项，交 T-003） |
| T-20260927-003-logging-c-linux-build | THREAD-LOG-P0 | developer | in-progress（复审 PASS，待板端复测） | T-002 板端实测结论（C 端目标平台编译失败） | 唯一主责=developer；修复 commit **164d4c7**（`_POSIX_C_SOURCE 200809L` + 轮转副本缓冲 528 可证安全 + selftest 板端 `-lpthread` + 文档同步）；复审 **PASS**（`REVIEW-T-20260927-003-164d4c7.md`，留档 8ac36fa）：5 项核销、format-truncation 为可证安全根因修复（非压制）、Windows 13/13+零告警独立复验、Linux 侧标 unverified；**待 software_tester 板端复测坐实**（Q1 13/13 + Q4 零警告），通过后回填验收并解冻归档 | 2026-09-28 12:00 | 2026-09-28 19:35 | 任务书 `developer/mailbox/inbox/MAIL-20260927-2157-…c-linux-build.md`；复审报告 `code_reviewer/script/REVIEW-T-20260927-003-164d4c7.md`；修复 commit 164d4c7（HEAD d3d0cfe） | —（待板端复测） |

## 里程碑（对应 `from_human/开发节奏规划.docx` 阶段）

| 里程碑 | 内容 | 对应任务 | 状态 |
|---|---|---|---|
| M1：初步文本日志平台可用 | rmlog 记得到/落得下/查得出 + 场下使用方法 | T-20260926-001 | in-flight |
| M2：比赛可用（阶段一收口） | 自启动/黑匣子/快照包/与节拍线程和SPI模块对接 | 待立（T-001 验收后） | pending |
| M3：稳定高性能（对应规划阶段三） | 性能优化/长跑验证/从机日志回传/CI | 远期 | pending |
