# -*- coding: utf-8 -*-
"""board.py — paramiko 直连 RDK X5 的测试采集工具（本机运行，非语义适配仅传输/执行）。

用法（作为模块被 runner 导入）:
    from board import Board
    b = Board()
    b.run(cmd, timeout=...) -> (exit_status, stdout, stderr)
    b.put(local, remote)
    b.get(remote, local)
"""
import os, sys, io
import paramiko

HOST = "2409:893d:5175:915b:7e04:818a:e96a:69ef"
PORT = 22
USER = "root"
PASSWORD = "root"

class Board:
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        self.client.connect(
            HOST, port=PORT, username=USER, password=PASSWORD,
            timeout=25, look_for_keys=False, allow_agent=False,
            banner_timeout=25, auth_timeout=25)

    def close(self):
        try:
            self.client.close()
        except Exception:
            pass

    def run(self, cmd, timeout=120):
        """执行 shell 命令，返回 (exit_status:int, stdout:str, stderr:str)。"""
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

    def put_dir(self, local_dir, remote_dir):
        """递归上传本地目录到远端（用 tar 打包后一次上传再解包，比逐文件快）。"""
        import tempfile, subprocess, tarfile
        # 本机打包（不含 __pycache__）
        tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_upload.tar")
        with tarfile.open(tmp, "w") as tf:
            tf.add(local_dir, arcname=os.path.basename(remote_dir.rstrip("/")))
        try:
            self.put(tmp, "/tmp/_upload.tar")
            rc, out, err = self.run(
                "mkdir -p %s && tar -xf /tmp/_upload.tar -C %s && rm -f /tmp/_upload.tar && echo UPLOAD_OK"
                % (os.path.dirname(remote_dir.rstrip("/")), os.path.dirname(remote_dir.rstrip("/"))),
                timeout=120)
            if rc != 0 or "UPLOAD_OK" not in out:
                raise RuntimeError("upload extract failed rc=%d out=%r err=%r" % (rc, out, err))
            return out
        finally:
            try:
                os.remove(tmp)
            except Exception:
                pass

    def exec_sudo_script(self, script_text, timeout=120):
        """以 root 执行一段 shell 脚本（本角色即 root 登录，无需 sudo）。"""
        return self.run("bash -s", timeout=timeout), None
