# -*- coding: utf-8 -*-
import os

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
from gcproject.settings import MYSQLINFO
root = os.getcwd()
filePath = os.path.join(root,'csv/all.csv')

conStr_94 = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO['PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO['DBNAME'])
mysqlcon_94_final = sqlalchemy.create_engine(conStr_94)
MYSQLINFO_99 = {
    "HOST": "172.16.10.99",
    "DBNAME": "shangqing",
    "USER": "xey",
    "PASSWORD": "Xey123456!@#$%^",
    "PORT":3306
}
conStr_99 = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO_99['USER'],
                                                                                           PASSWORD=MYSQLINFO_99['PASSWORD'],
                                                                                           HOST=MYSQLINFO_99['HOST'],
                                                                                           PORT=MYSQLINFO_99['PORT'],
                                                                                           DBNAME=MYSQLINFO_99['DBNAME'])
mysqlcon_99_test = sqlalchemy.create_engine(conStr_94)

def get_test_ztbRawInfo():
	exc = '''SELECT id,subclass,site,page_url,title,issue_time,creation_time,end_time,province_name,city_name,purchase_type,business_type,minor_business_type FROM ztbRawInfo WHERE creation_time > "2021-03-25"'''
	a1 = mysqlcon_99_test.execute(exc)
	a2 = tuple(a1)

	df = pd.DataFrame(a2,columns=['id','subclass','site','page_url','title','issue_time','creation_time','end_time','province_name',
	                             'city_name','purchase_type','business_type','minor_business_type'])
	df['status'] = 0

	df.to_csv(filePath,encoding='utf-8')
	return df

def get_test_content(id):
	exc = '''SELECT content FROM ztbRawInfoContent WHERE raw_data_id={}'''.format(id)
	a = mysqlcon_99_test.execute(exc)
	for i in a:
		content = i[0]
		break

	return content

def get_test_attment(ids):
	exc = '''SELECT * FROM ztbInfoAttachment WHERE raw_id={};'''.format(ids)
	aa = mysqlcon_99_test.execute(exc)
	attment = []
	print(aa)
	for i in aa:
		print(i)
		print('-------------')




if __name__ == '__main__':
	allInfo = pd.read_csv(filePath,header=0)
	for i in range(len(allInfo)):
		id = allInfo.iloc[i]['id']
		print(id)

