# STM-001 — O_APPEND 跨平台语义差异必须在编码期显式分流

| 字段 | 值 |
|---|---|
| 状态 | active（candidate 经验） |
| 置信度 | 0.85 |
| 证据 | T-20260926-001：selftest AC5 并发用例 4×250 丢 89 行（tests/selftest-20260926-2042.log）→ writer.py 增加 Windows 字节锁路径 → 10/10 PASS（tests/selftest-20260926-2020-final.log） |
| 记录日期 | 2026-09-26 |

## 经验内容

"同一份追加写代码两端都能跑"是错觉：Linux `open(2)` 的 O_APPEND 是内核级原子追加，
Windows CRT 的 `_O_APPEND` 是"每次写前 seek 到末尾"，seek+write 跨进程**不原子**，
多进程并发追加会互相覆盖丢行。正确姿势是在编码期就显式分流：
Linux 走纯 O_APPEND（零额外开销），Windows 加文件区域锁（如 `msvcrt.locking` 字节 0）
串行化 append——并把该差异写进文件头与 IMPL，防止后人"简化"掉分支。

## 可复用性自检（记忆三问）

1. 下一个不同项目还能用吗？——能：任何跨平台多进程/多线程追加写场景（数值日志、数据采集）。
2. 可证伪吗？——能：若某 Windows 版本 CRT append 已是原子（或所测并发丢失另有原因），
   修复前提即被推翻。
3. 有具体证据吗？——有：上表两个 selftest 日志 + task_id。

## 晋升条件

再经历 1 个不同任务（不同代码库/不同写入场景）仍复现该差异 → 晋升 LTM。
