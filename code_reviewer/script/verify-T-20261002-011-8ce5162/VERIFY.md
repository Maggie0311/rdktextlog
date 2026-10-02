# VERIFY — T-20261002-011-logging-v3-review 验证留档（commit 8ce5162）

> 角色: code_reviewer (R-004) · 审查基准: 来源 commit `8ce5162eda11c802eb0e6616d7baca1f6fce95a`
> 环境: Windows 开发机，Python 3.14.7 / gcc 13.2.0 (MinGW)
> 被审代码来源: `git archive 8ce5162 developer/script` 签出到本目录 `developer/`（工作树为 master 旧状态，**未碰工作树**）。`developer/`、`tmp*/` 及 `.o/.exe` 为审查工作副本/工作区产物，**不入库**；本目录仅选择性入库下列证据文件。

## 1. 独立实跑结果（退出码 + 留档）

| # | 命令 | 结果 | 留档 |
|---|---|---|---|
| V1 | `python -m rmlog.selftest`（PYTHONPATH=developer/script） | 13/13 PASS，37.6s，exit 0 | `selftest-v3-8ce5162.log` |
| V2 | `python tests/test_v2_smoke.py` | V2 SMOKE PASS accepted=1 dropped=9，exit 0 | `test_v2_smoke-8ce5162.log` |
| V3 | `python tests/test_v3_smoke.py` | V3 SMOKE PASS bit-map blackbox monitors stats schema，exit 0 | `test_v3_smoke-8ce5162.log` |
| V4 | `gcc -std=c99 -Wall -Wextra -I rmlog -c rmlog/rmlog.c` | exit 0，零告警 | `gcc-rmlog-8ce5162.log` |
| V5 | `gcc -std=c99 -Wall -Wextra -pedantic -I . schema_probe.c`（include `shared/rmlog_schema.h`） | exit 0，零告警；运行 `len=24 domains=5 bit_comm004=0x223004 code=E-COMM-004` | `gcc-schema-8ce5162.log`、`schema_probe.c` |
| V6 | 24 码双轨全量核对（encode→decode 往返 + 唯一性 + 与 C 头 RMLOG_BIT_* 逐码比对） | codes=24 unique_bits=24，`E-COMM-004 -> 0x223004`，未知码 `-> None`，BAD: none | 报告 §4-V6（脚本内联） |
| V7 | 重新生成 `rmlog_errors.h`/`shared/rmlog_schema.h` 与 commit 逐字节对比 | IDENTICAL | 报告 §4-V7 |

## 2. 基准核对（git 实证）

- `git log --oneline feature/logging-v2..feature/logging-v3` = 恰 3 提交：`5640987`→`ed90fca`→`8ce5162`（基于 v2 `fd8423c`）。
- `git diff --stat feature/logging-v2...feature/logging-v3 -- developer/script` = 15 文件 +828/-7（与任务书一致）。

## 3. 沙箱工作区说明（诚实记录）

V2/V3 首次运行失败，根因：`tempfile.mkdtemp()` 内部 `os.mkdir(mode=0o700)` 在 Windows 文件沙箱下生成 owner-only ACL，随后 `os.listdir` 报 `EACCES`（WinError 5）。**属 DSH 沙箱环境交互，非被审代码缺陷**（selftest 走 `os.makedirs` 默认 0o777 不受影响，故 V1 直接通过）。

处置：以本目录 `shim/sitecustomize.py`（仅将 `os.mkdir` 的 0o700 放宽为 0o777）垫片，`PYTHONPATH=<shim>;<developer/script>` 原样重跑 V2/V3 通过。**未修改任何被审代码/测试断言**。

## 4. 结论

CONDITIONAL（0 阻断 / 0 严重；4 一般 F-01~F-04 + 2 提示 F-05/F-06）。详见 `code_reviewer/script/REVIEW-T-20261001-logging-v3-8ce5162.md`。
