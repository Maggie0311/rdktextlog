# ENVIRONMENTS — 可用运行环境与工具链清单

> 所有者: `software_tester` (R-005) · 消费者: `management`（判断测试可行性）、全体
> **状态取值：`已验证` / `假设` / `不可用`。只有「已验证」的手段可以在承诺中使用**（`ROLE-LIMIT` TN4、LTM-007）。

## 1. 本机（工作机）

| 项 | 内容 | 状态 | 验证方式 / 证据 | 最近验证 |
|---|---|---|---|---|
| 操作系统 / 架构 | Windows x64；`python`=3.14.7、`python3`=3.13.14（AMD64） | 已验证 | `python --version` / `python3 --version` | 2026-09-27 |
| C 编译器（gcc/clang/其它） | 本机未验证（无需，板端 gcc 11.2.0 已用） | 假设 | — | — |
| Python 解释器 | 3.13.14 / 3.14.7 | 已验证 | `python3 -c 'import sys;print(sys.version)'` | 2026-09-27 |
| SSH 客户端 | `ssh.exe`（OpenSSH，`C:\Windows\System32\OpenSSH\ssh.exe`）；`paramiko` 5.0.0（直下 wheel 到工作区 `pylib/`，因 pip 受沙箱 `mkdtemp` 限制不可用） | 已验证 | `python3 -c 'import paramiko;print(paramiko.__version__)'` → 5.0.0 | 2026-09-27 |
| 构建工具 | `git archive`（用于签出 commit 副本） | 已验证 | 副本 `git hash-object` 与 commit blob 全 MATCH | 2026-09-27 |
| 测试工作区路径 | `software_tester/script/work/` | 已验证 | 本任务 `T-20260927-002/` 已建 | 2026-09-27 |

## 2. 目标硬件（RDK X5 开发板）

| 项 | 内容 | 状态 | 验证方式 / 证据 | 最近验证 |
|---|---|---|---|---|
| 板卡型号 | D-Robotics RDK X5 V1.0，aarch64 | 已验证 | `dmesg` / `uname -m` | 2026-09-27 |
| 操作系统 | Ubuntu 22.04.5 LTS；kernel `6.1.83-rt28` PREEMPT_RT | 已验证 | `cat /etc/os-release` | 2026-09-27 |
| Python 解释器 | python3 3.10.12（aarch64） | 已验证 | `python3 --version` | 2026-09-27 |
| C 编译器 | gcc 11.2.0（`/usr/bin/gcc`、`cc`）；**clang 不存在** | 已验证 | `which gcc clang` | 2026-09-27 |
| 通信接口 | SSH :22（IPv6 `2409:893d:5175:915b:7e04:818a:e96a:69ef`，root/root 密码认证） | 已验证 | paramiko 连接 + `uname -a` 成功 | 2026-09-27 |
| 存储 | `/userdata` 存在（挂载 `/dev/root` 29G）；journald 持久化目录 `/var/log/journal` 存在 | 已验证 | `ls -ld /userdata` / `ls -ld /var/log/journal` | 2026-09-27 |
| 板端工作目录 | `/root/rmlog_test/`（自建，不触碰系统配置、不 apt 安装） | 已验证 | 本任务上传/运行 | 2026-09-27 |

## 3. 远程计算机

| 项 | 内容 | 状态 | 验证方式 / 证据 | 最近验证 |
|---|---|---|---|---|
| 可达主机 / 连接方式 | RDK X5，IPv6 SSH :22 | 已验证 | paramiko `SSHClient.connect` 成功 | 2026-09-27 |
| 复制程序到远端的方式 | SFTP（paramiko `open_sftp().put` / 目录 tar 打包上传） | 已验证 | 上传后 md5 逐文件 MATCH | 2026-09-27 |
| 在远端执行的方式 | `exec_command` 执行 shell 命令 | 已验证 | Q1–Q4 全部执行 | 2026-09-27 |
| 结果回传方式 | stdout/stderr 捕获 + SFTP 下载日志 tar | 已验证 | `board_output/` 留档 | 2026-09-27 |

## 4. 采集能力（读取运行反馈）

| 反馈类型 | 手段 | 状态 | 说明 |
|---|---|---|---|
| 标准输出 / 退出码 | paramiko `exec_command` + `recv_exit_status` | 已验证 | Q1 selftest 退出码 1 已捕获 |
| 串口日志 | — | 不可用 | 本任务用 SSH，无串口 |
| 文件日志 | SFTP `get` / 板端 `tar` 打包下载 | 已验证 | `q3_logs.tar` 留档 |
| 寄存器 / 内存读数 | — | 不可用 | 需调试器 |
| 时间 / 时序 | 板端 `date`/`dmesg --time-format iso` | 已验证 | ISO 时间戳 `…T21:21:50,017503+08:00` |

## 5. 已知限制（诚实声明）

- 本机 `pip install` 不可用：沙箱拦截 `tempfile.mkdtemp` 目录写入（`Permission denied`），但 PyPI 网络可达——已用 `urllib` 直下 wheel + `zipfile` 解包绕过（paramiko 及依赖）。
- 板端**无 clang**、**无 systemd-coredump/coredumpctl**（`core_pattern=core`）；Q4 clang 侧与 UV-2 崩溃取证侧因此不可测。
- 板端 gcc 11.2.0 下 `rmlog.c` 用 `-std=c99` 编译**失败**（`CLOCK_MONOTONIC` 未声明），详见 `TESTREPORT-T-20260927-002-001.md` §6 Q4。
- 掉电/断电持久化（UV-5）、C 端 Linux flock 轮转路径（UV-2）未实测（见报告 §7 覆盖声明）。

## 6. 变更记录

| 日期 | 变更 | 依据 |
|---|---|---|
| 2026-09-25 | 骨架由 framework_admin 建立；全部条目标「假设」 | `DECISION-20260925-006` |
| 2026-09-27 | 实测回填本机/板端/远程/采集各节为「已验证/不可用」，附证据路径 | TASK `T-20260927-002`（板端 SSH 实测） |
