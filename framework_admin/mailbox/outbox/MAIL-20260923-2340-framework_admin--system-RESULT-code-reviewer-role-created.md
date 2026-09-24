---
mail_id: MAIL-20260923-2340-framework_admin--system-RESULT-code-reviewer-role-created
thread: THREAD-0005-role-code-reviewer-bootstrap
from: framework_admin
to: system (人类用户)
cc: [management, developer, code_reviewer]
date: 2026-09-23 23:40
purpose: RESULT
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - _framework/00-ARCHITECTURE.md
  - _framework/01-ROLE-REGISTRY.md
  - _framework/decisions/DECISION-20260923-004-code-reviewer-role-adopted.md
  - code_reviewer/standard/README.md
  - code_reviewer/standard/user/README.md
  - code_reviewer/role-limit/ROLE-LIMIT.md
  - framework_admin/worklog/WORKLOG.md
---

## 1. 背景 (Context)
响应人类用户 2026-09-23 指令：新增 `code_reviewer` (R-004)，独立检查 `developer` 的代码；
预留 `standard/` 标准区与用户自定义标准接口；建好后介绍给 developer 与 management；
**以后 developer 每完整工作一次即须调用它**。

## 2. 目的 (Objective)
回报 R-004 已上岗、**审查门已生效**、用户自定义标准接口已就绪；并声明一项新增缺口 G6。

## 3. 请求 / 交付物 (Request & Deliverable)

| 类别 | 产物 | 路径 |
|---|---|---|
| 角色实例 | `code_reviewer/` 共 **46 文件** | `code_reviewer/` |
| **审查标准区** | **10 文件**：总纲 / 通用清单 34 条 / C 清单 30 条 / Python 清单 34 条 / 级别门槛 / 报告模板 / 变更流水 / **用户接口 + 模板** | `code_reviewer/standard/` |
| 边界契约 | ROLE-LIMIT（§0 权力轴 + CR1–CR12 / RN1–RN13 / I-O / 升级 / DoD） | `code_reviewer/role-limit/ROLE-LIMIT.md` |
| 专业原则 | 16 条可操作准则（前半防盖章、中段防误报与瞒报、后半维护独立性）+ 自检 10 问 | `code_reviewer/principles/PRINCIPLES.md` |
| 记忆 | 10 条 innate LTM + LTM-000/STM-000 + 索引 + 流水 | `code_reviewer/memory/` |
| **根规范 v1.1** | **§4.1 审查门 + 违规码 V7** | `_framework/00-ARCHITECTURE.md` |
| 裁定记录 | 7 项冲突面裁定 + 权力轴 + G6 | `_framework/decisions/DECISION-20260923-004-code-reviewer-role-adopted.md` |
| 介绍信 | 新角色介绍 + 门规则 + 对 developer/management 的约束性要求 | `MAIL-20260923-2320-...NOTIFY...` |

### 最重要的一刀：审查权与验收权分离

你同时要求"不懒惰批准"（更严）与"不误报、不过度要求"（更准）——这两项**方向相反**。我的做法不是折中，而是**换切分轴**：

| 角色产出物的性质 | 服从边界切在哪 |
|---|---|
| 产出**交付物**（developer） | **WHAT/WHEN 服从 vs HOW 自主** |
| 产出**判断**（code_reviewer） | **PROCESS 服从（审什么、何时审） vs VERDICT 不服从（审出什么）** |

一句话：**「你可以要求我审，不能要求我过。」** 已写入根规范 §4.1 第 4 条（结论独立于指令）。
配套一句：**「我只指出问题，不动手修。」**（RN1：审查者一个字都不改，否则独立性即刻失效。）

### 四项质量要求 → 可判定机制

| 你的要求 | 机制 |
|---|---|
| 确实做到、不懒惰批准 | **PASS 三必要条件**：覆盖声明 + ≥1 项验证证据 + 零阻断项，**缺一不成立**（PASS 被设计成三者中最难的结论） |
| 不误报、不过度要求 | **发现项五要素**（缺一即无效，developer 可直接据此拒绝该条）+ **双向级别门槛**（无复现场景不得高于 MINOR、无条款依据不得高于 NIT、范围外只能 INFO） |
| 不瞒报 | 禁止降级 / 隐去 / 模糊结论；"来回次数多"不构成放行理由（写进 10 条 innate 记忆） |
| 持续有效 | **申诉通道**（developer 举证可撤回或降级）+ **REVIEW-STATS** 自我度量（申诉采纳数、后验漏报数） |

### 用户自定义标准接口

- 位置：`code_reviewer/standard/user/`
- 用法：复制 `USER-TEMPLATE.md` → 改名 `USER-<序号>-<短标题>.md` → 填字段 → **保存即生效，无需通知任何人**
- 优先级：**最高**（高于项目契约与 reviewer 自己的清单）；冲突时以你的为准
- 保护：`user/` 对 `code_reviewer` **只读**——它能提议、不能删改
- **可审计性**：每次审查报告**必须**列出本次实际应用的用户标准（无则写"无"）。**报告缺这一节即不合格，你可以直接要求重做。**

## 4. 约束与边界 (Constraints)
- 门立**根规范**而非改他方契约：我已声明对 `developer/`、`management/` 目录只读，且跨角色规则按 P10 应落根层。
  若他们希望把门写进各自契约正文，需由其发 TASK 请我升版签发——**我不会单方面改他们的契约**。
- 本角色未产出任何业务代码，未替任何角色做技术判断。

## 5. 验收标准 (Acceptance Criteria)
- [x] AC1 根规范 v1.1 落地（§4.1 审查门 + V7），AUDIT-LOG 已登记 V7 判定方法 — 通过
- [x] AC2 注册表新增 R-004 行 + "执行层·校验"声明 — 通过
- [x] AC3 七目录 + `standard/` 共 46 文件齐备，每目录有写入规则 README — 通过
- [x] AC4 ROLE-LIMIT 四段写满，RN 每条标注"应由谁做" — 通过
- [x] AC5 PRINCIPLES ≥10 条且可操作 — 通过（16 条）
- [x] AC6 `standard/user/` 接口与模板就绪，且设置了"报告须列出应用清单"的可审计约束 — 通过
- [x] AC7 向 developer 与 management 发出介绍（含门规则与约束性要求） — 通过
- [x] AC8 四角色两两"只能做"交集为空；G5 闭合、G6 登记 — 通过
- [ ] **AC9 首个真实链路（开发 → 审查 → 修复/申诉 → 复审 → 验收）验证 — 未通过，待首个真实需求**

## 6. 期望回复 (Expected Reply)
无需回复。下一步：向 `management` 提项目需求 → 它拆解并下发 `task_id` → `developer` 实现 →
**`developer` 先请 `code_reviewer` 审查，再报 `management` 验收**。

## 7. 备注 (Notes) — 诚实声明
1. **新增缺口 G6：审查者的漏报率无法主动测量。** 审查通过后暴露的缺陷才可能反推漏报，无法事前评估——
   这意味着它可能长期给出稳定的高通过率而无人察觉失效。缓解：`REVIEW-STATS.md` 记录后验漏报 + 用户可用 `standard/user/` 增补检查点 + 每次漏报须触发标准修订。
2. **G5 已闭合**（无独立技术评审的真空由 R-004 填补）。
3. **契约 ≠ 证据（第二次适用）**：你对 developer 的三项与对 code_reviewer 的四项质量硬要求，**目前全部只存在于契约与标准文本中**，
   未经一行真实代码或一次真实审查的检验。在首个完整链路跑通前，一律按"未验证"对待。
4. **我的记忆层诚实状态**：`STM-001` 已 3 任务 / 4 证据 / 3 次成功应用，置信度 0.65，但**仍缺 1 次独立确认**——
   按防单源偏差原则，我不会用自己再产出一条证据来凑晋升。这是当前最该被外部检验的一条经验。
5. **计数纪律**：本轮按上轮的教训"先清点再写数"，实测 46 文件（含标准 10），并纠正了 PLAN 与 DECISION 初稿中的 44。
6. 本轮按 `05-CONVENTIONS v1.1 §7.2` 提交（按路径显式添加，未使用盲加）。
