# WALKTHROUGH-001 — rmlog 逐模块代码走读（教学向）

> **归档版本 001 · 来源 commit `164d4c7`**。行号 = 归档带注版（`code/`）；来源 commit 行号换算见 SPEC-001 卷首说明。
> 读法：按本文 §1→§7 的顺序走一遍，即是一条"从业务视角进、从实现细节出"的完整路线。每个模块按 **职责 → 关键函数 → 数据流** 三段展开。

---

## 0. 全局地图（先建立空间感）

```
业务代码（你的电控程序）
   │  C: #include "rmlog.h" + RMLOG_I/W/E/F(...)      Python: import rmlog; rmlog.event(...)
   ▼
写入层   rmlog.c / rmlog.h（C，常驻 fd + emit 前对准）   rmlog/writer.py（Python，每写即开即关）
   │        两端共用一套协议：O_APPEND 一次写整行 + .rmlog.ROTLOCK 轮转互斥 + 锁内 stat
   ▼
磁盘     /userdata/rmlog/rmlog.log + rmlog.log.1...5（副本链）+ .rmlog.ROTLOCK（锁文件）
   ▼
读端     rmlog_read.py  parse / tail / filter —— 比赛日一条命令定位
支撑层   catalog.py（错误码唯一来源）→ gen_code.py 生成 rmlog_errors.h + ERR-CATALOG.md
         format.py（行格式 v1 编码/解析，两端同构的锚）
         selftest.py（13 用例）+ encode_cases.py + tests/probe_fdleak_rf6.c（验证体系）
```

**一个最重要的认知**：这份代码的注释密度极高（developer 契约要求"注释写为什么"），几乎每个非显然决策的旁边都有作者自己的理由。**本走读只补"作者没写的骨架"，不重复作者写过的理由**——凡有 `（maintainer 补注：…）` 的位置，正是归档维护者认为纯读代码看不出来的地方。

## 1. 入口层：业务怎么用（rmlog/__init__.py + example.c）

**职责**：把"写一条日志"变成一行代码。
- Python：`__init__.py` 转出 `event/get_writer/set_default_writer/Writer`（__init__.py:32）与 format 的 `encode/parse_line/...`（__init__.py:29-31）；`encode_line`（__init__.py:45）是 AC4 对照专用包装。业务最终调的 `rmlog.event(...)` 实现在 writer.py:531（模块级便捷 API，取进程级单例写事件）。
- C：`rmlog.h` 的宏族 `RMLOG_I/W/E/F(mod, code, fmt, ...)`（rmlog.h:50-53）——宏只是把"级别常量 + 你的参数"转交给 `rmlog_emit`（rmlog.h:57）。错误码常量 `RMLOG_CODE_*` 来自 include 的生成头（rmlog.h:35）。
- `example.c` 是最小可运行样例（40 行）：`rmlog_open` → 四级各一条 → `rmlog_close`（example.c:26-42）。

**数据流**：业务参数 → 宏/函数包装 → 写入层（§3/§4）。

## 2. 数据层：错误码与行格式（catalog.py + format.py）

**catalog.py**（职责：错误码的唯一数据源）：
- `DOMAINS`（catalog.py:29）五域定义；`ERRORS`（catalog.py:42）24 码本体，每码 `code/level/meaning/action` 四字段。
- 三个查表函数：`get`（127）、`codes_by_domain`（139）、`default_level`（149）。
- 数据流：本表 →(gen_code)→ C 头 + 文档；本表 →(writer.event 查默认级别)→ 每条日志的 LEVEL 字段。
- **为什么先读它**：后面一切"级别""码"字段都出自这里；且它零依赖，没有任何前置知识要求。

**format.py**（职责：行格式 v1 的编码与解析，双端同构的锚）：
- 编码：`encode`（format.py:167）按固定字段序拼 `LOGV1|seq|wall|mono|LEVEL|CODE|module|message[|k=v]`；每个文本段先过 `_escape`（78）——查转义表 `_ESCAPES`（67），未列出的控制字符走 `\xNN` 兜底。
- 解析：`parse_line`（201）三道闸——`LOGV1|` 前缀 → 段数 ≥8 → seq/mono 纯 ASCII 数字；通过后 `_unescape`（100）还原文本。任何输入不抛异常，不合法返回 None。
- 双时间戳：`wall_timestamp`（139，本地 ISO8601 毫秒）+ `mono_timestamp`（158，单调毫秒）。
- 数据流：`encode` 的输出行就是磁盘上的一行；`parse_line` 是读端一切功能的第一步。

## 3. 写入层·Python（writer.py —— 本组件最核心的一个文件）

**职责**：把一行文本可靠地追加进磁盘，多进程安全、超限轮转、失败不抛异常。

**关键函数与调用序**（Linux 主路径）：
```
event (247)
 └─ 查 catalog 默认级别（254-261，查表失败静默回退 INFO）
 └─ 持线程锁：seq++ → fmt.encode 组行 → _write_line (274)
     └─ _posix_write_line (298)   ← "每写即开即关"落点
         ├─ _open_append (200)     open(O_APPEND|O_CREAT|O_WRONLY)，失败计数返回 -1
         ├─ _write_once (227)      一次 os.write 整行；部分写补写一次
         ├─ _sync_fd (215)         ERROR/FATAL 才调（fdatasync，fsync=True 时升级）
         └─ close                  finally 里无条件关
 └─ 写成功后：_bytes += 行长 → 超 max_bytes → _rotate_if_needed (407)
     └─ open(.rmlog.ROTLOCK) → fcntl.flock(LOCK_EX)（阻塞式）
         └─ _rotate_step (444)     锁内 stat 真实大小：仍超限才轮转，否则校准计数
             └─ _rotate_file (97)  删最老 → .N 逐段后移 → 主文件改名 .1（纯链操作，无锁）
```
Windows 路径 `_win_write_line`（329）：整段（写+轮转）在 msvcrt 字节锁内；**降级路径**（锁文件 open 失败/取锁失败/解锁失败 → 计 `lock_degradations`，裸写不轮转）。
进程级单例：`get_writer`/`set_default_writer`（508/522）。

**为什么这样设计（模块头推理链 a~e 的骨架复述）**：旧协议"常驻 fd + close→rename→reopen"跨进程零协调，fd 会搁浅在旧 inode 上、整个文件被别人的轮转链当最老副本淘汰（已确认写成功的事件静默消失，reviewer 实证）。v2 用"每写按路径重开（fd 生命周期=一条事件）+ 链操作全程跨进程互斥 + 锁内真实大小裁决"三个手段，把丢数据通道在结构上封死。**推理链每步的"为什么成立"在 writer.py 模块 docstring（4-60 行）有作者完整版，先读它**。

**读码自检问题**（答案都在上文行号处）：为什么写路径不需要锁而轮转需要？（O_APPEND 单次 write 行原子 vs rename 链是复合操作）为什么 `_bytes` 偏小是安全的？（只会偏早触发，被锁内 stat 挡下）为什么降级时不轮转？（无锁链操作正是丢数据竞争）

## 4. 写入层·C（rmlog.c —— 板端部署目标）

**职责**：与 Python 端同协议同构行的 C 实现；常驻 fd 换低开销，用"emit 前对准"补回协议 v2 的关键性质。

**读码路线**（maintainer 补注于 rmlog.c 文件头，此处展开）：
1. **文件头注释（1-46）**：R1~R4 四轮变更史——每轮修了什么、在哪，读完对全文件有预期。
2. **特性测试宏块（56-58）**：`#if !defined(_WIN32) #define _POSIX_C_SOURCE 200809L`——必须在任何 include 之前（机理见 maintainer 补注与 IMPL §8.1；这是 R4 修复的板端编译失败根因）。
3. **平台适配层（70-108）**：同一组 `RMLOG_LOCK_*`/`RMLOG_FDATASYNC`/`RMLOG_OPEN_*` 宏在 Win32（CriticalSection/_commit/O_BINARY）与 POSIX（pthread_mutex/fdatasync）下各给一套实现——全文件其余代码不感知平台。
4. **`rmlog__open_locked`（219）**：裁决与打开分离（RF-6 结构）。盯住一个不变量：**全函数 open 恰好一次，在函数尾部（约 :246）**；头部各分支只裁决/复用 `g_path`。
5. **转义与渲染（287/330）**：`rmlog_escape` 与 Python `_ESCAPES` 同表同序；`rmlog_line` 同字段序 snprintf——这是 AC4 双端一致的实现侧。
6. **轮转协议 v2 段（393-535）**：`rmlog__rotlock_acquire`（423，flock；Windows 约定值 -2=平台无此能力不计数）→ `rmlog__rotate_chain_locked`（485，副本路径缓冲 528 可证安全）→ `rmlog__rotate_locked`（511，锁内 stat 确认）。
7. **`rmlog__reopen_current_locked`（541）**：写侧配合点——fd 若绑在他进程已改名的旧 inode（fstat/stat 的 size+inode 不一致）就关旧重开。
8. **`rmlog__emit_locked`（574）**：主路径组装——对准 → seq++ → 双时间戳 → rmlog_line → 一次 write（部分写补写）→ ERROR/FATAL fdatasync → 超限轮转。
9. **生命周期（666/706/722/735）**：`rmlog_open`（显式目录/缺省裁决两形态）、`rmlog_close`（fdatasync 后关 fd，g_path 保留——重开落点语义 RF-1）、`rmlog_flush`（P0 预留，未在头文件声明）、`rmlog_path`（诊断）。

**Python/C 两端对照表**（读一端时用另一端印证）：

| 概念 | Python | C |
|---|---|---|
| 行完整性 | O_APPEND 一次 os.write（writer.py:227） | O_APPEND 一次 write（rmlog.c:574 区） |
| 轮转互斥 | fcntl.flock on .rmlog.ROTLOCK（writer.py:407） | flock 同名锁文件（rmlog.c:423） |
| 锁内确认 | os.stat（writer.py:444） | stat(g_path)（rmlog.c:511） |
| 跨进程写协调 | Windows 写锁 / Linux 无锁 | 常驻 fd + emit 前对准（rmlog.c:541） |
| 关键级落盘 | fdatasync（writer.py:215） | RMLOG_FDATASYNC（rmlog.c:605 区） |
| 静默降级计数 | write_failures / lock_degradations | g_write_failures / g_lock_degradations |

## 5. 生成链：单一来源怎么落地（gen_code.py + rmlog_errors.h + ERR-CATALOG.md）

**职责**：让"错误码表"只存在一份。
- `render_header`（gen_code.py:67）把 catalog 表渲染成 `rmlog_errors.h`：级别常量（RMLOG_LVL_INFO..FATAL，顺序对齐 format.LEVELS）+ 每码两个宏（`RMLOG_CODE_<sym>` 字符串字面量、`RMLOG_LVL_<sym>` 默认级别）+ 静态码表数组 + 五域白名单。
- `render_doc`（140）渲染 `ERR-CATALOG.md`。
- selftest 的 GEN 用例（selftest.py:491）断言"生成物与表一致"——三份投影（Python 表 / C 头 / 文档）的一致性是被测试锁住的，不靠自觉。
- 数据流：catalog.py →（gen_code）→ rmlog_errors.h →（#include）→ rmlog.c/rmlog.h/example.c；catalog.py →（gen_code --doc）→ ERR-CATALOG.md。

## 6. 验证层：13 用例与两支 C 探针（selftest.py + encode_cases.py + tests/probe_fdleak_rf6.c）

**职责**：把 REQ 的 AC 断言化，跑一遍就知全部承诺是否成立。
- 用例注册表在 `main` 的 `tests` 列表（selftest.py:645 区）；**每用例守什么**已由 maintainer 补注逐条列在文件头（selftest.py:13-28），SPEC §3.6 有同名索引。
- AC4 的验证方法值得单独看（selftest.py:278 + encode_cases.py）：7 个固定输入用例 → `write_probe_input`（encode_cases.py:72）打成二进制（长度前缀，避免换行失真）→ gcc 现场编译 `_ac4_probe.c` + rmlog.c → 探针渲染 → `read_probe_output`（85）读回 → 与 Python `run_py_side`（59）输出逐字节比对。**时间由用例固定注入**，一致性判定只针对编码规则本身。
- RF6 探针（tests/probe_fdleak_rf6.c）：双组隔离变量（reopen 组=泄漏触发面，fast 组=对照）+ 落盘自检 + 句柄增量 <10 判定；修复前 1000 轮 +1000 / 修复后全 0 的对照数据在同目录 before_after 留档（未入档，`git show` 可取）。
- 零告警门槛是被用例强制执行的：C 探针编译 stderr 非空即 FAIL（selftest.py:263-265 与 :608-610 区两处 `if proc.stderr.strip()`）。

## 7. 读端（rmlog_read.py —— 比赛日的操作界面）

**职责**：parse（逐行 pretty 打印）/ tail（最后 N 条，--follow 每秒轮询）/ filter（级别+码前缀+时间窗 AND 组合）。
- 数据流：文件 → `iter_events`（38，流式逐行）→ `parse_line` 三道闸 → 条件过滤 → 人读打印；残行丢弃数与命中数走 **stderr**（stdout 保持纯事件流可安全重定向）——`_summary`（130）。
- F-2 修复落点 `_normalize_wall_prefix`（136）：把分钟级前缀按"日历段"补齐定宽（until 补 59/999=段末，since 补 00/000=段始），再与行内定宽时间戳做字典序比较——修掉"旧版 `--until 12:01` 漏掉整个 12:01 分钟"的系统性证据漏洞。`cmd_filter`（206）内的比较之所以可以直接用字符串 `<`/`>`，前提就是行内 wall_ts 定宽 + 输入已归一定宽。
- 读码自检：为什么用字典序比较而不转 datetime？（定宽 ⇒ 字典序=时间序，且免时区二次解释——见 maintainer 补注于 cmd_filter 上方）

## 8. 建议的完整读码路线（40 分钟版）

1. REQ §4 P0 一遍（需求语义）→ USAGE §4（行格式图解）→ ERR-CATALOG 扫一行例子（10 min）
2. catalog.py 全文 → format.py 模块头 + encode/parse_line（10 min）
3. writer.py 模块头推理链 a~e → `_posix_write_line`/`_rotate_if_needed`/`_rotate_step`（10 min）
4. rmlog.c：文件头变更史 → 特性宏块 → `rmlog__open_locked`（不变量：尾部唯一 open）→ `rmlog__emit_locked`（10 min）
5. 需要时再查：selftest 用例注册表、gen_code 渲染逻辑、读端 filter/前缀归一。
