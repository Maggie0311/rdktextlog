---
mail_id: MAIL-20260924-2315-framework_admin--system-RESULT-artifact-area-fixed
thread: THREAD-0006-artifact-area-v1-2
from: framework_admin
to: system (人类用户)
cc: [management, developer, code_reviewer]
date: 2026-09-24 23:15
purpose: RESULT
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - _framework/05-CONVENTIONS.md
  - _framework/decisions/DECISION-20260924-005-artifact-area-fix.md
  - _framework/decisions/DECISION-20260923-003-developer-role-adopted.md
  - developer/role-limit/ROLE-LIMIT.md
  - developer/script/README.md
  - code_reviewer/role-limit/ROLE-LIMIT.md
  - framework_admin/plan/PLAN-20260924-fix-artifact-area.md
---

## 1. 背景 (Context)
你指出 `src/` 既不存在也不必要：代码写在角色自己的 `script/` 里，更符合"每个角色一个文件夹"的定义，
交付时打包经邮件流转即可。要求我核查该设计是否多余，并更新 developer 角色的全部相关规定。

## 2. 目的 (Objective)
回报：**核查结论成立，`src/` 已废止**，全部相关文本已改写；同时报告核查中发现的**我自己的两处失误**。

## 3. 核查结论（你要的"是否设立得没有必要"）

**结论：没有必要，且这不是口味差异，是自相矛盾——责任在我。**

| 核查项 | 结果 |
|---|---|
| `src/` 是否存在 | **False（从未创建）** → 零迁移成本 |
| 全仓引用面 | **40 处**，分布于约 20 个文件 |
| 与框架自身定义的关系 | `00-ARCHITECTURE §2/§3` 早已定义 `script/` = "我**产出**了什么可用东西 / 可复现的资产"。**代码正是可复现资产。** 我却在角色目录之外另立产物区 |
| 额外代价 | 为此多写了一整套跨角色共享写入规则（v1.1 §7.1），把一个**角色内部**的问题上升成需要根规范约束的**跨角色**问题（违反 P6 最小充分、P10 规范性递减） |

**你的模型更简洁**：一个角色一个文件夹，产物落在自己的 `script/`，跨角色靠邮箱流转——**仓库里不需要共享产物目录**。

## 4. 已完成的修改

| 类别 | 变更 |
|---|---|
| 根规范 | `05-CONVENTIONS.md` **v1.1 → v1.2**：§7.1 重写为"`<role>/script/**` = 该角色的交付产物区（代码 / 报告 / 脚本 / 打包件）"，写明 `src/` 废止及依据 |
| 裁决 | 新增 `DECISION-20260924-005`：废止裁定 + **交付流转方式**（冻结）+ 残留风险；并在 `DECISION-003` 顶部加"§2.4 已被废止"状态指引（**只加指引，不改原结论**） |
| developer | 契约 D1/D2/D4/D6/D7 + **新增 D13（打包交付件）**、权限矩阵、§4 输出契约、接口冻结、上游依据；自检清单；`script/README.md` **重写**；`script/INDEX.md`（登记粒度改为**交付单元**，不逐文件登记）；记忆索引 |
| code_reviewer | 契约 CR11 / 权限矩阵 / RN3 / 输入契约；`standard/README.md` 优先级表；`script/README.md`；LTM-001（路径 + 修订记录行） |
| 任命信 | **两份重新签发（r2）**，旧版复制入各自 `archive/2026-09/`，新信以 `supersedes` 字段标注替代关系（协议 v1.1 §2.1 的"常驻件被替代"条款首次实际执行） |
| 通告 | `MAIL-20260924-2300` 已投递 management / developer / code_reviewer（含"你 inbox 中旧通告信仅 §7.1 部分被取代"的说明） |

### 新的交付流转方式（已冻结）

- 产物目录：`<role>/script/`；子目录结构与测试目录位置由产物所有者自定，但**必须写在其 `script/README.md`**；
- 打包件：`<role>/script/dist/<task_id>.<ext>`（是否入库由所有者定，但必须可重建）；
- 交付邮件必须给出：**① 路径 ② commit hash ③ 可复现的构建 / 验证命令**；打包件路径写入 `attachments`；
- **跨角色推进一律经邮箱**，不得直接改他方产物。

## 5. 我在核查中发现的两处自己的失误（一并报告）

1. **流程漏项**：`developer` 与 `code_reviewer` 的 v1.0 任命信当初**只投递 inbox、未按协议 §2 在 outbox 留副本**。
   本轮已按原内容补齐两份副本，并记入 `AUDIT-LOG` R5 与通告信 §7。
2. **架构缺陷**：即本次的 `src/`——已写入教训条 `STM-007`（salience: high，按"踩坑并复盘"口径置信度 0.40）：
   **在角色目录之外新设共享区之前，先查框架自身的目录定义是否已经覆盖它。**

## 6. 关于"改了他方目录"的说明（必须留痕）

我在 `DECISION-002 §6`、`003 §7`、`004 §6` 中声明过对 `management/`、`developer/`、`code_reviewer/` 目录只读。
本次直接修订了后两者的契约与记忆条目。**这不是自破规则**：指令来自**委托层**（本框架最高决策权），
内容为**错误更正**（非扩权、非改边界分配），且逐处留痕（`DECISION-20260924-005 §5` + worklog + NOTIFY）。
`management/` **未做任何修改**（其契约不涉及 `src/`）。

> 后续同类更正仍应优先由角色自己发起（发 TASK 请我升版签发）；本次由委托层直接触发，属例外而非常态。

## 7. 验收 (Acceptance)
- [x] `src/` 不再是任何**规定**的一部分（仅残留于历史件与"废止说明"）
- [x] `developer` / `code_reviewer` 全部相关文本指向 `<role>/script/`
- [x] 两份任命信重签、旧件归档、替代关系标注
- [x] NOTIFY 已投递全体；各角色被要求**自行**更新自己的记忆（我不代写他方 memory）
- [x] 全仓 `grep "src/"` 复扫通过
- [x] 按 `v1.2 §7.2` 显式路径提交 git

## 8. 期望回复 (Expected Reply)
无需回复。下一步把真实项目需求交给 `management` 即可；`developer` 上岗时会先补齐 `script/README.md` 的产物区结构声明，
之后每一轮交付走"开发 → 审查 → 验收"，交付件按新的流转方式给出路径与 commit hash。
