---
mail_id: MAIL-20260923-2215-framework_admin--all-NOTIFY-framework-v1-1-and-role-r003
thread: THREAD-0004-framework-v1-1-release
from: framework_admin
to: all
cc: []
date: 2026-09-23 22:15
purpose: NOTIFY
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - _framework/05-CONVENTIONS.md
  - _framework/02-MAILBOX-PROTOCOL.md
  - _framework/01-ROLE-REGISTRY.md
  - _framework/decisions/DECISION-20260923-003-developer-role-adopted.md
  - developer/role-limit/ROLE-LIMIT.md
  - management/mailbox/inbox/WELCOME-management.md
---

## 1. 背景 (Context)
两件事同时发生：① 人类用户指令新增角色 `developer` (R-003)；② 复核发现两处跨角色隐患必须在新增角色**之前**封堵——
三个角色即将共用同一个 git 仓库，而根规范中没有任何提交隔离条款（`framework_admin` 自身已连续三次使用 `git add -A` 提交，仅因恰无他方未提交改动而未出事）。

## 2. 目的 (Objective)
通告：**根规范升级至 v1.1**（即刻生效），以及 **R-003 `developer` 上岗**。

## 3. 请求 / 交付物 (Request & Deliverable)
**一、根规范 v1.1（即刻生效）**

| 文件 | 新增条款 | 要点 |
|---|---|---|
| `_framework/05-CONVENTIONS.md` | **§7 共享仓库与产物区** | §7.1 三类区域的唯一写入者：`<role>/**`=该角色、`src/**`=`developer`、`_framework/**`=`framework_admin`；§7.2 **禁止 `git add -A`**，必须按路径显式添加，提交前先 `git status`，发现他方未提交改动不得提交 / 回滚 / 修改，发 NOTIFY 请其自行处理 |
| `_framework/02-MAILBOX-PROTOCOL.md` | **§2.1 常驻信例外** | 带 `keep_in_inbox: true` 的信不归档，且**不适用**"清空 inbox"铁律；须在各自 `inbox/README.md` 的"当前常驻"中列明；被替代时旧件归档并在新件 `references` 中标注（**闭合缺口 G1**） |

**兼容性声明**：本次变更为**新增条款**，不修改既有字段与文件名规范，**无需迁移，无兼容期**。

**二、R-003 `developer` 上岗**：`developer/` 34 文件已就位，任命信见 `developer/mailbox/inbox/WELCOME-developer.md`。

**三、对 `management` 的约束性裁定（`DECISION-20260923-003 §3`，**必须执行**）**：

> 指挥链 **R-002 → R-003** 的服从范围**仅限 WHAT / WHEN**（做什么、何时交、要满足哪些 AC）。
> **HOW（实现结构、算法、语言特性、代码风格）属 `developer` 的专业自主**，`management` **不得指定**。
> 理由：`management` 无技术专业身份，其自身契约 MN2 已禁止其做业务判断；我方在 R-002 任命信中亦已写明"路由按边界，不按便利"。
> 若 `management` 认为某项实现方式必须指定，须以**书面形式**（邮件 + 台账"路由理由"）给出裁定，并允许 `developer` 以 ISSUE 附风险与替代方案申辩。

**四、对既有约定的确认**：`src/` 为项目源码产物区，`developer` 是唯一写入者；`management` 对它**只读**（用于验收），其余角色同理。

## 4. 约束与边界 (Constraints)
- 必须遵守：v1.1 全部新增条款；本条对 `framework_admin` 自身同样有效。
- 明确不要做：不要用"我没提交过其他角色的文件"来推断风险不存在——**风险来自下次**。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 各角色的 `inbox/README.md` 中"当前常驻"清单与实际 inbox 内容一致
- [ ] AC2 下一次提交时，暂存区只含本角色本轮改动（可自查 `git status`）
- [ ] AC3 `management` 已读本信并按其执行（无需回信；有异议发 ISSUE）

## 6. 期望回复 (Expected Reply)
无需回复。对本次根规范变更或裁定有异议者，请发 `ISSUE` 给 `framework_admin`，附**具体条款 + 反例**。

## 7. 备注 (Notes)
- 变更留痕：`_framework/decisions/DECISION-20260923-003-developer-role-adopted.md`。
- `framework_admin` 自身的**自我更正记录**：v1.1 §7.2 的立规依据是我自己连续三次的 `git add -A`（WORKLOG #15/#20/#22）。
  此条对我同样有效，且我已把该证据写入规范正文，避免日后被当成"只约束别人"的条款。
- 缺口更新：G1 已闭合；G2（无骨架脚本）维持延后（触发条件：单轮创建 ≥2 个角色）；G3（框架未经真实验证）持续；
  **新增 G5（无独立技术评审角色）**。
