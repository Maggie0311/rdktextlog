# VERSION-001 — T-20260926-001-logging-platform-p0 · 版本记录卡（版本 001）

| 字段 | 值 |
|---|---|
| task_id | `T-20260926-001-logging-platform-p0`（主交付；同归档单元含其 R4 修复轮 `T-20260927-003-logging-c-linux-build`） |
| 归档版本号 | **001（首版）** |
| 来源 commit | **`164d4c7643ae20699f73db9e733a29f783b8172a`（短 `164d4c7`）** — developer R4 终版，即被审查（REVIEW-T-20260927-003-164d4c7 PASS）与被板端复测（TESTREPORT-T-20260927-003-001 全绿）、被验收（ACCEPT v2 accepted）的同一份 |
| 版本链 | R0=`f3331b0` → R1=`45eeb04` → R2=`a675c8d` → R3=`2d83644` → **R4=`164d4c7`（本版）** |
| 验收状态 | **accepted**（`ACCEPT-20260927-logging-p0.md` v2，2026-09-28，归档许可指向 164d4c7） |
| 归档日期 | 2026-09-28 |
| 归档执行 | maintainer (R-006) |

---

## 1. 三份要件（齐备性核验，逐份确认）

| # | 要件 | mail_id / 文件 | commit 口径 | 核验结论 |
|---|---|---|---|---|
| 1 | **management 验收许可（accepted）** | `management/script/ACCEPT-20260927-logging-p0.md`（v2 追记 2026-09-28；非邮件，验收报告形态） | 归档版本指向 **164d4c7** | ✅ v1"有条件"→ v2 板端条件满足，升格 accepted；§4 明示归档已解冻 |
| 2 | **developer 合格确认通知（备料）** | `MAIL-20260928-2000-developer--maintainer-HANDOFF-T-20260927-003-linuxbuild` | **164d4c7** | ✅ 声明取代旧版覆盖 `2d83644` 的 HANDOFF（MAIL-20260927-1505，仅留档备查，不再是有效备料） |
| 3 | **software_tester 合格确认通知（备料）** | `MAIL-20260928-1958-software_tester--maintainer-HANDOFF-T-20260927-003` | **164d4c7** | ✅ git archive 签出 12 关键文件 blob 核对 MATCH、板端 md5 34/34 MATCH；未覆盖项已列 |

**hash 一致性**：三份要件的 commit 口径完全一致 = `164d4c7`。要件 2 明确声明"备料不是许可，归档以 management accepted 为准"。

## 2. 归档前核验（git archive 164d4c7 vs 工作区）

- **方法**：`git archive --format=tar 164d4c7 developer/script`（`-c core.autocrlf=false` 保证 blob 原始字节）签出到临时区，与 `developer/script/` 工作区逐文件 SHA-256 比对。
- **结果：32 文件中 28 个逐字节一致（MATCH=28）。4 个差异全部可解释且不涉源码**：
  1. `INDEX.md`、`tests/selftest-20260927-2208-r4.log` — 164d4c7 **之后** developer 自己的两笔簿记提交（`b38484c` 补登 INDEX #5 行 R4 hash、`d3d0cfe` 把 r4 自测日志从 UTF-16 重编码为 UTF-8 无 BOM；均为非代码簿记）；
  2. `tests/selftest-20260927-1235-rf.log`、`tests/selftest-20260927-1352-rf6.log` — 仅换行符表示差异（仓库 blob=LF，工作区=CRLF，`core.autocrlf=true` 全局配置所致，无 .gitattributes）；内容逐行相等。
- **结论**：**不构成"工作区有 developer 未提交改动"**（tracked 文件工作区与 HEAD 零差异；`git diff --name-only 164d4c7 HEAD -- developer/script` 仅上述 2 个簿记文件）。**不触发 QUERY 停止条件**，归档基准取 git archive 164d4c7 的 blob 原始字节（= 被审查/被测试/被验收的那一份）。
- 工作区中的 `__pycache__/`、`tests/_work/` 为运行中间物（`.gitignore` 排除），不属交付物，不归档（归档 README §4 大文件策略）。

## 3. 补注前指纹（来源基准）

**来源 commit：`164d4c7`（git archive blob 原始字节）。**
**归档范围：21 文件**（全部 32 文件中剔除非交付物 11 件：9 个 `tests/selftest-*.log` 留档、1 个 `tests/probe_fdleak_rf6_before_after.log` 数据留档、1 个 `.gitignore`——按归档 README §4"二进制/打包件/构建中间物不入库，只记录校验值+来源+重建方式"处理；留档文件的可重建性与原文校验值见 §6 留档注记）。

| 文件 | SHA-256 |
|---|---|
| `CODE-STYLE.md` | `30425c8449a75487f631fe592df5227ecf3fb83c111e4e5cb12da569dae9806d` |
| `ERR-CATALOG.md` | `f578d6205b5c9ac6da48a0a6e22031a1ad68ca7a202ce4164c097b76bb9fe16f` |
| `IMPL-T-20260926-001-logging-platform-p0.md` | `fddc558831eef90ad8519aabc37ef71e7260fbcfc6677db1a9fe811738424532` |
| `INDEX.md` | `2b970db9f400759627ae74a24431e31002d4e8912546d8e05a09ad65ab6b0ab1` |
| `README.md` | `36b717a75befd1eaa8797d50e6d080781c5ae4312ca03dd900c908762cdd689b` |
| `USAGE.md` | `d17858a328d6fa859a0c9511a34a304eaf275476ff620f054c4520b42b169b83` |
| `rmlog/__init__.py` | `f2c0eb4974b7c1ac554aaf40a5b3fe87099d1693a0497219709ec8105606975f` |
| `rmlog/_ac4_probe.c` | `af418775dbb15c3fa99d40101c592f4992d66123d93cde1c59032d118a8bf8a7` |
| `rmlog/catalog.py` | `4823821971ce87ba3bc803aa1d90c5c7fc7d0ef4bce1cc0c28fde07c75ea2ed0` |
| `rmlog/encode_cases.py` | `a0aa711d098cb24b28bf889cac95eef84cc20d878e2095f48a69638da94aba93` |
| `rmlog/example.c` | `66521a010cdeb1fb150eb136d273c8ba16943a372e48ebdfa357f77ed1e5c5af` |
| `rmlog/format.py` | `af7a164f3f6b40c4eaeb51c015a185dd5a942450f6f2837680e7e648d82e5a6e` |
| `rmlog/gen_code.py` | `9a0f424eb8a2bcabce265bc1d16e8cdfb5cfb6725c6052d55066a1fc59ce10a2` |
| `rmlog/rmlog.c` | `4839a15212dbcc49d535dc1548c82b7300e11510fc8df2c3c2c07f16974c21f1` |
| `rmlog/rmlog.h` | `ca513bdf0eb9097c94446a8077a80faa6118ff5b1f366b67a04582f4ea2500f6` |
| `rmlog/rmlog_errors.h` | `808a2224451ddddc695b5e1ebee39c1a337e8b06768cb1ce91b8f6926c7b1a2f` |
| `rmlog/selftest.py` | `3b1e5364434a0edbdeda86e5d8b206d5aa181ad7160bb40644eceece0cc05633` |
| `rmlog/worker.py` | `f39368e2af03a81ee78f58fd0eb8e9e458d22509ed7da9743f32f216644277e8` |
| `rmlog/writer.py` | `499d285629cb46c3a443cc7fed8950a0ef4bd8210f01e283ba10d693197d985f` |
| `rmlog_read.py` | `371d456ed9d4a8b7612df936ef7eabee24395a255f18829b203a2bf48f6856a0` |
| `tests/probe_fdleak_rf6.c` | `8f6228322afb94ac08f2f6b24757fcfc48f6820ae87d2adfce98e182c6034411` |

> 上述 hash 均为 git archive 签出件的实测值（= 仓库 blob 字节），已与工作区同名文件比对确认（28/32 一致，差异 4 件见 §2）。

## 4. 补注（唯一写操作，就地补注）

- **方式**：就地补注（归档 `code/` 即带注版），凡新增行均带 **`（maintainer 补注：…）`** 标记或属同一注释块的连续行；Python 用 `#`、C 用 `/* … */`、Markdown 用 `<!-- … -->` 单行注释；未触碰任何代码行/字符串/宏/编译指令/原有注释。
- **重点覆盖**（委托层指定）：writer.py 轮转协议 v2（每写即开即关 + ROTLOCK 互斥 + 锁内 stat）、Windows 字节锁降级路径（F-7/RF-4 三处计数口径）、format.py 转义表、rmlog.c 特性宏（为何必须在 include 之前）、rmlog__open_locked 裁决与打开分离、轮转副本缓冲 528 可证安全算术、selftest 13 用例各自守什么。
- **规模**：21 文件中 20 文件被补注（`rmlog_errors.h` 为生成物不补注），**共新增 130 行，删除 0 行**。

## 5. 补注后指纹（归档件实际内容）

| 文件 | SHA-256 |
|---|---|
| `CODE-STYLE.md` | `3e99f36e66f1f732b2c3b16fbb401b15b9286c86f13b8395aaf7f9643cea9512` |
| `ERR-CATALOG.md` | `1f3daf9e47bb67ed9abfc7773a866e689e91b3117088caa4ca579ecccf82a395` |
| `IMPL-T-20260926-001-logging-platform-p0.md` | `4ea991c712f37de661254fbffd3adc470928fb0a8b1a5f4c5357f295392fe778` |
| `INDEX.md` | `e443c04baf3e3eaba51529ee78f576b4c80372cb13a0e2e51def5aa403771623` |
| `README.md` | `19792e98d345d10e0ab26da2656bfbc36bb21b8d0e750349a5347cbfa9721221` |
| `USAGE.md` | `ac856bc6202155250b4374093106c12c90c9c2469541e3b2774745d6f2324494` |
| `rmlog/__init__.py` | `0d2554b2867068907ef3be5190545b1e3e232942d6d5eca274c5c9fd4674558a` |
| `rmlog/_ac4_probe.c` | `02c5c2df09ec45f8f50abb6c2f6256e58a45730423ea8ac8c61a6482b1a9c5d3` |
| `rmlog/catalog.py` | `0432797260214e4c454cf54b0b4238bc8bd9d35d18ea2720587b7588cc874a4f` |
| `rmlog/encode_cases.py` | `cb1566cc13cadbba31ee31688bd9f82dbed9071d1fc6ab5e4982594cfa1c0f6f` |
| `rmlog/example.c` | `b0a59bb5eef3904fb8d5f19dcfcbdaf91ab6592270943c8529bf98404aaa4c8d` |
| `rmlog/format.py` | `cceceff69742358ec08c0a5c7c1fd7c6ee92c483b72f0ff5bd707fc2abb995e6` |
| `rmlog/gen_code.py` | `e4a9c3a460a49f510e9108e99a21381af391d66bba0f2cd937703e1c5cb44fc1` |
| `rmlog/rmlog.c` | `b47dab1bb2f6dfe4aec96b6b07a85fcb317a87a6cde4133c1156052a97e52031` |
| `rmlog/rmlog.h` | `354cf93fcfff564f153aadcf00ce3774588ae193c888d0adfdff9edf2613fe2f` |
| `rmlog/rmlog_errors.h` | `808a2224451ddddc695b5e1ebee39c1a337e8b06768cb1ce91b8f6926c7b1a2f` |
| `rmlog/selftest.py` | `55a5f5f6ab464c05ea112b808b0c395421af6026d88bb415651bedf12ca87f19` |
| `rmlog/worker.py` | `17190b59ff58ef6773df7678a955b724cf941a5d48ef0d4dee508a1376b06fad` |
| `rmlog/writer.py` | `f501b997670ecbd554c64a8a3ddd2817cadca976280c4c724324e0f7e674cbd3` |
| `rmlog_read.py` | `95ddf5e81105de036555deb4e6cd167622a52c8182e06b7a5e345f1ed50efc82` |
| `tests/probe_fdleak_rf6.c` | `bf3796a0e0a2d9c521d8e5df3fd6a9f252b26028d0f01c8b021a1a25f59544e3` |

> `rmlog_errors.h` 补注前后 hash 相同（未补注，生成物保持来源原样）。

## 6. diff 结论（KN3 合规）

- **方法**：`git diff --no-index` 以补注前基准树（git archive 签出副本）对照 `code/` 归档件，`-U0` 逐行核对。
- **结论**：**新增 130 行、删除 0 行、修改 0 行；全部新增行均为注释行**（`#` / `/*…*/`块 / `<!--…-->`，其中 40 行直接携带"maintainer 补注"标记，其余为同一注释块的连续行与块定界符）。**KN3 合规（不违反"只增注释行"），KN2 冻结生效**：本版本卡落笔之时起，`code/` 内 21 文件一字不改；任何变动只能作为新版本（版本号递增）。
- 附带验证：带注 `rmlog.c` 以 `gcc -std=c99 -Wall -Wextra -c` 编译 **退出码 0、stderr 0 字节**（注释未破坏语法、未引入告警）。

## 7. 未入档的来源文件注记（校验值 + 来源 + 重建方式）

| 来源文件（developer/script/ 下） | blob SHA-256（git archive 字节） | 不入档理由 | 重建/获取方式 |
|---|---|---|---|
| `tests/selftest-*.log`（9 件：20260926-1958 / 2002 / 2020-final / 2035 / 2055、20260927-1010-r1 / 1028-r1 / 1235-rf / 1352-rf6） | 见 §8 自测留档索引对应行 | 测试运行留档（文本），非源码；完整演进证据已在各轮 IMPL/审查报告引用 | `git show 164d4c7:developer/script/tests/<文件名>` |
| `tests/selftest-20260927-2208-r4.log` | 留档文件，未纳入本版（1660→1191 字节重编码发生在 164d4c7 之后的 d3d0cfe） | 同上 | 同上；内容=13/13 PASS 留档（R4 末轮，双端已复验） |
| `tests/probe_fdleak_rf6_before_after.log` | 留档文件 | RF-6 前后对照数据（文本数据），结论已固化于 IMPL §1.3 与审查报告 | 同上 |
| `developer/script/.gitignore` | — | 版本管理配置，非交付产物 | 同上 |

> 以上 12 件均可在来源 commit 下随时经 `git show` 取回，字节不变；此注记满足归档 README §4"不入库者记录校验值+来源+重建方式"。

## 8. 自测留档索引（来源侧，R0–R4 全部轮次）

| 留档（developer/script/tests/） | 轮次 | 结果 |
|---|---|---|
| selftest-20260926-{1958,2002,2020-final,2035,2055}.log | R0 五轮 | 2×PASS 10/10（2020/2055）、3×FAIL（迭代） |
| selftest-20260927-{1010,1028}-r1.log | R1 两轮 | FAIL 10/12 → **PASS 12/12** |
| selftest-20260927-1235-rf.log | R2 末轮 | **PASS 12/12** |
| selftest-20260927-1352-rf6.log | R3 末轮 | **PASS 13/13** |
| selftest-20260927-2208-r4.log | R4 末轮（Windows） | **PASS 13/13**（43.8s，退出码 0） |
| 板端（software_tester/script/work/T-20260927-003/board_output/） | T-003 板端复测 | **R-Q1 13/13 全 PASS（退出码 0）· R-Q4 gcc stderr 0 字节 · R-Q3 组合对账无回归** |

## 9. 归档维护者的独立复验（SPEC §7 构建运行方式核实证据）

- **本机（Windows 11 x64，Python 3.14.7，gcc 13.2.0 MinGW-w64）**：以 git archive 164d4c7 签出副本实跑 `python -m rmlog.selftest` → **13/13 PASS，退出码 0，用时 44.9s**（2026-09-28 20:1x，maintainer 独立执行，输出留本机临时区，未入档）；`gcc -std=c99 -Wall -Wextra` 编译带注 rmlog.c → 退出码 0、stderr 0 字节。
- **板端证据（引用，非本角色实测）**：`TESTREPORT-T-20260927-003-001.md` R-Q1/R-Q4/R-Q3 全绿（software_tester 于 aarch64 gcc 11.2.0 板端实测）。
- 本机复跑证据来源 = maintainer 会话执行记录（selftest 全文输出已在会话中留存）；正式回贴仍以 developer 与 software_tester 留档为准。

## 10. 状态

| 项 | 值 |
|---|---|
| 状态 | **accepted · 已归档 · 冻结** |
| 配套文档 | SPEC-001 / WALKTHROUGH-001 / QUESTIONS-001 / DIFF-001 / GLOSSARY（项目级，`maintainer/script/`）/ INDEX 已更新 |
| 未解疑问 | 见 SPEC-001 §11（8 项，如实列出） |
