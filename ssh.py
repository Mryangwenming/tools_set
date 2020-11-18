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
   

class DataBaseConnection:
    """
    使用用户名密码连接mysql数据库
    """
    def __init__(self, host, username, passwd, db):
        try:
            self.conn = pymysql.connect(host=host, user=username, password=passwd, database=db)
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        except Exception:
            print('连接失败，请检查数据库配置！')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def query_many(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self, sql):
        self.cursor.execute(sql)

    def exec_many(self, template, args):
        self.cursor.executemany(template, args)

    def commit(self):
        self.conn.commit()


class SshDataBaseConn:
    """
    通过ssh连接docker容器的mysql数据库
    """
    def __init__(self, ssh_host, ssh_username, ssh_passwd, db_user, db_passwd, db):
        try:
            self.server = SSHTunnelForwarder(ssh_address_or_host=(ssh_host, 22),
                                        ssh_username=ssh_username,
                                        ssh_password=ssh_passwd,
                                        remote_bind_address=('localhost', 3306))
            self.server.start()

            self.conn = pymysql.connect(host='127.0.0.1',
                                   port=self.server.local_bind_port,
                                   user=db_user,
                                   password=db_passwd,
                                   database=db)
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        except Exception:
            print('连接失败，请检查数据库配置！')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.commit()
        self.server.close()

    def query_many(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self, sql):
        self.cursor.execute(sql)

    def exec_many(self, template, args):
        self.cursor.executemany(template, args)

    def commit(self):
        self.conn.commit()

if __name__ == '__main__':
    pass
