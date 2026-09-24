# 通用约定 (Conventions)

> 版本: **v1.2** · 维护者: framework_admin · 所有角色适用
> v1.1 生效: 2026-09-23（新增 §7 共享仓库与产物区）· **v1.2 生效: 2026-09-24（修订 §7.1：废止 `src/`，交付产物回归各角色 `script/`）**

## 1. 命名

| 对象 | 规范 | 示例 |
|---|---|---|
| 角色目录 | snake_case 小写 | `data_curator` |
| 邮件 | `MAIL-YYYYMMDD-HHMM-<from>--<to>-<CAT>-<slug>.md` | `MAIL-20260214-1030-framework_admin--data_curator-TASK-x.md` |
| 长期记忆 | `LTM-<NNN>-<slug>.md` | `LTM-003-boundary-first.md` |
| 短期记忆 | `STM-<NNN>-<slug>.md` | `STM-007-first-task.md` |
| 计划 | `PLAN-<YYYYMMDD>-<slug>.md` | `PLAN-20260214-role-skeleton.md` |
| 脚本/产物 | `<slug>.<ext>` + 版本 | `build_index.ps1`, `report-v2.md` |
| 线程 | `THREAD-<NNNN>-<slug>` | `THREAD-0007-corpus-build` |

## 2. 时间

- 一切时间戳用本地时间 `YYYY-MM-DD HH:MM`。
- 日期字段（front matter）用 `YYYY-MM-DD`。
- 归档目录用 `YYYY-MM`。

## 3. 语言

- 正文中文；字段名、文件名、代码标识符英文。
- 断言/结论必须**可证伪**，禁止"效果较好"这类模糊表述。

## 4. 不可变性

| 文件类型 | 可变性 |
|---|---|
| `worklog/` | **只追加**，禁止改写历史条目；更正用新条目 + `[更正: #N]` |
| `mailbox/outbox/` | 发出即冻结；更正发新信并 `references` 原信 |
| `memory/long-term/` | 证据表只追加；结论可改但必须记版本行 |
| `memory/short-term/` | 可编辑（工作记忆），但证据表同样只追加 |
| `role-limit/` `principles/` | 仅 framework_admin 可改；角色可发 ISSUE 建议 |
| 他人目录 | **只读**。需要改动 -> 发 TASK 给对方 |

## 5. 引用

- 提到任何文件必须写**相对仓库根的路径**，且该文件必须真实存在。
- 引用他人结论必须写明来源 ID（如 `LTM-003 of data_curator`）。

## 6. 空目录占位

任何标准目录若暂无内容，必须有 `README.md` 说明用途，避免"看起来坏了"。

---

## 7. 共享仓库与产物区（v1.1 新增 §7.2；**v1.2 修订 §7.1**）

### 7.1 仓库内容与写入者（v1.2 修订）

| 区域 | 内容 | 唯一写入者 | 其他角色 |
|---|---|---|---|
| `<role>/script/**` | **该角色的交付产物区**：代码、报告、脚本、打包件——即架构 §3 所说的"我产出了什么可用东西" | 该角色自己 | **只读**（供审查与验收） |
| `<role>/**` 其余 | 角色过程记录（memory / plan / worklog / mailbox / role-limit / principles） | 该角色自己 | **只读**（`mailbox/inbox/` 可投递） |
| `_framework/**` | 根规范、模板与裁决 | `framework_admin` | 只读 |

- **交付产物一律落在生产者自己的 `script/` 下**：`developer` 的代码在 `developer/script/`，
  `code_reviewer` 的报告在 `code_reviewer/script/`，`management` 的拆解书与台账在 `management/script/`。
  **仓库中不存在跨角色共享的产物目录。**
  > **v1.2 变更说明**：v1.1 曾设立 `src/` 作为"项目交付产物区"。该设计与 `00-ARCHITECTURE §2/§3` 对 `script/` 的定义相冲突，
  > 且凭空引入一个需要额外规则维护的跨角色共享写入面。**`src/` 已废止**（从未创建，无迁移）。依据：`DECISION-20260924-005`。
- **子目录结构由产物所有者自定**，但**必须**在其 `script/README.md` 中声明（含结构说明与构建 / 运行 / 复现方式）。
  测试目录**默认** `script/tests/`；所有者可在其 `CODE-STYLE.md` 中另行声明。
- **交付与流转**：产物所有者可将交付件**打包**为 `script/dist/<task_id>.<ext>`（视体积与可重建性决定是否入库），
  并在交付邮件（`RESULT` / `HANDOFF`）中给出：① 路径 ② **commit hash** ③ 可复现的构建 / 验证命令；
  `attachments` 字段填写交付件路径。**跨角色推进一律经邮箱**，不得直接改他方产物。
- 任何角色需要修改他方产物 → 发 `ISSUE`/`TASK` 给该产物的所有者，**禁止直接改**（架构 §7 V6）。

### 7.2 提交隔离（硬性，v1.1 新增）

所有角色共用同一个 git 仓库，因此：

1. **禁止** `git add -A`、`git add .` 等盲加命令；必须**按路径显式添加**自己本轮改动的文件。
2. 提交前**必须**先执行 `git status`。若发现**他方未提交的改动**：
   - 不得提交（否则会被一并卷入）；
   - 不得回滚、不得修改、不得丢弃；
   - 发 `NOTIFY` 给该角色，请其自行提交。
3. 每次任务**一个提交**；commit 信息必须含任务标识（`task_id` 或等效）与改动范围。
4. 出现真实冲突（同一文件同一处的改动）→ **停止操作**，发 `ISSUE` 给 `framework_admin` 仲裁；禁止强推、禁止覆盖他方改动。
5. 已提交历史**不得改写**（禁止用 `rebase -i` / `commit --amend` 修改已被他人引用的提交）；更正一律用新提交。

> **立规依据（真实事件，非假设）**：在本条生效前，`framework_admin` 连续三次使用 `git add -A` 提交（`WORKLOG` #15、#20、#22）。
> 当时因恰无他方未提交改动而未造成损失——这是**侥幸，不是安全**。本条对 `framework_admin` 自身同样具有约束力。
