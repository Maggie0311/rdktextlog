# WORKLOG — software_tester (R-005)

> 只追加。格式：#<序号> [YYYY-MM-DD HH:MM] <动作> | <理由> | <结果/证据>

## 2026-09

#1 [2026-09-27 21:53] 执行 T-20260927-002 板端 SSH 实测 | 应答 management TASK（ACK 21:39）| 产出 TESTPLAN/TESTREPORT/ENVIRONMENTS 回填；Q1=11/13(Q4 编译失败致 AC4+RF6 FAIL)、Q2 平台事实、Q3 多进程×轮转 PASS(无静默销毁)、Q4=FAIL(rmlog.c 在 aarch64 gcc11.2 无法 -std=c99 编译，CLOCK_MONOTONIC 未声明+format-truncation×3)；发 RESULT→management、ISSUE→developer(疑似缺陷,unverified)；因阻断级问题未发 HANDOFF；证据留 board_output/

#2 [2026-09-27 21:53] 工作区入库声明 | README"大体积副本是否入库由本角色声明" | work/T-20260927-002/ 下入库：board_output/(原始证据)、ssh/(采集/对账脚本)、_*.py(下载辅助)；不入库：src/(可由 git archive 2d83644 重建,md5 已留档)、pylib//wheels/(第三方 wheel)、tmp/(沙箱 mkdtemp 权限受限残留)，见 .gitignore

#3 [2026-09-28 19:58] 执行 T-20260927-003 板端聚焦复测（linux-build-fix） | 应答 management 复测指令（聚焦 2+1 问，不重复全量）| 被测 164d4c7（git archive 签出,12 文件 blob MATCH,板端 md5 34/34 MATCH）；R-Q1 selftest 13/13 PASS(退出码 0,AC4+RF6 转绿,RF6 delta=0)；R-Q4 gcc -std=c99 -Wall -Wextra 退出码 0 且 stderr 0 字节(上轮 1/2854B)；R-Q3 同参对账三组全 OK 无回归；UV-T003-1/2 实测坐实；发 HANDOFF→maintainer、RESULT→management(抄 developer+code_reviewer)、抄送件→developer；更新 ENVIRONMENTS/INDEX/STM-001；证据留 work/T-20260927-003/board_output/

#4 [2026-10-01 11:05] 执行 T-20261001-008 v2 板端自测+五域故障注入 | 应答 management TASK（ACK 11:01，v2 原 tester 无 SSH 通道，本角色补真机实测）| 被测 d2e1081（feature/logging-v2 HEAD，git archive 签出 45 文件,板端 6 关键文件 md5 全 MATCH）；五步全退出码 0：①身份核查(aarch64/Ubuntu22.04.5/Python3.10.12/gcc11.2.0)②上传③selftest 13/13 PASS④smoke V2 SMOKE PASS accepted=1 dropped=9⑤五域故障注入 init/comm/hw/fsm/sys 各出 E-INIT-001/E-COMM-004/E-HW-001/E-FSM-003/E-SYS-002；无报错；覆盖声明=未做压力/长时/断电/真实硬件；发 RESULT→management(抄 developer)；更新 ENVIRONMENTS(T-008 新地址)；证据留 work/T-20261001-008-boardtest/raw/
