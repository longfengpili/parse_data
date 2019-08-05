'''
@Author: longfengpili
@Date: 2019-07-12 10:51:48
@LastEditTime: 2019-08-05 10:52:19
@coding: 
#!/usr/bin/env python
# -*- coding:utf-8 -*-
@github: https://github.com/longfengpili
'''

import json
import re

import logging
from logging import config

config.fileConfig('parselog.conf')
repairbi_logger = logging.getLogger('repairbi')

class RepairJsonData(object):
    '''
    修复json数据
    '''
    def __init__(self, myjson, error_max=5, error=None):
        self.myjson_origin = myjson
        self.myjson = myjson
        self.error_num = 0
        self.error_max = error_max
        self.error = error
        self.errors = None

    def repair_for_bomerror(self):
        self.myjson = self.myjson.encode('utf-8')[3:].decode('utf-8')
        try:
            self.myjson = json.loads(self.myjson)
            self.error = None
        except Exception as e:
            self.error = f'>>>>{e}'
            self.errors.append(self.error)
            self.error_num += 1

    def repair_for_innerjson(self):
        self.myjson = self.myjson.replace('":"{"', '":{"').replace('}","', '},"') #去掉json内部json结构双引号
        self.myjson = re.sub('(?<!\:)""', '"', self.myjson) # 去掉多个双引号(前边非冒号)
        try:
            self.myjson = json.loads(self.myjson)
            self.error = None
        except Exception as e:
            self.error = f'>>>>{e}'
            self.errors.append(self.error)
            self.error_num += 1

    def repair_main(self):
        if not self.errors:
            self.errors = []
        try:
            self.myjson = json.loads(self.myjson)
        except Exception as e:
            self.error = f'>>>>{e}'
            self.errors.append(self.error)
            self.error_num += 1
            while self.error:
                if 'UTF-8 BOM' in self.error:
                    self.repair_for_bomerror()
                elif "Expecting ',' delimiter" in self.error:
                    self.repair_for_innerjson()
                else:
                    self.errors.append(self.error)
                    repairbi_logger.error(f'{self.myjson}')
                    repairbi_logger.error(f'{self.error}')
                    self.error_num += 1
                
                if self.error_num >= self.error_max:
                    # error = '\n'.join(self.errors)
                    # repairbi_logger.error(f"{error}")
                    # repairbi_logger.error(f'{str(self.myjson_origin)}')
                    self.error = None
                    myjson = self.myjson_origin.replace('"', "'")
                    self.myjson = {'error': f'{myjson}'}
        self.myjson = json.dumps(self.myjson)
        return self.myjson

