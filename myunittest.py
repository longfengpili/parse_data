'''
@Author: longfengpili
@Date: 2019-07-12 11:05:28
@LastEditTime: 2019-07-16 18:49:54
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
'''

import unittest
from parse_bi_data import RepairJsonData
from parse_bi_data import RepairMysqlDataOVO, ResolveData
from psetting import *
R_REPAIR_TABLENAME = R_REPAIR_TABLENAME + '_' + M_HOST.split('.')[-1]  # 根据不同的数据库创建不同的表
R_RESOLVE_TABLENAME = R_RESOLVE_TABLENAME + '_' + M_HOST.split('.')[-1]  # 根据不同的数据库创建不同的表

class tasktest(unittest.TestCase):

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print(f'tearDown...')

    def test_repair_main(self):
        myjson = ''
        rjd = RepairJsonData(myjson)
        myjson = rjd.repair_main()
        # print(rjd.myjson_origin)
        print(myjson)
        print(rjd.errors)

    def test_repair_row(self):
        # myrow = list((1,'﻿{"ts":"15655"","msg_type3":"end_up","isdds":false,"t":"d""}'))
        myrow = list((1,'{"ts":"15655"","msg_type3":"end_up","isdds":false,"t":"d""}'))
        rdovo = RepairMysqlDataOVO('mysql_host', 'mysql_user', 'mysql_password', 'mysql_database', 'redshift_host',
                                        'redshift_user', 'redshift_password', 'redshift_database', 'orignal_columns')
        id, myjson, errors = rdovo.repair_row(myrow)
        # print(rjd.myjson_origin)
        # print(id)
        # print(myjson)
        # print(errors)

    def test_repair_to_redshift(self):
        rdovo = RepairMysqlDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                                          db2_host=R_HOST, db2_user=R_USER, db2_password=R_PASSWORD, db2_database=R_DATABASE,
                                          orignal_columns=M_ORIGINAL_COLUMNS)
        # rdovo.get_tables_id_real(orignal_tablename=M_ORIGINAL_TABLENAME,repair_tablename=R_REPAIR_TABLENAME)
        rdovo.repair_data_main(orignal_tablename=M_ORIGINAL_TABLENAME,
                               repair_tablename=R_REPAIR_TABLENAME, id_min=28000)
        rd = ResolveData(host=R_HOST, user=R_USER, password=R_PASSWORD, database=R_DATABASE, 
                    orignal_columns=M_ORIGINAL_COLUMNS, resolve_columns=R_RESOLVE_COLUMNS, db_type='redshift')
        rd.resolve_data_main(repair_tablename=R_REPAIR_TABLENAME, resolve_tablename=R_RESOLVE_TABLENAME)

    def test_repair_to_mysql(self):
        rdovo = RepairMysqlDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                                   orignal_columns=M_ORIGINAL_COLUMNS)
        # rdovo.get_tables_id_real(orignal_tablename=M_ORIGINAL_TABLENAME,repair_tablename=R_REPAIR_TABLENAME)
        rdovo.repair_data_main(orignal_tablename=M_ORIGINAL_TABLENAME, repair_tablename=M_REPAIR_TABLENAME, id_min=0, id_max=3000)
        
        rd = ResolveData(host=M_HOST, user=M_USER, password=M_PASSWORD, database=M_DATABASE,
                         orignal_columns=M_ORIGINAL_COLUMNS, resolve_columns=M_RESOLVE_COLUMNS, db_type='mysql')
        rd.resolve_data_main(repair_tablename=M_REPAIR_TABLENAME, resolve_tablename=M_RESOLVE_TABLENAME, id_min=0, id_max=3000)

    def test_create_in_mysql(self):
        rdovo = RepairMysqlDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                                   orignal_columns=M_ORIGINAL_COLUMNS)
        # rdovo.get_tables_id_real(orignal_tablename=M_ORIGINAL_TABLENAME,repair_tablename=R_REPAIR_TABLENAME)
        rdovo.copy_data_to_idtable(tablename=M_AD_ORIGINAL_TABLENAME)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()  # 创建测试套件
    suite.addTest(tasktest('test_create_in_mysql'))
    runner = unittest.TextTestRunner()
    runner.run(suite)