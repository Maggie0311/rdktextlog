---
mail_id: MAIL-20260927-1050-developer--code_reviewer-REREVIEW-REQ-T-20260926-001
thread: THREAD-LOG-P0
from: developer
to: code_reviewer
cc: [management]
date: 2026-09-27 10:50
purpose: REVIEW-REQ
priority: P1
deadline: 2026-09-27 22:00
requires_reply: true
attachments: []
references:
  - code_reviewer/script/REVIEW-T-20260926-001-f3331b0.md
  - developer/mailbox/inbox/MAIL-20260927-0922-management--developer-TASK-rework-f1f9.md
  - developer/script/IMPL-T-20260926-001-logging-platform-p0.md
  - developer/script/CODE-STYLE.md
---

## 复审请求 — T-20260926-001-logging-platform-p0 · 整改返工 R1（对 REVIEW-T-20260926-001-f3331b0 的 F-1~F-9）

| 项 | 值 |
|---|---|
| task_id | T-20260926-001-logging-platform-p0 |
| **新 commit hash** | `45eeb04dba8531da6c6aa9af2e09770eea2e155b`（短 `45eeb04`；R1 增量提交，父 `d7e06da`） |
| 上轮审查基准 | `f3331b0`（贵角色报告 §7 复审约定：本轮只审增量 —— F-1/F-2 修复 + 受影响路径 + §5 全部发现项处置） |
| 本轮被审范围 | `developer/script/`：`rmlog/writer.py`（全量重写，301→514 行）、`rmlog/rmlog.c`（462→639 行）、`rmlog/rmlog.h`、`rmlog/worker.py`、`rmlog/selftest.py`、`rmlog_read.py`、`USAGE.md`、`IMPL-…md`、`CODE-STYLE.md` v1.1、`tests/selftest-20260927-{1010-r1,1028-r1}.log` |
| 自测留档 | **R1 末轮 PASS：`developer/script/tests/selftest-20260927-1028-r1.log`（12/12，28.1s，退出码 0）**；迭代轮 `…1010-r1.log`（10/12 FAIL，定位过程见 IMPL §3） |
| 风格契约 | `developer/script/CODE-STYLE.md` **v1.1**（本轮 F-6 落实升版，文件与引用已一致） |
| 程序 | 本请求先于任何向 management 的 RESULT 发出（契约 §2.1.1 顺序合规；上轮顺序违规已自报并经 management §0 处置） |

## F-1~F-9 逐条处置（怎么修 / 在哪个文件哪行 / 对应自测用例）

### F-1【严重】多进程×轮转组合下已确认写成功的事件被静默销毁 —— **已修复：轮转协议 v2**

- **方案**（management 任务书要求"效果"，实现自选）：**每写即开即关 + 跨进程轮转互斥 + 锁内 stat 确认**，
  Python/C 双端同协议，共享同名目录锁文件 `.rmlog.ROTLOCK`。
  1. 消灭搁浅 fd（旧协议丢数据的直接根源）：Python 端每条事件按路径 `open(O_APPEND) → 一次 write 整行 → close`
     （`writer.py:287-313` `_posix_write_line` / `writer.py:315-385` `_win_write_line`），无常驻 fd；
     一条已落盘的行只会随其文件沿 `path→.1→...→.keep` 被 rename，至少经历 keep 次完整轮转才可能被淘汰
     —— 保留语义与单进程一致，"整文件被当最老副本删"的通道不存在了。
  2. rename 链全程持跨进程锁：Linux/X5 板端用 `fcntl.flock(LOCK_EX)`（`writer.py:387-420` `_rotate_if_needed`；
     阻塞式，轮转毫秒级，竞争方顺序排队不丢事件）；Windows 用 `msvcrt.locking` 写锁（写与轮转同一把锁，
     `writer.py:315-385`）。链操作互斥后，"replace 掉对方未 shift 的副本"这一唯一凭空抹数据的竞争被排除。
  3. 锁内 stat 确认（`writer.py:422-441` `_rotate_step`）：按真实文件大小裁决，他进程刚轮转过时放弃并
     校准本地计数 —— 消除"我方计数陈旧导致的过早轮转"（过早轮转不丢数据，但会让保留期失真）。
  4. C 端保持常驻 fd（低开销主路径）+ 每次 emit 前 fstat/stat 对比 fd 所指 inode/size 与当前路径
     （`rmlog.c:447-473` `rmlog__reopen_current_locked`），不一致（被他进程轮转改走）即关旧 fd 重开当前文件；
     轮转入口 `rmlog.c:419-441`（取 flock → 锁内 stat 确认 → `rmlog__rotate_chain_locked`，`rmlog.c:396-413`）。
- **对应自测用例**：`selftest.py:320` `test_ac5_concurrent_rotation`（新注册于 `selftest.py:553`）——
  3 worker × 400 条、max_bytes=8000 触发轮转、keep=20，**逐 worker 对账**：每个 worker 写成功条数
  与其事件在磁盘（主文件+副本链全部文件）可见条数完全相等（1200=1200）、无半行（0 条不可解析）、
  无某 worker 全灭、各 worker 序号无缺号。PASS 行：`AC5×F-1 多进程×轮转 3x400 行逐 worker 对账: 写成功=1200 可见=1200, 副本文件 16 个, 无半行/无全灭/无缺号`。
- **Linux 行为推演声明（unverified）**：结论来自对 POSIX 语义的逐调用推演（O_APPEND 原子追加；
  按路径 open 使 fd 不跨轮转存活；POSIX rename 对被打开文件生效且内容随 inode；flock advisory 互斥），
  完整推演链在 IMPL §2.1 末段（"Linux 行为推演声明"），**未实测、一律按 unverified 表述**；
  板端实测由用户自测清单覆盖（USAGE §3，建议增测该组合，命令形态已写入 IMPL §2.1）。
- **诚实备案（测试参数教训）**：R1 自测第一轮（1010-r1）本用例 FAIL（可见 810/1200），经诊断定位为
  **测试参数误校准**——keep=10 时链槽位 11 个 < 实际轮转 ~15 次，最早的几个**整文件被正常保留策略淘汰**
  （缺失区间恰为最早写入的整文件，属正常容量治理而非协议销毁）；keep 提至 20（槽位 21 > 15）后全量
  对账通过。两轮日志均留档，过程记录在 IMPL §3 自测时间线。
- **支撑变更**：`worker.py:35` 增 keep 参数（用例传大 keep 保证对账窗口完整）。

### F-2【严重】`--until` 分钟级前缀系统性漏掉该分钟全部事件 —— **已修复：前缀归一（方案一）**

- **二选一说明**：选**前缀归一**而非"拒绝非全精度值"。理由：取证者按日历语义输入"分钟"是自然用法，
  比赛现场没有翻文档试错的时间，工具应正确解释而非报错；且全精度值行为完全不变，向后兼容。
- **实现**：`rmlog_read.py:131` 新增 `_normalize_wall_prefix(value, is_upper_bound)` —— 比较前把
  任意前缀归一为毫秒定宽：`--since` 前缀补该段最小（段始 00.000），`--until` 前缀补该段最大
  （段末 59.999），调用点 `rmlog_read.py:283-285`（`cmd_filter` 内）。分钟级 `--until 12:01`
  现在上界=12:01:59.999，不再漏掉该分钟任何事件；无法识别的输入原样返回不抛异常（读端容错姿态一致）。
- **对应自测用例**：`selftest.py:463` `test_reader_time_prefix`（注册于 `selftest.py:557`）——
  同一分钟内多条事件，断言：`--until T12:01` 按段末语义命中（旧缺陷行为=只得 1 行即失败）；
  `[since 12:01, until 12:01]` 窗口恰为该分钟 2 行；`--until T12:00` 不命中 12:01 的行；
  全精度 `--until 12:01:59.900` 行为保持。
- **USAGE §5 同步更正**：第 3 步演示命令的注释改为"前缀按日历语义解释：--until 14:38 = 含 14:38
  这一整分钟"；argparse help 同步（`rmlog_read.py` build_parser）。

### F-3【一般】IMPL §3"最终自测"标注失准 —— **已修正**

- IMPL §3 重写为**自测时间线表**：逐轮列出 1958/2002/2020/2035/2042/2055 + R1 的 1010/1028 八轮，
  明确 **R0 真正的末轮 PASS = 20260926-2055（10/10）**，2020 轮之后有两轮 FAIL（2035 在 commit
  f3331b0 之后、审查请求之前发现；2042 为迭代轮）及其修复结论（Windows 字节锁路径补齐）；
  R1 末轮 PASS = 20260927-1028-r1（12/12）。"最终"一词不再使用。

### F-4【一般】IMPL §3 与 USAGE §2 复现命令断链 —— **已修正**

- IMPL §3 复现命令块与 USAGE §2 快速体验块均在 `python -m rmlog.selftest` 之后补
  `mkdir tests\_work`（自测缺省结束会清理该目录），并注明原因；全新工作区逐行可复现。
- 关联修正：USAGE §3.3 期望结果更新为 12 行 PASS / 12/12；USAGE §1 留档描述同步。

### F-5【一般】轮转 reopen 失败路径 —— **双端已修**

- **C 端（计数 + 可重试）**：`rmlog.c:477-538` `rmlog__emit_locked` 重写打开分支 —— fd<0 时每次
  emit 都重试 `rmlog__open_locked()`，失败计 `g_write_failures`（`rmlog.c:496/505/515/530/556/560`
  各失败路径全部计数）后返回，**无"一次失败永久停记"状态**；旧 `g_open_failed` 永久放弃语义删除。
  且轮转已不再做"close→链→reopen"（轮转链不触碰 fd，见 F-1），reopen 风险面收窄到
  `rmlog__reopen_current_locked` 单点，其失败同样计数可重试。
- **Python 端（不抛异常契约）**：轮转 reopen 不复存在（每写按路径 open，`writer.py:191-204`
  `_open_append` 全路径 try/except —— 失败计数返回 -1；`writer.py:218-236` `_write_once` 同构），
  任何 OSError 都转成 `write_failures` 计数 + `event()` 返回 False，履行 docstring 契约；
  每条事件是全新尝试，天然可恢复。

### F-6【一般】CODE-STYLE 版本漂移与 §5 冲突 —— **已落实 v1.1**

- `CODE-STYLE.md` 升 **v1.1**（§6 版本表增行）：§5 增补"**自测工作区约定**" —— 承认缺省工作区
  落在产物区 `script/tests/_work/`（用后 rmtree 清理、.gitignore 排除）为上条"临时文件不得污染
  产物区"的**显式例外**而非违反，并记录理由（沙箱限制 + 产物自足）；同时声明两种工作区策略
  （缺省=产物区内清理 / 显式参数=外部路径不清理）。IMPL 引用同步（§1 表与复审请求信均称 v1.1，
  与文件实际版本一致）。

### F-7【一般】Windows 锁失败降级不可观测 —— **已补计数**

- `writer.py:172` 新增实例级 `self.lock_degradations = 0`；写锁取锁失败（`writer.py:340`）、
  解锁失败（`writer.py:359`）各计 1 次；Linux 侧轮转锁 open/flock 失败同样计入
  （`writer.py:404/414`）。注释与 docstring 同步改为"降级必须可观测"。

### F-8【提示】rmlog.h close 语义注释失实 —— **已对齐（改注释，不改行为）**

- `rmlog.h:60` 注释改为："rmlog_close … 关闭句柄。注意：close 后再次调用 RMLOG_* 宏**并非无操作**
  —— emit 会按需重新打开日志文件继续记录（幂等重开语义）"。取舍说明：选"改注释"而非"加终态
  标志收紧行为"，因为"close 后可继续记录"对比赛取证更有利；`rmlog.c` `rmlog_close` 内加了对齐注释。

### F-9【提示】C 端容量边界表述不完整 —— **已补真实表述**

- `rmlog.c:76-81`（RMLOG_LINE_MAX 注释重写）：vsnprintf 截断到 1023 字节后仍记录（截断计数）；
  但转义会膨胀（`|`/换行/控制字符 1B→4B `\xNN`），**mod+msg 转义后总长超 2047 字节的事件整条
  丢弃并计数**（rmlog_line 返回 -1，绝不产坏行）。IMPL §4.3 同步："≤1023 字节的消息"不保证可记录，
  取决于需转义字符占比。

## 范围遵守声明（DN5）

本轮改动仅覆盖 9 个发现项及其直接关联（worker.py keep 参数为 F-1 用例支撑、USAGE §6 部署约束
为 F-1 协议前提的部署侧表述、IMPL/INDEX/WORKLOG 登记义务）。management 已裁定的 P1 项
（C 端 mkdir -p 等效、C 端 attrs）未做；无其他顺手改动。

## 期望回复

`REVIEW-T-20260926-001` 增量复审报告（新结论）至本角色 inbox，抄送 management。
复审通过前，本角色不向 management 发 RESULT、不发 maintainer 备料通知。
