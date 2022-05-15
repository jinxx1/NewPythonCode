import csv
import os
import xlsxwriter
import pandas as pd
import datetime,time,pymysql
import pandas as pd
import numpy as np
from pandas import Series
pd.set_option('display.max_columns',None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.width', 5000)
# pd.set_option('display.unicode.ambiguous_as_wide', True)
# pd.set_option('display.unicode.east_asian_width', True)
from config import MYSQLINFO
import sqlalchemy

def pandas_INTOMYSQL(df):

    conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=MYSQLINFO[
                                                                                                   'PASSWORD'],
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
                                                                                                   'DBNAME'])
    mysqlcon = sqlalchemy.create_engine(conStr)
    df.to_sql(name='jzsc2016', con=mysqlcon, if_exists='append', index=False,chunksize=1000)

def timeLocaltiem(timeWord):
    timeWord_int = int(timeWord)
    lotime = time.localtime(timeWord_int/1000)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", lotime)
    return dt

def parser():

    input_path = "./data/"
    llist = []

    for filename in os.listdir(input_path):
        with open(os.path.join(input_path, filename), 'r',encoding='utf-8') as fp:
            print(f'正在整理 {filename} 文件。。。')
            for n, row in enumerate(csv.reader(fp)):
                data = {}
                if n == 0:
                    continue
                data['company_name'] = row[0]
                data['person_name'] = row[1]
                data['company_location'] = row[2]
                data['credit_id'] = row[3]
                data['art_code'] = row[4]
                data['credit_id_old'] = row[5]
                data['issueTime'] = timeLocaltiem(row[6])
                data['registry_type'] = row[7]
                llist.append(data)

    return pd.DataFrame(llist).drop_duplicates()


class MYSQLDB():
    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                           passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])

    def closeDB(self):
        self.db.close()

    def get_someInfo(self,tbName,keysList):


        cursor = self.db.cursor()
        keyStr = ','.join(keysList)
        sqlCode = '''SELECT {} FROM {} WHERE remark is null limit 1000'''.format(keyStr,tbName)
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()
        llist = []
        for i in seeAll:
            ddict = {}
            ddict['id'] = i[0]
            ddict['code'] = i[1]
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

if __name__ == "__main__":


    mysqldb = MYSQLDB()
    tbname = 'jzsc2016'
    keysList = ['id','art_code']
    print(mysqldb.get_someInfo(tbName=tbname,keysList=keysList))













    # a = parser()
    # pandas_INTOMYSQL(a)
    # print('-----------end-----------')
