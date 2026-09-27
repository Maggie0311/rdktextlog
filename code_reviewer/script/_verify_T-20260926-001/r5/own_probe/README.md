# r5/own_probe — code_reviewer 终轮复审自建探针留档（基准 2d83644，对照 a675c8d）

> REVIEW-T-20260926-001-rf6-2d83644 §4 W4/W5/W6/W6b 的独立验证件与实测输出。
> developer 留档探针 `developer/script/tests/probe_fdleak_rf6.c` 仅只读引用，未在其目录内构建执行。

## 文件

| 文件 | 说明 |
|---|---|
| `probe_fdleak_r5.c` | RF-6 句柄对照主探针: reopen 组（emit→close 每轮恰走一次 `rmlog__open_locked` 重开）/ fast 组（常驻 fd 对照）/ null 组（`rmlog_open(NULL)` 入口独立定量，落点为库缺省目录故无本目录落盘行） |
| `probe_null_r5.c` | 缺省裁决分支定量探针（配三份宏替换 rmlog.c 副本分别覆盖分支①②③；`R5_NULLRUN` 宏指定落盘检查点） |
| `fdleak_after_run.log` | 修复后（2d83644 副本）实测: 1000/500/600 轮 reopen/fast/null delta 全 0 + 缺省三分支 |
| `fdleak_before_run.log` | 修复前（a675c8d 副本）对照实测: 1000 轮 +1000（1:1）/ 500 轮 +500 / null 组 +1/轮 / 退出码 3 真报警（探针判别力证据） |
| `probe_null_unmodified_run.log` | 未修改库副本在本机（/userdata 不可建）自然复现分支③ ret=-1 delta=0 |
| `selftest_r5.log`（上级目录） | 全量 selftest 13/13 独立复跑（48.1s，退出码 0） |
| `run_*/rmlog.log`、`nullrun/rmlog.log` | 各组落盘自检原始文件（行数=轮数） |

## 再生成（宏替换副本仅存在于本验证区，不触碰被审区）

```powershell
# 副本 A/B/C: 仅替换 rmlog.c 中 RMLOG_DEFAULT_DIR / RMLOG_FALLBACK_DIR 两个宏
#   A(default):  DEFAULT→own_probe/nullrun,  FALLBACK 保持 /var/log/rmlog
#   B(fallback): DEFAULT→Q:/bogus_x5_default, FALLBACK→own_probe/nullrun
#   C(failboth): DEFAULT→Q:/bogus_x5_default2, FALLBACK→Q:/bogus_x5_fallback
gcc -std=c99 -Wall -Wextra -I <rmlog_dir> -o probe_null_r5.exe <variant>.c probe_null_r5.c
gcc -std=c99 -Wall -Wextra -I <rmlog_dir> -o probe_fdleak_r5_after.exe <rmlog_dir>\rmlog.c probe_fdleak_r5.c
.\probe_fdleak_r5_after.exe 1000 run_re_1000 run_fa_1000   # 500/600 同理
.\probe_null_r5.exe default    # B/C 副本对应 fallback/failboth
```

## 实测数据摘要（详见两份 run log）

| 组 | 修复前 a675c8d | 修复后 2d83644 |
|---|---|---|
| reopen 1000/500/600 轮 delta | +1000 / +500 / — | 0 / 0 / 0 |
| fast（对照） | +0 | 0 |
| null 组（N/2 轮 open(NULL)→close） | +500 / +250（1:1） | 0 |
| 缺省分支①单次 open(NULL) | delta=2（1 泄漏+1 常驻） | delta=1（仅常驻） |
| 分支②③ | —（未测） | ②ret=0 delta=1 落回退目录；③ret=-1 delta=0 |
| 落盘自检 | 1000/1000、500/500 | 1000/1000、500/500、600/600 |

口径: Windows `GetProcessHandleCount`（gcc 13.2.0，`-Wall -Wextra` 零告警）。
