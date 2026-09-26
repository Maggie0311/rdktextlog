---
mail_id: MAIL-20260926-1640-management--developer-TASK-req001-q1q2-decision
thread: THREAD-LOG-P0
from: management
to: developer
cc: []
date: 2026-09-26 16:40
purpose: TASK
priority: P1
deadline: 2026-09-27 23:59
requires_reply: false
attachments: []
references:
  - management/script/REQ-20260926-001-logging.md
  - developer/mailbox/inbox/MAIL-20260926-1620-management--developer-TASK-T-20260926-001-logging-platform-p0.md
  - management/mailbox/outbox/MAIL-20260926-1635-management-decision-req001-q1q2.md
---

## TASK 增补：T-20260926-001-logging-platform-p0 —— Q1/Q2 用户裁决与交付证据形态

（本信是对原 TASK 邮件的**增补**，不改动原 AC 编号与范围；deadline 不变。）

## 1. 人类用户已裁决（DECISION 已留痕，见 references）

- **Q1 = A**：板端"可运行"证据 = **人类用户按 USAGE.md 在 RDK X5 板端运行自测并回贴输出**；`software_tester` 后续以该输出为板端证据（届时另立小任务）；
- **Q2 = 认可默认值**：root + `/userdata/rmlog/`（路径不存在时回退 `/var/log/rmlog/`），全部做成可配置项。

## 2. 对交付形态的增补要求（并入 AC1/AC7/AC8 的执行细则）

1. **开发机证据（你交付时随 RESULT 提供）**：本开发机已具备 Windows + Python 3.13/3.14（`python`/`python3`）+ gcc 13.2（MinGW）+ git 2.53；`python3 -m rmlog.selftest` 与 C 侧自测（gcc 编译运行）的原始输出摘要随 RESULT 附上；
2. **USAGE.md 新增一等章节「板端自测步骤（用户执行）」**：面向非 Linux 专家的精确命令序列（含 `python3 --version` 等探测命令）、每步预期输出样式、需要回贴哪些输出（完整/截断规则）、以及 3–5 条常见失败的排查指引——用户将在赛后/场下独立照做，此章节质量直接决定 AC1 证据能否产生；
3. **平台差异如实标注**：Windows 开发机与 X5/Linux 在文件追加原子性（O_APPEND 语义）、路径分隔、权限模型上的差异写入 IMPL"已知风险与未覆盖项"；**不得**把 Windows 自测结果表述为 Linux 已验证——板端验证按 Q1=A 由用户实测补齐；
4. **板端不可得的信息**（板端 python3 版本、`/userdata` 分区是否存在等）继续按 AC8 处理：标"未核实"+ 给出用户可在板端执行的探测命令（可并入 USAGE 板端自测章节）。

## 3. 备注

对以上增补有异议或发现不可行点，按你的契约 D12 发 QUERY 给我；默认视为接受，随 RESULT 一并体现。
