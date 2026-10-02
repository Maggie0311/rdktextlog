# VERSION-001 — T-20261001-logging-v3

| 字段 | 值 |
|---|---|
| task_id | `T-20261001-logging-v3` |
| 归档版本号 | **001（首版）** |
| 来源 commit | **`d77d36c8535cdcb55249e400b56205254e50d299`**（短 `d77d36c`；feature/logging-v3 tip） |
| 验收状态 | **accepted**（management `ACCEPT-20261002-logging-v3.md` + DECISION `MAIL-20261002-1600`） |
| 归档日期 | 2026-10-02 |
| 归档执行 | maintainer (R-006) |

## 1. 三份要件与一致性

| 要件 | 真实证据（文件 / mail_id） | commit | 结论 |
|---|---|---|---|
| management 验收 / 归档许可 | `management/script/ACCEPT-20261002-logging-v3.md` + DECISION `MAIL-20261002-1600-management--maintainer-DECISION-accept-v3-and-archive` | `d77d36c` | ✅ accepted |
| 静态审查（code_reviewer） | `code_reviewer/script/REVIEW-T-20261001-logging-v3-d77d36c.md`（PASS；复审任务 `T-20261002-013-logging-v3-rereview`） | 报告落盘 `c2a014b`；被审 `d77d36c` | ✅ PASS（首轮 F-01~F-06 全核销，零新发现项） |
| 测试（software_tester） | HANDOFF `MAIL-20261002-1550-software_tester--maintainer-HANDOFF-T-20261002-014` + 板端 `software_tester/script/TESTREPORT-T-20261002-014-001.md` | `d77d36c` | ✅ BQ1~BQ5 全通过（BQ1 selftest 13/13、BQ2 v2+v3 smoke 双 PASS、BQ3 监控层读真实 dmesg/sysfs、BQ4 core 配置记录、BQ5 daemon 心跳+SIGTERM 收尾） |
| developer 合格确认（备料） | **无落盘 HANDOFF 邮件** | `d77d36c` | ⚠️ 外部 developer（ChatGPT）经 `logging-v3-final.bundle` 交付 d77d36c + 其 RESULT 说明，无邮箱通道；版本卡如实注记，不伪造 HANDOFF（见 §6） |

一致性：审查 / 验收 / 测试三件证据均以 `d77d36c` 对齐；`developer/script` 在 `d77d36c` 与工作树 HEAD（`7bc5789`）间逐字节一致（`git diff --stat d77d36c HEAD -- developer/script` 为空，已核），无混用旧版事实。

## 2. 归档范围与冻结

`code/` 为来源 commit `d77d36c` 的 `developer/script` **逐字节副本**（54 个 tracked 文件，经 `git cat-file blob` 逐文件落盘，`git -c core.autocrlf=false hash-object` 与 tree blob **54/54 一致**，含 `shared/rmlog_schema.h` 与历史 selftest 日志）。补注完成即冻结。

## 3. 补注前 / 后双指纹

### 3.1 补注前（来源 commit + 逐文件 SHA-256 清单，54 文件）

来源 commit：`d77d36c8535cdcb55249e400b56205254e50d299`。逐文件 SHA-256（按路径排序）：

| 文件 | 补注前 SHA-256 |
|---|---|
| `.gitignore` | `36f7082ebdc5a407931a53398a132bd43b9bc18cafd6f8d2769d6628f080a97b` |
| `CODE-STYLE.md` | `30425c8449a75487f631fe592df5227ecf3fb83c111e4e5cb12da569dae9806d` |
| `ERR-CATALOG.md` | `f578d6205b5c9ac6da48a0a6e22031a1ad68ca7a202ce4164c097b76bb9fe16f` |
| `export_evidence.py` | `ad2768bc02902732b82da460d99ec93b84c1920da9a6195500a0b59ad17cba09` |
| `IMPL-T-20260926-001-logging-platform-p0.md` | `6123faef2e227daff197d6ca7b13eee8f9ca7c4f5c72e5d394fa4e6950d7aec1` |
| `IMPL-T-20260930-005-logging-v2.md` | `e82055e85ef7c628528f26ca6637235fb86c7fea741d106b25cb8c3fe1d82981` |
| `IMPL-T-20261001-logging-v3.md` | `d23414e994607b547c7ae1e5dce7e2248c6793db5f936d6d0e6bc8e7e9e14fe4` |
| `INDEX.md` | `473b2032db22b05a83d94ddea94e07fb0b8d1068dfffb8e08ea9329a2fb272e1` |
| `PLAN-T-20260930-005-logging-v2.md` | `cedbb1880cf87b974e84c662020e4f0c4a98ec167b6f719e4210e935c09eb34a` |
| `README.md` | `ca5a6e464f25e6bb887cf0d2863db48765e18d5cff471fd073aa77f1ce90d7fa` |
| `rmlog/__init__.py` | `50d9b507af2667014146ec5ceb55460e2093f582c33e6d647a1c11f5c1f3a8c0` |
| `rmlog/_ac4_probe.c` | `af418775dbb15c3fa99d40101c592f4992d66123d93cde1c59032d118a8bf8a7` |
| `rmlog/async_writer.py` | `10c902087e7ded1d06d12f4279118b951cb77382fd65a3dce9843cf813f6b87f` |
| `rmlog/auto.py` | `aafb9c2956e7e6ec5347354e03bd85493fedd92f460546709f11cca014680ea9` |
| `rmlog/blackbox.py` | `f3202b3ec14d1c4fad8f4f1d06174d876dac797e890498ea34365d86b98aa8ad` |
| `rmlog/catalog.py` | `4823821971ce87ba3bc803aa1d90c5c7fc7d0ef4bce1cc0c28fde07c75ea2ed0` |
| `rmlog/checks.py` | `1873c7894d9631d0002b10d552283f722d643033721d6a1eb5eb148749f63e64` |
| `rmlog/code_map.py` | `9e37e153b3b343385ef6f3f0b04c11defba0da06e6a22f043e9c64e3144859d1` |
| `rmlog/crash.py` | `548b0d39360a1ae8d4f2efd11ad75c87c2bf41839eb587750fbf85556dc146d1` |
| `rmlog/daemon.py` | `bb8124de04051e08781f6ee3e826eac34b1c304419be022d9c1bc46d2d0c54d9` |
| `rmlog/encode_cases.py` | `a0aa711d098cb24b28bf889cac95eef84cc20d878e2095f48a69638da94aba93` |
| `rmlog/example.c` | `66521a010cdeb1fb150eb136d273c8ba16943a372e48ebdfa357f77ed1e5c5af` |
| `rmlog/fault_demo.py` | `12ed489c18e4a25b2666cd607a99ed9198ef892ada0f9469cc9f3bf5c6bb652e` |
| `rmlog/format.py` | `af7a164f3f6b40c4eaeb51c015a185dd5a942450f6f2837680e7e648d82e5a6e` |
| `rmlog/gen_code.py` | `a3e8454bd4af3e2c86f978cfcf76598c516d5cf41c28e324db70d80c35de222c` |
| `rmlog/monitors.py` | `06b874ddfae43190347b91ba34156b7224fdbb50885cf4bfa33e2a37bda6148c` |
| `rmlog/resources.py` | `da405843c6801b1eaffbb0e2e05adb158bb42abcdc2ee1cba2160f766617d5b7` |
| `rmlog/rmlog.c` | `4839a15212dbcc49d535dc1548c82b7300e11510fc8df2c3c2c07f16974c21f1` |
| `rmlog/rmlog.h` | `ca513bdf0eb9097c94446a8077a80faa6118ff5b1f366b67a04582f4ea2500f6` |
| `rmlog/rmlog_errors.h` | `5201631a314b1c57d92b539aa9a2622db0f0aaefa78916b0f92004ae815d17c7` |
| `rmlog/selftest.py` | `3b1e5364434a0edbdeda86e5d8b206d5aa181ad7160bb40644eceece0cc05633` |
| `rmlog/session.py` | `1c582f6731ea6ab58b23f03949cf75b2cbd055a9f35db17f9d4e686b983b035b` |
| `rmlog/USAGE.md` | `c238f94ee344146316b3289ed375079ebcf8e5fa455119f037b269d21df51a5d` |
| `rmlog/worker.py` | `f39368e2af03a81ee78f58fd0eb8e9e458d22509ed7da9743f32f216644277e8` |
| `rmlog/writer.py` | `499d285629cb46c3a443cc7fed8950a0ef4bd8210f01e283ba10d693197d985f` |
| `rmlog_read.py` | `2f53d420e4fef13fe8c5e6d666a4c03ea70300a021ea3fc9ba28be9e7211e055` |
| `shared/rmlog_schema.h` | `b1ddffe3d347e89f5a68d9104cf5d341dd93f8f2746a0096b96cb9dbb65ae0c3` |
| `systemd/rmlog-demo.service` | `f3f4f335d6491cb2d9b7a541e8ea473cfb820381420dcb2cda8cc71e14f6e258` |
| `tests/probe_fdleak_rf6.c` | `8f6228322afb94ac08f2f6b24757fcfc48f6820ae87d2adfce98e182c6034411` |
| `tests/probe_fdleak_rf6_before_after.log` | `1ed69fa9f9cc121312195ffc77674a0f5e8f5bf178e814bf863ee1b8ab6850b7` |
| `tests/selftest-20260926-1958.log` | `427924d730064fe3037cd773d0bc18ca9a62916b2c0870fe21edb93132f0ccf6` |
| `tests/selftest-20260926-2002.log` | `64aacdaed7fa7834aa73cb31a6d0419a7a19668f2d2724e7b108337e997dafdf` |
| `tests/selftest-20260926-2020-final.log` | `2df31b367013a242183a73c0f13625b21c39b9e7c2def336d6dc43dc6c579663` |
| `tests/selftest-20260926-2035.log` | `7419cb95dd08fd6ece24f85efe7fa814745a9c5c585e0db62863e86ae0f98560` |
| `tests/selftest-20260926-2042.log` | `fd3997bb4557a71abd9389a53b558679199ff41a2c10b295aac9e554c35c243c` |
| `tests/selftest-20260926-2055.log` | `a89942ec00f4ecb528d103aeba22d4f10744a9bf47d270e8d07b7128789e50ff` |
| `tests/selftest-20260927-1010-r1.log` | `686273ff90880fdffc6026d3a34d7a292aad34151864ccdd026893a69f12b8f6` |
| `tests/selftest-20260927-1028-r1.log` | `5d0ef13d5be9d9836251d95d9906d47b8da44b9122f257650aa68cd6792aa8fb` |
| `tests/selftest-20260927-1235-rf.log` | `c8932379fe955278383d4b5de0859cceee8126f32c600fc7b9d5d908e7e5f66c` |
| `tests/selftest-20260927-1352-rf6.log` | `780eade7649cdf412348d935ef302e629ed3b24b1de5953af35fccb875f18518` |
| `tests/selftest-20260927-2208-r4.log` | `4454230b1ef734bf3d4d91edfa699deea6a7ce4eebcd6b0a734be72a3290c011` |
| `tests/test_v2_smoke.py` | `221473916f46903668074d61d6d0d14c142e156b81e04c2e7028306db3f6beec` |
| `tests/test_v3_smoke.py` | `ab8ece5928b4863889e06852be2862d3b11eb18425a96fd189b2e3fcc6eebd0a` |
| `USAGE.md` | `f6521390657920e232ba64563559be16747c5a122d63764d49c02705cb1efad9` |

### 3.2 补注后（11 个补注文件；其余 43 文件与补注前逐字节一致）

| 文件 | 补注前 | 补注后 |
|---|---|---|
| `rmlog/blackbox.py` | `f3202b3ec14d1c4fad8f4f1d06174d876dac797e890498ea34365d86b98aa8ad` | `b0046cdd148f4ebd70e43964fca6ca201eff6a5f2dc1ebd2242e9ccee3d811b9` |
| `rmlog/crash.py` | `548b0d39360a1ae8d4f2efd11ad75c87c2bf41839eb587750fbf85556dc146d1` | `29d28ccab25ea572afbf36a78e616a096af5a66688f415927c299ba4865a4277` |
| `rmlog/monitors.py` | `06b874ddfae43190347b91ba34156b7224fdbb50885cf4bfa33e2a37bda6148c` | `ec9a6853e5c640b412ebe0500615270af3dafb1dab643efc41fd52f5dc74a78c` |
| `rmlog/resources.py` | `da405843c6801b1eaffbb0e2e05adb158bb42abcdc2ee1cba2160f766617d5b7` | `1f9263a708d638923377663297dc743095d062d1af371d46f5576f4aa316e376` |
| `rmlog/auto.py` | `aafb9c2956e7e6ec5347354e03bd85493fedd92f460546709f11cca014680ea9` | `d34e2da7f2000b54c6a700e767c8c2a83b1c0960465c0e3933851c634ae23273` |
| `rmlog/code_map.py` | `9e37e153b3b343385ef6f3f0b04c11defba0da06e6a22f043e9c64e3144859d1` | `1c188bbb8e80a959c4bd557d6bef23d32fd854ae0c17e6dc3562a2a51004218f` |
| `rmlog/gen_code.py` | `a3e8454bd4af3e2c86f978cfcf76598c516d5cf41c28e324db70d80c35de222c` | `c5ba5617cd59c4333396c3fa78c6ab35d419cacd2ddd830adc4a745965fa8e0f` |
| `rmlog/daemon.py` | `bb8124de04051e08781f6ee3e826eac34b1c304419be022d9c1bc46d2d0c54d9` | `521e00276e9b6567f463453010998c4b15d321ca2c924e2799fd5b0dcb38957a` |
| `shared/rmlog_schema.h` | `b1ddffe3d347e89f5a68d9104cf5d341dd93f8f2746a0096b96cb9dbb65ae0c3` | `4e9ac1014ff137427ee4c81900e0b0e5d354e9f2be49842c09b5283e0795b6e5` |
| `systemd/rmlog-demo.service` | `f3f4f335d6491cb2d9b7a541e8ea473cfb820381420dcb2cda8cc71e14f6e258` | `50ec80292f52290c096c7df3331a75b77a085b479ede20fb4e170e97c4464d13` |
| `tests/test_v3_smoke.py` | `ab8ece5928b4863889e06852be2862d3b11eb18425a96fd189b2e3fcc6eebd0a` | `24014d7e14b468e05877f334dbae6bd5f5783ff1efc7f398ac33ed8ecf065df1` |

## 4. KN3 校验（diff 结论）

以来源 `d77d36c` 的 tree blob 逐文件（`git cat-file blob`）为基准，对 `code/` 用 `git -c core.autocrlf=false diff --no-index -U0` 逐字节比对：

| 类别 | 文件数 | 结果 |
|---|---|---|
| 未补注文件（与来源逐字节一致） | 43 | SHA-256 全匹配，无任何内容差异 |
| 补注文件（diff 仅新增注释行） | 11 | **+57 / -0**；新增行全部以注释符号开头（`#` 或 `/* */`），无删除、无代码行/字符串/宏/格式改动 |

- **行尾说明**：`code/` 与来源 blob 逐字节一致——源码/配置/md 为 LF 行尾，8 个 `tests/selftest-*.log` 的 blob 本身即含 CRLF（历史日志提交时已带 CR），已按 blob 原样保留，未做归一化改写。
- **结论**：补注前后 diff **只包含以注释符号开头的新增行**，KN3 合规；未触碰 developer 源码、未改已归档 v1/v2。

## 5. 未验证边界（unverified）

板端 X5 基础运行已由 `TESTREPORT-T-20261002-014-001` 实测通过（BQ1~BQ5 全通过）；**仍 `unverified`**：板端 systemd 实装 + WatchdogSec 实际重启、sd_notify 实际投递（临时目录无 NOTIFY_SOCKET）、压力/长时/断电持久化、真实硬件故障接入（真实 SPI/CAN/电压）、1 kHz 硬实时边界、板端 core dump 实际放开（`ulimit -c=0`、`core_pattern=core`）。归档完成不等于发布或整车交付验收。

## 6. 程序性注记

1. **developer 无落盘 HANDOFF**：外部 developer（ChatGPT）经 `logging-v3-final.bundle` 交付 d77d36c 及其 RESULT 说明，无邮箱通道、无落盘 HANDOFF 邮件；本卡不伪造 HANDOFF，如实以 bundle + 审查/测试/验收三件 d77d36c 对齐证据承担"developer 交付"要件（口径同 management `ACCEPT-20261002-logging-v3.md` §1）。
2. 归档件不是审查/测试对象：`code/` 为带注版本，与来源 commit 不完全一致；审查与测试一律以 d77d36c 为准（见 ROLE-LIMIT §4 归档结构说明）。
3. SPEC/WALKTHROUGH/QUESTIONS/DIFF 中的 `file:line` 一律为**来源 commit d77d36c 行号**（带注版因补注行有偏移，换算见 SPEC-001 卷首）。
