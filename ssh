# coding=utf-8

import sys
import os

import logging
import paramiko

import config

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../.."))

logger = logging.getLogger('ssh')


class SshClient(object):
    def __init__(self, host_ip, port, username, id_rsa_path):
        self.root_priv_key = paramiko.RSAKey.from_private_key_file(id_rsa_path)
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=host_ip, port=port, username=username, pkey=self.root_priv_key,
                         timeout=config.DOCKER_SSH_CONNECTION_WAIT)
        self.transport = paramiko.Transport(host_ip, port)
        self.transport.connect(username=username, pkey=self.root_priv_key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def close(self):
        self.ssh.close()
        self.transport.close()

    def exce_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        out = stdout.readlines()
        err = stderr.readlines()
        recv_status = stdout.channel.recv_exit_status()
        return stdin, out, err, recv_status

    def upload_file(self, local_path, server_path):
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        sftp.put(local_path, server_path)

    def download_file(self, remote_path, local_path):
        sftp = paramiko.SFTPClient.from_transport(self.transport)
        sftp.get(remote_path, local_path)


if __name__ == '__main__':
    pass
