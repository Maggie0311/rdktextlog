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
- [ ] 向新角色 `mailbox/inbox/` 投递 WELCOME 任命信（含 purpose/priority/deadline/AC）
- [ ] 在本角色 `worklog/WORKLOG.md` 追加创建记录
- [ ] 在本角色 `memory/short-term/` 记录本次创建经验（若产生）

## 5. 已知缺口

- 本规格尚**无自动化脚本**（计划 `build_role_skeleton.ps1`），当前为手工执行，存在遗漏风险（DECISION-20260214-001 §3 G2）。
