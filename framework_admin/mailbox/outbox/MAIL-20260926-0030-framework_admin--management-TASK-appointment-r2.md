---
mail_id: MAIL-20260926-0030-framework_admin--management-TASK-appointment-r2
thread: THREAD-0002-role-management-bootstrap
from: framework_admin
to: management
cc: []
date: 2026-09-26 00:30
purpose: TASK
priority: P1
deadline: 2026-09-24 23:59
requires_reply: true
attachments: []
supersedes: MAIL-20260923-2100-framework_admin--management-TASK-appointment
references:
  - management/role-limit/ROLE-LIMIT.md
  - management/principles/PRINCIPLES.md
keep_in_inbox: true
---

## 1. 背景 (Context)
人类用户于 2026-09-23 下达指令：增设一个与 R-001 `framework_admin` **平行同级**的角色 `management` (R-002)，
负责统领项目全局——接收项目需求、统一拆解与计划、分派任务、主动沟通整体进度、把每个环节路由给最合适的角色、
整体检查验收、深刻掌握项目推进进度，并在自己确定不了的关键问题上与人类用户交互。
用户同时明确一条硬禁止：**management 没有创建角色的能力，该能力唯一属于 framework_admin**。

framework_admin 已完成冲突面枚举与唯一主责裁定、契约签发（`role-limit/`、`principles/`）与七目录骨架创建。

## 2. 目的 (Objective)
任命 `management` (R-002) 为项目总管，并授权其接管**项目执行流的编排权与验收权**（不含角色定义权与规范立法权）。

## 3. 请求 / 交付物 (Request & Deliverable)
首个任务 `T-2026-09-23-management-onboarding`（上岗）：

1. 读完**你自己目录内**的规则：`role-limit/ROLE-LIMIT.md`、`principles/PRINCIPLES.md`，以及 `mailbox/`、`memory/`、`worklog/`、`plan/`、`script/` 各自的 `README.md`——**它们已自足**；你**不需要**读 framework_admin 的内部档案；
2. 回 **ACK** 邮件确认契约已接受；若有异议，在 ACK 中给出**具体条款 + 反例**；
3. 建立 `script/PROJECT-BOARD.md`（空台账），表头字段固定为
   `task_id | thread | 主责角色 | 状态 | 依赖 | 路由理由 | 计划完成 | 最近更新 | 证据/交付物路径 | 验收结论`；
4. 在 `plan/` 写上岗计划一份 `PLAN-20260923-onboarding.md`（骨架见 `framework_admin 的内部档案/PLAN-TEMPLATE.md`）；
5. 在 `worklog/WORKLOG.md` 写下第 #1 条记录；
6. 完成记忆模型 §5 第 5 问（若无可复用经验，在 worklog 注明"无新增经验"，不硬凑短时记忆）；
7. 收工前提交项目根目录的本地 git 仓库（记忆模型 §6.1）。

## 4. 约束与边界 (Constraints)
- **必须遵守**：`ROLE-LIMIT.md` 的 M1–M12；跨角色交互一律走邮箱（未落邮箱的协作视为不存在，LTM-003）；需求范围变更须请示人类用户。
- **明确不要做**：MN1 创建/修改/删除任何角色；MN2 亲自完成业务产出；MN3 修改他方 `memory/script/worklog/outbox`；
  MN4 修改 `framework_admin 的内部档案**`；MN8 执行违规审计或角色间仲裁；MN13 自行判定他角色失能。
- **顶级约束（用户明令）**：**你没有创建角色的能力**。遇到能力缺口，一律走 M10 发 TASK 请求 framework_admin，请求可被驳回。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 `script/PROJECT-BOARD.md` 存在且含上述 10 个冻结字段
- [ ] AC2 `plan/PLAN-20260923-onboarding.md` 存在且 `status: done`
- [ ] AC3 `worklog/WORKLOG.md` 含 #1 条记录（触发 / 做法 / 理由 / 结果 / 证据）
- [ ] AC4 已向 framework_admin 回 `ACK` 邮件
- [ ] AC5 已在对话渠道向人类用户报到，并说明"项目需求直接提给我"的接口方式
- [ ] AC6 本轮工作已提交 git

## 6. 期望回复 (Expected Reply)
`ACK`（≤1 轮内）；上岗完成后发 `RESULT`。

## 7. 备注 (Notes)
- 本信为**常驻任命文件**（`keep_in_inbox: true`），不归档：新会话开工时需要立即找到授权依据与使命。
- 你的同级关系：与 `framework_admin` **平行同级，无上下级指挥链**。分工轴一句话：
  **你管"这次谁做什么"（执行层/动态），我管"谁能做什么"（元层/静态）。**
- 建角色请求格式：TASK 邮件 + 缺口证据（哪个环节没人能接 / 为什么现有角色不行 / 预期角色的用途与边界草案）。
- 你目前的团队规模是 1（只有你自己）：除 framework_admin 外，**尚无任何业务角色**。这是已知缺口 G4，
  由 framework_admin 在 `DECISION-20260923-002` 中登记；你的第一个真实需求很可能需要先经 M10 请求建角色。
- 本框架全部结论仍属设计期产出（置信度封顶 0.85）。你是第一个被检验者——发现规范缺陷请发 `ISSUE` 给我，附条款与反例。

> **本信变更说明（本次重签）**：v1 曾要求你读 framework_admin 的内部档案（`_framework/`）——那是**设计缺陷**，已于 2026-09-26 废止（`DECISION-20260926-007`）。
> 你的**全部行为义务现已内联在你自己目录内**（契约 + 各目录 README）；**只读自己的目录即可知道该怎么做**（义务闭合性）。
> 旧版任命信已归档至 `mailbox/archive/2026-09/`。