# -*- coding: utf-8 -*-
"""board.py — paramiko 直连 RDK X5 的测试采集工具（本机运行，非语义适配仅传输/执行）。

复用 T-20260927-002 的 board.py 操作包（STM-001）。HOST 按任务书 T-20261002-014
使用 Resolve-DnsName 取到的最新地址（2026-10-02 实测两条 AAAA），提供多地址回退。
"""
import paramiko

# 任务书已知回退地址 + 本轮 DNS 解析到的两个 AAAA 地址（按顺序尝试）
HOSTS = [
    "2409:893d:5126:4ac:fd6a:39a3:6650:3cc8",   # 任务书已知地址（DNS 首条，与任务书一致）
    "2409:893d:5126:4ac:c752:f7e7:a59:ce79",    # DNS 本轮新解析到的第二条
]
PORT = 22
USER = "root"
PASSWORD = "root"


class Board:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.host = None

    def connect(self):
        last_err = None
        for host in HOSTS:
            try:
                self.client.connect(
                    host, port=PORT, username=USER, password=PASSWORD,
                    timeout=25, look_for_keys=False, allow_agent=False,
                    banner_timeout=25, auth_timeout=25)
                self.host = host
                return host
            except Exception as e:  # noqa: BLE001
                last_err = "%s: %r" % (host, e)
        raise RuntimeError("all hosts failed: %s" % last_err)

    def close(self):
        try:
            self.client.close()
        except Exception:  # noqa: BLE001
            pass

    def run(self, cmd, timeout=120):
        stdin, stdout, stderr = self.client.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode("utf-8", "replace")
        err = stderr.read().decode("utf-8", "replace")
        rc = stdout.channel.recv_exit_status()
        return rc, out, err

    def put(self, local, remote):
        sftp = self.client.open_sftp()
        try:
            sftp.put(local, remote)
        finally:
            sftp.close()

    def get(self, remote, local):
        sftp = self.client.open_sftp()
        try:
            sftp.get(remote, local)
        finally:
            sftp.close()
