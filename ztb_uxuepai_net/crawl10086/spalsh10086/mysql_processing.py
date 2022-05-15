# -*- coding: utf-8 -*-

import pymysql,datetime
import pandas as pd
import numpy as np
from pandas import Series
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import sqlalchemy
from spalsh10086.settings import MYSQLINFO
NowTime = str(datetime.datetime.now()).split(' ')[0].replace('-','')

def pandas_insermysql(itmeList,pageNum,subclass):
    newList = []
    for i in itmeList:
        ddict = {}
        ddict['page_url'] = i['url']
        ddict['subclass'] = subclass
        ddict['issue_time'] = i['time']
        ddict['process_status'] = 0
        ddict['pageNum'] = pageNum
        newList.append(ddict)

    df = pd.DataFrame(newList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    df.to_sql(name='temp10086url', con=mysqlcon, if_exists='append', index=False)
    return '{} 中第 {}页，有{}篇文章链接已经收录'.format(subclass,str(pageNum),str(len(newList)))


if __name__ == "__main__":
    itmeList = [{
        'page_url':'ssss',
        'subclass':'aaa',
        'issue_time':'2017-08-08 11:11:11',
        'process_status':0,
        'pageNum':1
                 }]
    a = pandas_insermysql(itmeList)
    print(a)
    pass
