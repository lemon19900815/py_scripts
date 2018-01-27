#coding=utf-8
#!/usr/bin/python

'''
    ssh、sftp辅助函数
'''

import os
import sys  
import traceback
import util

paramiko = util.import_help('paramiko')

# 新ssh连接
def ssh_connect(ssh_conf):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_conf['host'], ssh_conf['port'], ssh_conf['user'], ssh_conf['passwd'])
    return ssh

# 关闭连接
def ssh_disconnect(client):
    client.close()

# windows客户端远程执行linux服务器上命令 
def exec_cmd(ssh_conf, command):
    # 创建连接
    ssh = ssh_connect(ssh_conf)

    stdin, stdout, stderr = ssh.exec_command(command)
    err = stderr.readlines()
    out = stdout.readlines()

    if len(err) > 0:
        [print(i.rstrip('\n')) for i in err]
    else:
        [print(i.rstrip('\n')) for i in out]
        
    # 关闭连接
    ssh_disconnect(ssh)

'''从Linux服务器下载文件到本地

Args:
    linuxpath: 文件在服务器上的路径及名字
    winpath: 文件下载到本地的路径及名字
    只能上传文件，不支持文件夹，而且目标文件夹必须存在
'''
def get_file_from_linux(ssh_conf, linuxpath, winpath):
    client = paramiko.Transport((ssh_conf['host'], ssh_conf['port']))
    client.connect(username=ssh_conf['user'], password=ssh_conf['passwd'])
    sftp = paramiko.SFTPClient.from_transport(client)

    sftp.get(linuxpath, winpath)
    client.close()

'''从windows向linux服务器上传文件

Args:
    winpath: 要上传的文件在本地的路径及位置
    linuxpath: 文件要上传至服务器的路径及名字
    只能上传文件，不支持文件夹，而且目标文件夹必须存在
'''
def put_file_to_linux(ssh_conf, win_path, linux_path):
    client = paramiko.Transport((ssh_conf['host'], ssh_conf['port']))
    client.connect(username=ssh_conf['user'], password=ssh_conf['passwd'])
    sftp = paramiko.SFTPClient.from_transport(client)

    win_path = os.path.abspath(win_path)
    sftp.put(win_path, linux_path)
    client.close()
