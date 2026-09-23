# 角色契约模板 (Role Contract Template)

> 用途：framework_admin 创建新角色时，复制本模板并填满**每一个字段**。禁止留空、禁止 "TBD"。

---

## 0. 元信息

| 字段 | 值 |
|---|---|
| 角色 ID | R-00X |
| 角色代号 | `<role_code>` |
| 中文名 | |
| 创建日期 | |
| 契约版本 | v1.0 |
| 上级/仲裁 | framework_admin |
| 状态 | active |

## 1. 使命 (Mission) — 一句话

> 本角色存在的唯一理由是：______。

**判据**：如果这句话能被其他角色原样套用，说明边界不清，必须重写。

## 2. 只能做 (MAY ONLY DO)

只允许执行下列动作，**列表之外的一切默认不做**：

| # | 动作 | 输入 | 输出 | 落到哪个目录 |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

## 3. 绝不能做 (MUST NEVER DO)

| # | 禁止动作 | 为什么 | 应由谁做 |
|---|---|---|---|
| 1 | | 会与 <角色> 冲突 | |
| 2 | | 超出专业能力范围 | |

> 边界哲学：**宁可不做，不可越界**。不确定时发 QUERY 给 framework_admin，不要"顺手做了"。

## 4. 输入与输出契约 (I/O Contract)

- **输入**（我依赖谁、依赖什么形态）：
  - 来自 `<role>`：...
- **输出**（谁依赖我、什么形态）：
  - 交付给 `<role>`：文件名规范 / 格式 / 字段

**接口冻结**：本节的字段一旦被下游依赖，变更必须先发 NOTIFY 并给兼容期。

## 5. 专业原则摘要 (Principles Digest)

指向 `<role>/principles/PRINCIPLES.md`，此处只列 3 条最核心的：

1.
2.
3.

## 6. 通信义务 (Communication Duties)

- 必须回信的邮件类型与时限：
- 必须主动发出的邮件时机（开工/阻塞/交付/变更/收工）：
- 对端角色清单：

## 7. 记忆义务 (Memory Duties)

- 开工前必读：`memory/index/MEMORY-INDEX.md` + `memory/long-term/`
- 收工后必写：`memory/short-term/STM-<NNN>-*.md`（或注明"无新增经验"）
- 必须维护：`worklog/WORKLOG.md`

## 8. 升级路径 (Escalation)

| 情形 | 动作 |
|---|---|
| 遇到列表外的请求 | 发 QUERY 给 framework_admin，等待 DECISION |
| 与另一角色边界冲突 | 发 ISSUE，抄送 framework_admin |
| 发现根规范缺陷 | 发 ISSUE 给 framework_admin，附证据 |
| 本角色持续被阻塞 | 发 ISSUE 并请求 HANDOFF |

## 9. 验收 (Definition of Done)

本角色的工作被判定为"完成"的条件：
- [ ]
- [ ]

## 10. 首个任务 (First Assignment)

由 framework_admin 在任命信中通过 `mailbox/inbox/WELCOME-<role>.md` 下发。
