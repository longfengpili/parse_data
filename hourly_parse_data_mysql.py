'''
@Author: longfengpili
@Date: 2019-07-01 11:59:54
@LastEditTime: 2019-07-03 11:53:30
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
'''

from psetting import *
from db_api import DBMysql
from parse_data import RepairMysqlData, ResolveMysqlData
import sys

import argparse
parser = argparse.ArgumentParser(description='input id_min id_max')
parser.add_argument('-id_min', type=int, default=None)
parser.add_argument('-id_max', type=int, default=None)
args = parser.parse_args()
id_min = args.id_min
id_max = args.id_max

# 创建repair_table
db = DBMysql(host=M_HOST, user=M_USER,password=M_PASSWORD, database=M_DATABASE)
sql = db.sql_for_create(tablename=M_REPAIR_TABLENAME, columns=M_ORIGINAL_COLUMNS)
db.sql_execute(sql)
rpmd = RepairMysqlData(host=M_HOST, user=M_USER,
                      password=M_PASSWORD, database=M_DATABASE, orignal_columns=M_ORIGINAL_COLUMNS)
rpmd.repair_mysql_main(orignal_tablename=M_ORIGINAL_TABLENAME, repair_tablename=M_REPAIR_TABLENAME, id_min=id_min, id_max=id_max)

# 创建resolve_table
db = DBMysql(host=M_HOST, user=M_USER, password=M_PASSWORD, database=M_DATABASE)
sql = db.sql_for_create(tablename= M_RESOLVE_TABLENAME,columns=M_RESOLVE_COLUMNS)
db.sql_execute(sql)
rsmd = ResolveMysqlData(host=M_HOST, user=M_USER,
                       password=M_PASSWORD, database=M_DATABASE, orignal_columns=M_ORIGINAL_COLUMNS, resolve_columns=M_RESOLVE_COLUMNS)
rsmd.resolve_mysql_main(repair_tablename=M_REPAIR_TABLENAME, resolve_tablename=M_RESOLVE_TABLENAME, id_min=id_min, id_max=id_max)