'''
@Author: longfengpili
@Date: 2019-07-10 20:15:58
@LastEditTime: 2019-10-16 18:53:32
@github: https://github.com/longfengpili
'''

#!/usr/bin/env python3
#-*- coding:utf-8 -*-


import sys
from daily_work import DailyMainRedshift
from psetting import *
from datetime import datetime, date, timedelta

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')



def set_date(interval_day):
    today = date.today()
    set_date = today + timedelta(days=int(interval_day))
    set_date = set_date.strftime('%Y-%m-%d')
    return set_date

def daily_work_main(date_min, date_max, now, **kw):
    dm = DailyMainRedshift(host=R_HOST, user=R_USER,
                           password=R_PASSWORD, database=R_DATABASE, sqlpath=SQL_PATH)
    dm.daily_execute_all(execute_order=EXECUTE_ORDER, date_min=date_min, date_max=date_max, now=now, **kw)


def daily_work_single_main(file, date_min, date_max, now, **kw):
    dm = DailyMainRedshift(host=R_HOST, user=R_USER,
                           password=R_PASSWORD, database=R_DATABASE, sqlpath=SQL_PATH)
    dm.daily_execute_single(file=file, date_min=date_min, date_max=date_max, now=now, **kw)


params = sys.argv
params = params[1:]

# 格式："\033[字背景颜色；字体颜色m————————\033[0m"   (——————表示字符串)
if not params:
    params = input(f'''every params please add blank !
【PARAM_1】which sqlfile?
    【all】     ：all
    【repair】  ：repair_data
    【raw】     ：raw_data
    【fact】    ：fact_data
    【report】  ：reprot_data
    【funnel】  ：funnel_data
【PARAM_2】from begin days? 
    example:today is 0, yesterday is -1
【PARAM_3】to end days?
    example:today is 0, yesterday is -1
请选择要执行的内容：''')
    params = params.split(' ')

if params and len(params) <= 3 and params[0] == 'all':
    p1, p2, p3 = 'all', '-100', '0'
elif params and len(params) == 3:
    p1, p2, p3 = params
else:
    raise 'please input according to the rule!'

if p1 == 'all':
    daily_work_main(set_date(p2), set_date(p3), now)
elif p1 == 'raw':
    daily_work_single_main('raw_data', set_date(p2), set_date(p3), now)
elif p1 == 'fact':
    daily_work_single_main('fact_data', set_date(p2), set_date(p3), now)
elif p1 == 'report':
    daily_work_single_main('report_data', set_date(p2), set_date(p3), now)
elif p1 == 'funnel':
    daily_work_single_main('funnel_data', set_date(p2), set_date(p3), now)
elif p1 == 'repair':
    daily_work_single_main('repair_data', set_date(p2), set_date(p3), now)
elif p1 == 'mytest':
    daily_work_single_main('mytest', set_date(p2), set_date(p3), now)

