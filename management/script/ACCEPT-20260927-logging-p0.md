# ACCEPT-20260927-logging-p0 — T-20260926-001-logging-platform-p0 验收报告

> **【v3 追记 2026-09-29】** 用户审查意见（USAGE 视角错位、板端自测章节过时）经 T-20260928-004 整改完毕：USAGE 重构为用户优先六主题手册 + 过时章节删除（commit **`08f6ce8`**，代码零变更）；复审 PASS 零发现项（`REVIEW-T-20260928-004-08f6ce8.md`，含 reviewer 独立实跑抽查）。**验收结论扩展：accepted（版本 002 = 08f6ce8，增量归档）**；归档许可相应更新——maintainer 以增量方式归档版本 002（USAGE.md + IMPL §9 + 双指纹增补），版本 001 归档件继续冻结不动。

> **【v2 追记 2026-09-28】** 板端条件已满足：T-002 实测发现 C 端目标平台编译失败 → T-003 修复（commit **`164d4c7`**，复审 PASS）→ **T-003 板端聚焦复测全绿**（R-Q1 selftest **13/13 全 PASS**、R-Q4 `gcc -std=c99 -Wall -Wextra` **stderr 0 字节**、R-Q3 多进程×轮转无回归；`TESTREPORT-T-20260927-003-001.md`）。§3 条件 1 **已满足**，验收结论升格为 **accepted（无条件遗留项见 §3.2）**；归档版本由 2d83644 更新为 **164d4c7**（三份要件：developer 侧 HANDOFF 链 + reviewer 终审（2d83644）与 T-003 复审 PASS（164d4c7）+ tester HANDOFF（164d4c7）+ 本报告）。

| 字段 | 值 |
|---|---|
| 需求/任务 | REQ-20260926-001-logging §4 P0 / T-20260926-001-logging-platform-p0 |
| 主责角色 | developer（R-003，唯一主责） |
| 被验收版本 | **commit `164d4c7`**（R4 终版 = R3 `2d83644` + T-003 linux-build-fix；全链 R0=`f3331b0` → R1=`45eeb04` → R2=`a675c8d` → R3=`2d83644` → R4=`164d4c7`） |
| 审查依据 | 审查链五份报告：`REVIEW-…-f3331b0.md`（CONDITIONAL）→ `REVIEW-…-45eeb04.md`（PASS）→ `REVIEW-…-rf-a675c8d.md`（FAIL，拦截 RF-6）→ `REVIEW-…-rf6-2d83644.md`（PASS）→ `REVIEW-T-20260927-003-164d4c7.md`（**PASS，绑定 164d4c7**） |
| 板端证据 | `TESTREPORT-T-20260927-002-001.md`（首测，发现 C 构建缺陷）+ `TESTREPORT-T-20260927-003-001.md`（**复测全绿**：13/13 / gcc stderr 0 / 无回归） |
| 验收结论 | **accepted**（v1 为"有条件"；v2 板端条件满足，遗留项见 §3.2） |
| 验收人 | management (R-002) · v1 2026-09-27 15:10 · v2 2026-09-28 |
| 归档许可 | **指向 `164d4c7`**：maintainer 凭 developer+tester 两份 HANDOFF 与本报告归档，产出说明书/走读/版本卡 |

## 1. AC 逐条验收（REQ §6，证据=落盘路径）

| AC | 结论 | 证据 |
|---|---|---|
| AC1 组件可运行 | **接受（开发机 + 板端双证实）** | 开发机：selftest 13/13（`tests/selftest-20260927-2208-r4.log` + reviewer 独立复跑 r6）；板端：**13/13 全 PASS**（`TESTREPORT-T-20260927-003-001.md` R-Q1）；C 端 gcc 零警告双端复验 |
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
- 【v2】板端首测（T-002，Q1=A→B 修订后由 software_tester SSH 实测）发现 C 端目标平台编译失败（Q4 FAIL/Q1 11/13）→ T-003 修复 164d4c7（复审 PASS）→ 板端聚焦复测（TESTREPORT-T-20260927-003-001）**全绿**：R-Q1 13/13、R-Q4 gcc stderr 0 字节、R-Q3 无回归——**审查链测不到的目标平台空白由真机实测补齐**，该协作模式（静态审查 + 真机实测互补）首次完整跑通。

## 3. 验收条件（v2 状态）

1. ~~AC1/AC8 板端部分待用户自测回贴~~ → **已满足**：Q1 裁决修订（A→B，MAIL-20260927-1525）后由 software_tester SSH 实测出具；AC8 平台核查已采集（TESTREPORT-T-20260927-002-001 Q2：python3 3.10.12、/userdata 存在、journald 持久化、rsyslog active、coredumpctl 不可用、dmesg ISO 可用）；
2. **遗留项（不阻断验收，已排程）**：AC4 一致性范围=无属性行（C 端 attrs 属 P1）；C 端 mkdir -p 等效、INFO-3 计数器读取出口属 P1；clang 编译（板端无 clang，未测）；掉电/断电持久化实测（UV-5）与 C 端 flock 竞争轮转专测（UV-2，selftest RF6 用例间接覆盖）列入 P1 板端项；**coredumpctl 板端不可用** → P1 崩溃取证需换方案（如自写 core 收集或内核日志捕获）；
3. ~~风险接受声明~~ → 不再需要（板端证据已补齐，v1 的该条款随之关闭）。

## 4. 后续

- **归档（已解冻）**：maintainer 归档 **164d4c7** 并产出 SPEC/WALKTHROUGH/QUESTIONS/DIFF/VERSION + GLOSSARY（三份要件齐备：developer HANDOFF 链 / reviewer 终审 PASS / tester HANDOFF / 本报告 v2）；
- **P1 规划（里程碑 M2）**：systemd 自启/黑匣子/快照包/与节拍线程和 SPI 模块对接，含 C 端 attrs 与 mkdir -p、UV-2/UV-5 板端项、coredumpctl 替代方案。
