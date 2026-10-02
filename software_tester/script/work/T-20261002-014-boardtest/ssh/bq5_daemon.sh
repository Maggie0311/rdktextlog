#!/bin/bash
# bq5_daemon.sh — BQ5 systemd watchdog 代码路径临时目录运行 + SIGTERM 收尾（事实采集）。
# 仅 /tmp 下活动，不装 systemd 服务、不改 /etc。实际 WatchdogSec 重启不做（安全边界外）。

set +e
ROOT=/tmp/rmlog-v3-test
D=$ROOT/bq5-daemon
rm -rf "$D"
mkdir -p "$D"

cd "$ROOT" || exit 9
PYTHONPATH=. python3 -m rmlog.daemon "$D" > "$D/stdout.log" 2> "$D/stderr.log" &
PID=$!
echo "DAEMON_PID=$PID"

sleep 3
echo "--- process alive check (after 3s) ---"
ps -o pid,ppid,stat,etime,cmd -p "$PID" || echo "PROCESS_NOT_FOUND"

echo "--- sending SIGTERM ---"
kill -TERM "$PID"
wait "$PID"
echo "DAEMON_EXIT=$?"

echo "--- daemon stdout ---"
cat "$D/stdout.log" 2>/dev/null
echo "--- daemon stderr ---"
cat "$D/stderr.log" 2>/dev/null

echo "--- files under $D ---"
find "$D" -type f | sort
echo "--- rmlog.log content ---"
cat "$D/rmlog.log" 2>/dev/null || echo "(rmlog.log 不存在)"

echo "BQ5 DONE"
