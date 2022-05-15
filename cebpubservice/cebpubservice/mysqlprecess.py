# -*- coding: utf-8 -*-
import json,emoji
import pymysql,datetime
import pandas as pd
from cebpubservice.settings import MYSQLINFO
from cebpubservice.scrapyParse import get_timestr
import numpy as np
from pandas import Series
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import sqlalchemy

NowTime = str(datetime.datetime.now()).split(' ')[0].replace('-','')

def pandas_insermysql(itmeList,subclass):
    newList = []
    for i in itmeList:
        ddict = {}
        # print(i['receiveTime'])
        # print(i['bulletinEndTime'])
        try:
            ddict['receiveTime'] = get_timestr(i['receiveTime'],outformat="%Y-%m-%d %H:%M:%S")
        except:
            ddict['receiveTime'] = i['receiveTime'] + " 00:00:00"
        # print(ddict['receiveTime'])
        # try:
        #         #
        #         #     ddict['bulletinEndTime'] = get_timestr(i['bulletinEndTime'],outformat="%Y-%m-%d %H:%M:%S")
        #         # except:
        #         #     ddict['bulletinEndTime'] = None

        ddict['businessObjectName'] = pymysql.escape_string(emoji.demojize(i['businessObjectName']))

        ddict['subclass'] = subclass
        ddict['industriesType'] = i['industriesType']
        ddict['regionName'] = i['regionName']
        ddict['transactionPlatfName'] = i['transactionPlatfName']
        ddict['businessId'] = pymysql.escape_string(emoji.demojize(i['businessId']))
        ddict['schemaVersion'] = i['schemaVersion']
        ddict['tenderProjectCode'] = i['tenderProjectCode']
        ddict['transactionPlatfCode'] = i['transactionPlatfCode']
        ddict['jsondata'] = pymysql.escape_string(json.dumps(i))
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

    df.to_sql(name='nonstandard', con=mysqlcon, if_exists='append', index=False,chunksize=1000)
    return '{} 有{}篇文章链接已经收录'.format(subclass,str(len(newList)))


def allTime():
    from datetime import timedelta, datetime

    subclassList = ['招标公告', '招标项目', '开标记录', '评标公示', '中标公告']
    llist = []
    for subclass in subclassList:
        today = datetime.today()
        while True:
            ddict = {}
            if today.strftime('%Y-%m-%d') == '1990-09-24':
                break
            nextday = today + timedelta(1)

            ddict['today_str'] = today.strftime('%Y-%m-%d')
            ddict['nextday_str'] = nextday.strftime('%Y-%m-%d')
            ddict['status_getpostinfo'] = 0
            ddict['status_crawlinfo'] = 0
            ddict['totalCount'] = 0
            ddict['subclass'] = subclass

            llist.append(ddict)
            today = today - timedelta(1)

    df = pd.DataFrame(llist)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    df.to_sql(name='nonstandard_alltime', con=mysqlcon, if_exists='append', index=False, chunksize=1000)

def getallTime():
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    getallTime = mysqlcon.execute("select * from nonstandard_alltime where status_getpostinfo = 0")
    llist = []
    for i in getallTime:
        ddict = {}
        ddict['id'] = i[0]
        ddict['subclass'] = i[1]
        ddict['starttime'] = datetime.datetime.strftime(i[2],"%Y-%m-%d")
        ddict['endtime'] = datetime.datetime.strftime(i[3],"%Y-%m-%d")
        llist.append(ddict)
    return llist


if __name__ == '__main__':
    getallTime()


