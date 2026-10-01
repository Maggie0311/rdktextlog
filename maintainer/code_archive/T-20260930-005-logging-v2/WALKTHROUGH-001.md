# WALKTHROUGH-001 — T-20260930-005-logging-v2

一句话：事件从业务适配器进入有界队列，由后台 writer 编码、写入并轮转，随后由导出/读端按来源和 session 复核。

## 1. 接入与生命周期

`rmlog/session.py:1` 负责生成/传播 session；`rmlog/async_writer.py:20` 将事件放入队列，`_worker` 消费并调用 writer。`flush` 依赖 `unfinished_tasks`，`close` 设置停止事件、flush 后 join。

## 2. 编码与写入

`rmlog/format.py:40` 定义 LOGV1 行格式；`encode` 负责转义和字段拼接。`rmlog/writer.py:180` 维护写入状态，`event` 组织序号、级别、错误码与 attrs；Linux 写入后在超限路径经 ROTLOCK 与真实 stat 决定轮转。

## 3. 业务事实

`rmlog/checks.py:1` 把五个业务域的结果映射为事件；`fault_demo.py:20` 提供可运行的五种失败注入。它们记录调用方提供的事实，不能据此推断真实设备状态。

## 4. daemon 与服务

`rmlog/daemon.py:20` 启动持续循环，写入 started/stopping 事件并处理 TERM；`systemd/rmlog-demo.service` 将其作为持续服务并配置失败重启。板端安装行为仍 unverified。

## 5. 证据导出与查询

`export_evidence.py:70` 查找主日志和连续轮转成员，逐源写出并生成 manifest；`rmlog_read.py:35` 逐行解析，`filter --session` 组合 session/时间/级别条件。缺失业务日志时 manifest 保留 MISSING，而非伪造成功。

## 6. 验证入口

`rmlog/selftest.py` 保留原 13 项回归；`tests/test_v2_smoke.py` 覆盖容量、drop、session、五域注入和轮转导出。review/tester 报告均绑定 `3148fed`。
