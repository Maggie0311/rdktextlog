# verify-T-20260930-005-3148fed — T-005 logging-v2 静态审查验证区

> 基准 commit：`3148fedec9f39dbf95184cdfd72ffb8bd605e892`。本区为 code_reviewer 独立验证证据，
> 全部验证在**自有副本**进行（`developer/script/**` 全程只读）。代码副本 `rmlog/`、`tests/`、
> `export_evidence.py`、`rmlog_read.py`、`_selftest_work/` 及 `__pycache__` 等为工作区临时产物，**不入库**。

## 留档清单（入库）

| 文件 | 内容 |
|---|---|
| `selftest-3148fed.log` | `python -m rmlog.selftest` 独立复跑：**13/13 PASS，exit 0**（22.8s） |
| `smoke-3148fed.log` | `python tests/test_v2_smoke.py`：**FAIL，exit 1**——`:21` FileNotFoundError: rmlog.log |
| `probe_smoke_race.py` + `.log` | 40 轮竞态探针：40/40 确定性 PermissionError(13)，close 返回 True、线程已 join、worker_fail=0 |
| `probe_perm_boundary.py` + `.log` | 权限边界：临时区 mkfile→PermissionError(13)/嵌套 mkdir→PermissionError(5)，工作区 OK |
| `probe_loc_thread.py` + `.log` | 判别变量 = 目录来源（tempfile.mkdtemp）而非线程身份 |
| `probe_positive_control.py` + `.log` | 正向对照：mkdtemp 10/10 FAIL vs os.makedirs 10/10 PASS（代码与测试逻辑正确） |
| `probe_full_smoke.py` + `.log` | mkdtemp→makedirs 补丁后全 smoke 主体 PASS（V2 SMOKE PASS accepted=1 dropped=9） |

## 结论摘要

- smoke 失败根因 = **DSH 沙箱（workspace-write）阻断 `tempfile.mkdtemp()` 目录内 `os.open(O_CREAT)`**（PermissionError 13/5）。
- **非竞态、非耐用性缺陷、非测试缺陷**：`AsyncWriter.close()` 正确 join + 排空（实证）；`Writer` 静默降级 + 计数（write_failures/lock_degradations）按 F-5/F-7 契约工作。
- 板端（T-008）/容器（T-007）Linux 均 PASS 与此一致（其临时目录写入未被阻断）。

## 复现命令（在自有副本内）

```powershell
cd code_reviewer/script/verify-T-20260930-005-3148fed
python -m rmlog.selftest          # 需代码副本 rmlog/（未入库，可自 developer/script 复制）
python tests/test_v2_smoke.py     # 复现 smoke FAIL
python probe_smoke_race.py 40     # 竞态探针
python probe_perm_boundary.py     # 权限边界
python probe_loc_thread.py        # 线程/目录判别
python probe_positive_control.py  # 正向对照
python probe_full_smoke.py        # 全 smoke 主体正向对照
```

> 代码副本 `rmlog/` 与 `developer/script/rmlog` 的 17 个被审文件 SHA256 逐文件 MATCH（审查时核对）。
