# ACCEPT-20260927-logging-p0 — T-20260926-001-logging-platform-p0 验收报告

| 字段 | 值 |
|---|---|
| 需求/任务 | REQ-20260926-001-logging §4 P0 / T-20260926-001-logging-platform-p0 |
| 主责角色 | developer（R-003，唯一主责） |
| 被验收版本 | **commit `2d83644`**（R3 终版；全链 R0=`f3331b0` → R1=`45eeb04` → R2=`a675c8d` → R3=`2d83644`） |
| 审查依据 | 审查链四份报告：`REVIEW-…-f3331b0.md`（CONDITIONAL）→ `REVIEW-…-45eeb04.md`（PASS）→ `REVIEW-…-rf-a675c8d.md`（FAIL，拦截 RF-6）→ `REVIEW-…-rf6-2d83644.md`（**PASS，终审，绑定 2d83644**） |
| 三份归档要件核对 | developer 备料通知（HANDOFF MAIL-20260927-1505，hash=2d83644）✓ ｜ 审查终审 PASS（绑定 2d83644）✓ ｜ 本报告（hash=2d83644）✓ —— **三者一致** |
| 验收结论 | **accepted（有条件）** —— 条件与期限见 §3 |
| 验收人 | management (R-002) · 2026-09-27 15:10 |
| 归档许可 | 本报告即归档许可：`maintainer` 可凭三份要件（均指向 2d83644）归档并产出说明书/走读/版本卡 |

## 1. AC 逐条验收（REQ §6，证据=落盘路径）

| AC | 结论 | 证据 |
|---|---|---|
| AC1 组件可运行 | **接受**（开发机侧证实） | selftest 终版 13/13 PASS 留档 `developer/script/tests/selftest-20260927-1352-rf6.log`；code_reviewer 独立复跑 13/13（`_verify…/r5/selftest_r5.log`）；C 端 gcc -Wall -Wextra 零警告（W7）。板端可运行按 Q1=A 由用户实测回贴（§3 条件 1） |
| AC2 行格式 v1 | **接受** | selftest AC2 roundtrip/残行三道闸/fuzz PASS（终版留档+独立复跑）；样例与解析一致性经审查 V3/W6b 复验 |
| AC3 错误码体系 | **接受** | 五域 24 码；单一来源生成（gen_code → rmlog_errors.h/ERR-CATALOG.md）；首轮审查 §4.2 已核"生成物与渲染逻辑逐码一致" |
| AC4 双端一致 | **接受**（声明范围内） | C/Python 同事件输出逐字节一致（AC4 探针，首轮 V1+复审复跑）；范围=无属性行，attrs 属 P1（IMPL §2.5 已声明） |
| AC5 落盘与查询 | **接受（含裁定强化）** | management 裁定 AC5 必须涵盖"多进程×轮转"组合 → R1 修复（轮转协议 v2：每写即开即关+跨进程轮转互斥+锁内 stat）→ 复审独立对账 600/600 精确相等、无半行/全灭/缺号（`REVIEW-…-45eeb04.md` §4）；selftest 组合用例对账强度经 W8 审查成立 |
| AC6 崩溃取证 | **接受** | selftest AC6（os._exit 后 FATAL 可读）PASS；复审 AC6 组合探针 4008/4008；板端持久化边界（fdatasync 语义）列 UV-5 随板端自测 |
| AC7 场下使用方法 | **接受** | USAGE.md §3 板端自测一等章节（含回贴清单）/§5 五分钟定位演示/§6 systemd 样例/§7 journald/dmesg 关联/§8 局限与 P1；首轮审查逐节核过"无未验证写成已验证"表述 |
| AC8 平台核查证据 | **接受（按 Q1=A 形态）** | IMPL §5 未核实项表+板端探测命令齐备；审查确认无"未核实写成已核实"表述；板端回贴为 §3 条件 2 |

## 2. 修复过程与质量记录（归档用）

- 首轮交付 f3331b0（自测 10/10）→ 审查 CONDITIONAL（2 严重 F-1 多进程×轮转数据销毁 / F-2 `--until` 分钟前缀漏事件，+5 一般 +2 提示）；
- management 裁定 AC5 涵盖组合场景 → 结论按报告预设规则升格 FAIL → R1 返工 45eeb04（F-1~F-9 全项）→ 复审 PASS（600/600 对账；新发现 RF-1/RF-4 一般 + RF-2/3/5 提示）；
- RF 微整改 a675c8d → RF 复审 **FAIL**：新引入 RF-6 严重（`rmlog__open_locked` 残留二次 open，1000 轮 close→重开句柄 +1000 实证）——**审查门有效拦截修复引入缺陷**；
- 终轮修复 2d83644（RF-6+MIN-1/2/3，含 selftest 第 13 用例句柄守恒回归闸）→ 终审 PASS（三重口径：结构逐行/语义等价走查/独立句柄对照修复前 +1000 复现→修复后全 0）。
- developer 顺序违规（首轮 RESULT 先于审查请求）已自报并采信自我纠正；worklog 双向留痕。

## 3. 验收条件（accepted 的边界，须明示）

1. **AC1/AC8 板端部分待用户按 `USAGE.md` §3 在 RDK X5 上执行自测并回贴输出**（Q1=A 裁决形态）。回贴输出如与开发机证据矛盾 → 本验收对该矛盾项降级为 rejected 并开新任务修复；**在此之前，本验收对"板端可运行"不作断言**（诚实边界，替代传统验收的实机项）。
2. 已知范围限制（均已文档化，不构成缺陷）：AC4 一致性范围=无属性行（attrs 属 P1）；轮转协议 Linux 行为为推演声明（UV-1，随板端自测）；C 端 mkdir -p 等效/attrs/INFO-3 计数器读取出口列入 P1。
3. **风险接受声明待用户书面确认**：若用户接受"板端验证延后完成"的现状（代码已归档、板端回贴后补证据），请书面（对话即可）确认一句，由 management 登记留痕——按框架 §2.1.2 第 2 条，该书面确认将抄送 framework_admin 备案。

## 4. 后续

- **归档**：maintainer 依三份要件归档 2d83644 并产出 SPEC/WALKTHROUGH/QUESTIONS/DIFF/VERSION + GLOSSARY；
- **板端自测**：用户按 USAGE §3 执行（约 10 分钟），回贴输出 → software_tester 立项核验（新 task_id）→ 证据并入本验收；
- **P1 规划**：systemd 自启/黑匣子/快照包/与节拍线程和 SPI 模块对接（PROJECT-BOARD 里程碑 M2），含 C 端 attrs 与 mkdir -p。
