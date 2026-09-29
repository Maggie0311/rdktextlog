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
| 6 | 复审报告（R3 终轮·RF-6 修复增量，结论 PASS：RF-6+MIN-1/2/3 核销，零新发现） | `script/REVIEW-T-20260926-001-rf6-2d83644.md` | 审查报告 | v1 | 2026-09-27 | T-20260926-001-logging-platform-p0 | `2d83644` | developer（流程后续）、management（验收裁量）、人类用户 |
| 7 | 验证工件（`r5/` 终轮复审验证区——2d83644 独立副本、10 项验证记录、自建句柄探针 probe_fdleak_r5/probe_null_r5 及修复前/后/缺省分支三份实测留档、selftest 13/13 复跑留档） | `script/_verify_T-20260926-001/r5/` | 验证证据区 | — | 2026-09-27 | 同上 | `2d83644`（对照 `a675c8d`） | 本角色复审基线 |
| 8 | 复审报告（T-003 linux-build·增量，结论 PASS：构建可移植性修复五项核销；Linux/aarch64 板端待 software_tester 复测） | `script/REVIEW-T-20260927-003-164d4c7.md` | 审查报告 | v1 | 2026-09-28 | T-20260927-003-logging-c-linux-build | `164d4c7` | developer（板端复测后流程）、management（验收裁量）、software_tester（板端复测）、人类用户 |
| 9 | 验证工件（`r6/` T-003 复审验证区——164d4c7 独立副本、三份零告警编译留档、selftest 13/13 复跑留档、README） | `script/_verify_T-20260926-001/r6/` | 验证证据区 | — | 2026-09-28 | 同上 | `164d4c7` | 本角色复审基线 |
| 10 | 复审报告（T-004 usage-rewrite 文档专项，结论 PASS：冻结 5 项全核销、零发现项；断点续完——实跑 2026-09-28 完成、报告/邮件 2026-09-29 收尾） | `script/REVIEW-T-20260928-004-08f6ce8.md` | 审查报告 | v1 | 2026-09-29 | T-20260928-004-usage-rewrite | `08f6ce8` | developer（后续备料流程）、management（验收裁量）、人类用户 |
| 11 | 验证工件（`r7/` T-004 复审验证区——08f6ce8 组件副本（8 件 blob MATCH）、V1~V5 实跑输出与脚本、轮转对照、读端 stdout/stderr 分离留档、VERIFY-R7 留档、selftest 13/13 复跑留档 selftest_r7.log；工作区目录不入库） | `script/_verify_T-20260926-001/r7/` | 验证证据区 | — | 2026-09-28（实跑）/ 2026-09-29（入库） | 同上 | `08f6ce8` | 本角色复审基线 |

**待产出（上岗后 / 首次审查时）**：

| 产物 | 用途 | 触发条件 |
|---|---|---|
| `REVIEW-STATS.md` | 审查质量度量（发现数 / 申诉采纳数 / 后验漏报数） | 完成第一次审查时建立 |
| `REVIEW-<task_id>-<commit7>.md` | 审查报告 | 收到第一个审查请求时 |
