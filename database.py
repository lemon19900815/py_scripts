#!/usr/bin/python
#coding=utf-8

"""
工具类
"""
import shutil
import os,sys
import traceback
import json
import util

pymysql = util.import_help('pymysql')
import pymysql.cursors

# 创建db连接
def create_connection(conf):
    connection = pymysql.connect(host=conf["host"],
         user=conf["user"], password=conf["password"], db=conf["database"], charset='utf8')
    return connection

# 执行sql
def execute_sql(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)

    conn.commit()
    cursor.close()

# 刷新表数据
def refresh_all_table(remote_info):
    conn = create_connection(remote_info)
    sql_ops = ['delete', 'insert', 'update']

    for op in sql_ops:
        sql_dir = os.path.join(os.curdir, '..', 'sql')
        sql_op_dir = os.path.join(sql_dir, op)
        if not os.path.exists(sql_op_dir):
            continue
        sql_files = os.listdir(sql_op_dir)
        for filename in sql_files:
            file = open(os.path.join(sql_op_dir, filename), 'rb')
            execute_sql(conn, file.read())
