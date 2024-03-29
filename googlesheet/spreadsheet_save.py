'''
@Author: longfengpili
@Date: 2019-07-02 11:41:25
@LastEditTime: 2019-10-16 15:06:21
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-



from googlesheet import Spreadsheet
from db_api import DBMysql, DBRedshift
import sys
from psetting import *
import logging
from logging import config

config.fileConfig('parselog.conf')
spreadsheet_logger = logging.getLogger('spreadsheet')


class SaveSpreadSheet(Spreadsheet):
    def __init__(self, host, port, user, password, database, spreadsheet_id):
        self.db = None
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.creds_pickle_path = CREDENTIALS_PICKLE_PATH
        self.creds_json_path = CREDENTIALS_JSON_PATH
        self.scopes = SCOPES
        self.spreadsheet_id = spreadsheet_id

    def _connect(self):
        pass

    def _get_spreadsheet_value(self, sheetname, columns):
        values = self.get_spreadsheet_main(
            self.spreadsheet_id, sheetname=sheetname, columns=columns)
        return values

    def save_values(self, sheetname, tablename, columns):
        spreadsheet_logger.info(f'【{sheetname}】,start load value !')
        values = self._get_spreadsheet_value(sheetname, columns)
        spreadsheet_logger.info(f'【{sheetname}】,end load value !')
        self._connect()
        sql = self.db.sql_for_drop(tablename)
        self.db.sql_execute(sql)
        spreadsheet_logger.info(f'【{self.database}.{tablename}】, dropped !')
        sql = self.db.sql_for_create(
            tablename=tablename, columns=columns)
        self.db.sql_execute(sql)
        spreadsheet_logger.info(f'【{self.database}.{tablename}】, created !')
        sql = self.db.sql_for_insert(
            tablename=tablename, columns=columns, values=values[1:])
        count, result = self.db.sql_execute(sql)
        spreadsheet_logger.info(
            f'【{self.database}.{tablename}】, inserted {count} counts !')


class SaveSpreadSheetToMysql(SaveSpreadSheet):
    def __init__(self, host, user, password, database, spreadsheet_id):
        self.db = None
        self.conn = None
        self.host = host
        self.port = 3306
        self.user = user
        self.password = password
        self.database = database
        self.creds_pickle_path = CREDENTIALS_PICKLE_PATH
        self.creds_json_path = CREDENTIALS_JSON_PATH
        self.scopes = SCOPES
        self.spreadsheet_id = spreadsheet_id

    def _connect(self):
        if not self.db:
            self.db = DBMysql(host=self.host, user=self.user,
                              password=self.password, database=self.database)
        if not self.conn:
            self.conn = self.db._connect()

class SaveSpreadSheetToRedshift(SaveSpreadSheet):
    def __init__(self, host, user, password, database, spreadsheet_id):
        self.db = None
        self.conn = None
        self.host = host
        self.port = '5439'
        self.user = user
        self.password = password
        self.database = database
        self.creds_pickle_path = CREDENTIALS_PICKLE_PATH
        self.creds_json_path = CREDENTIALS_JSON_PATH
        self.scopes = SCOPES
        self.spreadsheet_id = spreadsheet_id

    def _connect(self):
        if not self.db:
            self.db = DBRedshift(host=self.host, user=self.user,
                              password=self.password, database=self.database)
        if not self.conn:
            self.conn = self.db._connect()




