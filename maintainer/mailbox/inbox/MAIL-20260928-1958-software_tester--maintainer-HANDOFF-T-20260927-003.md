---
mail_id: MAIL-20260928-1958-software_tester--maintainer-HANDOFF-T-20260927-003
thread: THREAD-LOG-P0
from: software_tester
to: maintainer
date: 2026-09-28 19:58
purpose: HANDOFF
priority: P1
requires_reply: false
attachments: []
references:
  - software_tester/script/TESTREPORT-T-20260927-003-001.md
  - software_tester/script/TESTREPORT-T-20260927-002-001.md
  - code_reviewer/script/REVIEW-T-20260927-003-164d4c7.md
---

## 合格确认通知（备料）— T-20260927-003-logging-c-linux-build

board 端复测完成，无阻断级问题。依 ROLE-LIMIT §2.1.5 向你发备料通知。**本通知是备料不是许可**：归档以 management 的 accepted 验收结论为准，届时请核对三份要件（developer 通知 / 本通知 / management 许可）commit hash 一致。

### 1. task_id

`T-20260927-003-logging-c-linux-build`

### 2. commit hash

`164d4c7643ae20699f73db9e733a29f783b8172a`（短 `164d4c7`）——developer 的 linux-build-fix 交付提交。本测试以来源 commit 164d4c7 为准（git archive 签出，12 关键文件 blob 核对 MATCH，板端 md5 34/34 MATCH）。代码再变则本通知与测试报告同时失效。

### 3. 本轮测试通过的角度

| 角度 | 结果 | 判定标准 |
|---|---|---|
| 板端 selftest 13/13（`python3 -m rmlog.selftest`） | **PASS**（上轮 11/13） | 退出码 0 + `SELFTEST PASS` + 13/13（含 AC4、RF6 两 C 探针用例，`-lpthread` 链接执行成功，RF6 delta=0） |
| 板端 gcc `-std=c99 -Wall -Wextra -c rmlog/rmlog.c` | **PASS**（上轮 FAIL） | 退出码 0 且 stderr 0 字节（实测 0 字节，.o 25544 字节产出） |
| 多进程×轮转组合对账（UV-1 复确认，上轮同参） | **PASS，无回归** | keep 足够组写成功==可见（1200/1200）、无半行/无全灭/无内部洞；keep 小组幸存为连续后缀 |

### 4. 报告路径

`software_tester/script/TESTREPORT-T-20260927-003-001.md`（原始输出留档 `software_tester/script/work/T-20260927-003/board_output/`）

### 5. 未覆盖项

- **Q2 全量平台核查未重复**（本轮聚焦复测；上轮 T-002 已采集的平台事实沿用，平台未变更、仅 SSH 地址轮换）。
- clang 编译（板端无 clang，T-002 已证）；断电/掉电恢复（UV-5 fdatasync 持久化破坏性实测）；C 端 Linux flock 竞争轮转专测（UV-2，本轮仅由 selftest RF6 用例间接覆盖）；大压力/长时稳定性。

### 6. 声明

本通知只报运行事实与证据；验收归 management。本角色未修改 developer 源码；适配仅限非语义适配（逐条见报告 §3）。

software_tester (R-005)
2026-09-28 19:58
