# VERSION-001 — T-20260930-005-logging-v2

| 字段 | 值 |
|---|---|
| task_id | `T-20260930-005-logging-v2` |
| 归档版本号 | **001（首版）** |
| 来源 commit | **`3148fedec9f39dbf95184cdfd72ffb8bd605e892`** |
| 验收状态 | **accepted（板端实测通过）**，management `ACCEPT-20261001-logging-v2.md`（2026-10-01 16:06）+ DECISION `MAIL-20261001-1610` |
| 归档日期 | 2026-10-01 |
| 归档执行 | maintainer (R-006) |

## 1. 三份要件与一致性（2026-10-01 据真实证据更正）

| 要件 | 真实证据（文件 / mail_id） | commit | 结论 |
|---|---|---|---|
| management 验收 / 归档许可 | `management/script/ACCEPT-20261001-logging-v2.md`（2026-10-01 16:06）+ DECISION `MAIL-20261001-1610-management--maintainer-DECISION-accept-v2-and-archive-fix` | 对齐基准 `3148fed` | ✅ accepted（板端实测通过；未验证边界见 ACCEPT §3） |
| 静态审查（code_reviewer） | `code_reviewer/script/REVIEW-T-20260930-005-3148fed.md`（**第一份真实落盘审查**） | 报告落盘 `b6c8aac`；被审 `3148fed` | ✅ PASS（零阻断/严重；唯一 INFO-1 为沙箱环境观察，范围外） |
| 测试（software_tester） | 容器 `software_tester/script/TESTREPORT-T-20261001-007-001.md` **+ 板端真机 `software_tester/script/TESTREPORT-T-20261001-008-001.md`** | 容器 `3148fed`；板端 `d2e1081` | ✅ 容器 13/13 + smoke + 五域注入；板端 X5 实测 13/13 + smoke + 五域注入 5/5 |
| developer 合格确认（备料） | 原卡引 `MAIL-20261001-0200-developer--maintainer-HANDOFF-T-20260930-005` **在仓库与 git 历史中均不存在**（空壳引用） | `3148fed` | ⚠️ 无落盘 HANDOFF 信；developer 为外部实例，直接于 feature/logging-v2 提交 `3148fed`（见 §6） |

一致性：审查 / 验收 / 测试三件证据均以 `3148fed` 对齐；`developer/script` 在 `3148fed` / `d2e1081` / `75c3215` / HEAD `b6c8aac` 四处**逐字节一致**（`git diff --stat` 全空，已复核），无混用旧版板端事实。

## 2. 归档范围与冻结

`code/` 为从 `git -c core.autocrlf=false archive 3148fed developer/script` 取得的 32 个源码/文档/服务/smoke 文件；历史测试日志与 `.gitignore` 留在来源，可由 commit 重建。归档完成后 `code/` 冻结。v001/v002 旧归档、developer 原产物和 `management/from_human` 均未修改。（归档件磁盘行尾为 CRLF、来源 blob 为 LF——行尾说明见 §4。）

## 3. 补注前/后双指纹

本卡指纹均以 **LF 归一化内容** 计算（磁盘归档文件为 CRLF 行尾，行尾差异说明见 §4）。未补注文件（20 个）LF 归一化后与来源 commit blob 逐字节一致；以下是新增 maintainer 注释文件（12 个）的完整双指纹（前 → 后）：

| 文件 | 补注前 | 补注后 |
|---|---|---|
| `export_evidence.py` | `ad2768bc02902732b82da460d99ec93b84c1920da9a6195500a0b59ad17cba09` | `6ce764f6a8f1feba0907507da5b40924cdc5735fc116485117afa4ac568afb63` |
| `rmlog/async_writer.py` | `10c902087e7ded1d06d12f4279118b951cb77382fd65a3dce9843cf813f6b87f` | `7414966d5237e8c3b9edbab604a28731793761e9659b50fe3ce6ba132f144425` |
| `rmlog/checks.py` | `1873c7894d9631d0002b10d552283f722d643033721d6a1eb5eb148749f63e64` | `7784b7ec4faafb39d2e0e8b2be28cd25f7ecf936db59b71064343ed8cccbd232` |
| `rmlog/daemon.py` | `4abe43168b3a2f9b0111abb732c11c02e3cdc752d7ca94272c14e4ac98227ae0` | `b708842ecaa72b24d325946fd23c37d0f2a319b7c2041d93223054b818cad3f2` |
| `rmlog/fault_demo.py` | `12ed489c18e4a25b2666cd607a99ed9198ef892ada0f9469cc9f3bf5c6bb652e` | `da1ea8387f9afbfbe5007ed3bb1d41474a4b895d0d08b00895644651570005cd` |
| `rmlog/format.py` | `af7a164f3f6b40c4eaeb51c015a185dd5a942450f6f2837680e7e648d82e5a6e` | `93e9aaf5f33b5d5007a7256a8059657a43ef96dd5e8afc00b52093c2a65e3407` |
| `rmlog/rmlog.c` | `4839a15212dbcc49d535dc1548c82b7300e11510fc8df2c3c2c07f16974c21f1` | `ba8a486c0097c2bcf402a24cdacbbaee91ff0f8e179d7c34c3876a1f280a568a` |
| `rmlog/rmlog.h` | `ca513bdf0eb9097c94446a8077a80faa6118ff5b1f366b67a04582f4ea2500f6` | `dd2063dddbd8531c3429bac6a8197765de3e6d3da60591281c17469d684d9e1b` |
| `rmlog/session.py` | `1c582f6731ea6ab58b23f03949cf75b2cbd055a9f35db17f9d4e686b983b035b` | `c328dad3af6c0f9d850cc071d4999466476a3719dee88b7d008573f1a5cf67dd` |
| `rmlog/writer.py` | `499d285629cb46c3a443cc7fed8950a0ef4bd8210f01e283ba10d693197d985f` | `84473fbe4cb4e61ffc97110d940c193afb067e710500deb12df2c44f236a2b75` |
| `rmlog_read.py` | `413daf4949189e6c6e45878b42ed034dd19df9bdde76f73dc0dedcbf326d998c` | `05ec11791e2891051327faed2da96a7194bfeea6b259a875a41394da9d61d522` |
| `systemd/rmlog-demo.service` | `be564ad42dc4a02c8d686cfc3d584f1c40e337c518ade68d446b1b99723582af` | `d86cfb71940168698b079fad857782a5b5d3cc8c9f83e249322fbed18a31c245` |

## 4. KN3 校验（2026-10-01 复核）

以来源 `3148fed` blob 对 `code/` 逐文件复核（行尾 CRLF→LF 归一化后比对）：

| 类别 | 文件数 | 结果 |
|---|---|---|
| 未补注文件 | 20 | LF 归一化后与来源逐字节一致（SHA-256 匹配），无任何内容差异 |
| 补注文件（diff 仅新增注释行） | 11 | `git diff --no-index -U0`：删除=0，新增仅 `# Maintainer archive note (v001): source snapshot 3148fed; comments only.` 一类注释行，**KN3 合规** |
| 补注文件（KN3 越界） | 1（`systemd/rmlog-demo.service`） | 新增 2 行 = 1 注释行 + 1 个 `[Unit]` 行；`[Unit]` 为 systemd 节头、**非注释**，属 KN3 越界（归档件多出一个伪 `[Unit]` 节，来源 `3148fed` 无此问题） |

- **行尾说明**：32 个归档文件在磁盘上均为 CRLF 行尾，来源 blob 为 LF；这是 Windows 归档/补注过程的平台产物，非语义改动。本卡「补注前/后」指纹以 LF 归一化内容计算（§3 全部 12 组已复核一致）。
- **结论**：内容层面除 `systemd/rmlog-demo.service` 的 1 个伪 `[Unit]` 节头外，其余 31 文件 KN3 合规（只增注释、无删除、无语义改动）。该伪 `[Unit]` 为归档件自身缺陷，来源代码不受影响；按 KN2 归档 `code/` 已冻结，本角色不改动，已记入 §6 并向 management 如实报告。

## 5. 未验证边界

X5 aarch64 基础运行已由板端真机 `TESTREPORT-T-20261001-008-001` 实测通过（selftest 13/13 + smoke + 五域故障注入 5/5）；**仍 `unverified`**：板端 systemd 安装/权限/重启、真实 SPI/CAN/传感器接入、断电持久性、1 kHz 硬实时和长跑容量。历史板端报告未用于本版事实。归档完成不等于发布或整车交付验收。

## 6. 程序性更正记录（2026-10-01 核验后追加）

1. **原卡空壳引用**：VERSION-001 原 §1 引用的 `REVIEW-T-20260930-005-3148fed.md`、`ACCEPT-20261001-logging-v2.md`、DECISION `MAIL-20261001-1210`、developer HANDOFF `MAIL-20261001-0200` 在归档当时均不存在于仓库——即在审查门与验收未落盘时先行归档，属程序性空壳。
2. **现已补齐并据此更正**：审查报告（`b6c8aac`，PASS，第一份真实落盘审查）、验收报告 `management/script/ACCEPT-20261001-logging-v2.md`、DECISION `MAIL-20261001-1610`、板端真机 `TESTREPORT-T-20261001-008-001.md` 均已落盘；§1 三份要件表已按真实证据重写。
3. **developer 备料**：无落盘 HANDOFF 信；developer 为外部实例直接提交 `3148fed`（feature/logging-v2），`developer/script` 四处 commit 逐字节一致已由 code_reviewer 复核，本卡不伪造 HANDOFF 记录。
4. **SPEC/WALKTHROUGH/QUESTIONS/DIFF**：其 `file:line` 代码引用与来源一致，按 DECISION §2.3 不改内容。注：SPEC-001 §9 与 DIFF-001「事实边界」仍写 "accepted（开发机范围）/ 未覆盖 X5 aarch64"，该表述已被板端真机 T-008 与 ACCEPT「板端实测通过」取代——此项更正仅记于本卡，原文档冻结于归档时点不改（是当时基于空壳引用的诚实记录）。
5. **归档件 KN3 缺陷**：`systemd/rmlog-demo.service` 归档件含 1 个伪 `[Unit]` 非注释行（见 §4），来源代码无此问题；按 KN2 归档件冻结不改，留待 management 裁定是否以新版本纠正。

## 7. 版本去向注记（2026-10-01 追加，DECISION `MAIL-20261001-1630`）

本版本 `systemd/rmlog-demo.service` 归档件的伪 `[Unit]` 缺陷（§4 / §6-5 所述 KN3 越界）**已由版本 002 纠正**（见 VERSION-002 / DIFF-002 / `v002/systemd/rmlog-demo.service`）；本卡及 `code/` 32 文件保持冻结不改。
