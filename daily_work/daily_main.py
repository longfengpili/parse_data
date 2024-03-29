'''
@Author: longfengpili
@Date: 2019-07-01 14:17:52
@LastEditTime: 2019-09-27 20:55:25
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-


from db_api import DBMysql, DBRedshift
from .parse_sql import ParseSql
import os
from pandas import DataFrame

import logging
from logging import config
config.fileConfig('parselog.conf')
dailylogger = logging.getLogger('daily')

class DailyMain(object):
    '''
    sqlpath:默认sql地址
        '''
    def __init__(self, sqlpath):
        self.sqlpath = sqlpath

    def _connect(self):
        pass

    def daily_execute_all(self, execute_order, **kw):
        '''
        @description: 执行所有的sql文件，按照顺序
        @param {type} 
            execute_order:执行顺序
            kw:sql中需要设定的参数
        @return: 无
        '''
        ps = ParseSql(sqlpath=self.sqlpath)
        self._connect()
        for sql_file in execute_order:
            sql_file = self.sqlpath + sql_file + ".sql"
            sqls = ps.get_file_sqls(sql_file, **kw)
            for sql in sqls:
                dailylogger.info(f'【start】【{sql_file}】【{sql[0]}】begin execute！')
                # dailylogger.debug(sql[1])
                count, result = self.db.sql_execute(sql[1])
                dailylogger.info(f'【end】【{sql_file}】【{sql[0]}】executed！effect 【{count}】 rows！')

    def daily_execute_single(self, file, progress=False, ** kw):
        '''
        @description: 执行所有的sql文件，按照顺序
        @param {type} 
            kw:sql中需要设定的参数
        @return: 无
        '''
        progress = True if file.endswith('test') else progress
        ps = ParseSql(sqlpath=self.sqlpath)
        self._connect()
        sql_file = self.sqlpath + file + ".sql"
        sqls = ps.get_file_sqls(sql_file, **kw)
        for sql in sqls:
            dailylogger.info(f'【start】【{sql_file}】【{sql[0]}】begin execute！')
            count, result = self.db.sql_execute(sql[1], progress=progress)
            # print(f'{DataFrame(result)}')
            dailylogger.info(f'【end】【{sql_file}】【{sql[0]}】executed！effect 【{count}】 rows！')

class DailyMainMysql(DailyMain):
    def __init__(self, host, user, password, database, sqlpath):
        self.db = None
        self.conn = None
        self.host = host
        self.port = 3306
        self.user = user
        self.password = password
        self.database = database
        self.sqlpath = sqlpath

    def _connect(self):
        if not self.db:
            self.db = DBMysql(host=self.host, user=self.user,
                              password=self.password, database=self.database)
        if not self.conn:
            self.conn = self.db._connect()

class DailyMainRedshift(DailyMain):
    def __init__(self, host, user, password, database, sqlpath):
        self.db = None
        self.conn = None
        self.host = host
        self.port = '5439'
        self.user = user
        self.password = password
        self.database = database
        self.sqlpath = sqlpath

    def _connect(self):
        if not self.db:
            self.db = DBRedshift(host=self.host, user=self.user,
                              password=self.password, database=self.database)
        if not self.conn:
            self.conn = self.db._connect()
