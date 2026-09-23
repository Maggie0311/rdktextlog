# 记忆模型 (Memory Model) — 仿动物记忆 + 置信规则

> 版本: v1.0 · 维护者: framework_admin
> 目标：让角色**越做越聪明**，同时**不被错误经验污染**。

---

## 1. 生物学类比（我们模仿什么）

| 动物记忆机制 | 在本框架中的对应 |
|---|---|
| 工作记忆（working memory，秒~分钟，容量极小） | `short-term/` 的最新条目，容量上限 7±2 条 |
| 短期记忆（海马体，易失、需重复才固化） | `short-term/` 全部条目，滑动窗口 |
| 长期记忆（皮层，稳定、可终身） | `long-term/`，需通过固化（consolidation）流程 |
| 长时程增强 LTP（"一起激发的神经元连在一起"） | 同一经验被**多次独立复用成功** -> 置信度上升 |
| 突触衰减 / 遗忘曲线 | 长期未复用的记忆按轮次衰减置信度 |
| 情绪唤醒标记（杏仁核） | 出错/造成损失的教训获得 `salience: high`，衰减更慢 |
| 再巩固（reconsolidation） | 记忆被取用时可被修正，修正需记版本 |

**核心原则：短期记忆是"候选"，长期记忆是"已验证的信念"。两者不是等级，而是状态。**

---

## 2. 目录与文件

```
memory/
├── long-term/
│   ├── LTM-000-BOOTSTRAP.md      角色出厂自带的先验知识
│   ├── LTM-<NNN>-<slug>.md       每条一个文件（原子化，勿混装）
│   └── ...
├── short-term/
│   ├── STM-000-BOOTSTRAP.md
│   ├── STM-<NNN>-<slug>.md       每条一个文件
│   └── ...
└── index/
    ├── MEMORY-INDEX.md           总表：ID / 标题 / 位置 / 置信度 / 证据数 / 状态
    ├── CONSOLIDATION-LOG.md      每次晋升/降级/遗忘的流水
    └── CONFIDENCE-RULES.md       本角色对置信规则的实例化细则（可选）
```

---

## 3. 条目标准格式（强制字段）

```yaml
---
id: LTM-003
title: 一句话结论（必须是可执行的断言，不是描述）
layer: long-term            # long-term | short-term
status: active              # candidate | active | dormant | deprecated | retracted
confidence: 0.82            # 0.00 - 1.00
evidence_count: 4           # 独立证据次数（不同任务算不同证据）
success_count: 3
failure_count: 1
source_tasks: [T-2026-02-10-a, T-2026-02-12-b]
first_seen: 2026-02-10
last_used: 2026-02-14
last_reviewed: 2026-02-14
salience: high              # high(踩过坑/损失) | medium | low
decay_rate: 0.05            # 每闲置轮次的置信度衰减
promoted_from: STM-007      # 若由短时晋升
tags: [boundary, process]
---

## 断言 (Claim)
一条可被证伪的陈述。

## 适用条件 (When it holds)
在什么条件下这条成立；什么条件下**不成立**。

## 证据 (Evidence)
| 日期 | 任务 | 结果 | 备注 |
|---|---|---|---|
| 2026-02-10 | T-...-a | 成立 | ... |

## 反例 (Counter-evidence)
已知的例外。

## 应用方式 (How to apply)
下次遇到 X 时，应该做 Y。
```

---

## 4. 置信度规则

### 4.1 初始值
- 单一任务观察得到的短期记忆：`confidence = 0.30`
- 一次**踩坑并复盘**得到的短期记忆：`confidence = 0.40`，`salience = high`
- 来自 `_framework/` 根规范或 role-limit 的强制约束：直接 `confidence = 1.00`，直接入 long-term（属"本能"，非"经验"）

### 4.2 更新规则（贝叶斯式增量）

| 事件 | 置信度变化 |
|---|---|
| 在新任务中应用且**成功** | +0.10（evidence_count +1, success +1） |
| 在新任务中应用但**失败/不适用** | −0.15（evidence_count +1, failure +1），并必须补写"适用条件" |
| 被他人（另一方角色/审计）**独立确认** | +0.15（evidence_count +1） |
| 被他人**反驳且有证据** | −0.25 |
| 一个轮次（round）**闲置未用** | −decay_rate（高 salience 减半衰减） |
| 由"猜测/推断"引入且无证据 | 不得 > 0.30 |

置信度区间语义：

| 区间 | 含义 | 允许的用法 |
|---|---|---|
| 0.00–0.29 | 假设 | 只能写进 short-term，禁止据此做不可逆决策 |
| 0.30–0.59 | 候选 | short-term 正式条目；可用，但必须标注不确定 |
| 0.60–0.79 | 可信 | 可作为工作依据；可进入 long-term 但状态为 `candidate` |
| 0.80–1.00 | 信念 | long-term `active`；可作为默认做法 |

### 4.3 晋升规则（short-term -> long-term）

必须**同时**满足：

1. `confidence >= 0.75`
2. `evidence_count >= 3`，且来自 **>= 2 个不同任务**
3. 至少 **1 次**是"主动应用并成功"（不是被动观察）
4. 至少 **1 次**被另一个角色或审计独立确认（降低同源偏差）
5. 在长期记忆中尚不存在冲突条目（若有冲突，先写"冲突裁决"）

晋升动作：
- 在 `long-term/` 新建条目，`promoted_from` 指向短时 ID
- 短时条目标记为 `promoted` 并保留（不删除，保留可追溯）
- 在 `CONSOLIDATION-LOG.md` 追加一行

### 4.4 衰减与遗忘（禁止无限膨胀）

- 每完成一个任务记 1 轮。闲置条目按 `decay_rate` 扣减。
- `confidence < 0.45` 的 long-term 条目 -> `status: dormant`（仍可检索，不主动使用）
- `confidence < 0.25` 或 `last_used` 超过 20 轮 -> **移出 long-term**，降回 short-term 或直接删除，并在日志记 `forgot`
- 高 salience（踩过坑的教训）衰减速率减半，永不自动删除，只可 `dormant`
- 短时记忆容量：**最多 12 条**。超出时优先丢弃 `confidence` 最低且 `salience: low` 的条目。

### 4.5 禁止事项

- ❌ 把单次观察当信念（V5 违规）
- ❌ 修改历史证据表（只能追加）
- ❌ 无证据地提高他人条目的置信度
- ❌ 用"我觉得"替代证据字段

---

## 5. 记忆的使用（读记忆的正确姿势）

1. 开工前读 `memory/index/MEMORY-INDEX.md` 总表，按 `confidence` 降序看前 N 条。
2. 只对 `status: active` 且 `confidence >= 0.60` 的条目做默认依据。
3. `candidate/dormant` 条目只作提示，需在本任务中重新验证。
4. 若本任务中用到了某条记忆，**必须**更新其 `last_used` 与计数（这就是"再巩固"）。
5. 任务结束写短时记忆时，显式回答："这次任务是否产生了可复用的经验？"
   - 是 -> 写新短时条目
   - 否 -> 在 worklog 注明"无新增经验"，不硬凑

--- 

## 6. 人类用户初始化给每一个角色的长期记忆（创建任何角色都自带的先天性行为）

1. 每做一次任务，就要提交项目根目录的本地git仓库，写清楚commit信息，便于版本回退。
