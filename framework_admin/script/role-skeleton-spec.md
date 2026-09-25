# 角色骨架规格 (Role Skeleton Spec) — v1.0

> 所有者: framework_admin · 类型: 规范产物 · 创建: 2026-02-14 · 最近验证: 未验证
> 用途: 创建任何新角色时，**逐项复制**本规格，一次建全，不允许缺项。

## 1. 目录与文件清单（共 20 项）

```
<role>/
├── mailbox/
│   ├── README.md                        [用途+流转规则]
│   ├── inbox/README.md                  [开工必读；常驻例外]
│   ├── inbox/WELCOME-<role>.md          [framework_admin 任命信, keep_in_inbox: true]
│   ├── outbox/README.md
│   ├── archive/README.md
│   ├── archive/YYYY-MM/.gitkeep
│   └── drafts/README.md
├── memory/
│   ├── README.md
│   ├── long-term/README.md
│   ├── long-term/LTM-000-BOOTSTRAP.md   [角色先验/强制约束, promoted_from: innate]
│   ├── short-term/README.md
│   ├── short-term/STM-000-BOOTSTRAP.md  [初始 0 条说明，勿硬凑]
│   └── index/
│       ├── README.md
│       ├── MEMORY-INDEX.md              [总表]
│       └── CONSOLIDATION-LOG.md         [流水]
├── role-limit/
│   ├── README.md
│   └── ROLE-LIMIT.md                    [四段式, 见 §2]
├── principles/
│   ├── README.md
│   └── PRINCIPLES.md                    [可操作准则, 见 §3]
├── script/
│   ├── README.md
│   └── INDEX.md                         [产物登记表, 初始为空表]
├── plan/
│   ├── README.md
│   └── (首个 PLAN 由首个任务产生)
└── worklog/
    ├── README.md
    └── WORKLOG.md                       [初始只有表头与月份分节]
```

> **自足性（v1.2 强制）**：上述全部内容都位于新角色**自己的目录内**。角色目录必须**自足**——
> 不得要求、也不得引用任何跨角色共享的**写入区**（`00-ARCHITECTURE.md §2.1`）。
> 跨角色流转一律经邮箱（`RESULT` + 路径 + commit hash）。**只读访问他方产物不受此限。**
>
> **义务闭合性（v1.4 强制）**：新角色的**全部行为义务**必须写进它**自己的目录**，
> 使其**只读自己的目录就能知道该怎么做**（`00-ARCHITECTURE.md §2.1.1`）。
> 禁止用"见 framework_admin 的 `_framework/xx`"作为义务来源；引用只允许用于**溯源**。
> 需要写进它目录的通用规则至少包括：**邮件字段与消息义务**（`mailbox/README.md`）、
> **记忆规则与阈值**（`memory/README.md`）、**日志格式**（`worklog/README.md`）、
> **计划骨架**（`plan/README.md`）、**产物与交付规则**（`script/README.md`）、
> **提交隔离规则**（`role-limit` 或 `principles`）。

## 2. `ROLE-LIMIT.md` 强制四段

1. **一句话使命** —— 必须能被证伪，且不能与其他角色互换（P5）。
2. **只能做 (MAY ONLY DO)** —— 表格：编号 / 动作 / 输入 / 输出 / 落到哪个目录。列表之外默认不做。
3. **绝不能做 (MUST NEVER DO)** —— 表格：编号 / 禁止动作 / 为什么 / **应由谁做**。第三列缺一不可。
4. **输入输出契约 + 升级路径 + 完成判定** —— 含"接口冻结"声明与"列表外请求"的处理方式。

## 3. `PRINCIPLES.md` 强制形态

- 每条写成 `遇到 X 时，先做 Y，因为 Z`，禁止口号。
- 必须包含一节 **注意力焦点表**（我做 / 我刻意忽略），用于对抗角色失焦。
- 必须包含一节 **自检清单**，供交付前逐条自问。

## 4. 创建检查清单

- [ ] 在 `_framework/01-ROLE-REGISTRY.md` 登记行
- [ ] §1 的 20 项文件全部落盘
- [ ] §2 的四段全部写满，无空段
- [ ] §3 的准则 ≥8 条且均可操作
- [ ] 对**全部既有角色**两两做"只能做"集合交集检查 -> 交集必须为空
- [ ] 对工作流每个环节做覆盖检查 -> 无"没人管"的环节
- [ ] **自足性检查**：新角色产物全部落在其自身目录内，未创建/引用任何跨角色共享写入区（架构 §2.1）
- [ ] **义务闭合性检查（v1.4 新增）**：逐条列出该角色的行为义务，逐条确认"只读它自己的目录能否知道该怎么做"；
      凡答案是否定的，**必须内联**到它的目录内；`_framework/` 引用只允许作溯源
- [ ] **写入者唯一性检查**：涉及的每块区域"写入者数量"均为 1
- [ ] 向新角色 `mailbox/inbox/` 投递 WELCOME 任命信（含 purpose/priority/deadline/AC）
- [ ] 在本角色 `worklog/WORKLOG.md` 追加创建记录
- [ ] 在本角色 `memory/short-term/` 记录本次创建经验（若产生）

## 5. 已知缺口

- 本规格尚**无自动化脚本**（计划 `build_role_skeleton.ps1`），当前为手工执行，存在遗漏风险（DECISION-20260214-001 §3 G2）。
