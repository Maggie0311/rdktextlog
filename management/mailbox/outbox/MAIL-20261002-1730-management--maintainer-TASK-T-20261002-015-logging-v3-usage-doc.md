---
mail_id: MAIL-20261002-1730-management--maintainer-TASK-T-20261002-015-logging-v3-usage-doc
thread: THREAD-LOG-V3
from: management
to: maintainer
cc: []
date: 2026-10-02 17:30
purpose: TASK
priority: P1
deadline: 2026-10-03 12:00
requires_reply: true
attachments: []
references:
  - maintainer/code_archive/变更说明-v2.md
  - developer/script/IMPL-T-20261001-logging-v3.md
  - maintainer/code_archive/T-20261001-logging-v3/WALKTHROUGH-001.md
  - maintainer/code_archive/T-20261001-logging-v3/SPEC-001.md
  - software_tester/script/TESTREPORT-T-20261002-014-001.md
---

## 1. 背景 (Context)

人类用户第三次指出同一类问题：**v3 归档缺"用户使用说明"**（v1 靠 USAGE 重构补过、v2 靠变更说明-v2.md 补过，v3 这次又漏了）。根因：management 未把"用户使用说明"列为版本归档必备件。本任务补齐 v3，且**此后每个版本的归档都以本任务产物为模板**。

## 2. 目的 (Objective)

产出面向电控队员（会 C/Python、不要求 Linux 专家）的 **v3 用户使用说明** `变更说明-v3.md`，镜像 v2 的 `变更说明-v2.md` 结构，回答两问：**v3 相比 v2 新增了什么？用户怎么用？**

## 3. 交付（落 `maintainer/code_archive/`，全部增量、不改已归档 code/）

1. **`变更说明-v3.md`**（核心，用户视角，结构对齐 v2）：
   - §0 一句话结论（v3 在 v2 之上"加自动层"：v2 用法全兼容）；
   - §1 **v3 新增功能表**（功能/是什么/解决什么痛点/对应文件，逐条带 file:line）：黑匣子环形缓冲+错误前快照、崩溃遗言（保留 core dump）、dmesg/温度/电压/内存监控、心跳看门狗+systemd WatchdogSec、错误码字符串+24bit 双轨、Linux/STM32 公共头文件单源生成、日志统计 CLI、LogRuntime 一键初始化；
   - §2 **用户使用方法**（重点，每条给可复制的代码/命令）：① 怎么初始化（`LogRuntime` 或分模块导入）；② 怎么周期性喂心跳 + 高频样本（黑匣子样本）；③ 怎么启动通信/资源监控器；④ 出错时**自动**发生什么（黑匣子快照/崩溃遗言/监控事件）；⑤ 赛后怎么查（`rmlog_read` 统计 CLI、按错误码/会话过滤）；
   - §3 **注意点/迁移**：异步队列满丢（dropped）、黑匣子快照保留上限（max_snapshots）、板端 core dump 需放开 ulimit、下位机共用 `rmlog_schema.h` 的生成方式、systemd 实装待板端、开发机默认目录 /userdata 需 set_default_writer；
   - §4 **事实边界**：板端已验证（selftest 13/13、smoke、监控读真实 dmesg/温度/内存）vs unverified（systemd 实装重启、sd_notify 投递、断电/压力、真实 SPI/CAN/电压、1kHz 硬实时、板端 core 放开）；
   - 文末注记"本文对应框架 DIFF 概念，是 v2→v3 的用户向差异；完整差异见 DIFF-001.md"。
2. **更新 `maintainer/code_archive/README.md` 导航**：读者→文档映射表加入"想上手用 v3 → USAGE + 变更说明-v3.md"，命名术语表补"变更说明-v3.md = v3 用户使用说明"；
3. **GLOSSARY.md 增补** v3 用户会接触的术语（LogRuntime、黑匣子、环形缓冲、快照、喂狗/WatchdogSec、24bit 错误码等，若未覆盖）；
4. RESULT → management（副本自留 outbox）；worklog 追加；git 提交（先 status + diff --cached 核对，按路径显式 add 自己文件，禁 -A/.，commit 含 task_id）。

## 4. 约束与准确性

- 内容逐条对齐**代码事实**（读 `developer/script/rmlog/{auto,blackbox,crash,monitors,resources,code_map,daemon}.py`、`rmlog_read.py`、`shared/rmlog_schema.h`、`IMPL-T-20261001-logging-v3.md`）与**板端事实**（TESTREPORT-T-20261002-014-001），不得编造命令/API；
- 推断标"推断"、未验证标 unverified；用户视角少术语多可复制命令。
