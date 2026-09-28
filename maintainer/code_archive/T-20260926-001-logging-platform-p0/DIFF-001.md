# DIFF-001 — 版本差异说明

> **归档版本 001 = 首版归档**。本归档系统此前无该 task_id 的任何版本，故本文写「**首版**」，无与上一归档版本的代码差异可比对。

## 1. 首版声明

- `maintainer/code_archive/T-20260926-001-logging-platform-p0/` 下本版（001）之前无版本目录、无墓碑记录（`_tombstones/` 当前为空）；本版是该 task_id 进入归档系统的第一版，也是当前唯一版本。
- 归档基准 = **developer 侧完整演进链的终点** R4=`164d4c7`，即被审查链（五份报告）与板端复测、management 验收（accepted v2）共同指向的同一 commit。**此前四轮交付（R0~R3）未经过归档**——它们以 git 历史与 developer INDEX 登记的形式存在，本版归档不追溯补档（契约 §5：归档后来源更新时才以新版本递增归档）。

## 2. 来源侧五轮演进摘要（R0 → R4，各版本 commit 与缘由）

> 以下为**事实转述**，来源：developer INDEX.md（交付登记）、IMPL §1.1/§1.2/§1.3/§8、五份审查报告、ACCEPT-20260927 §2。commit 行号/细节以各报告原文为准。

| 轮次 | commit | 日期 | 缘由与内容 | 审查结论 |
|---|---|---|---|---|
| **R0 首交付** | `f3331b0` | 2026-09-26 | REQ §4 P0-a~f 全量：catalog/format/writer/worker/gen_code/selftest/encode_cases + rmlog.c/h + rmlog_read.py + USAGE/IMPL；selftest 10 用例 | **CONDITIONAL**：F-1【严重】多进程×轮转数据销毁、F-2【严重】--until 分钟前缀漏事件 + 7 项一般/提示（REVIEW-…-f3331b0.md） |
| **R1 整改返工** | `45eeb04` | 2026-09-27 | F-1~F-9 全项处置。核心=**轮转协议 v2**（每写即开即关 + ROTLOCK 跨进程互斥 + 锁内 stat，双端同协议）+ 读端时间前缀归一（F-2）+ selftest 增至 12 用例（新增组合对账、F-2 回归） | **PASS**（600/600 组合对账；新发现 RF-1 一般 + RF-2/3/5 提示 + RF-4 一般，见 REVIEW-…-45eeb04.md） |
| **R2 复审微整改** | `a675c8d` | 2026-09-27 | RF-1（close 后重开复用 g_path，显式目录落点保持）/ RF-4（Windows 锁 open 失败改计 lock_degradations）/ RF-5（C 端 g_lock_degradations）/ RF-2/3（文档数字与 docstring 更正） | **FAIL**——修复引入 **RF-6【严重】**：`rmlog__open_locked` 分支内 open + 尾部再 open，首个 fd 未 close 即被覆盖，按需重开每次泄漏 1 句柄（1000 轮实测 +1000）（REVIEW-…-rf-a675c8d.md §6） |
| **R3 终轮微修复** | `2d83644` | 2026-09-27 | RF-6 结构归位（**裁决与打开分离**：函数尾部唯一 open）+ MIN-1/2/3（占位符填实/R2 hash 补登/任务书入库流程更正）+ selftest 增第 13 用例 `test_c_fdleak_reopen`（600 轮句柄守恒回归闸）+ 前后对照留档 | **PASS**（三重口径：结构逐行/语义等价走查/独立句柄对照修复前 +1000→修复后全 0；REVIEW-…-rf6-2d83644.md） |
| **R4 构建可移植性修复** | `164d4c7` | 2026-09-27 | T-20260927-003（板端实测缺陷触发）：rmlog.c 源码内 `_POSIX_C_SOURCE 200809L`（特性宏置于任何 include 之前，根除 glibc 严格 c99 下 POSIX 声明隐藏的板端编译失败）+ 轮转副本路径缓冲放大 512→528 根除 3× `-Wformat-truncation`（可证安全，非压制）+ selftest C 探针板端链接追加 `-lpthread` + USAGE/IMPL §8 同步 | **PASS**（REVIEW-T-20260927-003-164d4c7.md；板端复测全绿：13/13、gcc stderr 0 字节、组合对账无回归——TESTREPORT-T-20260927-003-001） |

**验收轨迹**：management 初审有条件（板端证据缺口）→ 板端首测 T-002 发现 C 端目标平台编译失败 → 开 T-003 修复（R4）→ 板端聚焦复测全绿 → **accepted v2（2026-09-28，归档版本指向 164d4c7）**。全链记录见 `management/script/ACCEPT-20260927-logging-p0.md` §1~§3。

## 3. 本归档版本相对来源 commit 的差异（归档操作本身引入的差异）

| 项 | 内容 |
|---|---|
| 代码差异 | **无**（零代码改动） |
| 注释差异 | **+130 行注释，-0 行**（21 文件中 20 文件补注；全部为 `（maintainer 补注：…）` 标记的中文注释行或同块连续行；`rmlog_errors.h` 生成物未补注）——逐文件 SHA-256 双指纹与 diff 结论见 VERSION-001 §3~§6 |
| 范围差异 | 来源 32 文件中 12 件未入档（9 个 selftest 留档 + RF6 前后对照留档 + r4 自测留档 + .gitignore），理由与取回方式见 VERSION-001 §2/§7 |
| 行为差异 | 无（带注 rmlog.c 编译零告警复验通过；selftest 在签出副本 13/13 PASS） |

## 4. 下一版本触发条件（备忘）

- 来源 `developer/script/` 出现**新的合格交付**（developer HANDOFF + 复审 PASS + 板端复测 + management accepted，hash 一致）→ maintainer 以**版本 002** 归档，版本号递增，`code/` 内本版文件一字不改（KN2/KN9）。
- 本版归档件发现问题 → 不改本版；按 K11 发 ISSUE，修复落在新 task_id / 新版本。
