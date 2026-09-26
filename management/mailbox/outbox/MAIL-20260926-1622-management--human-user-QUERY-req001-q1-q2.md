---
mail_id: MAIL-20260926-1622-management--human-user-QUERY-req001-q1-q2
thread: THREAD-LOG-P0
from: management
to: human-user
cc: []
date: 2026-09-26 16:22
purpose: QUERY
priority: P1
deadline: 2026-09-27 23:59
requires_reply: true
attachments: []
references:
  - management/script/REQ-20260926-001-logging.md
---

## 致：人类用户（项目委托人）——需求已受理拆解并派工，两个关键问题请示

### 已完成（无需你操作）
1. 你的需求已受理并拆解：`management/script/REQ-20260926-001-logging.md`（平台日志设施盘点、分阶段思路、P0 任务 AC）；
2. 你的原件 `from_human/开发节奏规划.docx` 已登记（INTAKE-LOG #1，未做任何改动）；
3. 首个开发任务 `T-20260926-001-logging-platform-p0` 已派给 `developer`（初步平台 rmlog：C/Python 双端、错误码五域、双时间戳、可靠落盘、读端工具、场下使用方法 USAGE.md），deadline 2026-09-27 23:59；交付前将强制过 `code_reviewer` 审查。

### 请示 Q1：初步开发代码在哪跑？（影响"可运行"验收证据形态）
| 选项 | 内容 | 影响 |
|---|---|---|
| A（建议） | 交付后由你按 USAGE.md 在板端跑自测，回贴输出；`software_tester` 以该输出为板端证据 | 最小闭环；需要你约 10 分钟；证据链完整 |
| B | 你提供板子的 SSH 远程访问方式（IP/账号/授权），`software_tester` 自行适配环境实测 | 证据最全；你需提供访问凭据并接受远端操作 |
| C | 本轮仅开发机自测 + 交付自测代码，板端验证推迟到 P1 | 最快；但 AC1/AC8 的"实机可运行"缺证据，需你书面接受该缺口 |

### 请示 Q2：部署身份与路径（默认值确认，不影响开工）
默认：以 root 运行、日志落 `/userdata/rmlog/`（若该分区不存在则 `/var/log/rmlog/`），均做成可配置项。是否认可？有偏好（如专用非 root 用户、挂载点约定）请直接说明。

### 回复方式
直接在对话里回复选项即可（如："Q1 选 A，Q2 认可"）。deadline 前回复均不影响开发进行中。
