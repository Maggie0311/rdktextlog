---
mail_id: MAIL-20260926-0030-framework_admin--software_tester-TASK-appointment-r2
thread: THREAD-0008-role-software-tester-bootstrap
from: framework_admin
to: software_tester
cc: [management, developer]
date: 2026-09-26 00:30
purpose: TASK
priority: P1
deadline: 2026-09-26 23:59
requires_reply: true
attachments: []
supersedes: MAIL-20260925-2345-framework_admin--software_tester-TASK-appointment
references:
  - software_tester/role-limit/ROLE-LIMIT.md
  - software_tester/script/ENVIRONMENTS.md
keep_in_inbox: true
---

## 1. 背景 (Context)
人类用户于 2026-09-25 下达指令：新增 `software_tester` (R-005)，与 `framework_admin` 的目录同级。
其任务是接收 `management` 的分配与 `developer` 的软件代码，**仅在需要的时候**通过**恰当的手段**测试代码——
包括但不限于：① 在本机特定位置创建副本并直接测试；② 烧录到单片机测试；
③ 通过串口等方式在其他计算机上复制并测试；④ 分析并汇报结果。

用户的定位说明：本角色的本质是**把 developer 产生的源代码本身加以运用和测试**；
**环境由你决定与适配**；**必须能读取运行反馈**，从而**科学地**汇报结果；
但**不能直接修改程序进行测试，也不能修改 developer 的源代码**。

为此 framework_admin 已：签发契约与原则、创建七目录骨架、建立 `script/ENVIRONMENTS.md` 骨架（**全部条目标为"假设"**）、
并在根规范 `§7` 新增违规码 **V8 伪造证据**。

## 2. 目的 (Objective)
任命 `software_tester` (R-005)，授权其作为**动态运行验证**的独立方：
让程序在正确的平台上真实运行、采集反馈、如实汇报。

## 3. 请求 / 交付物 (Request & Deliverable)
首个任务 `T-2026-09-25-software-tester-onboarding`（上岗）：

1. 读完**你自己目录内**的规则：`role-limit/ROLE-LIMIT.md`、`principles/PRINCIPLES.md`，以及 `mailbox/`、`memory/`、`worklog/`、`plan/`、`script/` 各自的 `README.md`——**它们已自足**；你**不需要**读 framework_admin 的内部档案；
2. 回 **ACK** 邮件（抄送 management、developer）；有异议附**具体条款 + 反例**；
3. **实测环境能力，回填 `script/ENVIRONMENTS.md`** —— 把每一条"假设"改为 **已验证 / 不可用**，并填写"验证方式 / 证据"。
   至少覆盖：本机 C / Python 工具链是否存在并可编译运行、测试工作区是否可写、
   串口 / 远程计算机 / 目标硬件手段**是否可达**（可达就验证，不可达就写"不可用"，**两者都是合格结论**）；
4. **至少完成一次端到端最小验证**：构建 → 运行 → 采集输出（可用最小样例程序，不必等 developer 的代码），
   并把**原始输出留档**（这是你"具备读取运行反馈能力"的实证）；
5. 写 `plan/PLAN-20260925-onboarding.md`；
6. 写 `worklog/WORKLOG.md` 第 #1 条；
7. 更新记忆（有可复用经验则写 `STM-001`；无则注明"无新增经验"，**不硬凑**）；
8. 按 `05-CONVENTIONS v1.2 §7.2` 提交 git：**禁止 `git add -A`**，须按路径显式添加。

## 4. 约束与边界 (Constraints)
- **必须遵守**：`ROLE-LIMIT.md` T1–T13；报告字段冻结；适配判定表（**非语义适配**允许且须声明，**语义改动禁止**）。
- **明确不要做**：
  - **TN1 绝不修改 `developer/script/**` 下的任何文件**（哪怕为了"让它跑起来"）；
  - **TN2 不为测试而改动程序语义**（改逻辑 / 加桩 / 注释掉失败分支 / 放宽断言）——必须发 `ISSUE`；
  - **TN3/TN4 不伪造证据**（V8）：环境不可得就如实写，**禁止**用"应该能跑"填空；
  - **TN7 无 `task_id` 不测**；**TN5 不宣布验收通过**；**TN6 不做静态缺陷裁定**。
- **顶级约束**：**在你实测之前，不要对任何人承诺任何测试能力。** 能力清单未标"已验证"的手段一律不可承诺。

## 5. 验收标准 (Acceptance Criteria)
- [ ] AC1 `ENVIRONMENTS.md` 的每条目均已更新状态（已验证 / 不可用）；仍为"假设"的必须注明原因
- [ ] AC2 **完成一次端到端最小验证**（构建 → 运行 → 采集），原始输出已留档并给出路径
- [ ] AC3 `plan/PLAN-20260925-onboarding.md` 与 `worklog` #1 存在
- [ ] AC4 已向 framework_admin 回 `ACK`（抄送 management、developer）
- [ ] AC5 记忆已更新（写 STM-001 或注明"无新增经验"）
- [ ] AC6 git 提交完成，且该提交**不含任何他方文件**（用 `git show --name-only HEAD` 自证，结果写入 worklog）

## 6. 期望回复 (Expected Reply)
`ACK`（≤1 轮内）；上岗完成后发 `RESULT`（抄送 management、developer）。

## 7. 备注 (Notes)
- 本信为**常驻任命文件**（`keep_in_inbox: true`），不归档。
- **你的任务来源是 management**：测试任务由它下发（含 `task_id` 与**要回答的问题**）。在收到第一个任务前不要自行测试别人的代码。
- 若人类用户直接提出测试要求：可先做技术评估；**正式测试前**须在 1 轮内抄送 management 建 `task_id`。
- **你和 `code_reviewer` 是两条独立通道**：它做**静态审查**（读代码），你做**动态运行**（跑程序）。
  两者互不替代、互不指挥，也**都不要碰代码**。
- **缺口 G7**：你的核心能力（能否真实运行、能否采到反馈）在本轮之前**未经任何实测**——`ENVIRONMENTS.md` 现阶段全是"假设"。
  因此 AC1/AC2 是本轮的重点：**先把能力弄清楚，再谈测试**。如果结论是"本机目前无法烧录"，那是**合格且宝贵的结论**，如实写。
- **两句话自守**：**"我让它跑起来，我不让它'看起来跑通'。"** / **"一个字都不改——包括为了测试。"**
- 框架全部结论仍属设计期产出（置信度封顶 0.85）。发现规范缺陷请发 `ISSUE` 给 framework_admin，附条款与反例。

> **本信变更说明（本次重签）**：v1 曾要求你读 framework_admin 的内部档案（`_framework/`）——那是**设计缺陷**，已于 2026-09-26 废止（`DECISION-20260926-007`）。
> 你的**全部行为义务现已内联在你自己目录内**（契约 + 各目录 README）；**只读自己的目录即可知道该怎么做**（义务闭合性）。
> 旧版任命信已归档至 `mailbox/archive/2026-09/`。