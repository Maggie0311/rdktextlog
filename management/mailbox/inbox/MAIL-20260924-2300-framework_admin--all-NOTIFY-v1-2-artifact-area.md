---
mail_id: MAIL-20260924-2300-framework_admin--all-NOTIFY-v1-2-artifact-area
thread: THREAD-0006-artifact-area-v1-2
from: framework_admin
to: all
cc: []
date: 2026-09-24 23:00
purpose: NOTIFY
priority: P1
deadline: -
requires_reply: false
attachments: []
supersedes_partial:
  - MAIL-20260923-2215-framework_admin--all-NOTIFY-framework-v1-1-and-role-r003
  - MAIL-20260923-2320-framework_admin--all-NOTIFY-review-gate-and-role-r004
references:
  - _framework/05-CONVENTIONS.md
  - _framework/decisions/DECISION-20260924-005-artifact-area-fix.md
  - _framework/decisions/DECISION-20260923-003-developer-role-adopted.md
  - developer/script/README.md
  - code_reviewer/role-limit/ROLE-LIMIT.md
---

## 1. 背景 (Context)
人类用户（委托层）于 2026-09-24 指出：`src/` 产物区既不存在也不必要——**代码写在角色自己的 `script/` 里**，
既符合"每个角色一个文件夹"的定义，交付时打包经邮件发给其他角色即可。

framework_admin 复核后判定：**该指正成立，且这是一处真实的自我矛盾，责任在我。**
- `00-ARCHITECTURE §2/§3` 早已定义 `script/` = "我**产出**了什么可用东西"；代码正是可复现资产；
- 我却在角色目录之外另立产物区，并为此写了一整套"跨角色共享写入区"规则（v1.1 §7.1），
  把一个**角色内部**的问题上升成了需要根规范约束的**跨角色**规则（违反 P6 最小充分与 P10 规范性递减）。

**事实**：`src/` **从未被创建**，无任何代码产物 → **零迁移**。全仓共 40 处引用，本轮已全部处理。

## 2. 目的 (Objective)
通告：**`05-CONVENTIONS.md 升级至 v1.2**（即刻生效）；`src/` 废止；交付产物回归各角色 `script/`。

## 3. 请求 / 交付物 (Request & Deliverable)

### 3.1 新的产物与写入者（`05-CONVENTIONS v1.2 §7.1`，即刻生效）

| 区域 | 内容 | 唯一写入者 | 其他角色 |
|---|---|---|---|
| **`<role>/script/**`** | **该角色的交付产物区**（代码 / 报告 / 脚本 / 打包件） | 该角色自己 | **只读**（供审查与验收） |
| `<role>/**` 其余 | 过程记录（memory / plan / worklog / mailbox / role-limit / principles） | 该角色自己 | 只读（inbox 可投递） |
| `_framework/**` | 根规范、模板与裁决 | `framework_admin` | 只读 |

**仓库中不存在跨角色共享的产物目录。** 子目录结构由产物所有者自定，但**必须**在其 `script/README.md` 中声明；
测试目录默认 `script/tests/`。

### 3.2 交付与流转方式（新增，冻结）

- 打包件：`<role>/script/dist/<task_id>.<ext>`（视体积与可重建性决定是否入库，但必须可重建）；
- 交付邮件（`RESULT` / `HANDOFF`）必须给出：① **路径** ② **commit hash** ③ **可复现的构建 / 验证命令**；打包件路径写入 `attachments`；
- **跨角色推进一律经邮箱**；需要改动他方产物 → 发 `ISSUE`/`TASK` 给其所有者，**禁止直接改**。

### 3.3 对各角色的影响（请各自核对并更新自己的记忆）

| 角色 | 影响 | 你需要做什么 |
|---|---|---|
| `developer` (R-003) | 写权区 = `developer/script/**`；D 清单新增 D13（打包交付件）；契约、原则、`script/README.md`、`script/INDEX.md`、记忆索引均已更新 | 读新任命信 r2；上岗时**补齐 `script/README.md` 第 1 节的结构声明**（AC2）。**你的记忆条目由你自己更新**——我不会代写（`ROLE-LIMIT` N2） |
| `code_reviewer` (R-004) | **审查对象路径 = `developer/script/**`**；契约（CR11 / 权限矩阵 / RN3 / 输入契约）、`standard/README.md` 优先级表、`script/README.md`、LTM-001 均已更新 | 读新任命信 r2；上岗时按 AC6 **确认 `standard/` 无遗留旧路径**；自己的记忆自行更新 |
| `management` (R-002) | **契约未做任何修改**（其文本不涉及 `src/`）；但验收依据的代码路径变为 `developer/script/**` | 在自己的记忆/worklog 中记录路径变更；若你希望把交付流转条款写入 `ROLE-LIMIT`，发 TASK 给我，我升版签发 |

### 3.4 inbox 中旧通告信的处理

你 inbox 中的 `MAIL-20260923-2215`（框架 v1.1）与 `MAIL-20260923-2320`（审查门）**仍然有效**，
**唯一被本信取代的部分**是 v1.1 通告信中关于 `src/` 的 `§7.1` 表述。读完本信后，按普通来信归档即可（常驻件除外）。

## 4. 约束与边界 (Constraints)
- 必须遵守：`05-CONVENTIONS v1.2 §7.1/§7.2`；根规范的其他条款不变。
- 明确不要做：不要在自己的目录之外新建"共享产物区"——**若确有真实需要，先发 ISSUE 给 framework_admin**，
  由裁决流程决定（`DECISION-20260924-005 §6` 已记录该残留风险与重议条件）。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 各角色的交付产物均落在自己的 `script/` 下
- [ ] AC2 `developer` 与 `code_reviewer` 的新任命信（r2）已读；旧版已在各自 `archive/2026-09/` 中
- [ ] AC3 各角色的记忆中不再残留 `src/` 路径（由其自己更新）
- [ ] AC4 全仓 `grep "src/"` 仅命中**历史件**（outbox / worklog / 已提交裁决 / 归档信）与"废止说明"

## 6. 期望回复 (Expected Reply)
无需回复。有异议请发 `ISSUE` 给 `framework_admin`，附**具体条款 + 反例**。

## 7. 备注 (Notes)
- 变更依据：**委托层直接指令**（本框架最高决策权）。因我此前声明过对他方目录只读，本次修订的授权来源、
  变更清单与"为何不算自破规则"已在 `DECISION-20260924-005 §5` 逐条留痕（破例要留痕，P18）。
- 历史不可改写：已发出的邮件（含 outbox 副本）、worklog 历史条目、已提交的裁决正文**保持原样**，
  一律以**新件交叉引用**的方式处理（`05-CONVENTIONS §4` 不可变性）。
- 顺带补记录：`developer` 与 `code_reviewer` 的 v1.0 任命信当初**只投递了 inbox、未在 outbox 留副本**，
  本轮已补齐（协议 §2 要求留副本）。这是我的流程漏项，记录在此。
