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
from cicCrawl.settings import MYSQLINFO
# from settings import MYSQLINFO

NowTime = str(datetime.datetime.now()).split(' ')[0].replace('-','')
conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
                                                                                               'DBNAME'])
mysqlcon = sqlalchemy.create_engine(conStr)


def from_mysql_get_type():
    exc_jou_programa = "select name,dictionaries from jou_programa"
    exc_jou_subtopic = "select name,dictionaries from jou_subtopic"
    ddict = {}
    ddict['programa'] = []
    ddict['subtopic'] = []
    for i in mysqlcon.execute(exc_jou_programa):
        nDict = {}
        nDict['name'] = i[0]
        nDict['value'] = i[1]
        ddict['programa'].append(nDict)

    for i in mysqlcon.execute(exc_jou_subtopic):
        nDict = {}
        nDict['name'] = i[0]
        nDict['value'] = i[1]
        ddict['subtopic'].append(nDict)
    return ddict

def get_type(llist):
    mysql_type = from_mysql_get_type()

    for num,xx in enumerate(llist):
        for i in mysql_type['programa']:
            if llist[num]['programa_dictionaries'] == i['name']:
                llist[num]['programa_dictionaries'] = int(i['value'])
                break


        for i in mysql_type['subtopic']:
            if llist[num]['subtopic_dictionaries'] == '0':
                break
            if llist[num]['subtopic_dictionaries'] != 0 and llist[num]['subtopic_dictionaries'] == i['name']:
                llist[num]['subtopic_dictionaries'] = int(i['value'])
                break
    return llist

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
    df.to_sql(name='temp10086url', con=mysqlcon, if_exists='append', index=False)
    return '{} 中第 {}页，有{}篇文章链接已经收录'.format(subclass,str(pageNum),str(len(newList)))

def get_dupurl(source):
    sqlexc = '''select url from jou_journalism where source = "{}"'''.format(source)
    gettouple = mysqlcon.execute(sqlexc)
    llist = [x[0] for x in gettouple]
    return llist

if __name__ == "__main__":
    print(get_dupurl('中国通信学会'))



    exit()

    word = '''http://www.china-cic.cn/list/60/24/{}/	学会新闻	学会新闻
http://www.china-cic.cn/list/63/24/{}/	学会新闻	地方动态
http://www.china-cic.cn/list/61/24/{}/	学会新闻	委员会动态
http://www.china-cic.cn/list/65/13/{}/	学会新闻	委员会动态
http://www.china-cic.cn/list/67/24/{}/	通知公告	0
http://www.china-cic.cn/list/69/25/{}/	通知公告	0
http://www.china-cic.cn/list/62/24/{}/	会议活动	0
http://www.china-cic.cn/list/64/13/{}/	会议活动	0
http://www.china-cic.cn/list/66/13/{}/	会议活动	0'''.split('\n')
    llist = []

    for i in word:
        ddict ={}
        a = i.split('\t')
        ddict['url'] = a[0]
        ddict['programa_dictionaries'] = a[1]
        ddict['subtopic_dictionaries'] = a[2]
        llist.append(ddict)
    # import pprint
    # pprint.pp(llist)
    print(llist)
    print('------------')

    print(get_type(llist))

