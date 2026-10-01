# -*- coding: utf-8 -*-
"""board.py — paramiko 直连 RDK X5 的测试采集工具（本机运行，非语义适配仅传输/执行）。

复用 T-20260927-002 的 board.py 操作包（STM-001），HOST 按任务书 T-20261001-008
使用 Resolve-DnsName 取到的最新地址；提供多地址回退。
"""
import os, sys
import paramiko

# 任务书已知回退地址 + DNS 本轮解析到的两个地址（按顺序尝试）
HOSTS = [
    "2409:893d:5144:3d5c:a87d:a71:6eac:4fa5",   # 任务书已知地址（DNS 首条）
    "2409:893d:5144:3d5c:b8b3:7b8:a711:f382",   # DNS 本轮新解析到的第二条
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
