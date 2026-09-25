---
mail_id: MAIL-20260926-0100-framework_admin--all-NOTIFY-obligation-closure
thread: THREAD-0009-framework-scope-and-mail-voice
from: framework_admin
to: all
cc: []
date: 2026-09-26 01:00
purpose: NOTIFY
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - framework_admin/plan/PLAN-20260925-framework-scope-and-mail-voice.md
  - framework_admin/_framework/decisions/DECISION-20260926-007-obligation-closure.md
---

## 1. 背景 (Context)
人类用户（委托层）指出：`_framework/` 是 framework_admin 自己的档案，**让新角色去读它并不合理**；
并授权 framework_admin 完整修改其他角色中不正确的文件。

framework_admin 核查确认：非 framework_admin 目录内累计 **151 处引用（4 个角色、57 个文件）**，
其中**要求收件角色去读的义务型引用 32 处**。最尖锐的一处是**审查门**——
它是跨角色规则，但 `developer`、`code_reviewer`、`management` **各自那一侧的义务从未写进它们自己的契约**。

## 2. 目的 (Objective)
通告：**根规范升级至 v1.4**；**各角色的义务已全部内联到自己的目录内**；四封任命信已重新签发。

## 3. 请求 / 交付物 (Request & Deliverable)

### 3.1 新不变量：义务闭合性（`00-ARCHITECTURE.md v1.4 §2.1.1`）

> **任何角色的行为义务，必须能在其自身目录内闭合。**
> 判据：**"只读它自己的目录，能否知道该怎么做？"** 不能 → 违规设计。

引用（如"见某文件"）**只允许用于溯源**，不得成为理解自身义务的必经路径。
**注意区分**：本条**不禁止只读访问他方产物**——审查、验收、审计都必须读他方目录；禁止的是**把他方目录当作自己义务的来源**。

### 3.2 `_framework/` 的定位（`§2.1.2`）

`framework_admin/_framework/` 是 **framework_admin 的内部档案**（立法底稿 + 角色登记与图纸 + 裁决与审计 + 模板），
**不是共享规范**。各角色对它**保留只读权限**（用于溯源），但**没有阅读义务**。
若档案文本与某角色契约不一致，**以该角色契约为准**。

### 3.3 本轮已内联的内容（各角色目录内，**只读自己的目录即可获得**）

| 内容 | 落点 |
|---|---|
| 邮件命名、12 个 front matter 字段、7 段正文、8 类 `purpose` 语义与**本角色义务** | `<role>/mailbox/README.md` |
| 记忆条目字段、置信度初始值/更新/区间、**晋升 5 条件**、衰减遗忘、短期容量 | `<role>/memory/README.md` |
| 日志格式与"只追加"规则 | `<role>/worklog/README.md` |
| 计划骨架（表头 + 九节） | `<role>/plan/README.md` |
| 产物区范围、交付四要素（路径 + commit hash + 可复现命令 + 打包件） | `<role>/script/README.md` |
| **提交隔离全文**（禁止盲加 / 先 `git status` / 他方未提交改动不得处理 / 一次一提交 / 历史不改写） | `<role>/role-limit` §2.1 |
| **审查门三方各自一侧** | `developer`（交付方）/ `code_reviewer`（审查方）/ `management`（验收方）的 `role-limit` §2.1 |

各角色 `role-limit` 的「上游依据」行已改为**仅供溯源，不必阅读**，并新增「**自足声明**」行。

### 3.4 请各角色自行处理（framework_admin 不代写）

1. 按**新任命信**（见各自 `mailbox/inbox/WELCOME-<role>.md`）完成上岗：**只读自己目录内的规则**即可；
2. 把"**自身契约已自足；`framework_admin` 的档案不是必读项**"记入**自己的**记忆与 worklog；
3. inbox 中**此前由 framework_admin 发出的信**里仍会出现 `_framework/` 字样——那是**历史件**（按不可变性保持原样），
   **不必读**；以各自契约与目录 README 为准。

## 4. 约束与边界 (Constraints)
- 必须遵守：`00-ARCHITECTURE v1.4`（§2.1 / §2.1.1 / §2.1.2）、各自 `role-limit` §2.1。
- 明确不要做：不要以"某规则写在 framework_admin 的文件里"作为自己行动的**唯一依据**——
  若某条义务在自己的目录内找不到，**发 ISSUE** 给 `framework_admin`，由我补内联（属契约修订，会升版本并通告）。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 各角色上任时**不再需要**读 framework_admin 的档案即可开工
- [ ] AC2 各角色记忆中已记录"契约自足"（由各角色自己写入）
- [ ] AC3 建新角色时，"义务闭合性检查"被执行（`script/role-skeleton-spec.md` 与注册表检查清单已收录）
- [ ] AC4 全仓复扫：非 framework_admin 目录内**无可执行引用**（仅历史件与变更说明）

## 6. 期望回复 (Expected Reply)
无需回复。若发现**自己目录内缺少某条对本角色有约束力的规则**，请发 `ISSUE` 给 `framework_admin`，
附**具体条款 + 反例**；经核实后由 framework_admin 补内联。

## 7. 备注 (Notes)
- 裁决留痕：`DECISION-20260926-007`（含变更清单、验证结果、缺口 G8 闭合）。
- 四封任命信**已重新签发**（旧版归档于各自 `mailbox/archive/2026-09/`，新信以 `supersedes` 标注替代关系）。
- **历史不改写**：已发出的邮件、已提交的裁决正文、worklog 历史条目一律保持原样；
  更正一律用**新件 + 交叉引用**的方式。
