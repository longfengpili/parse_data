
'''
@Author: longfengpili
@Date: 2019-06-19 15:34:00
@LastEditTime: 2019-07-05 18:47:35
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
''' 


import sys
sys.path.append('..')
import mysetting


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
# GOOGLE
CREDENTIALS_JSON_PATH = '../credentials.json'
CREDENTIALS_PICKLE_PATH = '../token.pickle'
#item_info
ITEM_TABLENAME = mysetting.item_table
R_ITEM_TABLENAME = mysetting.r_item_table
ITEM_COLUMNS = mysetting.item_columns
ITEM_SPREADSHEET_ID = mysetting.item_spreadsheet_id
ITME_SHEETNAME = mysetting.item_sheetname
#bi_info
BI_TABLENAME = mysetting.bi_table
R_BI_TABLENAME = mysetting.r_bi_table
BI_COLUMNS = mysetting.bi_columns
BI_SPREADSHEET_ID = mysetting.bi_spreadsheet_id
BI_SHEETNAME = mysetting.bi_sheetname
#funnel_info
FUNNEL_TABLENAME = mysetting.funnel_table
R_FUNNEL_TABLENAME = mysetting.r_funnel_table
FUNNEL_COLUMNS = mysetting.funnel_columns
FUNNEL_SPREADSHEET_ID = mysetting.funnel_spreadsheet_id
FUNNEL_SHEETNAME = mysetting.funnel_sheetname

# Redshift
R_DATABASE = mysetting.redshift_database
R_HOST = mysetting.redshift_host
R_USER = mysetting.redshift_user
R_PASSWORD = mysetting.redshift_password
R_REPAIR_TABLENAME = mysetting.r_repair_table
R_RESOLVE_TABLENAME = mysetting.r_resolve_table
R_RESOLVE_COLUMNS = mysetting.resolve_columns

# Mysql
M_DATABASE = mysetting.mysql_database
M_HOST = mysetting.mysql_host
M_USER = mysetting.mysql_user
M_PASSWORD = mysetting.mysql_password
M_ORIGINAL_TABLENAME = mysetting.original_table
M_ORIGINAL_COLUMNS = mysetting.original_columns
M_REPAIR_TABLENAME = mysetting.repair_table
M_RESOLVE_TABLENAME = mysetting.resolve_table
M_RESOLVE_COLUMNS = mysetting.resolve_columns
# daily
EXECUTE_ORDER = mysetting.execute_order
SQL_PATH = mysetting.sql_path
#messge
MSG_USERS = mysetting.message_users

