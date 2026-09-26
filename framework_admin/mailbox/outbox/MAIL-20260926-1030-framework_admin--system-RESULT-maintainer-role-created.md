---
mail_id: MAIL-20260926-1030-framework_admin--system-RESULT-maintainer-role-created
thread: THREAD-0010-role-maintainer-bootstrap
from: framework_admin
to: system (人类用户)
cc: [management, developer, code_reviewer, software_tester, maintainer]
date: 2026-09-26 10:30
purpose: RESULT
priority: P1
deadline: -
requires_reply: true
attachments: []
references:
  - maintainer/role-limit/ROLE-LIMIT.md
  - maintainer/code_archive/README.md
  - _framework/decisions/DECISION-20260926-008-maintainer-role-adopted.md
---

## 1. 背景 (Context)
你下达了 R-006 `maintainer` 的创建指令（两封，后封为补充），并要求其余功能**用选项框交互确认**。

**关于选项框的说明（必须先讲）**：我发起了 `ask_user_question`（6 个问题），**调用超时（10 分钟无响应）**。
为不空转，我改为：**核心功能按你的原话直接落地**（这部分不需要选），
**六项待定按推荐默认值落地并标注"待确认"**，在 §6 给出文字版选项供你勾选。

## 2. 目的 (Objective)
回报 R-006 已上岗、`code_archive` 归档系统已建立、**移交链路已接通**；并请你确认六项待定取值。

## 3. 交付物

| 类别 | 产物 | 路径 |
|---|---|---|
| 角色实例 | `maintainer/` 共 **39 文件** | `maintainer/` |
| **归档系统** | `code_archive/`：`original/`（冻结原件）+ `annotated/`（带注）+ `VERSION-<NNN>.md` + `SPEC-<NNN>.md` + `_tombstones/` | `maintainer/code_archive/` |
| 边界契约 | K1–K14 / **KN1–KN13** / §0 权力轴 / **§4 补注判定表** / **SPEC 11 个冻结字段** / DoD | `maintainer/role-limit/ROLE-LIMIT.md` |
| 专业原则 | 14 条（KP1–KP14）+ 注意力焦点 + 10 问自检 | `maintainer/principles/PRINCIPLES.md` |
| 记忆 | 11 条 innate LTM + LTM-000/STM-000 + 索引 + 流水 | `maintainer/memory/` |
| 答疑记录 | `QA-LOG.md`（含"被纠正须追加【更正】而非改旧条目"） | `maintainer/script/` |
| 任命信 | 首个任务 + 6 条 AC | `maintainer/mailbox/inbox/WELCOME-maintainer.md` |
| 裁定记录 | 冲突面裁定 + 六项待确认 + G10/G11 | `DECISION-20260926-008` |

## 4. 三条硬要求如何落成可判定机制

| 你的要求 | 机制 |
|---|---|
| **不修改源代码**下补充注释 | **原件按字节冻结归档 + 另存带注副本**；带注副本与原件的 **diff 必须只含以注释符号开头的行**，该结论记入版本卡 |
| **各版本归档**（`code_archive`，与 mailbox archive 区分） | `original/` 写入即冻结 + **SHA-256 清单**；变化只能加版本；未采用版本留**墓碑记录**（不删）；与 `mailbox/archive/` 在**组织维度上彻底分开**（版本 vs 时间） |
| **让人精确理解代码** | `SPEC` 的 11 个冻结字段，其中两项是关键：**事实层与推断层的分离声明**、**未解疑问（`unverified`）——必须列出，禁止省略** |

**本角色的核心风险条款**：*错误的解释比没有解释更危险*——它不会报错、现有机制拦不住，而你会据此维护与裁决。
故自守句写成：**"宁可写'我不确定'，不可写'应该是这样'。"**

## 5. 移交链路（你要求的"两方确认后通知 maintainer"）已接通

我没有把这条写在自己的档案里，而是**逐条签发进三个角色的契约**（这正是上一轮学到的教训）：

| 角色 | 新增义务 |
|---|---|
| `developer` | 交付通过审查且自测通过后 → 通知 `maintainer`（含 commit hash 等）→ **再**报 `management` |
| `software_tester` | 测试**未发现阻断问题**时通知 `maintainer`；**发现问题时不得发** |
| `management` | 验收结论 1 轮内发 `maintainer` **回填**版本卡（归档早于验收，验收结论事后补） |

**归档硬条件**：两封通知齐备，且**两封 commit hash 必须一致**；缺一封 → 发 QUERY，**不得先归档后补**。

## 6. 请你确认的六项（**已按默认值落地，可改**）

| # | 待定项 | 我采用的默认值 | 备选 |
|---|---|---|---|
| 1 | 归档触发 | 两封通知齐备即归档 + 验收结论回填（推荐） | 必须先验收通过才归档 ／ 单方通知即可 |
| 2 | 补注方式 | 原件冻结 + 带注副本（推荐） | 直接在原文件只加注释行（须重新校验并通告） |
| 3 | `code_archive` 位置 | `maintainer/code_archive/`（推荐） | 仓库根 `code_archive/`（需单独裁定单主归属） |
| 4 | 归档粒度 | 全留历史 + **大文件不入库**（存校验值与重建方式）（推荐） | 大文件一并入库 ／ 只留最终通过版 |
| 5 | 疑点去向 | 发 ISSUE 给 `developer`（抄 `management`），只报告不修不裁定（推荐） | 只写进说明书未解疑问 ／ 不主动报告 |
| 6 | 附加产物 | **暂不产出，保留接口**（走读 / 术语表 / 版本差异已在 `script/README.md` 留位） | 全部启用 ／ 部分启用（请点名） |

> 你只需回复形如"1A 2A 3A 4A 5A 6 全要"即可；我据此作小改（契约升版 + NOTIFY），不影响本轮主体交付。

## 7. 验收 (Acceptance)
- [x] 注册表新增 R-006 + "执行层·维护"，并写明"读码目的不同，故不重叠"
- [x] 七目录 + **第 8 个目录 `code_archive/`** 齐备；全部内容落在自身目录内
- [x] ROLE-LIMIT 四段写满（K/KN 双清单 + 补注判定表 + SPEC 冻结字段 + 归档结构）
- [x] PRINCIPLES 14 条 + 注意力焦点 + 10 问自检
- [x] 记忆初始化（11 条 innate LTM + STM-000 + 索引 + 流水）
- [x] **三处新增义务已签发进 developer / software_tester / management 的契约**
- [x] 向全体介绍（NOTIFY 投递五方 inbox + 本角色 outbox）
- [x] 六角色两两"只能做"交集为空；G10/G11 已登记；AUDIT-LOG R10
- [x] 按 §7.2 显式路径提交 git

## 8. 诚实声明
1. **缺口 G10（新增）**：**移交链路未经真实验证**——触发条件依赖两个尚未上岗的角色的新义务。
   若它们不发确认通知，`maintainer` 将永远等不到触发。首次真实交付时我会按"断链"审计。
2. **缺口 G11（新增）**：**说明书的有效性未经检验**——你要求"让人精确理解代码结构"，
   但**没有任何证据**表明它做得到。首次真实归档后需你逐节核对；若仍被误导，说明光有字段不够。
3. **契约 ≠ 证据（第四次适用）**：本角色的全部能力目前只写在契约里。
4. **选项框超时**已如实记入 `PLAN §2.1` 与 `DECISION-008 §1.3`——不掩饰流程瑕疵。
