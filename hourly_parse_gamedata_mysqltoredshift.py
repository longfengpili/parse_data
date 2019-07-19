'''
@Author: longfengpili
@Date: 2019-07-01 11:59:54
@LastEditTime: 2019-07-18 11:57:16
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
'''

from psetting import *
from db_api import DBMysql, DBRedshift
from parse_bi_data import RepairMysqlDataOVO, ResolveData
import sys
from sendmessage import sent_message_tousers
from datetime import datetime

import argparse
parser = argparse.ArgumentParser(description='input id_min id_max')
parser.add_argument('-id_min', type=int, default=None)
parser.add_argument('-id_max', type=int, default=None)
args = parser.parse_args()
id_min = args.id_min
id_max = args.id_max


R_REPAIR_TABLENAME = R_REPAIR_TABLENAME + '_' + M_HOST.split('.')[-1]  # 根据不同的数据库创建不同的表
R_RESOLVE_TABLENAME = R_RESOLVE_TABLENAME + '_' + M_HOST.split('.')[-1]  # 根据不同的数据库创建不同的表


rmdovo = RepairMysqlDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                            db2_host=R_HOST, db2_user=R_USER, db2_password=R_PASSWORD, db2_database=R_DATABASE,
                            orignal_columns=M_ORIGINAL_COLUMNS)
rmdovo.repair_data_main(orignal_tablename=M_ORIGINAL_TABLENAME,repair_tablename=R_REPAIR_TABLENAME, id_min=id_min, id_max=id_max)

if rmdovo.count > 0:
    rd = ResolveData(host=R_HOST, user=R_USER, password=R_PASSWORD, database=R_DATABASE, 
                    orignal_columns=M_ORIGINAL_COLUMNS, resolve_columns=R_RESOLVE_COLUMNS, db_type='redshift')
    rd.resolve_data_main(repair_tablename=R_REPAIR_TABLENAME, resolve_tablename=R_RESOLVE_TABLENAME, id_min=id_min, id_max=id_max)
                        