# r7 — T-20260928-004-usage-rewrite 复审验证区（基准 commit 08f6ce8）

- 审查角色: code_reviewer (R-004) · 轮次: T-004 文档专项复审（USAGE.md 重构为用户优先手册）
- 实跑时段: **2026-09-28 22:17~22:25（会话中断前完成）**；报告/RESULT/登记/入库于 2026-09-29 断点续完成
  （详见 `../REVIEW-T-20260928-004-08f6ce8.md` 断点续完声明与本角色 worklog #7——未重做任何实跑，
  唯一新增为 selftest_r7 在库复跑留档补齐）
- 环境: Windows 开发机, Python 3.14.7 / gcc 13.2.0（与 developer IMPL §9.2 声明同版本）
- 副本基准: `rmlog/` 组件副本与 `rmlog_read.py` 拷自被审 commit 08f6ce8 工作区（拷贝时工作树与
  08f6ce8 对两被审文件零 diff 已核）；入库后经 `git hash-object` 抽查 8 件（rmlog.c / writer.py /
  rmlog_read.py / example.c / selftest.py / catalog.py / rmlog.h / rmlog_errors.h）与
  `git rev-parse 08f6ce8:developer/script/...` **全 MATCH**（报告 §4-S1）。副本本体不入库
  （同 r5/r6 口径），等价性由上述 blob 核对命令可随时复验。
- 纪律: 全程未触碰 `developer/script/**`（只读拷贝）；被审文件零修改。

## 入库证据清单（`tests/_work*` 工作区目录与 `*.exe`/`__pycache__` 不入库，可由脚本即时重建）

| 文件 | 验证点 |
|---|---|
| `VERIFY-R7.md` | 中断前实跑全记录：基准核对 B1~B4、V1~V5 判定与过程留痕（含两次环境构建失败诚实记录）、静态一致性抽查 9 项、未实跑项诚实清单 |
| `v1_quickstart.py` | V1/V3 素材脚本：USAGE §1.1 Python 快速上手**原样命令**（2 行起步 + attrs 版 + 自定义目录版）+ 同一分钟 3 条事件作时间窗素材 |
| `run/v1log/rmlog.log` + `run/v1log/.rmlog.ROTLOCK` | V1 输出：5 行落盘与 USAGE §1.4 八段字段图逐段一致（含 attrs 版第 8 段拆分 `\|dev=/dev/spidev0.0\|retry=3`） |
| `rmlog_read.py` | 被测读端副本（= 08f6ce8 blob），V3 全部命令以其执行 |
| `run/so.txt` / `run/se.txt` | V3: `filter --level ERROR` 的 stdout（3 行纯事件流）/ stderr（恰 `rmlog_read: 命中 3 条`）**分离留档**——USAGE §2.5"可安全重定向"声明成立 |
| `e4so.txt` / `e4se2.txt` / `e4err.txt` | V3: 全精度毫秒窗（22:17:06.930~06.940）stdout 2 行 / stderr `命中 2 条`；`e4err.txt` 为 PowerShell 5.1 UTF-16LE 重定向副本（内容同 e4se2，含 PS 包装行，编码事实如实注明） |
| `run/c_demo/rmlog.log` | V2 输出: C 示例四级别各 1 行（INFO/WARN/ERROR/FATAL，E-INIT-000/E-HW-005/E-COMM-001/E-FSM-004），与 Python 行同格式共存（编译命令见 VERIFY-R7 V2：`-std=c99 -Wall -Wextra` 零告警；编译产物不入库） |
| `v4_rotate.py` | V4 脚本: `Writer(max_bytes=400, keep=3)` 连写 60 条 + 追加 1 条观察主文件重建 |
| `run/rotlog/rmlog.log`、`rmlog.log.1/.2/.3` + `.rmlog.ROTLOCK` | V4 输出: 轮转文件族形态（副本各 415B）+ 0 字节 ROTLOCK 锁文件（"属正常现象不要删"）；60 条后主文件不存在、追加写入后重建 85B——USAGE §2.4 与 FAQ Q6 实测成立 |
| `selftest_r7.log` / `selftest_r7.err` | V5b（2026-09-29 补跑留档）: 全量 selftest **13/13 PASS，42.9s，`__EXIT_CODE__=0`，stderr 0 字节**；与中断前 V5（`tests/_work_r7b`，13/13, 21.4s）及 developer 声明（13/13, 21.1s）同口径——行为面回归证据（工作区目录不入库） |

## 与报告的对应

结论、覆盖声明与门槛核对见 `../REVIEW-T-20260928-004-08f6ce8.md`（§3 覆盖声明 / §4 验证动作与证据 /
§5 冻结项核销 / §6 unverified / §7 结论 PASS）。本验证区为审查证据，**不构成验收结论**（RN9，验收归 management）。
