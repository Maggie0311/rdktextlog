# DIFF-001 — T-20260930-005-logging-v2

本版为 `T-20260930-005-logging-v2` 首次归档，上一版不存在；相对上一候选 `136ed68`，developer/reviewer 记录的修复主题为有界容量校验、轮转副本导出、持续 daemon、flush 完成等待和开发机验证边界澄清。

## 归档差异

- 来源：`3148fedec9f39dbf95184cdfd72ffb8bd605e892`，由 git archive 逐字节复制。
- 带注副本：只在归档 `code/` 的若干 Python/C 文件头新增 maintainer 注释；未改 developer 原产物、字符串、语句、宏或格式。
- 归档策略：测试日志与 `.gitignore` 等非源码留在来源，可由 commit 重建；代码、文档、服务模板和 smoke 源码入档。
- 旧归档：既有 `T-20260926-001-logging-platform-p0` v001/v002 零修改；`management/from_human` 零修改。

## 事实边界

review PASS、tester report 和 ACCEPT 都只支持开发机范围；X5 aarch64、板端 systemd、真实硬件、断电、硬实时与长跑容量均保持 `unverified`。本文件不作质量或发布裁定。
