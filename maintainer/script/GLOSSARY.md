# GLOSSARY — 项目级术语表

> 所有者: `maintainer` (R-006) · **跨版本累积**（不随版本重置）
> 目的：把代码中的**命名、缩写、领域词**翻译成人类能直接使用的话。第一次出现即收录。

## 收录原则

1. **只收"看不出来"的词**：能从代码一眼看懂的命名不收（收了反而增加维护成本）；
2. 每条给出三样：**词** / **人话解释** / **在代码中的位置与用法**（`file:line`，随版本更新）；
3. 同义词、历史遗留命名要注明（例如"老代码里叫 X，现在叫 Y"）；
4. **不确定含义的词标 `unverified`**——宁可留空并提问，不可猜一个解释（见契约 KN6）。

## 术语表

> 位置行号以归档版本 001（来源 commit `164d4c7`）带注版为准；换算来源 commit 行号的方法见 SPEC-001 卷首。

| 术语 / 缩写 | 人话解释 | 代码位置与用法 | 备注 |
|---|---|---|---|
| **rmlog** | 本项目的业务层文本日志平台名（"RM"=RoboMaster + log）。场上自动记错误，场下一条命令定位 | 包名 `rmlog/`、`rmlog_read.py`、C 前缀 `rmlog_` | REQ §3 裁定命名；"平台层（journald/dmesg）直接用 + 业务层自建"中的业务层 |
| **错误码五域** | 错误码 `E-<域>-<3位序号>` 的五个域：INIT 初始化 / COMM 通信 / HW 硬件 / FSM 状态机 / SYS 系统资源 | `DOMAINS`（catalog.py:29）、`ERRORS`（catalog.py:42）、生成头 `rmlog_error_table` | 用户四类错误 + 系统资源类（REQ §4 P0-a）；每码绑定默认级别/含义/建议动作 |
| **行格式 v1 / LOGV1** | 一行一条事件的冻结字段序：`LOGV1|seq|墙上时间戳|单调ms|LEVEL|CODE|MODULE|message[|k=v…]`；`LOGV1` 前缀是读端识别有效行的依据 | 唯一权威定义 format.py 模块头 + `PREFIX`（format.py:47）、`encode`（167）、`parse_line`（201）；C 端同构 rmlog.c `rmlog_line`（330） | 破坏性变更须升格式版本并同步 `__version__`（__init__.py:36 区） |
| **双时间戳** | 每行同时带墙上时间（ISO8601 毫秒，对表/对时间线用）与单调时间（ms，防 NTP 跳变，算间隔用）；跨上电比较单调时间无意义 | `wall_timestamp`（format.py:139）/ `mono_timestamp`（158）；C 端 `rmlog__wall_ts`/`rmlog__mono_ms`（rmlog.c:358/378 区） | CODE-STYLE §4.4"缺一不可" |
| **轮转协议 v2** | 多进程×轮转不丢数据的写入协议：①每写按路径 open→一次 write→close（无常驻 fd）②rename 链全程持跨进程轮转锁 ③锁内 stat 真实大小裁决。R1 为修 F-1 引入，双端同协议 | writer.py 模块 docstring"轮转协议 v2"（14-59 行）；rmlog.c 372-392 行注释块 | 旧协议（R0，常驻 fd）已废；C 端保留常驻 fd 但 emit 前"对准"补齐关键性质 |
| **ROTLOCK / .rmlog.ROTLOCK** | 跨进程轮转互斥锁的锁体文件：与日志同目录的隐藏文件，只当锁用，不写数据、永不进副本链；双端同名=协议约定 | `_ROTLOCK_NAME`（writer.py:84）、`RMLOG_ROTLOCK_NAME`（rmlog.c:121）；取锁 `_rotate_if_needed`（writer.py:407）/`rmlog__rotlock_acquire`（rmlog.c:423） | advisory 锁：互斥前提=同目录所有写入方都经本组件（部署约束，USAGE §6） |
| **O_APPEND** | open(2) 的追加标志：每次 write 自动写到文件当前末尾。Linux 上是内核级原子追加——"一次 write 写整行"行完整性的根基 | `_open_append`（writer.py:200）、`RMLOG_OPEN_FLAGS`（rmlog.c:106 区） | Windows CRT 的 _O_APPEND 是"写前 seek"不原子 → Windows 写路径加字节锁（writer.py:54-56 注释） |
| **特性测试宏（_POSIX_C_SOURCE）** | POSIX 规定的宏：在 include 任何标准头**之前**定义，告诉 glibc 暴露哪一代 POSIX 声明。`200809L`=POSIX.1-2008，解锁 clock_gettime/localtime_r/fdatasync 等 | rmlog.c:56-58（`#if !defined(_WIN32) #define _POSIX_C_SOURCE 200809L`） | R4 修复核心：严格 `-std=c99` 下 glibc 默认隐藏这些声明（板端编译失败根因，IMPL §8.1） |
| **advisory 锁（建议锁）** | 内核不强制执行的锁——不参与约定的进程可以无视它直接操作文件。flock/msvcrt.locking 都属此类 | rmlog.c:395-397 注释；USAGE §6 部署约束 | 后果：第三方工具直写 rmlog.log 时互斥前提失效（已知边界，非缺陷判定） |
| **残行三道闸** | 读端丢弃崩溃/断电残行的三道顺序判定：①`LOGV1|` 前缀 ②段数 ≥8 ③seq 与 mono 为纯 ASCII 数字；解析永不抛异常 | `parse_line`（format.py:201-226）、`_ASCII_DIGITS`（format.py:63 区） | AC2；rmlog_read 的丢弃计数（stderr）依赖它 |
| **转义表 / \xNN 编码** | 行内危险字符的编码替换规则：`\`→`\\`（最先）、`\|`→`\x7c`、换行→`\x0a`、其余 C0/DEL→`\xNN`。选编码替换而非引用转义，解析端零状态机 | `_ESCAPES`（format.py:67）、`_escape`（78）；C 端同表 `rmlog_escape`（rmlog.c:287） | 双端同表=AC4 一致的根基；改任一侧即跨端接口变更 |
| **write_failures / lock_degradations** | 两个必须分开的健康计数：前者=真实写失败（打开/写入），后者=锁相关降级（锁文件开不出/取锁失败/解锁失败）。混计会让健康检查误报 | writer.py:175-181 注释、`_win_write_line` 降级路径（329-382）；C 端 `g_write_failures`/`g_lock_degradations`（rmlog.c:164-165 区） | RF-4 口径收紧；C 端 Windows rotlock 约定值 -2 不计（RF-5） |
| **每写即开即关** | Python 端写路径形态：每条事件按路径 open(O_APPEND)→一次 write 整行→close，无常驻 fd。fd 生命周期=一条事件 | `_posix_write_line`（writer.py:298）+ maintainer 补注 | 代价=每条事件 3 次系统调用（µs 级）；换来多进程×轮转数据不灭失（F-1） |
| **裁决与打开分离** | C 端 `rmlog__open_locked` 的结构不变量：函数头部各分支只裁决/复用落点 `g_path`，open 全函数恰好一次在尾部。R3 为修 RF-6（双重 open 句柄泄漏）归位 | rmlog.c:194-218 注释 + `rmlog__open_locked`（219，尾部唯一 open 约 :246） | 回归闸=selftest 第 10 用例 + tests/probe_fdleak_rf6.c |
| **可证安全（528 缓冲）** | 指缓冲放大不是"试出来没告警"，而是给出最坏输出算术让 gcc 能证明不截断：副本路径最坏 511+1+11+1=524 字节 ≤ 528 | `RMLOG_ROTATE_PATH_CAP = RMLOG_PATH_CAP + 16`（rmlog.c:126-149 注释） | R4 根除 3× -Wformat-truncation 的方式（非 -Wno 压制） |
| **fdatasync / fsync / _commit** | fd 级落盘三形态：fdatasync 只刷数据最快（Linux）、fsync 连元数据（其他 POSIX 回退）、_commit 是 MSVCRT 等效 | `RMLOG_FDATASYNC`（rmlog.c:100-105 区）、`_sync_fd`（writer.py:215） | ERROR/FATAL 写后立即调用（AC6 崩溃取证）；INFO/WARN 靠页缓存回写（断电窗口声明，IMPL §4.2） |
| **AC1~AC8** | 需求验收标准编号（REQ §6 冻结）：AC1 可运行 / AC2 行格式 / AC3 错误码 / AC4 双端一致 / AC5 落盘与查询 / AC6 崩溃取证 / AC7 使用方法 / AC8 平台核查 | REQ-20260926-001 §6；selftest 覆盖矩阵（selftest.py:20-33 区） | selftest 覆盖 AC1~AC6 可自测项；AC7=USAGE、AC8=平台核查证据 |
| **F-x / RF-x / MIN-x / NIT-x / UV-x** | 审查体系编号：F=首轮发现项、RF=复审发现项、MIN=轻微登记项、NIT=提示级（不要求返工）、UV=unverified（审查/测试无法实测项） | REVIEW-* 系列报告 §5/§6/§7；UV-1~5 见 REVIEW-…-rf-a675c8d §6 | 本角色只转述不裁定（KN4） |
| **selftest 13 用例** | `python3 -m rmlog.selftest` 的断言式自测集：AC2×2/AC3/AC4/AC5×4/AC6/RF6/GEN/F2/READ | 注册表 selftest.py:645 区；逐用例说明=maintainer 补注（selftest.py:13-28） | 12→13 用例的分界=R3（新增 RF6 句柄守恒） |
| **k=v 属性（attrs）** | 事件消息后的可变参数字段：落盘为行尾 `|k=v` 段，读端解析回显，便于肉眼比对与脚本统计；**只放会变化、需事后比对的参数**（如 `dev=/dev/spidev0.0`、`retry=3`），固定上下文写进消息文本即可；C 端宏暂不支持（P1 扩展项） | Python `attrs={...}` 参数（writer.py:247/531、format.py:167/178）、解析回显 format.py:223-238；C 端无（encode_cases.py:15-16 声明） | v002 USAGE §2.3 给出使用时机口径（本版手册新增的整理）；行为面 v001 起未变 |
| **分钟级前缀（时间窗）** | `--since/--until` 接受非全精度时间前缀（如 `T14:38`）：按**日历段语义**解释——`--until 14:38` 含 14:38 这一整分钟（段末 59.999），`--since` 前缀=段始 00.000；实现为读端把前缀归一成毫秒定宽串再做字典序比较 | `_normalize_wall_prefix`（rmlog_read.py:136-156 区）、CLI 参数说明（rmlog_read.py:263-265）、maintainer 补注（rmlog_read.py:139-143/205 区） | F-2 修复的读端落点；v002 USAGE §2.5/§3.3 的命令语义来源 |
| **有界队列（bounded queue）** | 设定正整数容量的内存队列；满时显式拒绝事件并计数，不把无限堆积伪装成成功 | `rmlog/async_writer.py:20`、`AsyncWriter` 构造与入队路径 | v2 新增接入层；开发机 smoke 已测，硬实时边界 `unverified` |
| **session（会话标识）** | 启动到停止的一段事件共同携带的短标识，用于跨轮转文件筛选和 manifest 对账 | `rmlog/session.py:1`、`export_evidence.py` session filter | v2 新增业务接入词；不等于进程或 systemd unit 的唯一身份 |
| **manifest（导出清单）** | `export_evidence.py` 逐来源导出的清单：列出每个证据来源（business.log / journal / kernel / version 等）的状态（OK / MISSING / UNAVAILABLE）与行数，缺失项如实标注而非伪造成功 | `export_evidence.py` 生成 MANIFEST 段；SPEC-001 §8 声明本版增补 | v2 新增；与「有界队列」「session」同属 v2 证据导出主线 |
| **AsyncWriter（异步写入器）** | v2 新增的异步写入类：调用线程只做**非阻塞入队**（`put_nowait`），落盘由后台线程完成；队列满显式丢弃并计数。它是「有界队列」的宿主类——有界队列讲"容量满即拒"，AsyncWriter 讲"谁入队、谁落盘" | `rmlog/async_writer.py:12`（类）、`emit` :27（`put_nowait` :33）、`_run` :39（后台消费）、`flush` :54、`close` :72 | v2 源码行号（来源 3148fed）；**非硬实时**，IMPL 第 4 条 |
| **dropped（丢队计数）** | `AsyncWriter` 队列满时被丢弃事件的计数；**非零 = 丢过事件**（"非零丢失"的诚实出口，不伪装成功），调用方应把它接入健康监控 | `rmlog/async_writer.py:20`（初始化）、`:35-37`（`queue.Full`→`dropped += 1`） | 与 `write_failures`/`worker_failures` 分开计数（:21-22）；v2-USAGE「故障与队列边界」节 |
| **checks（检测适配器）** | 把业务传入的五域检测事实（init/comm/hw/fsm/sys）**映射到既有错误码**的适配函数 `emit_check`；库不探测硬件，只记录业务提供的事实 | `rmlog/checks.py:8`（`emit_check`）、`:10-12`（mapping 表 init/comm/hw/fsm/sys）、`:1-5`（模块头边界声明） | 映射到的码全为 v1 既有 24 码——**v2 无新增错误码**，新增的是"事实→错误码"适配层 |
| **fault_demo（五域故障注入演示）** | 可运行的故障注入演示脚本：`--fail` 指定某一域注入失败、其余四域记 ok，用于开发机/板端 smoke | `rmlog/fault_demo.py:9`（`main`）、`:15`（`Session("fault-demo")`）、`:16-18`（五域循环 `emit_check`） | 演示"事实→错误码"接口形态；真实 SPI/CAN/电机事实须由业务提供（`unverified`） |
| **export_evidence（证据导出）** | 一键导出脚本：业务日志（主文件 + 轮转副本 `.1...N`）始终先导出，再尝试 journal/dmesg/uname，逐项降级、失败标 `UNAVAILABLE`、缺失标 `MISSING`，最后生成 `MANIFEST.txt` | `export_evidence.py:18`（`main`）、`:32-54`（business.log 导出与 `--session` 过滤）、`:55-58`（可选证据 + MANIFEST） | 与「manifest」互补——manifest 是它的输出清单；v2-USAGE「证据与平台边界」节 |

## 维护提示

- 每完成一次归档，检查本版本是否引入新术语；有则补充，无则记一行"本版无新术语"；
- 术语解释若被用户或 `developer` 纠正，**不改旧行**，在该行下加"【更正】"并注明纠正内容。

## 版本收录记录

| 归档版本 | 新增术语 |
|---|---|
| 001（来源 164d4c7，2026-09-28） | 首次建档：上表全部 22 条（rmlog、错误码五域、行格式 v1/LOGV1、双时间戳、轮转协议 v2、ROTLOCK、O_APPEND、特性测试宏、advisory 锁、残行三道闸、转义表/\xNN、write_failures 与 lock_degradations、每写即开即关、裁决与打开分离、可证安全 528、fdatasync 三形态、AC 编号、审查编号体系、selftest 13 用例等） |
| 002（来源 08f6ce8，2026-09-29） | +2 条：k=v 属性（attrs）、分钟级前缀（时间窗）——v002 USAGE 手册六主题重排后，这两个"看不出来"的使用口径词有了成文出处；行为面本身 v001 起未变（零代码变更） |
| 003（来源 3148fed，2026-10-01） | +3 条：有界队列、session（会话标识）、manifest（导出清单）——v2 接入与跨轮转导出主线；板端 X5 基础运行经 T-008 实测通过，systemd 实装/断电/硬实时边界仍 `unverified` |
| T-20261001-010（文档重整，非代码归档，2026-10-01） | +5 条：AsyncWriter（异步写入器）、dropped、checks、fault_demo、export_evidence——统一文档入口任务（T-20261001-010）§3.3 补记；`session` 与「有界队列」已随 003 收录，本次不重复 |
