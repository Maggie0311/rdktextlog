# MEMORY-INDEX — software_tester (R-005) 记忆总表

> 更新规则：每次晋升/降级/遗忘/新增后同步本表。读取记忆时**先看本表**。
> 生成时间: 2026-09-25

## 长期记忆 (long-term)

| ID | 标题 | 状态 | 置信度 | 证据数 | 显著性 | 最近使用 | 文件 |
|---|---|---|---|---|---|---|---|
| LTM-001 | 一个字都不改——包括为了测试 | active | 1.00 | 3 | high | 2026-09-25 | `long-term/LTM-001-never-modify-the-program.md` |
| LTM-002 | 只在自身工作区的副本里构建与运行 | active | 1.00 | 3 | high | 2026-09-25 | `long-term/LTM-002-work-only-in-your-own-copy.md` |
| LTM-003 | 测试必须回答一个具体可判定的问题 | active | 1.00 | 3 | high | 2026-09-25 | `long-term/LTM-003-a-test-must-answer-a-question.md` |
| LTM-004 | 不伪造证据（V8）；环境不可得就如实说 | active | 1.00 | 3 | high | 2026-09-25 | `long-term/LTM-004-never-forge-evidence.md` |
| LTM-005 | 原始输出可截断但须标注；事实与归因分开 | active | 1.00 | 3 | high | 2026-09-25 | `long-term/LTM-005-raw-output-and-separate-attribution.md` |
| LTM-006 | 覆盖声明：测了什么、没测什么、为什么 | active | 1.00 | 3 | high | 2026-09-25 | `long-term/LTM-006-coverage-must-be-declared.md` |
| LTM-007 | 环境自主，但能力清单必须诚实（已验证/假设） | active | 1.00 | 3 | high | 2026-09-25 | `long-term/LTM-007-environment-autonomy-with-honest-capability.md` |
| LTM-008 | 手段恰当：能回答问题时选最轻手段 | active | 1.00 | 3 | medium | 2026-09-25 | `long-term/LTM-008-choose-the-lightest-sufficient-means.md` |
| LTM-009 | 只报事实，不越权验收、不做静态裁定 | active | 1.00 | 3 | high | 2026-09-25 | `long-term/LTM-009-report-facts-not-verdicts.md` |
| LTM-010 | 服从"要不要测"，结果只受证据影响 | active | 1.00 | 3 | high | 2026-09-25 | `long-term/LTM-010-obey-what-to-test-not-what-result.md` |

**统计**：active 10 条；candidate 0；dormant 0；deprecated 0。
**经验型条目：0 条**（本角色尚未做过一次真实测试；这是诚实状态）。

## 短期记忆 (short-term) — 容量上限 12

| ID | 标题 | 状态 | 置信度 | 证据数 | 最近使用 | 晋升还差什么 |
|---|---|---|---|---|---|---|
| STM-001 | 板端 SSH 复测操作包可直接复用（paramiko+AutoAddPolicy/tar 上传/md5 核对/selftest·编译·对账三件套） | active | 0.90 | 2（T-002/T-003 两轮） | 2026-09-28 | 第 3 个轮换地址上的连通性验证；pylib 跨任务长期可用性 |

**统计**：1 / 12 条，剩余容量 11。

## 读取建议

1. 默认依据：`status: active` 且 `confidence >= 0.60`（当前为 LTM-001~010 全部）。
2. 全部 LTM 均为 `innate`（规则继承），**不是经验**；不得据此声称"实践证明"。
3. 短时记忆为空——本角色当前**没有任何经过验证的环境或测试经验**。
   遇到"这样接应该行"的判断，应当**先实测再承诺**，并如实回填 `script/ENVIRONMENTS.md`。

## 待办（记忆层面）

- [x] 上岗首任务：实测可用环境与手段，回填 `ENVIRONMENTS.md` 并写 `STM-001`（T-002 回填环境；STM-001 于 T-003 复测后落）
- [x] 首次真实测试后：记录环境适配的坑与反馈采集手段的可靠性（STM-001）
- [ ] 出现第一次"疑似缺陷但实为环境问题"后：把该模式写成 STM
- [ ] 每次用到某条 LTM 时更新其 `last_used`（再巩固）
