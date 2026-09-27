# r4 探针汇总 — T-20260926-001 RF 复审（基准 a675c8d，2026-09-27）

> 用途: 本轮复审发现 RF-6 的决定性证据索引；developer 修复后可直接复用本组探针复验（预期值见下）。

## 探针清单（全部为 reviewer 验证件，位于本目录）

| 文件 | 目的 | 本轮结果（a675c8d） |
|---|---|---|
| `probe_rf1_r4.c` | RF-1 功能复验: 显式目录 open → 2 事件 → close×2 → 再 emit 2 事件 → close；对账 rf1_dir | **PASS（语义达成）**: close 后事件 seq=3/4 落回显式目录，rf1_dir/rmlog.log 恰 4 行、单文件 |
| `probe_fdleak_r4.c` | RF-6 定量: 1000 轮 emit→close（每轮走一次 rmlog__open_locked 的 g_path 复用重开），GetProcessHandleCount 前后差 | **delta=+1000（1:1 泄漏）**（base=54 → after=1054） |
| `probe_fdleak2_r4.c` | RF-6 对照实验: 模式 B=常驻 fd 快路径 1000 条 emit（不 close）→ 期望 0；模式 A=500 轮 emit→close → 期望 ≈500 | **B: delta=0；A: delta=+498** —— 隔离变量=是否经 rmlog__open_locked 重开，比例性成立 |
| `probe_degr_r4.c` | RF-5 Windows 运行时验证: 4000 条 ~2.3MB 触发轮转决策路径（rotlock_acquire 恒返 -2），事件应全落盘无异常 | **PASS**: 全部落盘、degr_dir 单文件、退出 0（-2 不计数口径在运行时无副作用） |
| `probe_rf4_r4.py` | RF-4 复验: 锁文件路径被同名目录占位 → 40 条；另正常路径回归 60 条 | **占位: 40/40 落盘、write_failures=0、lock_degradations=40**（修复前 40/0，完全反转）；**正常: 0/0** |
| `selftest_r4.log` | 独立复跑全量 selftest（副本 pkg 内，工作区 own_run_work） | **12/12 PASS，28.2s，退出码 0**（注意: selftest 测不出 RF-6 —— 资源泄漏不在其断言面） |

## RF-6 复验预期（developer 修复后下一轮）

1. `probe_fdleak_r4.exe` → `delta` ≈ 0~2（环境噪声级）；
2. `probe_fdleak2_r4.exe` → 模式 A/B 均 delta ≈ 0；
3. `probe_rf1_r4.exe` → rf1_dir 仍恰 4 行、close 后事件落显式目录（RF-1 语义不得回退）；
4. 全量 selftest 12/12。
5. 修复形态核对: `rmlog__open_locked` 内 open 调用应恰 1 次（尾部），三分支只裁决/复用 g_path。

## 复现命令（reviewer 验证区, Windows + gcc 13.2.0）

```pwsh
cd D:\rdk_x5_software\code_reviewer\script\_verify_T-20260926-001\r4\pkg\developer\script
gcc -std=c99 -Wall -Wextra -Irmlog ..\..\..\probe_rf1_r4.c rmlog\rmlog.c -o ..\..\..\probe_rf1_r4.exe
gcc -std=c99 -Wall -Wextra -Irmlog ..\..\..\probe_fdleak_r4.c rmlog\rmlog.c -o ..\..\..\probe_fdleak_r4.exe
gcc -std=c99 -Wall -Wextra -Irmlog ..\..\..\probe_fdleak2_r4.c rmlog\rmlog.c -o ..\..\..\probe_fdleak2_r4.exe
gcc -std=c99 -Wall -Wextra -Irmlog ..\..\..\probe_degr_r4.c rmlog\rmlog.c -o ..\..\..\probe_degr_r4.exe
cd ..\..\.. ; .\probe_rf1_r4.exe ; .\probe_fdleak_r4.exe ; .\probe_fdleak2_r4.exe ; .\probe_degr_r4.exe
python .\probe_rf4_r4.py
```
