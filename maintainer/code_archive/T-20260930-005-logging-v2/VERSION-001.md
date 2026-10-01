# VERSION-001 — T-20260930-005-logging-v2

| 字段 | 值 |
|---|---|
| task_id | `T-20260930-005-logging-v2` |
| 归档版本号 | **001（首版）** |
| 来源 commit | **`3148fedec9f39dbf95184cdfd72ffb8bd605e892`** |
| 验收状态 | **accepted（开发机范围）**，management ACCEPT-20261001 |
| 归档日期 | 2026-10-01 |
| 归档执行 | maintainer (R-006) |

## 1. 三份要件与一致性

| 要件 | mail_id / 文件 | commit | 结论 |
|---|---|---|---|
| management accepted / 归档许可 | `MAIL-20261001-1210-management--maintainer-DECISION-accept-v2`; `management/script/ACCEPT-20261001-logging-v2.md` | `3148fed` | ✅ accepted（开发机范围） |
| developer HANDOFF | `MAIL-20261001-0200-developer--maintainer-HANDOFF-T-20260930-005` | `3148fed` | ✅ 备料齐全 |
| reviewer PASS | `code_reviewer/script/REVIEW-T-20260930-005-3148fed.md` | `3148fed` | ✅ PASS |
| tester report | `software_tester/script/TESTREPORT-T-20261001-007-001.md` | `3148fed` | ✅ Linux 容器结果 |

三份要件（许可、开发交付、测试/审查证据）的完整 commit 均为 `3148fedec9f39dbf95184cdfd72ffb8bd605e892`，无混用旧版板端事实。

## 2. 归档范围与冻结

`code/` 为从 `git -c core.autocrlf=false archive 3148fed developer/script` 取得的 32 个源码/文档/服务/smoke 文件；历史测试日志与 `.gitignore` 留在来源，可由 commit 重建。归档完成后 `code/` 冻结。v001/v002 旧归档、developer 原产物和 `management/from_human` 均未修改。

## 3. 补注前/后双指纹

未补注文件的 SHA-256 与来源 commit blob 相同。以下是新增 maintainer 注释文件的完整双指纹（前 → 后）：

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

## 4. KN3 校验

以来源 commit blob 对 `code/` 逐文件 `git diff --no-index -U0`：变化仅为新增注释行（Python `#`、C 注释块、systemd `#`），删除=0，未改语义。代码归档自本卡落笔后冻结。

## 5. 未验证边界

X5 aarch64、板端 systemd 安装/权限/重启、真实 SPI/CAN/传感器接入、断电持久性、1 kHz 硬实时和长跑容量均为 `unverified`；历史板端报告未用于本版事实。归档完成不等于发布或整车交付验收。
