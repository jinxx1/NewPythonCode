# -*- coding: utf-8 -*-

import pymysql,datetime
import pandas as pd
import numpy as np
from pandas import Series
import pprint
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import sqlalchemy
from getmysqlInfo import jsonInfo
NowTime = str(datetime.datetime.now()).split(' ')[0].replace('-','')
from getmysqlInfo import jsonInfo
MYSQLINFO = jsonInfo['uxuepai_sql']
conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME='jxtest')
mysqlcon = sqlalchemy.create_engine(conStr)

def pandas_insermysql(itmeList,subclass,process_stauts=0):
    from getmysqlInfo import jsonInfo
    MYSQLINFO = jsonInfo['uxuepai_sql']
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME='jxtest')
    mysqlcon = sqlalchemy.create_engine(conStr)
    newList = []
    for i in itmeList:
        ddict = {}
        ddict['page_url'] = i['url']
        ddict['subclass'] = subclass
        ddict['issue_time'] = i['time']

        newList.append(ddict)
    df = pd.DataFrame(newList)
    df.to_sql(name='listform10086', con=mysqlcon, if_exists='append', index=False)
    print('共{}篇链接录入到监控库里'.format(len(newList)))


def pandas_insermysql_copy(itmeList,subclass):
    newList = []
    for i in itmeList:
        ddict = {}
        ddict['page_url'] = i['url']
        ddict['subclass'] = subclass
        ddict['issue_time'] = i['time']

        newList.append(ddict)
    df = pd.DataFrame(newList)
    df.to_sql(name='listform10086_copy1', con=mysqlcon, if_exists='append', index=False)
    print('共{}篇链接录入到监控库里---时间排序文章'.format(len(newList)))


def get_urlList():
    excWord = "SELECT id,page_url,issue_time,subclass FROM listform10086 WHERE process_status = 0 ORDER BY issue_time DESC LIMIT 9;"
    alltoup = mysqlcon.execute(excWord)
    llist = []
    for n in alltoup:
        ddict = {}
        ddict['id'] = n[0]
        ddict['page_url'] = n[1]
        ddict['issue_time'] = str(n[2])
        ddict['subclass'] = n[3]
        llist.append(ddict)
    return llist

def get_3day_url(subclass):
    excWord = '''select page_url from listform10086 where process_status = 0 and subclass="{subclass}" and issue_time>=DATE_SUB(NOW(),INTERVAL 3 DAY);'''
    allurl = mysqlcon.execute(excWord.format(subclass=subclass))
    return tuple([x[0] for x in allurl])

def update_stats(artID):
    excWord = '''UPDATE listform10086 SET process_status=1 WHERE id={};'''.format(artID)
    mysqlcon.execute(excWord)



def urlIsExist(urllist):
    import json
    import requests
    HEA = {
        "Connection": "close",
    }
    posturlapi = 'https://umxh.xue2you.cn/pc/api/caijiApi/urlIsExist'
    str_c = json.dumps(urllist)
    dataApi = {"urlListJson": str_c}
    try:
        a = requests.post(url=posturlapi, data=dataApi, headers=HEA)
        jsonT = json.loads(a.text)
        return jsonT['data']
    except:
        return None



if __name__ == "__main__":
    mysqlinfo='''https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=744332
https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=744622'''.split('\n')
    linkAll_index = '''3'''.split('\n')

    # for i in indexWeb_linkAll:
    #     if i not in sql_linAll:
    #         print(i)

    splitA = "selectResult('"
    splitB = "https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id="
    splitC = "')"
    splitD = ''
    linkAll = [x.replace(splitA,splitB).replace(splitC,splitD) for x in linkAll_index]
    print(linkAll)


    noinsertList = urlIsExist(linkAll)

    print(noinsertList)

    exit()

    exc = "SELECT page_url FROM listform10086 WHERE issue_time like '%%2021-03-22%%';"
    a = mysqlcon.execute(exc)
    llist = []
    for i in a:
        # ddict={}
        # ddict['tempUrl'] = i[0]
        llist.append(i[0])
    print(len(llist))
    noinsertList = urlIsExist(llist)
    print(noinsertList)


