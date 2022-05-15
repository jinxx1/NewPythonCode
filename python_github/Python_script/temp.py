# -*- coding: utf-8 -*-

import pymysql, datetime
from rexTime import get_location
from getBase import getBase

import sqlalchemy
import pprint

import pandas as pd
import numpy as np
from mysql_Final import MYSQLDB


def get_allInfo_online():
    MYSQLINFO_online = {
        "HOST": "120.24.4.84",
        "DBNAME": "crawlURL",
        "USER": "xey",
        "PASSWORD": "85f0a9e2e63b47c0b56202824195fb70#AAA",
        "PORT": 3306
    }
    db_online = pymysql.connect(host=MYSQLINFO_online['HOST'], port=MYSQLINFO_online['PORT'],
                                user=MYSQLINFO_online['USER'],
                                passwd=MYSQLINFO_online['PASSWORD'], db=MYSQLINFO_online['DBNAME'])
    cursor = db_online.cursor()
    sqlCode = '''SELECT id,excel_rownum,category,Name FROM construction_tb6'''

    cursor.execute(sqlCode)
    seeAll = cursor.fetchall()
    df = pd.DataFrame(list(seeAll), columns=['id', 'excel_rownum', 'category', 'Name'])
    cursor.close()
    db_online.close()

    return df


def get_allInfo_local():
    from config import MYSQLINFO
    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                         passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])

    cursor = db.cursor()
    sqlCode = '''SELECT id,excel_rownum,Name FROM construction_tb6_20191007 where Name LIKE "%天津电信建设工程有限公司%" or Name like "%河北省通信建设有限公司%"'''

    cursor.execute(sqlCode)
    seeAll = cursor.fetchall()
    df = pd.DataFrame(list(seeAll), columns=['id', 'excel_rownum', 'Name'])
    cursor.close()
    db.close()

    return df


def catmark():
    from config import MYSQLINFO
    from getBase import getBase
    from mysql_Final import MYSQLDB
    mysqldb = MYSQLDB()

    keysList = ['id', 'category']
    llist = []
    idList = []
    datemysql = mysqldb.get_mysqlInfo(tbName='construction_tb6_20191007', keysList=keysList, whereSQL='cat_remark = 2')
    for ii in datemysql:
        ddict = {}
        ddict['from_id'] = ii[0]
        ddict['category'] = ii[1]
        ddict['from_table'] = 'construction_tb6_20191007'
        llist.append(ddict)
        idList.append(ii[0])

    mysqlDF = pd.DataFrame(llist)
    baseDF = getBase()
    resultTEMP = pd.merge(mysqlDF, baseDF, on=['category'])
    result = resultTEMP.drop_duplicates(['from_id'])

    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    result.to_sql(name='catmark_20191007', con=mysqlcon, if_exists='append', index=False, chunksize=1000)
    print('catmark_20191007更新完毕')
    mysqldb.update_Remark_many(idList=idList, tbName='construction_tb6_20191007', keys='cat_remark')
    print('construction_tb6_20191007的cat_remark更新为1')


def update_many_tb6(df):
    from config import MYSQLINFO

    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                         passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])

    cursor = db.cursor()

    sql1 = '''UPDATE construction_tb6_20191007 SET category = CASE id '''
    sql1_1 = '''UPDATE construction_tb6_20191007 SET cat_remark = CASE id '''
    sql2 = ','.join([str(x) for x in list(df['id'])])

    for i in range(len(merge_pd)):
        id_v = int(merge_pd.loc[i]['id'])
        category_v = str(merge_pd.loc[i]['category'])
        sql1 += ''' WHEN %d THEN '%s' ''' % (id_v, category_v)
        sql1_1 += ''' WHEN %d THEN 2 ''' % (id_v)

    sql_category = sql1 + ' END' + " WHERE id IN (%s)" % (sql2)
    # print(sql_category)

    cursor.execute(sql_category)
    print('construction_tb6_20191007的category更新为完毕')

    sql_remark = sql1_1 + ' END' + " WHERE id IN (%s)" % (sql2)
    cursor.execute(sql_remark)
    print('construction_tb6_20191007的cat_remark更新为2')

    db.commit()
    cursor.close()
    db.close()


def get_timeInfo():
    from mysql_Final import MYSQLDB
    mysqldb = MYSQLDB()
    keyList = ['from_id', 'contract_date']

    seeAll = mysqldb.get_mysqlInfo('time_info_20191007', keyList, limit=None,whereSQL='contract_date is not null and from_id is not null')

    df = pd.DataFrame(list(seeAll), columns=keyList)

    return df


def update_many_tb6_timeinfo(merge_pd):
    from config import MYSQLINFO

    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                         passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])

    cursor = db.cursor()

    bei = 1000

    sql1 = '''UPDATE construction_tb6_20191007 SET contract_date = CASE id '''

    idList = []

    for i in range(0,len(merge_pd)):
        id_v = int(merge_pd.loc[i]['from_id'])
        contract_date = str(merge_pd.loc[i]['contract_date'])
        sql1 += ''' WHEN %d THEN '%s' ''' % (id_v, contract_date)

        idList.append(str(id_v))

        if i <100:
            continue

        if i % bei == 0 or i == len(merge_pd) - 1:
            sql2 = ','.join(idList)
            sql_category = sql1 + ' END' + " WHERE id IN (%s)" % (sql2)
            print(len(sql_category))
            # print(sql_category)
            cursor.execute(sql_category)
            db.commit()
            print('第{}条已经更新完毕'.format(i))

            sql1 = '''UPDATE construction_tb6_20191007 SET contract_date = CASE id '''
            del sql2
            del sql_category
            idList = []




    cursor.close()
    db.close()

def tb3_prolocation(info):
    llist = []
    print('location一共有多少项',len(info))
    for i in info:
        ddict ={}
        ddict['id'] = i[0]
        ddict['province_original'] = i[1]
        ddict['county_original'] = i[2]
        ddict['address'] = i[3]

        item = get_location(ddict['address'])
        ddict['province'] = item['Project_province']
        ddict['county'] = item['Project_country']

        if ddict['province'] and ddict['county']:
            llist.append(ddict)
            continue

        if ddict['province_original']:
            item = get_location(ddict['province_original'])
            ddict['province'] = item['Project_province']
            ddict['county'] = item['Project_country']
            if ddict['province'] and ddict['county']:
                llist.append(ddict)
                continue

        if ddict['county_original']:
            item = get_location(ddict['county_original'])
            ddict['province'] = item['Project_province']
            ddict['county'] = item['Project_country']
            if ddict['province'] and ddict['county']:
                llist.append(ddict)
                continue

        ddict['province'] = ddict['province_original']
        ddict['county'] = ddict['county_original']
        llist.append(ddict)
    print('处理后的数量',len(llist))
    return llist


if __name__ == '__main__':
    mysqldb = MYSQLDB()
    keysList = ['id','province','county','address']

    tb3Info = mysqldb.get_mysqlInfo(tbName='construction_tb3_20191007',keysList=keysList,limit=None,whereSQL='address is not null')
    tb3List = tb3_prolocation(tb3Info)
    # pprint.pprint(tb3List)
    keyslist1 =['county','county_original','province','province_original']
    aa = mysqldb.update_many(tbName='construction_tb3_20191007',keyslist=keyslist1,jsonitem=tb3List,wherekey='id')


    print(aa)

