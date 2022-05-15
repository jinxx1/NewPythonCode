# -*- coding: utf-8 -*-

import pymysql
from config import MYSQLINFO
import datetime
import pprint
import numpy as np
import random
from decimal import Decimal
import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
from numpy.random import random

# a = pd.DataFrame(np.random.randn(5,5),columns=['a','b','c','d','e'],index=['joe','steven','wes','jim','tom'])
#
# # print(a)
# a.ix[2:3,['b','c','d']] = np.nan
# print(a)

# df = pd.DataFrame({'A':[1,2,3,4], 'B':[5,6,7,8], 'C':[1,1,1,1]})
# print(df)


# df['D'] = np.where(df.A<3, 1, 0)  # 如果A＜3，D为1；如果A≥3，D为0
# print(df)
# df.index = pd.date_range('1900/1/30', periods=df.shape[0])
# print(df)

# filepath = r'C:/PthonCode/Python_script/File\1.安徽/6.供应商信息核查申报表（通信工程施工服务）-安徽-安徽鸿宇通信科技有限公司.xlsx'.replace('\\', '/')
# df = pd.read_excel(filepath)
#
# pprint.pprint(df)


def func1(i):
    n = str(i) + '--n'
    yield n

    # llist = []
    # n = str(i) + '--n'
    # llist.append(n)
    #
    # if i%100 == 0:
    #     yield llist
    #     llist=[]
#
# def func2(func):
#     for i in func:
#         print(i)



a = 12.345
q=round(a, 2)
print(q)

