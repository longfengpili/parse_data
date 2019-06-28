'''
@Author: longfengpili
@Date: 2019-06-20 12:37:41
@LastEditTime: 2019-06-28 10:29:01
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
'''
from datetime import date, timedelta, datetime
import re
import sys

import pandas as pd
from pandas import DataFrame
import logging
import logging.handlers

#1.创建logger
dblogger = logging.getLogger(name='db')
dblogger.setLevel(logging.INFO)
#2.创建handler写入日志
logfile = './log/db.log'
fh = logging.handlers.TimedRotatingFileHandler(
    logfile, when='D', interval=1, backupCount=100, encoding='utf-8')
fh.setLevel(logging.ERROR)
#3.创建handler输出控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
#4.创建格式
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d行 - %(message)s"
formatter = logging.Formatter(fmt=LOG_FORMAT)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
#5.将handler加入到logger
dblogger.addHandler(fh)
dblogger.addHandler(ch)


class DBBase(object):
    def __init__(self, host=None, port=None, user=None, password=None, database=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
    
    def connect(self):
        pass

    def __close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def __check_sql_type(self, sql):
        result = re.match('(\D.*?) ', sql)
        return result.group(1)

    def sql_execute(self, sql, count=None):
        # print(sql)
        if not self.conn:
            self.connect()
        sql_type = self.__check_sql_type(sql)
        result = f'{sql_type} completed !'

        cursor = self.conn.cursor()
        if sql_type == 'select':
            if count:
                cursor.execute(sql)
                result = cursor.fetchmany(count)
            else:
                cursor.execute(sql)
                result = cursor.fetchall()
        else:
            try:
                cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                dblogger.error(sql)
                dblogger.error(e)

        self.__close()
        return result

    def sql_for_create(self, tablename, columns):
        if not isinstance(columns, dict):
            raise 'colums must be a dict ! example:{"column_name":"column_type"}'
        sql = f'''create table if not exists {tablename}
                    ({','.join([k.lower() + ' '+ v for k, v in columns.items()])});'''

        sql = re.sub('\s{2,}', '\n', sql)
        return sql

    def sql_for_drop(self, tablename):
        sql = f'drop table if exists {tablename};'
        return sql

    def sql_for_insert(self, tablename, columns, values):
        columns = ','.join(columns)
        values = ',\n'.join(
            ['(' + ','.join([f"'{i}'" for i in value]) + ')' for value in values])
        sql = f'''insert into {tablename}
                 ({columns})
                 values
                 {values};'''
        return sql

    def sql_for_select(self, tablename, columns, contions=None):
        columns = ','.join(columns)
        if contions:
            sql = f'''select {columns} from {tablename} {contions};'''
        else:
            sql = f'''select {columns} from {tablename};'''
        return sql