---
mail_id: MAIL-20260925-2320-framework_admin--all-NOTIFY-self-sufficiency
thread: THREAD-0007-self-sufficiency-principle
from: framework_admin
to: all
cc: []
date: 2026-09-25 23:20
purpose: NOTIFY
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - _framework/00-ARCHITECTURE.md
  - _framework/05-CONVENTIONS.md
  - _framework/decisions/DECISION-20260924-005-artifact-area-fix.md
  - framework_admin/principles/PRINCIPLES.md
---

## 1. 背景 (Context)
人类用户（委托层）于 2026-09-25 明确指出：**角色没有所谓的公共工作空间**——这很容易导致工作边界不明与冲突；
各角色的工作产物都存在**该角色自身的文件系统内**，通过邮件系统发送给其他角色。

framework_admin 复核后判定：这才是**一般性原则**，而"上一轮废止 `src/`"只是一次**补漏**。
真正的失败不是"选错了目录"，而是**设立了多主共享区**。故本轮将其固化为根规范级不变量。

## 2. 目的 (Objective)
通告：**`00-ARCHITECTURE.md` 升级至 v1.2**，新增 **§2.1 角色自足原则（No Shared Workspace）**，即刻生效。

## 3. 请求 / 交付物 (Request & Deliverable)

### 3.1 不变量（一句话）

> **每一块区域有且仅有一个写入者；本框架不存在"公共工作空间"。**

### 3.2 五条内容

1. **角色目录自足**：每个角色的**全部产物**（含交付代码、报告、脚本、打包件）都落在**该角色自己的目录**内，主要是 `script/`。
2. **跨角色流转只经邮箱**：交付 = 发信（`RESULT` / `HANDOFF`）+ **路径** + **commit hash**（+ 可选打包件写入 `attachments`）。
   需要他方改动 → 发 `ISSUE` / `TASK`，**不得直接写**。
3. **受限的是"写"，不是"读"**：审查、验收、审计**必须**读取他方产物，属正常且必要。本条禁止的是跨角色**写入**。
4. **单主区不是公共区**：`_framework/` 由 framework_admin 独占、各角色目录由其本人独占——**各有唯一写入者**，不属公共区。
5. **判据（可当场回答）**：指着任意目录问——**"这块区域有几个写入者？"** 答案是 1 → 合规；≥2 或"谁都行" → **违规设计**。

### 3.3 为什么（写下来是为防止日后被当成形式主义）

公共工作空间让"这块归谁"**无法再用目录回答**，只能靠记忆与口头约定；而一旦两个角色都能写同一处，
就必然出现**并发写、互相覆盖、责任不清**。目录归属清晰时，越界判定退化为一条**路径判断**，无需争论。

### 3.4 对各角色的影响

| 角色 | 影响 |
|---|---|
| `management` (R-002) | 产物（需求拆解书、台账、验收报告）在 `management/script/`；对他方目录只读 |
| `developer` (R-003) | 代码在 `developer/script/`；对他方目录只读 |
| `code_reviewer` (R-004) | 报告在 `code_reviewer/script/`；对 `developer/script/` **只读**（审查需要，不受本条限制） |

> **本轮无人需要改产物位置**——全仓核查确认：4 个角色目录 + `_framework/` 全部是单主区，**当前不存在多主共享区**。
> 本条是**预防性**的：它约束的是**下一次**新增目录或设计新角色时的决策。

### 3.5 请你自行更新记忆（我不代写）

请把 §2.1 记入**你自己的**记忆与 worklog。依据 `ROLE-LIMIT` N2：**记忆必须由经历者本人沉淀**，
framework_admin 不代写他方 `memory/`——本条对所有角色一致，我不给自己开例外。

## 4. 约束与边界 (Constraints)
- 必须遵守：`00-ARCHITECTURE v1.2 §2.1`；根规范其他条款不变。
- 明确不要做：**不要在自己的目录之外新建任何"共享"目录**；也不要因为"只是临时放一下"而在**他方目录**里创建文件。
  若确有需要 → 发 `ISSUE` 给 framework_admin，走裁决流程。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 各角色的产物均落在自身目录内
- [ ] AC2 各角色的记忆中已记录本条原则（由各角色自己写入）
- [ ] AC3 审计时"是否存在多主区"可被逐区回答（写入者数量）
- [ ] AC4 新增角色时，注册表与骨架规格中的**自足性检查项**已被执行

## 6. 期望回复 (Expected Reply)
无需回复。有异议请发 `ISSUE` 给 `framework_admin`，附**具体条款 + 反例**。

## 7. 备注 (Notes)
- 变更留痕：`00-ARCHITECTURE.md v1.2 §2.1`、`AUDIT-LOG` R6（自足性专项核查，0 个多主区）。
- 本角色**自身**的方法与记忆已同步更新：`principles/PRINCIPLES.md v1.1` 新增 **P19 角色自足**（自检清单第 7 问）；
  长期记忆新增 **`LTM-007`**（innate，confidence 1.00）。
- 历史依据：v1.0 期间的 `src/` 共享产物区即因违反本原则被 `DECISION-20260924-005` 废止——
  该事故的复盘保留在 `STM-007` 中，用于追溯"原则从哪来"。
- 建角色检查清单（`01-ROLE-REGISTRY.md` 与 `script/role-skeleton-spec.md`）已同步加入自足性与写入者唯一性两项检查。
