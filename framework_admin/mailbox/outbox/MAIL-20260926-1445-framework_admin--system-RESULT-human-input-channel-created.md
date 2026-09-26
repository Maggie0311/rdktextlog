---
mail_id: MAIL-20260926-1445-framework_admin--system-RESULT-human-input-channel-created
thread: THREAD-0012-human-input-channel
from: framework_admin
to: system (人类用户)
cc: [management, developer, code_reviewer, software_tester, maintainer]
date: 2026-09-26 14:45
purpose: RESULT
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - management/from_human/README.md
  - HANDBOOK.md
  - _framework/decisions/DECISION-20260926-011-human-input-channel.md
---

## 1. 背景 (Context)
你问：`management` 里有没有一个人给你传输文件的入口？
**核查结果：没有。** `management/` 下当时只有标准七目录，你与它沟通工作目标时**只能口头描述**。

## 2. 目的 (Objective)
回报：入口已建立、规则已内联进 `management` 契约与记忆、人类用户手册已升版。

## 3. 交付物：`management/from_human/`

```
management/from_human/
├── README.md         ← 写给你看的：放什么、怎么放、它会怎么处理
└── INTAKE-LOG.md     ← management 维护的登记表（只追加）：哪个文件用在了哪个任务
```

### 你怎么用（只有两步）

1. **把文件复制到 `management/from_human/`**（放这一层即可）；
2. 提需求时带一句：**「参考 `management/from_human/<文件名>`」**。

### 三条保证（写进了它的契约）

| # | 保证 | 落点 |
|---|---|---|
| 1 | **只有你能写这个目录**；`management` 只读 | 权限矩阵**只读例外行** + **MN14**（禁止修改/移动/重命名/删除） |
| 2 | **不说也能被看到**：它每次开工都会扫这个目录，与登记表对比，找出未处理文件 | 新增 **§3.1 开工前置** |
| 3 | **以路径引用你的文件，不复制内容**——永远以你的原件为准 | §3 输入契约新增"人类参考文件"行 |

**另外**：它读不懂或发现你的文件与需求矛盾时，**会发信问你，不会自己猜**。

## 4. 记忆与手册已同步

- **`management` 记忆**：注入 **`LTM-007`**（innate，confidence 1.00）"人类投放的文件是一手依据：只读、登记、以路径引用，绝不改动"；索引与固化流水同步。
  > 关于"代写记忆"的边界我说明一下：注入的是**规则类（innate）**条目——与建角色时注入 `LTM-000` 是同一机制，**不违反 N2**；**经验型记忆仍由它自己写**。
- **`HANDBOOK.md` → v1.1**（7 处更新）：§3.1 角色表新增"文件入口"行、**§4 第 1 步新增「要给它参考文件怎么办」**、
  §6 产物地图、常用入口表、§7 你的权利、§9 红线、§12 术语表。

## 5. 合规性说明（需要留证的一点）

这个目录**不违反**"无公共工作空间"：它**只有一个写入者（你）**，是**单主区**；
且位于 `management/` 目录**之内**，不在仓库根另立顶层区。已记入 `DECISION-20260926-011 §3`。

## 6. 一处刻意的克制

**未来若其他角色也需要人类投放入口，我不会默认推广**——须逐角色单独裁定。
理由：入口一多，你的依据就会散落在多处，反而容易漏读（这是"最小充分"原则的应用）。

## 7. 验收 (Acceptance)
- [x] 核查确认此前无此机制
- [x] `management/from_human/`（README + INTAKE-LOG）建立
- [x] 规则内联进 `management` 契约：权限矩阵例外 / §3 输入契约 / **§3.1 开工前置** / **MN14**
- [x] `management` 记忆更新（LTM-007 innate + 索引 + 流水）
- [x] `HANDBOOK.md` 升至 v1.1（含"要给它参考文件怎么办"一节）
- [x] TASK 已投递 `management`（抄送其余四角色）；`AUDIT-LOG` R13；`script/INDEX` 34–36；worklog #69–#72
- [x] 按 §7.2 显式路径提交 git

## 8. 备注 (Notes)
- **待验证**：尚无真实投放；"开工扫描 + 登记 + 路径引用"是否顺手，要等 `management` 上岗后用它跑一次才知道。
- 大文件（几十 MB 以上）建议不要直接放，改为给路径或链接。
