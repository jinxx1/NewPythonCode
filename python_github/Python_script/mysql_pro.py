# -*- coding: utf-8 -*-
from rexTime import get_location
import pymysql
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
import cpca

import datetime,json
import pprint
from decimal import Decimal


def main1():


    mysqldb = MYSQLDB()
    update_key = ['Project_province', 'Project_country', 'Project_district']
    keysList = ['id', 'location_original_str','']
    tablesList = ['supervisor_tb7', 'design_tb6', 'construction_tb6']

    for tName in tablesList:
        llist = []
        infoList = mysqldb.get_someInfo(tbName=tName, keysList=keysList)
        for num, n in enumerate(infoList):
            ddict = {}
            if n['info'] is None or n['info'] == '':
                ddict['Project_province'] = ''
                ddict['Project_country'] = ''
                ddict['Project_district'] = ''
            else:
                location = get_location(n['info'])
                ddict['Project_province'] = location['Project_province']
                ddict['Project_country'] = location['Project_country']
                ddict['Project_district'] = location['Project_district']
            ddict['from_id'] = n['id']
            ddict['location_original_str'] = n['info']
            ddict['from_table'] = tName
            llist.append(ddict)

        df = pd.DataFrame(llist)
        pandas_update(df)
        print('修改完成----{}---{}'.format(num, tName))

    mysqldb.closeDB()


def main2():
    mysqldb = MYSQLDB()
    listkeys = ['id', 'location_original_str', 'from_id', 'from_table']
    LocationInfoList = mysqldb.get_locationInfo(tbName='locationinfo', keysList=listkeys)
    for num, nn in enumerate(LocationInfoList):
        ddict = {}
        if not nn['location_original_str']:
            nn['location_original_str'] = ''
        if num == 0:
            if '同上' not in nn['location_original_str']:
                org = nn['location_original_str']
                mark = 'id={},from_tb={},from_id={},原始值={}'.format(nn['id'], nn['from_table'], nn['from_id'],
                                                                   nn['location_original_str'])
            else:
                org = ''
        else:
            if '同上' not in nn['location_original_str']:
                org = nn['location_original_str']
                mark = 'id={},from_tb={},from_id={},原始值={}'.format(nn['id'], nn['from_table'], nn['from_id'],
                                                                   nn['location_original_str'])
            else:

                location = get_location(org)
                ddict['id'] = nn['id']
                ddict['Project_province'] = location['Project_province']
                ddict['Project_country'] = location['Project_country']
                ddict['Project_district'] = location['Project_district']
                ddict['from_table'] = nn['from_table']
                ddict['from_id'] = nn['from_id']
                ddict['remark'] = '本条为(同上),填充自{}'.format(mark)

                mysqldb.insert_date2(ddict)
                print('-----------------------------------')

def main3():
    mysqldb = MYSQLDB()
    listkeys = ['id', 'location_original_str', 'from_id', 'from_table']
    LocationInfoList = mysqldb.get_locationInfo(tbName='locationinfo', keysList=listkeys)
    for num, nn in enumerate(LocationInfoList):
        ddict = {}
        if nn['location_original_str'] and nn['location_original_str'] !='':
            org = nn['location_original_str']
            mark = 'id={},from_tb={},from_id={},原始值={}'.format(nn['id'], nn['from_table'], nn['from_id'],
                                                                       nn['location_original_str'])
        else:
            ddict['location_original_str'] = org
            location = get_location(ddict['location_original_str'])
            ddict['id'] = nn['id']
            ddict['Project_province'] = location['Project_province']
            ddict['Project_country'] = location['Project_country']
            ddict['Project_district'] = location['Project_district']
            ddict['from_table'] = nn['from_table']
            ddict['from_id'] = nn['from_id']
            ddict['remark'] = '本条为(null),填充自{}'.format(mark)
            mysqldb.insert_date3(ddict)





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

def pandas_update(itmeList):
    df = pd.DataFrame(itmeList)
    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='locationinfo', con=mysqlcon, if_exists='append', index=False,chunksize=1000)


class MYSQLDB():
    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                           passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])

    def closeDB(self):
        self.db.close()

    def get_someInfo(self,tbName,keysList):


        cursor = self.db.cursor()
        keyStr = ','.join(keysList)
        sqlCode = '''SELECT {} FROM {}'''.format(keyStr,tbName)
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()
        llist = []
        for i in seeAll:
            ddict = {}
            ddict['id'] = i[0]
            ddict['Name'] = i[1]
            ddict['from_excel_path'] = i[2]
            ddict['excel_rownum'] = i[3]
            ddict['Is_it_operator_remark'] = i[4]
            ddict['Is_it_operator'] = i[5]
            llist.append(ddict)
        cursor.close()
        return llist

    def get_locationInfo(self,tbName,keysList):
        cursor = self.db.cursor()
        keyStr = ','.join(keysList)
        sqlCode = '''SELECT {} FROM {}'''.format(keyStr,tbName)
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()
        llist = []
        for i in seeAll:
            ddict = {}
            ddict['id'] = i[0]
            ddict['location_original_str'] = i[1]
            ddict['from_id'] = i[2]
            ddict['from_table'] = i[3]
            llist.append(ddict)
        cursor.close()
        return llist

    def insert_date(self,dictWord,tableName):
        cursor = self.db.cursor()
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

    def insert_date2(self,dictWord):
        cursor = self.db.cursor()
        mysqlID = dictWord['id']
        Project_province = dictWord['Project_province']
        Project_country = dictWord['Project_country']
        Project_district = dictWord['Project_district']
        remark = dictWord['remark']
        from_id =dictWord['from_id']
        from_table = dictWord['from_table']


        sqlCode_locationInfo = '''UPDATE locationinfo set Project_province='{Project_province}',Project_country='{Project_country}',Project_district='{Project_district}',remark='{remark}' where id={mysqlID}'''

        sqlexecut_locationInfo = sqlCode_locationInfo.format(Project_province = Project_province,
                                   Project_country = Project_country,
                                   Project_district = Project_district,
                                   remark = remark,
                                   mysqlID = mysqlID)
        cursor.execute(sqlexecut_locationInfo)
        self.db.commit()

        sqlCode_tb = '''UPDATE {tableName} set Project_province='{Project_province}',Project_country='{Project_country}',Project_district='{Project_district}' where id={mysqlID}'''


        sqlexecut_tb = sqlCode_tb.format(tableName = from_table,
                                   Project_province = Project_province,
                                   Project_country = Project_country,
                                   Project_district = Project_district,
                                   mysqlID = from_id)

        cursor.execute(sqlexecut_tb)
        self.db.commit()

        cursor.close()
        print('修改完成')

    def insert_date3(self,dictWord):
        cursor = self.db.cursor()
        mysqlID = dictWord['id']
        Project_province = dictWord['Project_province']
        Project_country = dictWord['Project_country']
        Project_district = dictWord['Project_district']
        remark = dictWord['remark']
        from_id =dictWord['from_id']
        from_table = dictWord['from_table']
        location_original_str = dictWord['location_original_str']

        sqlCode_locationInfo = '''UPDATE locationinfo set location_original_str='{location_original_str}',Project_province='{Project_province}',Project_country='{Project_country}',Project_district='{Project_district}',remark='{remark}' where id={mysqlID}'''

        sqlexecut_locationInfo = sqlCode_locationInfo.format(Project_province = Project_province,
                                location_original_str = location_original_str,
                                   Project_country = Project_country,
                                   Project_district = Project_district,
                                   remark = remark,
                                   mysqlID = mysqlID)
        cursor.execute(sqlexecut_locationInfo)
        self.db.commit()

        sqlCode_tb = '''UPDATE {tableName} set location_original_str='{location_original_str}',Project_province='{Project_province}',Project_country='{Project_country}',Project_district='{Project_district}' where id={mysqlID}'''


        sqlexecut_tb = sqlCode_tb.format(tableName = from_table,
                                 location_original_str=location_original_str,
                                   Project_province = Project_province,
                                   Project_country = Project_country,
                                   Project_district = Project_district,
                                   mysqlID = from_id)

        cursor.execute(sqlexecut_tb)
        self.db.commit()

        cursor.close()
        print('修改完成')

    def update_isit(self,dictWord):
        cursor = self.db.cursor()
        mysqlID = dictWord['id']
        isit = dictWord['isit']

        try:
            sqlCode_locationInfo = '''UPDATE construction_tb6 set Is_it_operator_remark='{Is_it_operator_remark}',Is_it_operator='{Is_it_operator}' where id={mysqlID}'''

            sqlexecut_locationInfo = sqlCode_locationInfo.format(Is_it_operator_remark = '修改自章哥excel',
                                    Is_it_operator = isit,
                                       mysqlID = mysqlID)
            cursor.execute(sqlexecut_locationInfo)
            self.db.commit()
            print('isit修改完成')
        except:
            cursor.rollback()
            print('isit修改--失败')
        finally:
            cursor.close()



    def update_Timeinfo(self,dictWord):
        cursor = self.db.cursor()
        mysqlID = dictWord['id']
        Name = dictWord['Name']
        from_excel_path = dictWord['from_excel_path']
        excel_rownum = dictWord['excel_rownum']

        indexTime = (excel_rownum,Name)
        try:
            sqlCode_locationInfo = '''UPDATE time_info set from_id={from_id} where Name='{Name}' and excel_rownum = {excel_rownum}'''
            sqlexecut_locationInfo = sqlCode_locationInfo.format(from_id = mysqlID,
                                                                Name = Name,

                                                                excel_rownum = excel_rownum)

            # sqlCode_locationInfo = '''UPDATE time_info set from_id={from_id} where INDTime1({a1},"{a2}")'''
            #
            # sqlexecut_locationInfo = sqlCode_locationInfo.format(from_id =mysqlID,a1=excel_rownum,a2=Name)

            cursor.execute(sqlexecut_locationInfo)
            self.db.commit()
            print('timeinfo修改完成')
        except:
            cursor.rollback()
            print('timeinfo修改--失败')
        finally:
            cursor.close()




def get_zhangJson():
        rootPath = os.getcwd().replace('\\', '/')
        jsonPath = rootPath + '/zhang_isitopter.json'

        with open(jsonPath, 'r') as jf:
            jsonLoad = json.load(jf)
            jf.close()
        return jsonLoad

if __name__ == "__main__":
    import datetime,os
    starttime = datetime.datetime.now()

    zhangJson = get_zhangJson()

    mysqldb = MYSQLDB()

    construction_tb6_list = ['id', 'Name', 'from_excel_path', 'excel_rownum', 'Is_it_operator_remark', 'Is_it_operator']

    get_contb6 = mysqldb.get_someInfo(tbName='construction_tb6',keysList=construction_tb6_list)

    for num,tb6 in enumerate(get_contb6):

        mysqldb.update_Timeinfo(tb6)


        # print('Time_Info',num)
        # print('***********')


    endtime2 = datetime.datetime.now()
    print(endtime2 - starttime)
    print('-----------------------------The End-----------------------------')




