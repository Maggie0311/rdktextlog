# DECISION-20260924-005 — 废止 `src/` 产物区，交付产物回归各角色 `script/`

| 字段 | 值 |
|---|---|
| 决定 ID | DECISION-20260924-005 |
| 日期 | 2026-09-24 |
| 裁决人 | framework_admin (R-001) |
| 触发 | **人类用户（委托层）直接指令**："src 不存在，但正好也不需要……过程代码写在 script 里面不就行了？很符合我对于每个角色的文件夹的定义……最终输出代码到自己的 script 比较合理，之后可以打包发邮件给其他角色进行沟通和推进下一步操作。请你检查是否设立了没有必要的 src，并更新 developer 角色所有有关 src 的规定。" |
| 依据条款 | `_framework/00-ARCHITECTURE.md §2/§3`（七目录与 `script/` 的定义）、`_framework/05-CONVENTIONS.md` v1.2 §7.1、`framework_admin/principles/PRINCIPLES.md` P6（最小充分）/ P10（规范性递减） |
| 争议双方 | 无（委托层指令 + 架构自我一致性修正） |
| 废止对象 | `DECISION-20260923-003 §2.4`（设立 `src/` 为项目源码产物区） |

## 1. 事实 (Facts)
1. `src/` **从未被创建**（`Test-Path src` = False），`developer/script/` 下当时仅有 `README.md` 与 `INDEX.md`。
   → **无任何代码产物需要迁移**。
2. 全仓 `src/` 引用共 **40 处**，分布于约 20 个文件（含根约定、两份角色契约、标准区、记忆条目、任命信与已发出的邮件）。
3. 委托层判定：产物应写在各角色自己的 `script/` 内——这与"每个角色一个文件夹"的定义一致；交付时打包、经邮件发给其他角色推进下一步。

## 2. 决定 (Decision)
1. **废止 `src/` 产物区设计**。仓库中不再存在跨角色共享的产物目录。
2. **交付产物一律落在生产者自己的 `script/` 下**：
   `developer` 的代码 → `developer/script/`；`code_reviewer` 的报告 → `code_reviewer/script/`；
   `management` 的拆解书与台账 → `management/script/`。
3. **交付与流转方式（新增，冻结）**：
   - 打包件：`<role>/script/dist/<task_id>.<ext>`（视体积与可重建性决定是否入库）；
   - 交付邮件（`RESULT` / `HANDOFF`）必须给出：① 路径 ② **commit hash** ③ 可复现的构建 / 验证命令；
   - `attachments` 字段填交付件路径；**跨角色推进一律经邮箱**，不得直接改他方产物。
4. **根约定升级 `05-CONVENTIONS.md` → v1.2**：§7.1 重写（三类区域 → 交付产物区 = 各自 `script/`），§7.2 提交隔离不变。
5. **子目录结构与测试目录位置由产物所有者自定**，但必须在其 `script/README.md` 中声明；测试目录默认 `script/tests/`。

## 3. 我对自己这个设计的评估（不掩饰）

**这不是"口味差异"，是一处真实的自相矛盾，责任在我。**

| 问题 | 说明 |
|---|---|
| 与框架自身定义冲突 | `00-ARCHITECTURE §2/§3` 早已定义 `script/` = "我**产出**了什么可用东西 / 可复现的资产"。代码正是可复现资产。我却在角色目录之外另立产物区 |
| 违背 P6 最小充分 | 为了一个并不存在的需求（"项目需要一个共享源码树"），引入了第三种区域类型与一整套写入者规则 |
| 违背 P10 规范性递减 | 该设计把"交付物放哪"这件**角色内部**的事，上升成了需要根规范约束的**跨角色**规则 |

> 教训已写入本角色短时记忆（`STM-007`）：**在角色目录之外新设产物区之前，先检查框架自身的目录定义是否已经覆盖了它。**

## 4. 变更清单（本轮实际改动）

| 文件 | 变更 |
|---|---|
| `_framework/05-CONVENTIONS.md` | **v1.1 → v1.2**：§7.1 重写，`src/` 废止 |
| `_framework/decisions/DECISION-20260923-003` | 顶部加"§2.4 已被本文废止"状态指引（**不改写结论**） |
| `developer/role-limit/ROLE-LIMIT.md` | D1/D2/D4/D6/D7 及新增 D13、权限矩阵、§4 输出契约、接口冻结 |
| `developer/principles/PRINCIPLES.md` | 自检清单第 6 问的路径 |
| `developer/script/README.md` | **重写**：本目录即产物区（含代码），补结构 / 打包 / 流转说明 |
| `developer/script/INDEX.md` | 登记规则改为"登记交付单元（按 task_id），不逐文件登记" |
| `developer/memory/index/MEMORY-INDEX.md` | 待办条目中的路径 |
| `developer/mailbox/inbox/WELCOME-developer.md` | **重新签发 v1.1**（旧版复制入 `archive/2026-09/`，新信标注替代关系） |
| `code_reviewer/role-limit/ROLE-LIMIT.md` | CR11、权限矩阵、RN3、§3 输入契约 |
| `code_reviewer/standard/README.md` | 优先级表第 2 行 |
| `code_reviewer/script/README.md` | 路径说明 |
| `code_reviewer/memory/long-term/LTM-001` | 路径 + 修订行 |
| `code_reviewer/mailbox/inbox/WELCOME-code_reviewer.md` | **重新签发 v1.1**（同上） |
| 新增 | `DECISION-20260924-005`（本文）、`PLAN-20260924-fix-artifact-area.md`、NOTIFY v1.2 |

**保留原样（历史不可改写）**：`mailbox/outbox/` 中已发出的 4 封信、`worklog/WORKLOG.md` 历史条目、
已提交的 `PLAN-20260923-*`、`DECISION-20260923-003/004` 正文。对它们的处理方式是**新件交叉引用**，
而非回改——依据 `05-CONVENTIONS §4`（不可变性）与 P9（可审计性）。

## 5. 授权来源与只读声明的处理（必须留痕）

我在 `DECISION-002 §6`、`003 §7`、`004 §6` 中声明过：`management/`、`developer/`、`code_reviewer/` 目录对我**只读**。

本次直接修订了 `developer/` 与 `code_reviewer/` 的契约与记忆条目。**这不是自破规则**，理由：
1. 指令来自**委托层（人类用户）**——本框架的最高决策权，高于我自设的自我约束；
2. 修订内容为**错误更正**（消除规范自相矛盾），非单方面扩张权限或改变边界分配；
3. 变更**逐处留痕**（本文件 + worklog + NOTIFY），符合 P18"破例要留痕"。
4. `management/` 未做任何修改（其契约不涉及 `src/`）；其 inbox 中的 v1.1 NOTIFY 由新 NOTIFY 交叉引用替代。

> 后续若同类更正再次发生，仍应优先由该角色**自己**发起（发 TASK 请 framework_admin 升版签发）；
> 本次由委托层直接触发，属例外而非常态。

## 6. 残留风险（已知，不掩盖）

| 风险 | 说明 | 重议条件 |
|---|---|---|
| 若项目将来需要独立的构建 / 部署布局（例如 CI 期望特定源码根目录） | 届时可能需要引入构建产物区或调整目录 | 当出现**真实的、被工具链强制的**目录要求时重新裁定；不得凭预想提前设立 |
| 代码与文档同处 `script/`，可能混淆"过程文档"与"交付代码" | 由 `script/README.md` 声明的结构区分（建议源码入子目录） | 若混淆实际造成协作问题 |
| 交付靠邮件传递路径与打包件，大文件可能不便 | 打包件是否入库由所有者声明；`commit hash` 是权威依据 | 若无仓库访问能力的一方成为消费者 |

## 7. 申诉 (Appeal)
任何角色对本次废止或新的交付流转方式有异议，须附**具体条款 + 反例**发 ISSUE，可申诉一次。

## 8. 后续 (Follow-ups)
- [ ] `developer` 上岗任务中的 `AC2` 已随之改为 `developer/script/README.md`（新任命信 v1.1）
- [ ] 首个真实交付时验证第 3 条的交付方式（路径 + commit hash + 可复现命令 + 打包件）是否够用
- [ ] 若 `management` 认为其 `ROLE-LIMIT` 需要写入交付流转条款，由其发 TASK 请我升版
