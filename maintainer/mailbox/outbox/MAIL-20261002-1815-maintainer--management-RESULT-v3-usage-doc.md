---
mail_id: MAIL-20261002-1815-maintainer--management-RESULT-v3-usage-doc
thread: THREAD-LOG-V3
from: maintainer
to: management
cc: []
date: 2026-10-02 18:15
purpose: RESULT
priority: P1
requires_reply: false
attachments: []
references:
  - maintainer/mailbox/inbox/MAIL-20261002-1730-management--maintainer-TASK-T-20261002-015-logging-v3-usage-doc.md
  - maintainer/code_archive/变更说明-v3.md
  - maintainer/code_archive/变更说明-v2.md
  - maintainer/code_archive/README.md
  - maintainer/script/GLOSSARY.md
  - developer/script/IMPL-T-20261001-logging-v3.md
  - maintainer/code_archive/T-20261001-logging-v3/SPEC-001.md
  - maintainer/code_archive/T-20261001-logging-v3/WALKTHROUGH-001.md
  - software_tester/script/TESTREPORT-T-20261002-014-001.md
---

## RESULT — T-20261002-015 补 v3 用户使用说明完成

依 TASK `MAIL-20261002-1730` §3 完成增量交付，全部落 `maintainer/` 下，**未改已归档 `code/`、未改 developer 源码、未触碰他方未提交改动**。内容逐条对齐代码事实（`file:line` 取自来源 commit `d77d36c`，工作树 `developer/script` 与其逐字节一致）与板端事实（`TESTREPORT-T-20261002-014-001`）；推断与 `unverified` 均显式标注（KN6/KN13）。

### 1. 三个交付物

1. `maintainer/code_archive/变更说明-v3.md`（**新建**，本任务核心）：镜像 v2 版结构——§0 一句话结论 / §1 v3 新增功能表（9 项，逐条 `file:line`）/ §2 用户使用方法（初始化 / 喂数据 / 启动监控器 / 出错自动发生什么 / 赛后怎么查，全为可复制代码命令，取自真实 API）/ §3 注意点迁移（6 条）/ §4 事实边界（板端已验证 vs `unverified`）/ 文末 DIFF 关系注记；
2. `maintainer/code_archive/README.md`（**更新**导航）：读者→文档映射表加"想上手用 v3"与"想知道 v3 相比 v2"等行，命名术语表补"变更说明-v3.md = v3 用户使用说明"，§2 归档关系升为 v1/v2/v3 三列，§4 目录结构补 v3 行；
3. `maintainer/script/GLOSSARY.md`（**增补** +2 条）：快照（blackbox snapshot / .jsonl）、喂狗/心跳看门狗（heartbeat / HeartbeatWatchdog）——其余 v3 术语（LogRuntime、黑匣子、环形缓冲、崩溃遗言、sd_notify、WatchdogSec、错误率滑动窗口、24bit 双轨码、公共头、资源监控、stats）已随 004 收录，不重复。

### 2. §2 用户使用方法提炼出的「三件事」

1. **初始化**（一句话）：`runtime = LogRuntime(writer, "<dir>/blackbox", session=session)` —— 一个对象把日志写入 + 黑匣子 + 会话合成一处（`rmlog/auto.py:19`），或分模块导入 `BlackBox` / `install_signal_hooks`。
2. **喂数据**（一句话）：`runtime.heartbeat("main")` 喂心跳 + `runtime.sample(kind, **v)` 喂高频样本（只进内存）+ `runtime.emit(code, module, msg)` 写事件——写 ERROR/FATAL 时自动倒黑匣子快照并补 `E-SYS-005`。
3. **查日志**（一句话）：`python3 rmlog_read.py stats|filter <log>` 按错误码/级别/会话统计与过滤定位，黑匣子快照直接 `cat blackbox-*.jsonl` 回放错误前窗口。

### 3. 收尾

worklog 已追加（#9）；git 提交含 task_id `T-20261002-015`，按路径显式 add 自身文件（变更说明-v3.md / README.md / GLOSSARY.md / RESULT×2 / worklog），禁 `-A`/`.`，未触碰他方未提交改动（任务邮件两个未跟踪文件留待 management 侧处理）。

maintainer (R-006)
2026-10-02 18:15
