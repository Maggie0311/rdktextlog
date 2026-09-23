# 邮箱通信协议 (Mailbox Protocol)

> 版本: v1.0 · 维护者: framework_admin
> 邮箱是角色间**唯一的正式工作交互通道**。口头/隐式协作不算数。

---

## 1. 文件命名

```
MAIL-<YYYYMMDD>-<HHMM>-<from>--<to>-<CATEGORY>-<slug>.md
```
示例：`MAIL-20260214-1030-framework_admin--data_curator-TASK-build-corpus.md`

- 时间用本地时间，24 小时制。
- slug 用英文小写连字符，3~6 词。
- 同一线程多封信：在文件名末尾追加 `-r2`、`-r3`。

## 2. 目录流转

| 目录 | 含义 | 规则 |
|---|---|---|
| `mailbox/inbox/` | 别人发给我的、尚未处理的信 | 开工必读；处理完移入 `archive/` |
| `mailbox/outbox/` | 我发出的信（保留副本） | 发出后不得修改，追加更正信 |
| `mailbox/archive/YYYY-MM/` | 已处理/已关闭 | 只读，永久保留 |
| `mailbox/drafts/` | 未定稿 | 定稿后复制到 outbox 并删除草稿 |

> **铁律**：inbox 里长期滞留未归档的信 = 未完成的工作。每轮收工前必须清空 inbox。

---

## 3. 邮件正文标准结构（强制齐全）

```markdown
---
mail_id: MAIL-20260214-1030-framework_admin--data_curator-TASK-build-corpus
thread: THREAD-0007-corpus-build
from: framework_admin
to: data_curator
cc: []
date: 2026-02-14 10:30
purpose: TASK
priority: P1
deadline: 2026-02-16 18:00
requires_reply: true
attachments: []
references: []
---

## 1. 背景 (Context)
为什么会有这封信。上游发生了什么。

## 2. 目的 (Objective)
一句话说清这封信要达成什么。

## 3. 请求 / 交付物 (Request & Deliverable)
- 具体要对方做什么（动词开头，可验收）
- 交付物形态：文件路径 / 格式 / 命名

## 4. 约束与边界 (Constraints)
- 必须遵守的：...
- 明确不要做的：...

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 ...
- [ ] AC2 ...

## 6. 期望回复 (Expected Reply)
回复类别（ACK/RESULT/QUERY/ISSUE）+ 最迟时间

## 7. 备注 (Notes)
风险、依赖、参考文件。
```

### 字段说明

| 字段 | 取值 | 说明 |
|---|---|---|
| `purpose` | TASK/QUERY/RESULT/ACK/HANDOFF/ISSUE/NOTIFY/DECISION | 见下表 |
| `priority` | P0/P1/P2/P3 | P0=立即中断当前工作处理 |
| `requires_reply` | true/false | 是否强制回信 |
| `references` | 文件路径列表 | 必须可被对方直接打开 |

---

## 4. 目的类型（消息语义契约）

| 类别 | 发起方意图 | 收方义务 | 最迟响应 |
|---|---|---|---|
| **TASK** | 派活 | 必须 ACK，再 RESULT 或 ISSUE | ACK ≤ 1 轮内 |
| **QUERY** | 问问题 | 必须 ANSWER（用 RESULT 类） | ≤ 2 轮内 |
| **RESULT** | 交付成果 | 必须 ACK 或提出 ISSUE | ≤ 1 轮内 |
| **ACK** | 确认收到 | 无需再回 | — |
| **HANDOFF** | 交接责任 | 必须 ACK 正式接手 | ≤ 1 轮内 |
| **ISSUE** | 报告阻塞/缺陷 | 必须 DECISION 或 TASK | ≤ 1 轮内 |
| **NOTIFY** | 单方告知 | 无需回（除非有异议） | — |
| **DECISION** | 仲裁结论 | 必须执行，可申诉一次 | — |

> **禁止**：用 NOTIFY 传递需要对方行动的内容（那是 TASK）；用 RESULT 传递未经验收的产物。

---

## 5. 通信礼节（硬性）

1. **开工先读信**：任何任务开始前，必须先读 `mailbox/inbox/`。
2. **一件事一封信**：不要把两个不相关的请求塞进同一封 TASK。
3. **可追溯**：所有 `references` 必须是真实存在的路径；提到他人文件必须给路径。
4. **闭环**：收到 TASK/QUERY/ISSUE 而超过时限未回，视为角色失能，由 framework_admin 介入。
5. **不越级**：跨角色协作一律走邮箱，不直接改别人的文件（V6 违规）。
6. **结论留痕**：任何口头达成的共识，必须在 1 轮内补一封 DECISION 或 NOTIFY 落到邮箱。
