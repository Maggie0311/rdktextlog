# VERIFY-R7 — T-20260928-004 文档专项复审实跑留档（基准 commit 08f6ce8）

- 审查人: code_reviewer (R-004) · 2026-09-28 22:17~22:25
- 环境: Windows 开发机, Python 3.14.7 / gcc 13.2.0（与 developer IMPL §9.2 声明同环境同版本）
- 验证区: `code_reviewer/script/_verify_T-20260926-001/r7/`（组件副本拷自被审 commit 08f6ce8 的工作区,
  工作树当时与 08f6ce8 零 diff——`git diff --stat 08f6ce8 -- <两被审文件>` 为空已核）
- 纪律: 全程未触碰 `developer/script/**`（只读拷贝）; 被审文件零修改。

## 基准核对（git 实证）

| # | 命令 | 结果 |
|---|---|---|
| B1 | `git cat-file -t 08f6ce8` / `git rev-parse 08f6ce8` | commit / `08f6ce840d3bdbbeb2df2c20fcba0b4e54fe25a3` |
| B2 | `git log --format='%H %P' -1 08f6ce8` | parent = `df6cd427064662140b7a6ef2e0526398e24e2da8` ✓ |
| B3 | `git diff --stat df6cd42..08f6ce8` | 恰 2 文件: IMPL +49 / USAGE.md 重写, 合计 +338/−129 ✓ |
| B4 | `git diff --name-only df6cd42..08f6ce8 -- "developer/script/*.py" "*.c" "*.h" "rmlog/*"` | **空**（代码冻结面为零）✓ |

## 实跑清单（V1~V5）

### V1 — USAGE §1.1 Python 快速上手（原样命令）— PASS
- 脚本: `v1_quickstart.py`（逐字执行文档命令 + 追加 5 条作 V3 素材）, 退出码 0。
- 落盘 `v1log/rmlog.log`: 5 行, 逐段与 §1.4 字段图一致
  （`LOGV1|1|2026-09-28T22:17:06.929|541832386|INFO|E-INIT-000|ctrl|上电启动完成`;
  attrs 版第 8 段拆分 `|dev=/dev/spidev0.0|retry=3`, 与 IMPL §9.2 记录同构）。

### V2 — USAGE §1.2 C 起步示例（原样命令）— PASS
- `gcc -std=c99 -Wall -Wextra -I rmlog -o example rmlog/example.c rmlog/rmlog.c -lpthread`
  → 编译退出码 0、**零告警**; `./example ./c_demo` 运行退出码 0。
- 落盘 4 行: INFO/WARN/ERROR/FATAL 各 1（E-INIT-000/E-HW-005/E-COMM-001/E-FSM-004）,
  行格式与 Python 行同构共存 ✓。

### V3 — USAGE §2.5 读端命令 + 分钟前缀 + 通配符警示 — PASS
| 子项 | 命令 | 实测 | 判定 |
|---|---|---|---|
| filter --level ERROR | `filter .\v1log\rmlog.log --level ERROR` | 3 条 ERROR, 输出格式 `时间 [级别] 码 模块: 消息 k=v` 与 §1.3 一致 | ✓ |
| filter --code 通配 | `--code E-COMM-*` | 恰 1 条 E-COMM-001 | ✓ |
| tail | `tail -n 3` | 最后 3 条原序 | ✓ |
| stderr/stdout 分离 | `1>so.txt 2>se.txt` | stdout 纯事件流 3 行; stderr 恰 `rmlog_read: 命中 3 条` | ✓（§2.5"可安全重定向"声明成立） |
| 分钟前缀含端点 | `--since 2026-09-28T22:17 --until 2026-09-28T22:17` | 命中该分钟全部 5 条; `+--level ERROR` 3 条; `22:16` 窗口命中 0 | ✓（F-2 语义与文档 §2.5 表述一致） |
| 全精度交叉验证 | `--since T22:17:06.930 --until T22:17:06.940` | 恰 2 条（06.932/06.937）, stderr `命中 2 条` | ✓ |
| 通配符字面路径 | `filter '.\v1log\rmlog.log*'` | stderr `文件不存在` + `命中 0 条`, exit 0 | ✓（§2.5 警示如实） |

### V4 — USAGE §2.4/§5 轮转文件族 + FAQ Q6 — PASS
- 脚本: `v4_rotate.py`（`Writer(max_bytes=400, keep=3)` 连写 60 条）。
- 60 条后目录: `.rmlog.ROTLOCK` + `rmlog.log.1/.2/.3`（各 415B）, **主文件不存在**;
  追加 1 条写入后 `rmlog.log` 重建（85B）→ FAQ Q6"轮转后主文件待下次写入重建"实测成立。
- ROTLOCK 为 0 字节锁文件, 与 §2.4"属正常现象, 不要删"一致。

### V5 — 全量 selftest 冒烟（行为面回归）— PASS（13/13, 21.4s, exit 0）
- `python -m rmlog.selftest tests\_work_r7b`（干净工作区）→ SELFTEST PASS, 与 developer
  声明（13/13, 21.1s）同口径。
- 过程留痕（诚实记录）: 第 1 次 12/13 FAIL——我副本漏拷 `tests/probe_fdleak_rf6.c`（RF6 探针,
  环境缺件, 非代码缺陷）; 第 2 次 9/13 FAIL——复用含 V4 轮转素材的工作区（污染）; 第 3 次
  干净工作区 13/13 全绿。两次失败均为**验证环境构建问题**, 结论以第 3 次为准。

## 静态一致性抽查（未实跑、逐条对照源码）

| 文档声明 | 源码事实 | 判定 |
|---|---|---|
| 默认目录 `/userdata/rmlog/`、回退 `/var/log/rmlog/` | writer.py L78-79 `DEFAULT_DIR`/`FALLBACK_DIR` | ✓ |
| 目录建不出来构造期直接报错、不静默丢 | writer.py L135-137/152-153 docstring + `os.makedirs`（构造期唯一允许失败） | ✓ |
| 2 MB × keep 5、占用 ≈ max_bytes×(keep+1) | writer.py L130 `max_bytes=2*1024*1024, keep=5` | ✓ |
| ERROR/FATAL 即写即落盘（fdatasync） | writer.py L131 `flush_levels=("ERROR","FATAL")`、L209-219 `_sync_fd` | ✓ |
| `.rmlog.ROTLOCK` 同名锁双端互斥 | writer.py L84 + rmlog.h/自述 | ✓ |
| 级别语义/五域/错误码含义与建议动作 | catalog.py L10-30 五域 + 24 码逐条比对（E-INIT-000=INFO 里程碑、E-COMM-004=ERROR"触发安全态，检查两端连接器"、E-SYS-002 落盘失败/E-SYS-004 水位告警——FAQ Q3 引述一致） | ✓ |
| `--until` 前缀=该段末（分钟前缀含整分钟） | rmlog_read.py L134-153/L204-214 + help 文本 L258 | ✓ |
| C 端宏族 RMLOG_I/W/E/F、`rmlog_open` 深层目录限制 | rmlog.h L47-50/L56-67 | ✓ |
| ERR-CATALOG 未重新生成（catalog.py 未变） | `git diff df6cd42..08f6ce8 -- rmlog/catalog.py` 为空 + selftest GEN 项 PASS（生成物与 catalog 单一来源一致） | ✓ |

## 未实跑项（诚实清单）

- 板端平台事实（/userdata 存在、journald 持久化、rsyslog、coredumpctl 不可用、dmesg ISO）:
  本轮未复测, 采信 TESTREPORT-T-20260927-002-001 §6 Q2（software_tester 真机实测）。
- 残行 `[DROP]` 标注实跑（developer 跑过）: 本轮以 selftest AC2"残行三道闸"+ fuzz 300 次
  PASS 覆盖判定, 未单独重演——判据链: selftest 全绿 + 代码 L50-56/L128。
- `--follow` 实时跟踪、journald/dmesg 交叉查询: 板端/长时操作, 开发机无对应环境, 未跑。
- FAQ Q1③ PermissionError 直跑复现（developer 跑过）: 本轮以 writer.py 构造期裁决源码
  （L135-137, L178-192）+ 文档 §5 Q1/Q2 表述比对核验, 未在验证区直跑默认目录。
