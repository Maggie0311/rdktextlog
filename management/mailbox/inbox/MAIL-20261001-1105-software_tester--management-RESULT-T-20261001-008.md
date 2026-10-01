---
mail_id: MAIL-20261001-1105-software_tester--management-RESULT-T-20261001-008
thread: THREAD-LOG-V2
from: software_tester
to: management
cc: [developer]
date: 2026-10-01 11:05
purpose: RESULT
priority: P1
deadline: 2026-10-01 23:59
requires_reply: false
attachments: []
references:
  - MAIL-20261001-1058-management--software_tester-TASK-T-20261001-008-logging-v2-boardtest
  - software_tester/script/TESTREPORT-T-20261001-008-001.md
  - software_tester/script/ENVIRONMENTS.md
---

## RESULT — T-20261001-008-logging-v2-boardtest

### 被测对象

commit `d2e10812f63de13f39c030889a0d6cb99607135d`（`feature/logging-v2` HEAD，工作树干净）。副本经 `git archive d2e1081 developer/script` 生成，上传到板端 `/tmp/rmlog-v2/`，6 个关键文件 md5 与本地全 MATCH。

### 环境（均实测，标记已验证）

RDK X5 V1.0（aarch64），Ubuntu 22.04.5 LTS，kernel `6.1.83-rt28`，Python 3.10.12，gcc 11.2.0。连接 `2409:893d:5144:3d5c:a87d:a71:6eac:4fa5`（DNS AAAA 首条，paramiko root/root 成功）。全程仅在板端 `/tmp` 下活动，未碰系统配置、未安装包、未改源码。

### 四类测试结果（原始输出全文见报告 §5 与 raw/）

1. **身份与环境核查**：退出码 `0`。hostname=`ubuntu`，model=`D-Robotics RDK X5 V1.0`，`aarch64`，Python 3.10.12，gcc 11.2.0，`/userdata` 存在。
2. **selftest**：退出码 `0`，`自测结束: 13/13 通过`、`SELFTEST PASS`。关键行：`AC4 双端 7 个用例逐字节一致`、`AC5×F-1 …写成功=1200 可见=1200…无半行/无全灭/无缺号`、`RF6 …delta=0 …lines=600/600`。
3. **smoke**：退出码 `0`，`V2 SMOKE PASS accepted=1 dropped=9`。
4. **五域故障注入**（init/comm/hw/fsm/sys 五次）：退出码均 `0`，各生成 `/tmp/rmlog-fault-<kind>/rmlog.log`，注入域以 ERROR 级记录其失败码：`E-INIT-001` / `E-COMM-004` / `E-HW-001` / `E-FSM-003` / `E-SYS-002`。

### 报错 / 异常

无。所有步骤退出码 0，stdout/stderr 无报错。唯一需说明的事实：`cat /proc/device-tree/model` 输出无换行，与下一行 `uname -a` 粘连（板端原始字节如实呈现，非错误）。

### 覆盖声明

本轮为 v2 板端自测事实采集，**未做**压力/长时/断电项、真实硬件故障接入、systemd 安装重启、1 kHz 硬实时、静态审查。本报告只描述观察到的现象，不作发布/验收结论。

### 交付物

- 报告：`software_tester/script/TESTREPORT-T-20261001-008-001.md`
- 原始输出：`software_tester/script/work/T-20261001-008-boardtest/raw/`（`01_identity` `02_upload` `03_selftest` `04_smoke` `05_fault_{init,comm,hw,fsm,sys}` `SUMMARY`）
- 环境清单已更新：`software_tester/script/ENVIRONMENTS.md`

software_tester (R-005)
2026-10-01 11:05
