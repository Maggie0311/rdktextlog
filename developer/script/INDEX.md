# script/INDEX — developer 产物登记表

> 规则：登记**交付单元**（按 `task_id` 的产出批次、说明文档与打包件），**不逐文件登记源码**。
> 理由：逐文件登记会让登记表退化成文件清单，反而看不出交付边界与消费者。
> 源码结构由 `script/README.md` 声明；交付的权威依据是 **commit hash**（`DECISION-20260924-005 §2.3`）。

| # | 交付单元 | 路径 | 类型 | 关联 task_id | commit | 创建日期 | 消费者 |
|---|---|---|---|---|---|---|---|
| 1 | rmlog P0 文本日志平台（代码+自测+文档） | `script/`（`rmlog/`、`rmlog_read.py`、`USAGE.md`、`ERR-CATALOG.md`、`IMPL-T-20260926-001-logging-platform-p0.md`、`tests/selftest-*.log`） | 源码+文档+测试 | T-20260926-001-logging-platform-p0 | （本单元提交 hash，见 RESULT 邮件） | 2026-09-26 | code_reviewer（审查）、management（验收）、人类用户（板端自测与场下使用） |

**待产出（上岗后）**：

| 产物 | 用途 | 触发条件 |
|---|---|---|
| `CODE-STYLE.md` | 代码风格与注释规范（**必须先于第一行项目代码**） | 上岗首个交付物，见 `mailbox/inbox/WELCOME-developer.md` |
| 本目录结构声明（`README.md` 第 1 节） | 让消费方能定位源码与测试 | 同上 |
| `IMPL-<task_id>.md` | 实现说明（含可复现验证证据） | management 下发第一个编码任务时 |
| `dist/<task_id>.<ext>` | 交付包（可选） | 有跨角色流转需求时 |
