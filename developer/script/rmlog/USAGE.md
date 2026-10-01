# rmlog v2 使用要点

## 会话

启动时创建 `Session("match")`，把 `session.wrap(writer)` 传给检测/业务适配器，或将同一对象传给 `AsyncWriter(..., session=session)`。事件会保留 `session=<id>` 与 `pid=<pid>` 属性。查询：

```sh
python3 developer/script/rmlog_read.py filter rmlog.log --session <id>
python3 developer/script/export_evidence.py rmlog.log evidence --session <id>
```

旧日志没有 session 属性，不能按 session 查询；请按文件、时间、错误码查询。

## 故障与队列边界

`checks.emit_check` 需要业务提供 init/comm/hw/fsm/sys 的事实；库不读取 SPI、CAN 或电机状态。异步队列满时 `dropped` 增加，调用方应将计数接入健康监控。该实现提供非阻塞入队便利，不提供硬实时或零丢失承诺。

## 证据与平台边界

导出先处理业务日志，再尝试 journal、dmesg 和版本命令；权限不足或命令缺失会写入 `MANIFEST.txt`。systemd 模板 `systemd/rmlog-demo.service` 的路径、用户和 `/userdata/rmlog` 权限必须在 X5 上确认。当前开发机测试结果不代表板端已验证。
