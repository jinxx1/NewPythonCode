# -*- coding: utf-8 -*-
from rexTime import get_location
import pymysql,datetime
from config import MYSQLINFO
from getBase import getBase
import pandas as pd
import numpy as np
from pandas import Series
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import sqlalchemy
NowTime = str(datetime.datetime.now()).split(' ')[0].replace('-','')



def insert_bugfileinfo(filePath,errorword):

    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                           passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])
    cursor = db.cursor()

    insertCode = '''
                    INSERT INTO bugfileinfo(bugFile,reLoad,BugExplain,reLoadsueccful)
                    VALUES (
                    '{bugFile}',
                    '{reLoad}',
                    '{BugExplain}',
                    '{reLoadsueccful}'
                    )'''
    inser_execute = insertCode.format(
        bugFile = pymysql.escape_string(filePath),
        reLoad = 0,
        reLoadsueccful = 0,
        BugExplain = pymysql.escape_string(str(errorword)))
    cursor.execute(inser_execute)
    db.commit()

    cursor.close()
    db.close()

def pandas_supervisor_tb7(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    try:
        df.category.fillna(method='pad', inplace=True)
    except:
        pass

    try:
        df.contractor.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.contract_name.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.registration_id.fillna(method='pad', inplace=True)
    except:
        pass

    try:
        df.Name.fillna(method='pad', inplace=True)
    except:
        pass

    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS supervisor_tb7_{} (LIKE supervisor_tb7);".format(NowTime))
        df.to_sql(name='supervisor_tb7_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='supervisor_tb7', con=mysqlcon, if_exists='append', index=False)

def pandas_supervisor_tb4(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS supervisor_tb4_{} (LIKE supervisor_tb4);".format(NowTime))
        df.to_sql(name='supervisor_tb4_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='supervisor_tb4', con=mysqlcon, if_exists='append', index=False)

def pandas_supervisor_tb3(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS supervisor_tb3_{} (LIKE supervisor_tb3);".format(NowTime))
        df.to_sql(name='supervisor_tb3_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)

    else:
        df.to_sql(name='supervisor_tb3', con=mysqlcon, if_exists='append', index=False)

def pandas_supervisor_tb5(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS supervisor_tb5_{} (LIKE supervisor_tb5);".format(NowTime))
        df.to_sql(name='supervisor_tb5_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)

    else:
        df.to_sql(name='supervisor_tb5', con=mysqlcon, if_exists='append', index=False)

def pandas_design_tb6(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    try:
        df.category.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.contractor.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.sheetName.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.protocol.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.contract_name.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.registration_id.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.years.fillna(method='pad', inplace=True)
    except:
        pass

    try:
        df.Name.fillna(method='pad', inplace=True)
    except:
        pass

    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS design_tb6_{} (LIKE design_tb6);".format(NowTime))
        df.to_sql(name='design_tb6_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='design_tb6', con=mysqlcon, if_exists='append', index=False)

def pandas_design_tb4(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS design_tb4_{} (LIKE design_tb4);".format(NowTime))
        df.to_sql(name='design_tb4_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='design_tb4', con=mysqlcon, if_exists='append', index=False)

def pandas_design_tb3(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS design_tb3_{} (LIKE design_tb3);".format(NowTime))
        df.to_sql(name='design_tb3_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='design_tb3', con=mysqlcon, if_exists='append', index=False)

def pandas_construction_tb6(itmeList,inputWord):
    print('一共--------------',len(itmeList))
    df = pd.DataFrame(itmeList)
    try:
        df.category.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.contractor.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.Is_it_operator.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.contractor_address.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.Project_name.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.Name.fillna(method='pad', inplace=True)
    except:
        pass

    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    if inputWord:
        tbName = 'construction_tb6_{}'.format(NowTime)
        timeWord = NowTime
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS {} (LIKE construction_tb6);".format(tbName))
    else:
        tbName = 'construction_tb6'
        timeWord = None

    df.to_sql(name=tbName, con=mysqlcon, if_exists='append', index=False,chunksize=1000)
    print('tb6完成')
    main_locationmark(mysqlcon,tbName,timeWord)
    print('main_locationmark完成')
    main_catmark(mysqlcon,tbName,timeWord)
    print('main_catmark完成')
    main_timemark(mysqlcon,tbName,timeWord)
    print('main_timemark完成')

def pandas_construction_tb6_tmp(itmeList,inputWord):
    MYSQLINFO = {
        "HOST": "120.24.4.84",
        "DBNAME": "crawlURL",
        "USER": "xey",
        "PASSWORD": "85f0a9e2e63b47c0b56202824195fb70#AAA",
        "PORT": 3306
    }


    print('一共--------------',len(itmeList))
    df = pd.DataFrame(itmeList)
    try:
        df.category.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.contractor.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.Is_it_operator.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.contractor_address.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.Project_name.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.Name.fillna(method='pad', inplace=True)
    except:
        pass

    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    if inputWord:
        tbName = 'construction_tb6_{}'.format(NowTime)
        timeWord = NowTime
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS {} (LIKE construction_tb6);".format(tbName))
    else:
        tbName = 'construction_tb6'
        timeWord = None

    df.to_sql(name=tbName, con=mysqlcon, if_exists='append', index=False,chunksize=1000)
    print('tb6完成')
    # main_locationmark(mysqlcon,tbName,timeWord)
    # print('main_locationmark完成')
    # main_catmark(mysqlcon,tbName,timeWord)
    # print('main_catmark完成')
    # main_timemark(mysqlcon,tbName,timeWord)
    # print('main_timemark完成')

def pandas_construction_tb3(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS construction_tb3_{} (LIKE construction_tb3);".format(NowTime))
        df.to_sql(name='construction_tb3_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='construction_tb3', con=mysqlcon, if_exists='append', index=False)

def pandas_construction_tb4(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS construction_tb4_{} (LIKE construction_tb4);".format(NowTime))
        df.to_sql(name='construction_tb4_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='construction_tb4', con=mysqlcon, if_exists='append', index=False)



def pandas_maintaining_tb3(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS maintain_tb3_{} (LIKE maintain_tb3);".format(NowTime))
        df.to_sql(name='maintain_tb3_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='maintain_tb3', con=mysqlcon, if_exists='append', index=False)

def pandas_maintaining_tb7(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS maintain_tb7_{} (LIKE maintain_tb7);".format(NowTime))
        df.to_sql(name='maintain_tb7_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='maintain_tb7', con=mysqlcon, if_exists='append', index=False)

def pandas_maintaining_tb7_negative(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    if inputWord:
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS maintain_tb7_{} (LIKE maintain_tb7);".format(NowTime))
        df.to_sql(name='maintain_tb7_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    else:
        df.to_sql(name='maintain_tb7_negative', con=mysqlcon, if_exists='append', index=False)

def pandas_maintaining_tb4(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    # if inputWord:
    #     mysqlcon.execute("CREATE TABLE IF NOT EXISTS maintain_tb7_{} (LIKE maintain_tb7);".format(NowTime))
    #     df.to_sql(name='maintain_tb7_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    # else:
    df.to_sql(name='maintain_tb4', con=mysqlcon, if_exists='append', index=False)

def pandas_maintaining_tb5(itmeList,inputWord):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)

    # if inputWord:
    #     mysqlcon.execute("CREATE TABLE IF NOT EXISTS maintain_tb7_{} (LIKE maintain_tb7);".format(NowTime))
    #     df.to_sql(name='maintain_tb7_{}'.format(NowTime), con=mysqlcon, if_exists='append', index=False)
    # else:
    df.to_sql(name='maintain_tb5', con=mysqlcon, if_exists='append', index=False)

def pandas_TimeInfo(itmeList):
    df = pd.DataFrame(itmeList)

    try:
        df.Name.fillna(method='pad', inplace=True)
    except:
        pass

    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='time_info', con=mysqlcon, if_exists='append', index=False)


def main_locationmark(mysqlcon,tbName,timeWord=None):
    mysqldb = MYSQLDB()
    keysList = ['id', 'location_original_str', 'contractor', 'contractor_address']
    llist = []
    idList = []
    datemysql = mysqldb.get_mysqlInfo(tbName=tbName, keysList=keysList,whereSQL='location_remark is null')

    for ii in datemysql:
        ddict = {}
        ddict['from_id'] = ii[0]
        ddict['location_original_str'] = ii[1]
        ddict['contractor'] = ii[2]
        ddict['contractor_address'] = ii[3]
        ddict['from_table'] = tbName
        idList.append(ii[0])


        # 先通过'location_original_str'原始字段，获取三个地理信息
        if ddict['location_original_str']:
            item_location = get_location(ddict['location_original_str'])
        else:
            item_location = get_location('无')
        ddict['Project_province'] = item_location['Project_province']
        ddict['Project_country'] = item_location['Project_country']
        ddict['Project_district'] = item_location['Project_district']
        ddict['remark'] = 'country by location_original_str'

        # 再通过'contractor'，获取三个地理信息
        if ddict['contractor']:
            item_contractor = get_location(
                ddict['contractor'].replace('北京', '').replace('上海', '').replace('天津', '').replace('重庆', ''))
        else:
            item_contractor = get_location('无')


        # 通过'contractor'获取区县信息。如果不为空，那么最终地市信息算作'contractor'区县
        if item_contractor['Project_district'] != '':
            ddict['Project_district'] = item_contractor['Project_district']
        else:
            pass

        # 如果最终地市、省  都信息为空，那么最终地市、省信息等于'contractor'地市、省、区县
        if ddict['Project_country'] == '' and ddict['Project_province'] == '':

            ddict['Project_province'] = item_contractor['Project_province']
            ddict['Project_country'] = item_contractor['Project_country']
            ddict['Project_district'] = item_contractor['Project_district']
            ddict['remark'] = 'all by contractor'
        # 否则，如果最终地市为空，而省不空，那么最终地市、区县等于'contractor'地市、区县
        elif ddict['Project_country'] == '' and item_contractor['Project_country'] != '':
            ddict['Project_country'] = item_contractor['Project_country']
            ddict['Project_district'] = item_contractor['Project_district']
            ddict['remark'] = 'country by contractor'
        else:
            pass

        # 如果最终地市为空，并且最终省不为空。则正式应用。
        if ddict['Project_country'] == '' and ddict['Project_province'] != '':
            llist.append(ddict)
            continue
        # 如果什么数据都没得到，并且contractor_address有数值  则通过contractor_address补全。最终应用。
        elif ddict['Project_country'] == '' and ddict['Project_province'] == '' and ddict['Project_district'] == '' and ddict['contractor_address'] != '':
            addrItem = get_location(ddict['contractor_address'])
            ddict['Project_province'] = addrItem['Project_province']
            ddict['Project_country'] = addrItem['Project_country']
            ddict['Project_district'] = addrItem['Project_district']
            ddict['remark'] = 'Country by contractor_address'
            llist.append(ddict)
            continue
        elif ddict['contractor_address'] != '':
            # 如果contractor_address不为空，则通过 最终地市信息 生成supervisorItem核查数据

            supervisorItem = get_location(ddict['Project_country'])
                # 如果最终省，跟核查数据不相符。则通过contractor_address生成补全数据。最终数据等于补全数据
            if ddict['Project_province'] != supervisorItem['Project_province']:
                addrItem = get_location(ddict['contractor_address'])
                ddict['Project_country'] = addrItem['Project_country']
                ddict['Project_district'] = addrItem['Project_district']
                ddict['remark'] = 'Country by contractor_address'
                llist.append(ddict)
                continue
            else:
                llist.append(ddict)
                continue
        else:
            llist.append(ddict)
            continue

    df = pd.DataFrame(llist)

    if timeWord:
        locationName = 'locationinfo_{}'.format(timeWord)
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS {} (LIKE locationinfo);".format(locationName))
    else:
        locationName = 'locationinfo'
    df.to_sql(name=locationName, con=mysqlcon, if_exists='append', index=False,chunksize=1000)
    mysqldb.update_Remark_many(idList=idList,tbName=tbName,keys='location_remark')

def main_catmark(mysqlcon,tbName,timeWord=None):

    mysqldb = MYSQLDB()
    keysList = ['id', 'category']
    llist = []
    idList = []
    datemysql = mysqldb.get_mysqlInfo(tbName=tbName,keysList=keysList,whereSQL='cat_remark is null')
    for ii in datemysql:
        ddict = {}
        ddict['from_id'] = ii[0]
        ddict['category'] = ii[1]
        ddict['from_table'] = tbName
        llist.append(ddict)
        idList.append(ii[0])


    mysqlDF = pd.DataFrame(llist)
    baseDF = getBase()
    resultTEMP = pd.merge(mysqlDF, baseDF, on=['category'])
    result = resultTEMP.drop_duplicates(['from_id'])
    if timeWord:
        NAME = 'catmark_{}'.format(timeWord)
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS {} (LIKE catmark);".format(NAME))
    else:
        NAME = 'catmark'

    result.to_sql(name=NAME, con=mysqlcon, if_exists='append', index=False,chunksize=1000)
    mysqldb.update_Remark_many(idList=idList,tbName=tbName,keys='cat_remark')

def main_timemark(mysqlcon,tbName,timeWord=None):
    mysqldb = MYSQLDB()
    keysList = ['id','Name', 'contract_date', 'contract_ReMark', 'invoice_date', 'invoicet_ReMark', 'from_excel_path', 'excel_rownum','sheetName']
    llist = []
    idList = []
    datemysql = mysqldb.get_mysqlInfo(tbName=tbName,keysList=keysList,whereSQL='time_remark is null')
    for ii in datemysql:
        ddict = {}
        ddict['from_id'] = ii[0]
        ddict['Name'] = ii[1]
        ddict['contract_date'] = ii[2]
        ddict['contract_ReMark'] = ii[3]
        ddict['invoice_date'] = ii[4]
        ddict['invoicet_ReMark'] = ii[5]
        ddict['from_excel_path'] = ii[6]
        ddict['excel_rownum'] = ii[7]
        ddict['sheetName'] = ii[8]
        ddict['from_table'] = tbName
        llist.append(ddict)
        idList.append(ii[0])

    df = pd.DataFrame(llist)

    if timeWord:
        NAME = 'time_info_{}'.format(timeWord)
        mysqlcon.execute("CREATE TABLE IF NOT EXISTS {} (LIKE time_info);".format(NAME))

    else:
        NAME = 'time_info'
    df.to_sql(name=NAME, con=mysqlcon, if_exists='append', index=False,chunksize=1000)
    mysqldb.update_Remark_many(idList=idList,tbName=tbName,keys='time_remark')





class MYSQLDB():
    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                           passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])



    def get_allInfo(self,tbName,limit=None):
        cursor = self.db.cursor()
        sqlCode = '''SELECT * FROM {} limit {}'''.format(tbName, limit)
        if not limit:
            sqlCode = '''SELECT * FROM {}'''.format(tbName)
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()

        sqlCode = '''SHOW COLUMNS FROM {}'''.format(tbName)
        cursor.execute(sqlCode)
        keysAll = cursor.fetchall()

        cursor.close()
        return seeAll,keysAll

    def get_mysqlInfo(self,tbName,keysList,whereSQL=None,limit=None):
        cursor = self.db.cursor()
        keyStr = ','.join(keysList)
        if whereSQL:
            sqlCode = '''SELECT {} FROM {} where {}'''.format(keyStr,tbName,whereSQL)
        else:
            sqlCode = '''SELECT {} FROM {}'''.format(keyStr, tbName)
        if limit:
            sqlCode = sqlCode + " limit {}".format(limit)
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()
        cursor.close()
        return seeAll

    def update_Remark_many(self,idList,tbName,keys):
        sql1 = '''UPDATE {} SET {} = CASE id '''.format(tbName,keys)
        sql2 = ','.join([str(x) for x in idList])

        for IDNUM in idList:
            sql1 += ''' WHEN %d THEN "%s" '''%(IDNUM,'aaa')

        sql = sql1 + ' END' + " WHERE id IN (%s)" % (sql2)

        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()


    def update_many(self,tbName,keyslist,jsonitem,wherekey = None):
        '''
        :param tbName: 表名称
        :param keyslist: 需要修改的字段名list
        :param jsonitem: 所有json字典数据
        :param wherekey: 表明以哪个字段为修改依据，默认值为None，则自动以id字段名为准。
        :return: None
        '''
        cursor = self.db.cursor()

        idList = [x['id'] for x in jsonitem]
        sql2 = ','.join([str(x) for x in idList])

        for keyName in keyslist:
            if not wherekey:
                sql1 = '''UPDATE {tbName} SET {keyName} = CASE id \n'''.format(tbName=tbName, keyName=keyName)
            else:
                sql1 = '''UPDATE {tbName} SET {keyName} = CASE {wherekey} \n'''.format(tbName=tbName, keyName=keyName,wherekey=wherekey)

            for info in jsonitem:
                if not info[keyName]:
                    info[keyName] = ''
                sql1 += ''' WHEN %d THEN "%s" \n'''%(info['id'],info[keyName].replace('\\',''))

            sql = sql1 + ' END' + " WHERE id IN (%s)" % (sql2)


            cursor.execute(sql)
            self.db.commit()


        cursor.close()


    def insert_date(self,dictWord = None):
        cursor = self.db.cursor()
        tableName = dictWord['table']
        mysqlID = dictWord['id']
        Project_province = dictWord['Project_province']
        Project_country = dictWord['Project_country']
        Project_district = dictWord['Project_district']

        sqlCode = '''UPDATE {tableName} set Project_province='{Project_province}',Project_country='{Project_country}',Project_district='{Project_district}' where id={mysqlID}'''

        sqlexecut = sqlCode.format(tableName = tableName,
                                   Project_province = Project_province,
                                   Project_country = Project_country,
                                   Project_district = Project_district,
                                   mysqlID = mysqlID)

        cursor.execute(sqlexecut)
        self.db.commit()
        cursor.close()
        print('修改完成')

    def get_TimeInfo(self):
        cursor = self.db.cursor()

        sqlCode = '''SELECT id,contract_date,contract_ReMark,invoice_date,invoicet_ReMark
        FROM time_info where invoice_date is null'''
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()
        if seeAll:
            for i in seeAll:
                ddict={}
                ddict['id'] = i[0]
                ddict['contract_date'] =i[1]
                ddict['contract_ReMark'] =i[2]
                ddict['invoice_date'] =i[3]
                ddict['invoicet_ReMark'] =i[4]
                yield ddict
        cursor.close()

    def update_TimeNullinfo(self,ddict):
        cursor = self.db.cursor()

        setWordList = [x for x in ddict.keys()]

        if 'contract_date' in setWordList and 'invoice_date' in setWordList:
            sqlCode_Info = '''UPDATE time_info set contract_date = '{}',invoice_date = '{}' where id={}'''.format(ddict['contract_date'],ddict['invoice_date'],ddict['id'])
        elif 'contract_date' in setWordList and 'invoice_date' not in setWordList:
            sqlCode_Info = '''UPDATE time_info set contract_date = '{}' where id={}'''.format(ddict['contract_date'],ddict['id'])
        elif 'invoice_date' in setWordList and 'contract_date' not in setWordList :
            sqlCode_Info = '''UPDATE time_info set invoice_date = '{}' where id={}'''.format(ddict['invoice_date'],ddict['id'])
        else:
            return None

        cursor.execute(sqlCode_Info)
        self.db.commit()
        cursor.close()



    def closeDB(self):
        self.db.close()



if __name__ == "__main__":
    pass