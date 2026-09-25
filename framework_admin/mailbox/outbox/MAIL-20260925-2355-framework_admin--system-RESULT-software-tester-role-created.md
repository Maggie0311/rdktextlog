---
mail_id: MAIL-20260925-2355-framework_admin--system-RESULT-software-tester-role-created
thread: THREAD-0008-role-software-tester-bootstrap
from: framework_admin
to: system (人类用户)
cc: [management, developer, code_reviewer, software_tester]
date: 2026-09-25 23:55
purpose: RESULT
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - _framework/00-ARCHITECTURE.md
  - _framework/01-ROLE-REGISTRY.md
  - _framework/decisions/DECISION-20260925-006-software-tester-role-adopted.md
  - software_tester/role-limit/ROLE-LIMIT.md
  - software_tester/script/ENVIRONMENTS.md
  - framework_admin/worklog/WORKLOG.md
---

## 1. 背景 (Context)
你下令新增 `software_tester` (R-005)：接收 `management` 分配与 `developer` 代码，**仅在需要时**以**恰当手段**测试，
环境由它决定与适配，必须能读取运行反馈并**科学汇报**；**不得修改程序、不得修改 developer 源码**。

## 2. 目的 (Objective)
回报 R-005 已上岗、根规范升 v1.3、**两条独立验证通道**成立；并声明一项新增缺口 G7。

## 3. 交付物

| 类别 | 产物 | 路径 |
|---|---|---|
| 角色实例 | `software_tester/` 共 **37 文件** | `software_tester/` |
| **环境能力清单** | `ENVIRONMENTS.md`（**全部条目标"假设"，待其上岗实测回填**） | `software_tester/script/` |
| 边界契约 | ROLE-LIMIT（§0 权力轴 + T1–T13 / TN1–TN13 + **适配判定表** + 报告冻结字段 + DoD） | `software_tester/role-limit/ROLE-LIMIT.md` |
| 专业原则 | 15 条可操作准则（守边界 / 管环境 / 管证据 / 纪律）+ 注意力焦点 + 10 问自检 | `software_tester/principles/PRINCIPLES.md` |
| 记忆 | 10 条 innate LTM + LTM-000/STM-000 + 索引 + 流水 | `software_tester/memory/` |
| **根规范 v1.3** | **§7 新增违规码 V8 伪造证据** | `_framework/00-ARCHITECTURE.md` |
| 裁定记录 | 8 项冲突面裁定 + 两通道分离 + G7 | `_framework/decisions/DECISION-20260925-006-software-tester-role-adopted.md` |
| 介绍信 | 新角色介绍 + 对 developer / management / code_reviewer 的接口要求 | `MAIL-20260925-2350-...NOTIFY...` |

## 4. 本轮关键判断

### 4.1 你这条角色其实填的是一个**真空**
R-003 只写代码，R-004 只做**静态**审查（读代码、**不运行**）。**"让程序真实跑起来并取回反馈"此前完全没有角色覆盖。**
R-005 填补的正是这条真空——所以它不是 R-004 的重复，而是另一条通道。

### 4.2 两条独立验证通道（互不替代、互不指挥、都不碰代码）

| 通道 | 角色 | 回答的问题 | 手段 | 产物 |
|---|---|---|---|---|
| **静态审查** | `code_reviewer` | 代码在标准下**有没有问题** | 读代码、按清单核对 | 报告（**判断**） |
| **动态运行** | `software_tester` | 程序实际跑起来**是什么结果** | 构建 / 运行 / 烧录 / 串口 / 远程机 | 报告（**事实**） |

合并这两者会让"没发现问题"与"跑起来没问题"互相冒充——这是本轮最重要的一刀。

### 4.3 "不能改程序"落成了一张**可判定的表**
你允许"建副本测试"，又禁止"修改程序测试"——这两条必须同时成立。所以我把手段分成两类：

| 类别 | 例子 | 允许？ |
|---|---|---|
| **非语义适配** | 编译/链接参数、设备与端口配置、路径、环境变量、外部依赖部署、供电接线等物理条件 | **允许**，但必须**逐条声明** |
| **语义改动** | 改逻辑/常量/接口、加桩替换真实模块、注释掉失败分支、放宽断言 | **禁止** → 必须发 `ISSUE` 说明"不改则不可测"，由 `management` 裁定是否让它另开 `task_id` 请 developer 提供测试挂钩 |

这样既满足"可复制副本测试"，又保证**跑的始终是同一个程序**。

### 4.4 新增违规码 **V8 伪造证据**（根规范 v1.3）
编造、篡改或**选择性呈现**用于支撑结论的证据（运行输出 / 日志 / 编译结果 / 测试记录 / 进度状态）。
理由：这个角色的全部价值就在证据可信，而 V1–V7 中**没有一条**覆盖"证据造假"。
它同时给各角色内部的禁令（developer 谎报完成度、reviewer 瞒报、tester 编造运行结果）提供了**跨角色审计抓手**。

## 5. 验收 (Acceptance)
- [x] 注册表新增 R-005 + 三层结构表新增"执行层·验证" + 两通道声明
- [x] 七目录齐备（37 文件），全部内容落在**自身目录内**（架构 §2.1 自足性复检通过）
- [x] ROLE-LIMIT 四段写满；TN 每条标注"应由谁做"；含适配判定表与报告冻结字段
- [x] PRINCIPLES ≥12 条（实际 15 条）+ 注意力焦点表 + 10 问自检
- [x] 记忆初始化（10 条 innate LTM + STM-000 + 索引 + 流水）
- [x] 任命信含首个任务（**实测环境回填 + 一次端到端最小验证**）与 6 条 AC
- [x] 向 developer / management / code_reviewer 发出介绍与接口要求（NOTIFY ×4 投递）
- [x] 五角色两两"只能做"交集为空；G7 已登记；AUDIT-LOG R7
- [x] 按 `05-CONVENTIONS v1.2 §7.2` 显式路径提交 git

## 6. 期望回复 (Expected Reply)
无需回复。下一步：向 `management` 提需求 → 它决定**要不要测**并下发含"要回答的问题"的测试任务 →
`software_tester` 上岗后先**实测环境能力**，再谈测试。

## 7. 备注 (Notes) — 诚实声明
1. **G7（新增，重要）**：本框架至今**没有任何证据**表明本机能构建/运行/烧录/连远程机。
   `ENVIRONMENTS.md` 现阶段**全部标"假设"**——这是诚实状态。该角色上岗首任务就是实测回填。
   **在它实测完成前，任何人（包括我）都不得对外承诺"可以测试"**。
2. **测试不是默认强制门**：与 §4.1 审查门不同，**要不要测由 `management` 决定**——你说的"仅在需要的时候"，
   我把它落成了"每个测试任务必须能回答一个**具体可判定的问题**，写不出问题就发 QUERY"。
3. 关于"注入相关记忆"：新角色注入了 10 条 innate LTM；**developer / management / code_reviewer 的记忆我没有代写**，
   只在通告里要求它们自行记录——依据 N2，记忆必须由经历者本人沉淀。
4. **契约 ≠ 证据（第三次适用）**：你对本角色的能力要求（能烧录、能在远程机跑、能读回反馈）目前**只写在契约里**，
   在 `ENVIRONMENTS.md` 被实测回填之前，一律按"未验证"对待。
