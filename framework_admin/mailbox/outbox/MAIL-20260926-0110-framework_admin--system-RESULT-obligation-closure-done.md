---
mail_id: MAIL-20260926-0110-framework_admin--system-RESULT-obligation-closure-done
thread: THREAD-0009-framework-scope-and-mail-voice
from: framework_admin
to: system (人类用户)
cc: [management, developer, code_reviewer, software_tester]
date: 2026-09-26 01:10
purpose: RESULT
priority: P1
deadline: -
requires_reply: false
attachments: []
references:
  - framework_admin/_framework/decisions/DECISION-20260926-007-obligation-closure.md
  - framework_admin/_framework/00-ARCHITECTURE.md
  - framework_admin/plan/PLAN-20260925-framework-scope-and-mail-voice.md
---

## 1. 背景 (Context)
委托层质疑 `_framework/` 的所属与它被要求给其他角色阅读是否合理，并授权 framework_admin
按自身建议**完整修改其他角色不正确的文件**；同时判定问题二（邮件人称）不成立，指示**只处理问题一**。

## 2. 目的 (Objective)
回报问题一已按**方案丁（私有化 + 内联化 + 制度化）**处理完毕；问题二按其判定关闭并留档。

## 3. 回答：`_framework/` 到底是什么

它 **不是共享规范，是 framework_admin 的内部档案**，内含四类：立法底稿、角色登记与图纸、裁决与审计、模板。
其中"通用规则"对角色**有约束力**，但**载体错了**——我用"**引用**"（"见 `_framework/xx`"）代替了"**签发**"（写进对方自己的契约）。
后果：契约不自足、阅读负担外泄、规范易漂移。**已全部改为签发内联。**

## 4. 已完成的改造（方案丁）

| 层 | 变更 |
|---|---|
| **根规范** | `00-ARCHITECTURE.md` **v1.3 → v1.4**：新增 **§2.1.1 义务闭合性**（判据：只读它自己的目录，能否知道该怎么做）、**§2.1.2 `_framework` 定位**（内部档案；只读权限保留、阅读义务取消；档案与契约冲突以契约为准） |
| **档案自述** | `_framework/README.md` 重写：明确"不是共享规范"、四类内容、"通用规则通过签发生效"、变更须同步更新受影响角色的契约 |
| **四角色契约** | 逐条内联：邮件字段与消息义务 / 记忆规则与晋升阈值 / 日志格式 / 计划骨架 / 产物区与交付四要素 / **提交隔离全文** / **审查门三方各自一侧** / 产物自足 / 接口冻结 / 伪造证据红线；`上游依据` 改"仅供溯源"，新增「**自足声明**」 |
| **记忆溯源** | 各角色 `LTM-000`、`CONSOLIDATION-LOG` 与相关 LTM 证据行："来自 `_framework/` 根规范" → "来自本角色契约的强制约束" |
| **制度化** | `script/role-skeleton-spec.md` §1/§4 与 `01-ROLE-REGISTRY.md` 检查清单新增**义务闭合性检查**（v1.4 强制）；固定问法："只读它自己的目录，能否知道该怎么做？" |
| **任命信** | 四封（management / developer / code_reviewer / software_tester）**重新签发**：删除"读完 `_framework/` 六份根规范"，改为"读你自己目录内的契约与 README——它们已自足"；旧版归档，新信 `supersedes` 标注 |

### 最尖锐的一处实例（值得单独说）
**审查门**是跨角色规则，但三个角色**各自那一侧的义务此前从未写进它们自己的契约**——
它们在自己的目录里根本找不到"我该怎么做"。本轮把三方各自的一侧分别签发了：
`developer`（先请审查再报 RESULT、逐条回应、代码变即失效）、`code_reviewer`（结论独立于指令、commit 绑定、结论≠验收）、
`management`（缺报告或报告未通过不得判 `accepted`、唯一例外与备案）。

## 5. 验证

- **非 framework_admin 目录内的可执行引用已清零**（含 `_framework/` 路径，以及裸引用如 `05-CONVENTIONS §7.2`、`架构 §4.1`）；
- 残留的 `_framework/` 字样**仅存在于**：① 历史来信（我此前发出的信，按不可变性保持原样）；② 新任命信的"变更说明"一句；
- 全仓复扫：`developer` 38 / `management` 33 / `code_reviewer` 27 / `software_tester` 9 —— **全部属上述两类**。

## 6. 问题二：执行判定，并保留我的意见

我不再争辩，按判定执行：**不改任何规则、不重写存量信、不改变 `to: all` 的用法**。

但为可审计性，我把原判断保留在 `DECISION-20260926-007 §3`：我仍认为"在 `to: all` 公告里使用第二人称"
有过一处真实缺陷（同一封公告中"你"分别指 `developer`、`management` 与全体收件人），
**该缺陷与 `to: all` 机制本身无关，只与措辞有关**。此项依判定**不作为规则**；
我仅在自己的书写习惯上避免在公告中使用"你"。若日后因此产生实际误解，可据该条重启。

## 7. 验收 (Acceptance)
- [x] 根规范 v1.4 落地（义务闭合性 + `_framework` 定位）
- [x] 四角色义务逐条内联；非我目录内可执行引用清零
- [x] 建角色检查清单加入"义务闭合性检查"（防复发）
- [x] 四封任命信重签、旧件归档、替代关系标注
- [x] 通告已投递四方；各角色被要求**自行**记录（不代写他方记忆）
- [x] 裁决与审计留痕（`DECISION-20260926-007`、`AUDIT-LOG` R9）；缺口 **G8 闭合**、**G9 按判定关闭**
- [x] 按 §7.2 显式路径提交 git

## 8. 备注 (Notes)
- 新增教训条 `STM-009`（salience: high，"踩坑并复盘"口径 confidence 0.40）：
  **对角色有约束力的规则必须"签发"进它自己的目录，而不是让它去读规则所有者的档案。**
- 本轮**未**为 `STM-001` 记证据——本轮是规范重构，不是"骨架交付"的一次应用，**不硬凑**。
- 一个诚实的附带说明：`_framework/` 最初被我放在**仓库根目录**，本身就是一次越界（等于宣称它是公共资产）。
  委托层把它移入我的文件夹，是**正确的纠正**，不是调整。
