# -*- coding: utf-8 -*-

from urllib import parse as urlparse
from urllib.parse import quote_plus
import pymysql, datetime
import pandas as pd
import numpy as np
from pandas import Series
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import sqlalchemy
from gcproject.settings import MYSQLINFO

badpass = urlparse.quote_plus(MYSQLINFO['PASSWORD'])

conStr = '''mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'''.format(USER=MYSQLINFO['USER'],
                                                                                               PASSWORD=badpass,
                                                                                               HOST=MYSQLINFO['HOST'],
                                                                                               PORT=MYSQLINFO['PORT'],
                                                                                               DBNAME=MYSQLINFO[
	                                                                                               'DBNAME'])

mysqlcon = sqlalchemy.create_engine(conStr)
Session = sessionmaker(bind=mysqlcon)
db_session = Session()


def get_dupurl(source):
	sqlexc = '''select page_url from ztbRawInfo where site = "{source}";'''.format(source=source)
	gettouple = mysqlcon.execute(sqlexc)
	llist = [x[0] for x in gettouple]
	return tuple(llist)


def corren_getInfo(source):
	# sqlexc = '''select id,page_url,title from ztbRawInfo where site = "{source}" limit 10;'''.format(source=source)
	sqlexc = '''select id,page_url,title from ztbRawInfo where site = "{source}";'''.format(source=source)
	gettouple = mysqlcon.execute(sqlexc)
	llist = []
	for i in gettouple:
		ddict = {}
		ddict['id'] = i[0]
		ddict['page_url'] = i[1]
		ddict['title'] = i[2]
		ddict['status'] = 0
		llist.append(ddict)
	return pd.DataFrame(llist)

def corren_updateInfo(updatePage_url,updateTitle,updateMinor_business_type,whereid):

	sqlexc = f"UPDATE ztbRawInfo SET page_url='{updatePage_url}', title='{updateTitle}',minor_business_type='{updateMinor_business_type}' WHERE id={whereid};"
	mysqlcon.execute(sqlexc)
	db_session.commit()



if __name__ == '__main__':

	'''
	66042		
	中标公示	
	www.tobaccobid.com	
	http://www.tobaccobid.com/detailTenderpublic.action?id=98	
	浙江省烟草公司绍兴市公司文件设计印刷制作服务中标公告	
	0	
	2013-03-26 00:00:00		
	2	
	2020-10-28 13:16:01	
	2020-10-28 13:16:01							
	印刷设计		
	'''
	import requests,re
	url = "http://search.tobaccobid.com/detailTenderpublic.action?id=98"
	# url = "http://search.tobaccobid.com/detailTenderpublic.action?id=12571"
	brow = requests.get(url=url)
	hhtml = brow.text
	id = 66042



	title = re.findall('''class="y3"><p><span>(.*?)</span>''',hhtml,re.M|re.S)
	Minor_business_type = re.findall("招标类型.*<span>(.*?)</span>",hhtml,re.M|re.S)
	# aa = regcom.search(hhtml)
	print(Minor_business_type)
	print(title)

	corren_updateInfo(updatePage_url=url,updateTitle=title[0],updateMinor_business_type=Minor_business_type[0],whereid=id)






	exit()
	site = '''www.tobaccobid.com'''

	df = corren_getInfo(site)
	df.to_csv('atobaccobid.csv')

	import csv

	url1 = "https://search.tobaccobid.com/detailTenderpublic.action?id=44987"
	url2 = "https://search.tobaccobid.com/detailTenderpublic.action?id=44111111111987"
	df = pd.read_csv('atobaccobid.csv', index_col=['id', 'page_url', 'title'])

	import json

	df = corren_getInfo(site)
	# print(df)
	# df.set_index('page_url',inplace=True)
	# print(df)
	# a = df[(df['page_url'] == url)]
	# print(a)
	# a = df.iloc[df['page_url'].isin([url])]
	# df.iat()
	# print(df.columns)
	# print(df.index)
	#
	getInfo_1 = df[df['page_url'] == url1]
	a1 = getInfo_1.any()
	if a1.id:
		print('a1')
	print(a1)
	print('-------------------*')
	print(getInfo_1.iloc[0]['title'])


