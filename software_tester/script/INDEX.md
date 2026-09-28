# script/INDEX — software_tester 产物登记表

> 规则：登记**交付单元**（按 `task_id` 的报告与复现材料），**不逐文件登记**。
> 测试结论的权威依据是：**报告 + 原始输出 + 被测 commit hash**（三者缺一不可）。

| # | 交付单元 | 路径 | 类型 | 关联 task_id | 被测 commit | 创建日期 | 消费者 |
|---|---|---|---|---|---|---|---|
| 1 | 板端 SSH 实测（Q1–Q4） | `TESTPLAN-T-20260927-002.md` + `TESTREPORT-T-20260927-002-001.md` + `work/T-20260927-002/` | TEST | `T-20260927-002-logging-boardtest-ssh` | `2d83644` | 2026-09-27 | management / developer / code_reviewer |
| 2 | linux-build-fix 板端聚焦复测（R-Q1/R-Q4/R-Q3） | `TESTREPORT-T-20260927-003-001.md` + `work/T-20260927-003/` | TEST | `T-20260927-003-logging-c-linux-build` | `164d4c7` | 2026-09-28 | management / developer / code_reviewer |

**待产出（上岗后）**：

| 产物 | 用途 | 触发条件 |
|---|---|---|
| `ENVIRONMENTS.md` 的**实测回填** | 把全部"假设"改为"已验证/不可用"，并附验证方式与证据 | 上岗首个交付物（见 `mailbox/inbox/WELCOME-software_tester.md` AC1） |
| `TESTPLAN-<task_id>.md` | 测试方案（含"要回答的问题"与判定标准） | management 下发第一个测试任务时 |
| `TESTREPORT-<task_id>-<NNN>.md` | 运行结果报告 | 同上 |
