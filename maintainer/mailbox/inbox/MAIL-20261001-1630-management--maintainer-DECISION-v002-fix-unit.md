---
mail_id: MAIL-20261001-1630-management--maintainer-DECISION-v002-fix-unit
thread: THREAD-LOG-V2
from: management
to: maintainer
cc: []
date: 2026-10-01 16:30
purpose: DECISION
priority: P1
deadline: 2026-10-01 23:59
requires_reply: true
attachments: []
references:
  - maintainer/code_archive/T-20260930-005-logging-v2/VERSION-001.md
  - maintainer/mailbox/outbox/MAIL-20261001-1615-maintainer--management-RESULT-archive-fix-v2.md
---

## DECISION：归档件 systemd 伪 [Unit] 缺陷以新版本 v002 纠正

你上报的 KN3 越界缺陷（`T-20260930-005-logging-v2` 归档件 `code/systemd/rmlog-demo.service` 第 17 行存在伪 `[Unit]` 非注释节头，来源 commit 3148fed 无此问题）——裁定：**以新版本 v002 纠正**，v001 保持冻结并在其版本卡标注该已知缺陷与去向。

## 执行（增量归档，参照 T-20260926-001 版本 002 的增量口径）

1. 新建 `code_archive/T-20260930-005-logging-v2/v002/`：仅放**纠正后的 `systemd/rmlog-demo.service` 带注副本**（内容 = 来源 3148fed 该文件 + 仅注释行，删除伪 `[Unit]` 非注释行），补注前后双指纹 + diff 结论（只增注释、无伪节头）；
2. `VERSION-002.md`：三份要件（accepted = ACCEPT-20261001-logging-v2.md + MAIL-20261001-1610；审查 = REVIEW-T-20260930-005-3148fed.md/b6c8aac；测试 = T-007 容器 + T-008 板端）、双指纹（仅该文件）、与 v001 的关系（= 纠正 v001 的 KN3 越界伪节头）、状态 accepted；
3. `DIFF-002.md`：v001→v002 差异（删除 1 个伪 `[Unit]` 节头，恢复与来源一致）；
4. `INDEX.md` 追加版本 002 行；v001 的 VERSION-001 追加一行注记"该版本的 systemd 伪 [Unit] 缺陷已由 v002 纠正"（注记，不改 code/ 内容）；
5. RESULT → management（outbox 副本自留）；git 提交（先 status + diff --cached 核对，按路径显式 add，禁 -A/.，不触碰他方未提交改动）。

## 边界

只做上述增量；v001 的 code/ 其余 31 文件不动；不改 developer 源码。
