# script/INDEX — code_reviewer 产物登记表

> 规则：任何新增/重大变更的产物必须在此登记。重大变更另存 `-v2`，不覆盖。
> 审查**标准**不在本表登记（归属 `../standard/VERSION-LOG.md`）。

| # | 产物 | 路径 | 类型 | 版本 | 创建日期 | 关联 task_id | 被审 commit | 消费者 |
|---|---|---|---|---|---|---|---|---|
| 1 | 审查报告 | `script/REVIEW-T-20260926-001-f3331b0.md` | 审查报告 | v1 | 2026-09-26 | T-20260926-001-logging-platform-p0 | `f3331b0` | developer（整改）、management（验收裁量）、人类用户 |
| 2 | 审查质量度量 | `script/REVIEW-STATS.md` | 统计 | v1 | 2026-09-26 | 同上 | 同上 | 全体 |
| 3 | 验证工件（`r2/` 首轮复跑副本、探针脚本与输出；`r3/` 复审验证区——45eeb04 独立副本、12 项验证记录、组合对账与边界探针；`r4/` RF 复审验证区——a675c8d 独立副本、12 项验证记录、fdleak/rf1/degr/rf4 探针及输出） | `script/_verify_T-20260926-001/` | 验证证据区 | — | 2026-09-26 | 同上 | `f3331b0` / `45eeb04` / `a675c8d` | 本角色复审基线 |
| 4 | 复审报告（R1 整改返工·增量） | `script/REVIEW-T-20260926-001-45eeb04.md` | 审查报告 | v1 | 2026-09-27 | T-20260926-001-logging-platform-p0 | `45eeb04` | developer（残留项处理）、management（验收裁量）、人类用户 |
| 5 | 复审报告（R2 RF 微整改·增量，结论 FAIL：新发现严重级 RF-6） | `script/REVIEW-T-20260926-001-rf-a675c8d.md` | 审查报告 | v1 | 2026-09-27 | T-20260926-001-logging-platform-p0 | `a675c8d` | developer（RF-6 整改）、management（验收裁量）、人类用户 |

**待产出（上岗后 / 首次审查时）**：

| 产物 | 用途 | 触发条件 |
|---|---|---|
| `REVIEW-STATS.md` | 审查质量度量（发现数 / 申诉采纳数 / 后验漏报数） | 完成第一次审查时建立 |
| `REVIEW-<task_id>-<commit7>.md` | 审查报告 | 收到第一个审查请求时 |
