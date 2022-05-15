# -*- coding: utf-8 -*-

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

import datetime
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


def pandas_process(itmeList):
    df = pd.DataFrame(itmeList)
    try:
        df.category.fillna(method='pad', inplace=True)
    except:
        pass
    try:
        df.Project_province.fillna(method='pad', inplace=True)
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
    df.to_sql(name='table6', con=mysqlcon, if_exists='append', index=False)

def insert_table(item,num):
    # return None

    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                           passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])
    cursor = db.cursor()
    keysList = [x for x in item.keys()]

    keysList_value_mod = []
    value_list = []
    for i in keysList:
        a = type(item[i])
        if a is int:
            mod = '%s'
            keysList_value_mod.append(mod)
            value_list.append(int(item[i]))
        elif a is str:
            mod = '\'%s\''
            keysList_value_mod.append(mod)
            value_list.append(str(item[i]))
        elif a is float:
            mod = '%s'
            keysList_value_mod.append(mod)
            value_list.append(float(item[i]))
        else:
            mod = '\'%s\''
            keysList_value_mod.append(mod)
            value_list.append(item[i].strftime("%Y-%m-%d %H:%M:%S"))

    keysList_value_mod_str = ','.join(keysList_value_mod)
    keysList_str = ','.join(keysList)
    value_tuple = tuple(value_list)

    insertCode = '''INSERT INTO table{} ({}) VALUES ({})'''.format(num,keysList_str, keysList_value_mod_str)
    sql = insertCode % value_tuple

    cursor.execute(query=sql)
    db.commit()

    cursor.close()
    db.close()

class MYSQLDB_Table6():
    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                           passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])

    def closeDB(self):
        self.db.close()

    def get_invoiceCode_from_noMark_noPerfect(self):
        cursor = self.db.cursor()
        # sqlCode = '''
        # SELECT * FROM table6 WHERE after_treatment_mark IS NULL and perfectItem IS NULL GROUP BY invoice_code
        # '''



        sqlCode = '''
        SELECT * FROM table6 limit 1000
        '''


        dateList =[]
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()

        for i in seeAll:
            item = {}
            item['id'] =i[0]
            item['excel_id'] =i[1]
            item['category'] =i[2]
            item['Project_province'] =i[3]
            item['Project_district'] =i[4]
            item['contractor'] =i[5]
            item['Is_it_operator'] =i[6]
            item['contractor_address'] =i[7]
            item['Project_name'] =i[8]
            item['contract_amount'] =i[9]
            item['contract_date'] =i[10]
            item['invoice_num'] =i[11]
            item['invoice_code'] =i[12]
            item['invoice_amount'] =i[13]
            item['invoice_date'] =i[14]
            item['from_excel_path'] =i[15]
            item['excel_rownum'] =i[16]
            item['after_treatment'] =i[17]
            item['perfectItem'] =i[18]
            item['after_treatment_mark'] =i[19]
            item['Name'] =i[20]



            dateList.append(item)
        # get_invoiceCode_list = [x['invoice_code'] for x in dateList if x['invoice_code']]
        cursor.close()
        # return get_invoiceCode_list
        df = pd.DataFrame(dateList)
        # print(len(dateList))
        return df

    def get_needPrecessitem(self,nlist):
        item = dict(id=[],excel_id=[],category=[],Project_province=[],Project_district=[],contractor=[],Is_it_operator=[],contractor_address=[],Project_name=[],contract_amount=[],contract_date=[],invoice_num=[],invoice_code=[],invoice_amount=[],invoice_date=[],from_excel_path=[],excel_rownum=[],after_treatment=[],perfectItem=[],after_treatment_mark=[],Name=[])
        cursor = self.db.cursor()
        llist = []
        sqlCode = '''
        SELECT * FROM table6 WHERE invoice_code = '{}'
        '''
        oneItem = {}
        for i,sql in enumerate(nlist):
            if i > 2:
                break
            cursor.execute(sqlCode.format(sql))
            seeAll = cursor.fetchall()
            for i in seeAll:
                item['id'].append(i[0])
                item['excel_id'].append(i[1])
                item['category'].append(i[2])
                item['Project_province'].append(i[3])
                item['Project_district'].append(i[4])
                item['contractor'].append(i[5])
                item['Is_it_operator'].append(i[6])
                item['contractor_address'].append(i[7])
                item['Project_name'].append(i[8])
                item['contract_amount'].append(i[9])
                item['contract_date'].append(i[10])
                item['invoice_num'].append(i[11])
                item['invoice_code'].append(i[12])
                item['invoice_amount'].append(i[13])
                item['invoice_date'].append(i[14])
                item['from_excel_path'].append(i[15])
                item['excel_rownum'].append(i[16])
                item['after_treatment'].append(i[17])
                item['perfectItem'].append(i[18])
                item['after_treatment_mark'].append(i[19])
                item['Name'] .append(i[20])

        df = pd.DataFrame(item)
        cursor.close()
        return df
                # if item['invoice_code'] not in oneItem.keys():
                #     oneItem[str(item['invoice_code'])] = []
                # oneItem[str(item['invoice_code'])].append(item)
                # llist.append(oneItem)


        # cursor.close()
        # return oneItem
        # return llist

    def usePathGetMYSQLINFO(self,excelPath):
        item = dict(id=[], excel_id=[], category=[], Project_province=[], Project_district=[], contractor=[],
                    Is_it_operator=[], contractor_address=[], Project_name=[], contract_amount=[], contract_date=[],
                    invoice_num=[], invoice_code=[], invoice_amount=[], invoice_date=[], from_excel_path=[],
                    excel_rownum=[], after_treatment=[], perfectItem=[], after_treatment_mark=[], Name=[])
        cursor = self.db.cursor()

        sqlCode = '''
                SELECT * FROM table6 WHERE from_excel_path = '{}'
                '''.format(excelPath)


        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()

        for i in seeAll:
            item['id'].append(i[0])
            item['excel_id'].append(i[1])
            item['category'].append(i[2])
            item['Project_province'].append(i[3])
            item['Project_district'].append(i[4])
            item['contractor'].append(i[5])
            item['Is_it_operator'].append(i[6])
            item['contractor_address'].append(i[7])
            item['Project_name'].append(i[8])
            item['contract_amount'].append(i[9])
            item['contract_date'].append(i[10])
            item['invoice_num'].append(i[11])
            item['invoice_code'].append(i[12])
            item['invoice_amount'].append(i[13])
            item['invoice_date'].append(i[14])
            item['from_excel_path'].append(i[15])
            item['excel_rownum'].append(i[16])
            item['after_treatment'].append(i[17])
            item['perfectItem'].append(i[18])
            item['after_treatment_mark'].append(i[19])
            item['Name'].append(i[20])
        df = pd.DataFrame(item)
        cursor.close()
        return df



if __name__ == "__main__":
    pass
















    # for i in df.index:




    # for x,y in df:
    #     print(df.info())
    #     # print('')
    #     # print(y)
    #     print('-------------')




    # mysqldb.closeDB()
    # print(df.T.loc['perfectItem'])
    # for i in df.T.loc['perfectItem']:
    #     print(i)
    # a1 = df.T#表格反转
    # a3 =df.sort_values(by = ['invoice_code'])#根据发票代码进行排序。
    # a4 = a3.drop_duplicates(['invoice_code'])#发票号去重
    # a5 = a4.invoice_code#.loc[0]#获取独立发票号

    # a6 = df['perfectItem'].groupby([df.invoice_code,df.excel_rownum,df.id])
    # print(a6.count())
    # print('---------------------')
    # print(a6.size())
    # print(a5.values)a5所有的值，返回类型list
    # newSeries = Series(a5.values,index=list(range(len(a5))))#为本表所有去重后的发票代码建立新的series
    # newDF = pd.DataFrame(a5.values,index=list(range(len(a5))),columns=['invoiceCode'])#为本表所有去重后的发票代码建立新的DF
    # a7 = df.groupby([df.invoice_code])
    # print(a7)
    # # print(a7)
    # for x,y in a7:
    #     # print(x)
    #     # print(type(x))
    #     # print('**--**')
    #     print(y)
    #     # print(len(y))
    #     # print(type(y))
    #     print('---------------')
    #     # print(pd.isnull(y.contractor).index)
    #     y.category.fillna(method='pad',inplace=True)
    #     y.Project_province.fillna(method='pad', inplace=True)
    #     y.contractor.fillna(method='pad', inplace=True)
    #     y.Is_it_operator.fillna(method='pad', inplace=True)
    #     y.contractor_address.fillna(method='pad', inplace=True)
    #     y.Project_name.fillna(method='pad', inplace=True)
    #
    #     # y.fillna(method='bfill', inplace=True)
    #     print(y)
    #     print('**********************')
    #
    #     # df.dropna(inplace=True)
    #     # print(y.contractor.index)
    #     # for i in y.contractor.index:
    #     #     isitNone = y['contractor'].loc[i]
    #         # if not isitNone:
    #
    #     # if pd.isnull(y.contractor):
    #     #     y['contractor'].fillna(method='pad')
    #     #     print(y)
    #
    # print(df[(df.id==728857)])

    #     print(x[0])
    #     print(x[1])
    #     print(x[2])
    #
    #     print('')
    #     print(y.perfectItem != 1.0)
    #     print(y.values)
    #     print(y.columns)
    #     newDF = pd.DataFrame(y.values,index=y.columns)
    # print(newDF)






    # print(a5.values)a5所有的值，返回类型list
    # newSeries = Series(a5.values,index=list(range(len(a5))))#为本表所有去重后的发票代码建立新的series
    # newDF = pd.DataFrame(a5.values,index=list(range(len(a5))),columns=['invoiceCode'])#为本表所有去重后的发票代码建立新的DF







    # print(newDF)
    # a5['newIndex'] = range(a5.shape[0])
    # newDF = pd.DataFrame(df_duplicat.values,index=list(range(len(df_duplicat))),columns=[x for x in df_duplicat])
    # a6 = a5.set_index('newIndex')
    # print(a6)
    # listt = []
    # for i in range(3):
    #     aaa = a5.loc[i]
    #     print(aaa)
    #     listt.append(aaa)
    #
    # print(listt)


    # print([a5.loc[i] for i in range(len(a5))])

    # print(df.set_index('perfectItem').isnull)
    # print(df['perfectItem'].notnull)
    # print(df[df.perfectItem.notnull])
    # print(df.index(['perfectItem']).isnull)
    # print(df.drop_duplicates(['invoice_code']))


    # get_invoiceCode_list = mysqldb.get_invoiceCode_from_noMark_noPerfect()
    # df = mysqldb.get_needPrecessitem(get_invoiceCode_list)
    # df_duplicat = df.drop_duplicates(['invoice_code','Name'])
    # newDF = pd.DataFrame(df_duplicat.values,index=list(range(len(df_duplicat))),columns=[x for x in df_duplicat])
    #
    # for i in range(3,4):
    #     invoice_code = newDF.loc[i].invoice_code
    #     from_excel_path = newDF.loc[i].from_excel_path
    #
    #     sameinCode_excelPath = df[(df.invoice_code == invoice_code) & (df.from_excel_path == from_excel_path)]
    #     print(sameinCode_excelPath)
    #
    #     print(invoice_code)
    #     print(from_excel_path)





