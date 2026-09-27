# script/INDEX — developer 产物登记表

> 规则：登记**交付单元**（按 `task_id` 的产出批次、说明文档与打包件），**不逐文件登记源码**。
> 理由：逐文件登记会让登记表退化成文件清单，反而看不出交付边界与消费者。
> 源码结构由 `script/README.md` 声明；交付的权威依据是 **commit hash**（`DECISION-20260924-005 §2.3`）。

| # | 交付单元 | 路径 | 类型 | 关联 task_id | commit | 创建日期 | 消费者 |
|---|---|---|---|---|---|---|---|
| 1 | rmlog P0 文本日志平台（代码+自测+文档） | `script/`（`rmlog/`、`rmlog_read.py`、`USAGE.md`、`ERR-CATALOG.md`、`IMPL-T-20260926-001-logging-platform-p0.md`、`tests/selftest-*.log`） | 源码+文档+测试 | T-20260926-001-logging-platform-p0 | f3331b0（R0）/ d7e06da（reviewer 勘误） | 2026-09-26 | code_reviewer（审查）、management（验收）、人类用户（板端自测与场下使用） |
| 2 | rmlog P0 整改返工 R1（F-1~F-9 逐条处置：轮转协议 v2 / 时间前缀归一 / selftest 12 用例） | 同上（变更：`rmlog/writer.py` 全量重写、`rmlog/rmlog.c` `rmlog.h`、`rmlog/worker.py`、`rmlog/selftest.py`、`rmlog_read.py`、`USAGE.md`、`IMPL-…md`、`CODE-STYLE.md` v1.1、`tests/selftest-20260927-{1010-r1,1028-r1}.log`） | 源码+文档+测试 | T-20260926-001-logging-platform-p0 | 45eeb04（R1） | 2026-09-27 | code_reviewer（复审）、management（验收） |
| 3 | rmlog P0 复审微整改 R2（RF-1~RF-5 逐条处置：C 端 close 后重开复用 g_path / 写锁 open 失败计数口径收紧 / C 端锁降级计数 / 文档数字与 docstring 更正） | 同上（变更：`rmlog/rmlog.c`、`rmlog/rmlog.h`、`rmlog/writer.py`、`rmlog/selftest.py`、`IMPL-…md`、`tests/selftest-20260927-1235-rf.log`） | 源码+文档+测试 | T-20260926-001-logging-platform-p0 | a675c8d（R2，交付权威 hash；复审请求信 MAIL-20260927-1305-rf。MIN-2 补登记） | 2026-09-27 | code_reviewer（复审）、management（验收） |
| 4 | rmlog P0 终轮微修复 R3（RF-6 结构归位消除按需重开句柄泄漏 + selftest 增 RF-6 句柄守恒回归用例共 13 用例 + MIN-1/2/3 登记与流程更正：占位符填实 / R2 hash 补登 / 1215 任务书按收件方原则补入库） | 同上（变更：`rmlog/rmlog.c`、`rmlog/selftest.py`、`IMPL-…md`、`INDEX.md`、`tests/probe_fdleak_rf6.c`、`tests/probe_fdleak_rf6_before_after.log`、`tests/selftest-20260927-1352-rf6.log`；另有 inbox 1215 任务书入库） | 源码+文档+测试 | T-20260926-001-logging-platform-p0 | 2d83644（R3，交付权威 hash；复审请求信 MAIL-20260927-1435-rf6） | 2026-09-27 | code_reviewer（复审）、management（验收） |

**自测留档索引**：

| 留档 | 轮次 | 结果 |
|---|---|---|
| `tests/selftest-20260926-{1958,2002}.log` | R0 迭代 | FAIL（修复过程） |
| `tests/selftest-20260926-2020-final.log` | R0 第 3 轮 | PASS 10/10（R0 曾误标"最终"，见 F-3） |
| `tests/selftest-20260926-{2035,2042}.log` | R0 迭代 | FAIL（AC5 并发丢行，commit 后发现） |
| `tests/selftest-20260926-2055.log` | R0 末轮 | PASS 10/10 |
| `tests/selftest-20260927-1010-r1.log` | R1 迭代 | FAIL 10/12（新用例参数误校准，定位后校准；过程见 IMPL §3） |
| `tests/selftest-20260927-1028-r1.log` | **R1 末轮** | **PASS 12/12** |
| `tests/selftest-20260927-1235-rf.log` | **R2 微整改末轮** | **PASS 12/12** |
| `tests/selftest-20260927-1352-rf6.log` | **R3 终轮微修复末轮** | **PASS 13/13**（新增 RF-6 句柄守恒用例；句柄前后对照 `tests/probe_fdleak_rf6_before_after.log`） |

**待产出（上岗后）**：

| 产物 | 用途 | 触发条件 |
|---|---|---|
| `CODE-STYLE.md` | 代码风格与注释规范（**必须先于第一行项目代码**） | 上岗首个交付物，见 `mailbox/inbox/WELCOME-developer.md` |
| 本目录结构声明（`README.md` 第 1 节） | 让消费方能定位源码与测试 | 同上 |
| `IMPL-<task_id>.md` | 实现说明（含可复现验证证据） | management 下发第一个编码任务时 |
| `dist/<task_id>.<ext>` | 交付包（可选） | 有跨角色流转需求时 |
