# PROJECT-BOARD — 全局进度台账（唯一真相源）

> 维护者：`management` (R-002)。字段冻结见 `role-limit/ROLE-LIMIT.md §4`。
> 状态取值：`pending / assigned / in-progress / blocked / submitted / accepted / rejected / cancelled`。

| task_id | thread | 主责角色 | 状态 | 依赖 | 路由理由 | 计划完成 | 最近更新 | 证据/交付物路径 | 验收结论 |
|---|---|---|---|---|---|---|---|---|---|
| T-20260926-001-logging-platform-p0 | THREAD-LOG-P0 | developer | accepted（已归档·版本001） | 无（前置已由人类完成：镜像/WiFi/rt_patch） | 唯一主责=developer；审查门必经；角色由 management 会话以 subagent 上岗，只采信落盘证据；全链：R0 f3331b0（CONDITIONAL）→ R1 45eeb04（PASS）→ R2 a675c8d（复审 FAIL 拦截 RF-6）→ R3 2d83644（终审 PASS）→ **R4 164d4c7（T-003 linux-build-fix，复审 PASS + 板端复测全绿）**；验收报告 v2：**accepted**；**maintainer 归档完成（版本 001，三份要件 164d4c7 一致，补注 +130/-0，RESULT MAIL-20260928-2135，留档 75eae7f）** | 2026-09-27 15:10 | 2026-09-28 21:40 | 验收报告 v2 `management/script/ACCEPT-20260927-logging-p0.md`；审查链五份报告；板端证据 TESTREPORT-T-20260927-{002-001,003-001}.md；**归档 `maintainer/code_archive/T-20260926-001-logging-platform-p0/`（SPEC/WALKTHROUGH/QUESTIONS/DIFF/VERSION/GLOSSARY 全套）** | **accepted（已归档）** |
| T-20260927-002-logging-boardtest-ssh | THREAD-LOG-P0 | software_tester | completed | T-001（被测对象=commit 2d83644）；SSH 凭据已由人类用户提供 | 唯一主责=software_tester；板端 IPv6 直连实测；Q1 selftest 11/13 FAIL（AC4/RF-6 因 C 探针编译失败）、Q2 平台核查已采集（python3 3.10.12；/userdata 存在；journald 持久化；rsyslog active；coredumpctl 不可用；dmesg ISO 可用）、Q3 Linux 多进程×轮转 PASS（1200==1200 无静默销毁）、Q4 板端 gcc 编译 rmlog.c FAIL（CLOCK_MONOTONIC 未声明+3×format-truncation）；发现阻断级问题未发 HANDOFF（契约 §2.1.5） | 2026-09-27 23:59 | 2026-09-27 21:53 | TESTREPORT-T-20260927-002-001.md / TESTPLAN-T-20260927-002.md；RESULT MAIL-20260927-2153；ISSUE MAIL-20260927-2153（→developer）；commit 8970849 | 报告已出（含阻断项，交 T-003） |
| T-20260927-003-logging-c-linux-build | THREAD-LOG-P0 | developer | accepted | T-002 板端实测结论（C 端目标平台编译失败） | 唯一主责=developer；修复 commit **164d4c7**（`_POSIX_C_SOURCE 200809L` + 轮转副本缓冲 528 可证安全 + selftest 板端 `-lpthread` + 文档同步）；复审 **PASS**（`REVIEW-T-20260927-003-164d4c7.md`，留档 8ac36fa）；**板端聚焦复测全绿**（TESTREPORT-T-20260927-003-001.md：R-Q1 13/13、R-Q4 stderr 0 字节、R-Q3 无回归；tester HANDOFF 已发，留档 23c9116） | 2026-09-28 12:00 | 2026-09-28 20:05 | 任务书 `developer/mailbox/inbox/MAIL-20260927-2157-…c-linux-build.md`；复审报告 `code_reviewer/script/REVIEW-T-20260927-003-164d4c7.md`；复测报告 `software_tester/script/TESTREPORT-T-20260927-003-001.md`；RESULT MAIL-20260928-1958 | **accepted** |
| T-20260928-004-usage-rewrite | THREAD-LOG-P0 | developer | accepted（已归档·版本002） | 人类用户审查意见（2026-09-28）：USAGE 视角错位 + 板端自测章节过时 | 唯一主责=developer；USAGE.md 重构为用户优先手册（快速上手/日常使用/比赛日操作流/FAQ），删除过时板端自测章节；**代码零变更**；交付 commit **08f6ce8**；复审 **PASS 零发现项**；management 验收 **accepted**（ACCEPT v3）；**maintainer 版本 002 增量归档完成**（v002/code + VERSION-002 + DIFF-002，三份要件均指向 08f6ce8，补注 +13/-0 KN3 校验通过，RESULT MAIL-20260929-2015，留档 4c6606c） | 2026-09-29 12:00 | 2026-09-29 20:20 | 复审 `code_reviewer/script/REVIEW-T-20260928-004-08f6ce8.md`；验收 `ACCEPT-…p0.md` v3；**归档 `maintainer/code_archive/T-20260926-001-logging-platform-p0/v002/`** | **accepted（已归档）** |

## 里程碑（对应 `from_human/开发节奏规划.docx` 阶段）

| 里程碑 | 内容 | 对应任务 | 状态 |
|---|---|---|---|
| M1：初步文本日志平台可用 | rmlog 记得到/落得下/查得出 + 场下使用方法 | T-20260926-001 / T-003 | **done（2026-09-28 归档版本 001，commit 164d4c7）** |
| M2：比赛可用（阶段一收口） | 自启动/黑匣子/快照包/与节拍线程和SPI模块对接 | 待立（T-001 验收后） | pending |
| M3：稳定高性能（对应规划阶段三） | 性能优化/长跑验证/从机日志回传/CI | 远期 | pending |
