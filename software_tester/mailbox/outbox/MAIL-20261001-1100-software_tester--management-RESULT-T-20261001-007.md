---
mail_id: MAIL-20261001-1100-software_tester--management-RESULT-T-20261001-007
thread: THREAD-LOG-V2
from: software_tester
to: management
cc: [developer, code_reviewer]
date: 2026-10-01 11:00
purpose: RESULT
priority: P1
deadline: 候选 commit 产生后
requires_reply: false
attachments: []
references:
  - MAIL-20261001-0920-management--software_tester-TASK-v2-validation
  - software_tester/script/TESTPLAN-T-20261001-007.md
  - software_tester/script/TESTREPORT-T-20261001-007-001.md
---

## RESULT — T-20261001-007-v2-validation

### 被测对象

最终候选 commit：`3148fedec9f39dbf95184cdfd72ffb8bd605e892`。测试证据提交：`410fae3`（仅 software_tester 测试计划、报告和原始输出）。

### 本机实测

- 原 13 项 selftest：退出码 0，`13/13 通过`。
- v2 smoke：退出码 0，`accepted=1 dropped=9`。
- 五域故障注入：init/comm/hw/fsm/sys 五次均退出码 0，分别观察到 `E-INIT-001`、`E-COMM-004`、`E-HW-001`、`E-FSM-003`、`E-SYS-002`。
- 队列边界：`maxsize=0` 拒绝；容量 1 的 30 次入队为 `accepted=1 dropped=29`；close 后线程退出。
- 轮转导出：4 个日志成员均被扫描，session 导出 `7/7 lines`。
- daemon TERM：SIGTERM 后退出码 0，启动/停止事件均落盘。
- 导出降级：缺失业务日志报告 `MISSING`，kernel 命令报告 `UNAVAILABLE`，未伪造成功。

### 待验与边界

本轮未访问/运行 RDK X5；板端编译运行、systemd 安装重启、断电、1 kHz 硬实时和真实硬件/通信接入均待验。未使用历史板端结果替代新版证据。详情及原始输出见测试报告与 `software_tester/script/work/T-20261001-007/raw/`。

software_tester (R-005)
2026-10-01 11:00
