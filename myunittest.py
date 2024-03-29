'''
@Author: longfengpili
@Date: 2019-07-12 11:05:28
@LastEditTime: 2019-10-11 19:06:02
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import unittest
from parse_bi_data import RepairJsonData
from parse_bi_data import CopyDataOVO, ResolveData
from db_api import DBRedshift
from psetting import *
R_REPAIR_TABLENAME = R_REPAIR_TABLENAME + '_' + M_HOST.split('.')[-1]  # 根据不同的数据库创建不同的表
R_RESOLVE_TABLENAME = R_RESOLVE_TABLENAME + '_' + M_HOST.split('.')[-1]  # 根据不同的数据库创建不同的表
R_AD_REPAIR_TABLENAME = R_AD_REPAIR_TABLENAME + '_' + M_HOST.split('.')[-1]  # 根据不同的数据库创建不同的表
R_AD_RESOLVE_TABLENAME = R_AD_RESOLVE_TABLENAME + '_' + M_HOST.split('.')[-1]  # 根据不同的数据库创建不同的表

class tasktest(unittest.TestCase):

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print(f'tearDown...')

    def test_repair_main(self):
        myjson = '{"dfs":"sdf}'
        rjd = RepairJsonData(myjson)
        myjson = rjd.repair_main()
        # print(rjd.myjson_origin)
        print(myjson)
        print(rjd.errors)

    def test_repair_row(self):
        # myrow = list((1,'﻿{"ts":"15655"","msg_type3":"end_up","isdds":false,"t":"d""}'))
        myrow = list((1, '{"ts":1564727341,"'))
        rdovo = CopyDataOVO('mysql_host', 'mysql_user', 'mysql_password', 'mysql_database', 'redshift_host',
                                        'redshift_user', 'redshift_password', 'redshift_database', 'original_columns')
        id, myjson, errors = rdovo.repair_row(myrow)
        print(id)
        print(myjson)

    def test_resolve_row(self):
        # myrow = list((1,'﻿{"ts":"15655"","msg_type3":"end_up","isdds":false,"t":"d""}'))
        myrow = list((1, '{"ts":1564727341,"error":"err","errr2":"33","b":33}'))
        rd = ResolveData(host=M_HOST, user=M_USER, password=M_PASSWORD, database=M_DATABASE,
                         original_columns=M_ORIGINAL_COLUMNS, resolve_columns=M_RESOLVE_COLUMNS, resolve_index=R_RESOLVE_INDEX,
                         no_resolve_columns=R_NO_RESOLVE_COLUMNS, db_type='mysql')
        row = rd.resolve_row(myrow)
        print(row)

    def test_repair_to_redshift(self):
        rdovo = CopyDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                                          db2_host=R_HOST, db2_user=R_USER, db2_password=R_PASSWORD, db2_database=R_DATABASE,
                                          original_columns=M_ORIGINAL_COLUMNS)
        # rdovo.get_tables_id_real(original_tablename=M_ORIGINAL_TABLENAME,repair_tablename=R_REPAIR_TABLENAME)
        rdovo.copy_game_data_main(original_tablename=M_ORIGINAL_TABLENAME,
                               repair_tablename=R_REPAIR_TABLENAME, id_min=28000)
        rd = ResolveData(host=R_HOST, user=R_USER, password=R_PASSWORD, database=R_DATABASE, 
                         original_columns=M_ORIGINAL_COLUMNS, resolve_columns=R_RESOLVE_COLUMNS, resolve_index=R_RESOLVE_INDEX,
                         no_resolve_columns=R_NO_RESOLVE_COLUMNS, db_type='redshift')
        rd.resolve_data_main(repair_tablename=R_REPAIR_TABLENAME, resolve_tablename=R_RESOLVE_TABLENAME)

    def test_repair_to_mysql(self):
        rdovo = CopyDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                                   original_columns=M_ORIGINAL_COLUMNS)
        # rdovo.get_tables_id_real(original_tablename=M_ORIGINAL_TABLENAME,repair_tablename=R_REPAIR_TABLENAME)
        rdovo.copy_game_data_main(original_tablename=M_ORIGINAL_TABLENAME, repair_tablename=M_REPAIR_TABLENAME, id_min=0, id_max=3000)
        
        rd = ResolveData(host=M_HOST, user=M_USER, password=M_PASSWORD, database=M_DATABASE,
                         original_columns=M_ORIGINAL_COLUMNS, resolve_columns=M_RESOLVE_COLUMNS, resolve_index=R_RESOLVE_INDEX,
                         no_resolve_columns=R_NO_RESOLVE_COLUMNS, db_type='mysql')
        rd.resolve_data_main(repair_tablename=M_REPAIR_TABLENAME, resolve_tablename=M_RESOLVE_TABLENAME, id_min=0, id_max=3000)

    def test_copy_in_mysql(self):
        rdovo = CopyDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                                   original_columns=M_ORIGINAL_COLUMNS)
        rdovo._connect()
        rdovo.copy_data_to_idtable(tablename=M_AD_ORIGINAL_TABLENAME)

    def test_reset_in_mysql(self):
        rdovo = CopyDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                                   original_columns=M_ORIGINAL_COLUMNS)
        rdovo._connect()
        temp1 = None
        for i in range(100):
            rdovo.db.reset_auto_increment_id(tablename=M_AD_ORIGINAL_TABLENAME)
            _, result = rdovo.db.sql_execute(f'select * from {M_AD_ORIGINAL_TABLENAME} limit 100,1;')
            print(i, result)
            if result != temp1:
                print(f'=========={i}============'*5)
            temp1 = result

    def test_create_in_mysql(self):
        rdovo = CopyDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                                   original_columns=M_ORIGINAL_COLUMNS)
        rdovo.copy_data_to_idtable(tablename=M_AD_ORIGINAL_TABLENAME)

    def test_threading(self):
        rdovo = CopyDataOVO(db_host=M_HOST, db_user=M_USER, db_password=M_PASSWORD, db_database=M_DATABASE,
                                   original_columns=M_ORIGINAL_COLUMNS)
        print(rdovo._connect)

    def test_alter_table_columns(self):
        dbr = DBRedshift(host=R_HOST, user=R_USER, password=R_PASSWORD, database=R_DATABASE)
        dbr.alter_table_columns(tablename=R_REPAIR_TABLENAME, columns=R_RESOLVE_COLUMNS)
        # dbr.get_table_columns(tablename=R_REPAIR_TABLENAME)

    def test_resolve_in_redshift(self):
        # repair_tablename = R_AD_REPAIR_TABLENAME
        # resolve_tablename = R_AD_RESOLVE_TABLENAME
        # original_columns = M_AD_ORIGINAL_COLUMNS
        # resolve_columns = R_AD_RESOLVE_COLUMNS
        # no_resolve_columns = R_AD_NO_RESOLVE_COLUMNS
        repair_tablename = R_REPAIR_TABLENAME
        resolve_tablename = R_RESOLVE_TABLENAME
        original_columns = M_ORIGINAL_COLUMNS
        resolve_columns = R_RESOLVE_COLUMNS
        no_resolve_columns = R_NO_RESOLVE_COLUMNS
        rd = ResolveData(host=R_HOST, user=R_USER, password=R_PASSWORD, database=R_DATABASE,
                         original_columns=original_columns, resolve_columns=resolve_columns, resolve_index=R_RESOLVE_INDEX,
                         no_resolve_columns=no_resolve_columns, db_type='redshift')
        rd.resolve_data_main(repair_tablename=repair_tablename, resolve_tablename=resolve_tablename, id_min=0, n=1000)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestSuite()  # 创建测试套件
    suite.addTest(tasktest('test_resolve_in_redshift'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
