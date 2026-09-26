---
mail_id: MAIL-20260926-1430-framework_admin--management-TASK-human-input-channel
thread: THREAD-0012-human-input-channel
from: framework_admin
to: management
cc: [developer, code_reviewer, software_tester, maintainer]
date: 2026-09-26 14:30
purpose: TASK
priority: P1
deadline: -
requires_reply: true
attachments: []
references:
  - management/from_human/README.md
  - management/from_human/INTAKE-LOG.md
  - _framework/decisions/DECISION-20260926-011-human-input-channel.md
---

## 1. 背景 (Context)
人类用户（委托层）要求：在 `management` 里留一个**人类传输文件的入口文件夹**，以便在沟通工作目标时给出具体的文件参考。
核查确认**此前没有此机制**，现已建立。

## 2. 目的 (Objective)
派活：请 `management` 接受并执行新的**人类输入通道**规则（**已内联进你的契约**）；其余角色知悉即可。

## 3. 请求 / 交付物 (Request & Deliverable)

### 3.1 新通道：`management/from_human/`

| 项 | 内容 |
|---|---|
| 用途 | 人类用户投放**参考文件**（需求文档、协议手册、样例、截图……） |
| **唯一写入者** | **人类用户** |
| `management` 的权限 | **只读**——**不得修改、移动、重命名或删除**其中任何文件（**MN14**，已写入你的契约） |
| 内含 | `README.md`（写给人类的用法）· `INTAKE-LOG.md`（**你维护的登记表，只追加**） |

### 3.2 你需要做的四件事（已内联进你的契约）

1. **开工前置新增一步**（契约 §3.1）：每次接活先扫描 `from_human/`，与 `INTAKE-LOG.md` 对比，
   找出**未登记**的文件并处理——**人类可能在你不在的时候投放文件**；
2. **必须登记**：处理后追加一行（文件 / 收到日期 / 用在哪个需求或任务 / 备注）；
3. **以路径引用，不复制内容**：在需求拆解书（`script/REQ-*.md`）里写**路径引用**，
   **不要粘贴内容**——原件才是权威，复制会产生"抄错了"的版本；
4. **读不懂或与需求矛盾 → 发 `QUERY` 问人类用户**，**不要猜**，也不要"顺手把文件改成一致"。

**必须响应**：人类投放的文件（**≤1 轮内**登记到 `INTAKE-LOG.md`）。

### 3.3 记忆已更新

已为你注入 **`LTM-007`**（`promoted_from: innate`，confidence 1.00）：
"人类投放的文件是一手依据：**只读、登记、以路径引用，绝不改动**"。
同步更新了 `memory/index/MEMORY-INDEX.md` 与 `CONSOLIDATION-LOG.md`。

> **说明**：注入的是**规则类（innate）**条目——与创建角色时注入 `LTM-000` 是同一机制。
> **经验型记忆（STM）仍由你自己写**，framework_admin 不代写。

### 3.4 其余角色（知悉）

`from_human/` 是**人类用户与 `management` 之间的通道**，其他角色**不写、也不依赖**它。
若人类用户向其他角色提要求，仍按既有规则：**需求经 `management` 转成 `task_id`** 后再动手。

## 4. 约束与边界 (Constraints)
- 必须遵守：你契约的 **MN14**、权限矩阵的只读例外行、**§3.1 开工前置**。
- 明确不要做：**不要"整理"人类投放的文件**（改名、移动、归入子目录、删除旧版）——
  那是委托人的一手依据；若确需整理，**请人类用户自己决定**。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 下次开工时，`from_human/` 中的文件已在 `INTAKE-LOG.md` 中登记（若尚无文件则记一行"本目录为空"）
- [ ] AC2 需求拆解书引用人类文件时，用的是**路径**而非复制内容
- [ ] AC3 `from_human/` 中的文件**未被修改、移动或重命名**
- [ ] AC4 你的记忆中已有 LTM-007（已注入；如需补充你自己的观察，写进 `short-term/`）

## 6. 期望回复 (Expected Reply)
`ACK`（≤1 轮内）。

## 7. 备注 (Notes)
- 裁决留痕：`DECISION-20260926-011`（含 `§2.1` 合规性说明：**该目录只有人类一个写入者，是单主区**，
  且位于 `management/` 内，不构成公共工作空间）。
- 人类用户手册已升至 **v1.1**，新增"要给它参考文件怎么办"一节。
- **未来若其他角色也需要人类投放入口，须逐角色单独裁定**——不默认推广，避免依据分散在多处。
