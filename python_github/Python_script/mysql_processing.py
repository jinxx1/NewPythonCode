# -*- coding: utf-8 -*-
from rexTime import get_location
import pymysql,datetime
from config import MYSQLINFO
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
import cpca

import datetime,json
import pprint
from decimal import Decimal


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

def pandas_supervisor_tb7(itmeList):
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

    df.to_sql(name='supervisor_tb7', con=mysqlcon, if_exists='append', index=False)

def pandas_supervisor_tb4(itmeList):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='supervisor_tb4', con=mysqlcon, if_exists='append', index=False)

def pandas_supervisor_tb3(itmeList):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='supervisor_tb3', con=mysqlcon, if_exists='append', index=False)

def pandas_supervisor_tb5(itmeList):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='supervisor_tb5', con=mysqlcon, if_exists='append', index=False)

def pandas_design_tb6(itmeList):
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
    df.to_sql(name='design_tb6', con=mysqlcon, if_exists='append', index=False)

def pandas_design_tb4(itmeList):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='design_tb4', con=mysqlcon, if_exists='append', index=False)

def pandas_design_tb3(itmeList):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='design_tb3', con=mysqlcon, if_exists='append', index=False)

def pandas_construction_tb6(itmeList):
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
    df.to_sql(name='construction_tb6', con=mysqlcon, if_exists='append', index=False)

def pandas_construction_tb3(itmeList):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='construction_tb3', con=mysqlcon, if_exists='append', index=False)

def pandas_construction_tb4(itmeList):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='construction_tb4', con=mysqlcon, if_exists='append', index=False)


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



class MYSQLDB():
    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                           passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])

    def closeDB(self):
        self.db.close()

    def get_someInfo(self,tablesList,keysList):
        cursor = self.db.cursor()
        keyStr = ','.join(keysList)
        for tbName in tablesList:
            sqlCode = '''SELECT {} FROM {}'''.format(keyStr,tbName)
            cursor.execute(sqlCode)
            seeAll = cursor.fetchall()
            yield seeAll
            for i in seeAll:
                ddict = {}
                ddict['info'] = i
                ddict['table'] = tbName
                yield ddict
        cursor.close()

    def get_mysqlinfo(self,tbName,keysList):
        cursor = self.db.cursor()
        keyStr = ','.join(keysList)

        sqlCode = '''SELECT {} FROM {}'''.format(keyStr,tbName)
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()
        cursor.close()
        return seeAll



    def insert_date(self,dictWord):
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

 #        sqlCode = '''SELECT id,contract_date,contract_ReMark,invoice_date,invoicet_ReMark
 # FROM time_info where contract_date is null or invoice_date is null'''
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

if __name__ == "__main__":

    url = 'C:\PthonCode\Python_script\File\construction/11、北京锦程前方科技有限公司.xls'


    mysqldb=MYSQLDB()
    update_key = ['Project_province','Project_country','Project_district']
    keysList = ['id','location_original_str']
    tablesList = ['supervisor_tb7','design_tb6','construction_tb6']
    for n in mysqldb.get_someInfo(tablesList=tablesList,keysList=keysList):
        ddict = {}
        if n['info'][1] is None or n['info'][1] == '':
            ddict['Project_province'] = ''
            ddict['Project_country'] = ''
            ddict['Project_district'] = ''
        else:
            location = get_location(n['info'][1])
            ddict['Project_province'] = location['Project_province']
            ddict['Project_country'] = location['Project_country']
            ddict['Project_district'] = location['Project_district']
        ddict['id'] = n['info'][0]
        ddict['table'] = n['table']
        mysqldb.insert_date(ddict)
    mysqldb.closeDB()
    print('-----------------------------The End-----------------------------')
