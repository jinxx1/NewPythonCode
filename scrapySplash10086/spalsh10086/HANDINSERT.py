# coding=utf-8
import re
from bs4 import BeautifulSoup
import sqlalchemy
from pymysql.converters import escape_string
import pymysql, datetime
import pandas as pd
import numpy as np
from pandas import Series
import pprint



# '''chrome_options.add_argument('--proxy-server=http://171.37.135.94:8123')'''
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_colwidth', 500)

splitA = "selectResult('"
splitB = "https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id="
splitC = "')"
splitD = ''


def get_timestr(date, outformat="%Y-%m-%d", combdata=False):
	import time
	time_array = ''
	format_string = [
		"%Y-%m-%d %H:%M:%S",
		"%Y-%m-%d %H:%M",
		"%Y-%m-%d %H",
		"%Y-%m-%d",
		"%Y/%m/%d %H:%M:%S",
		"%Y/%m/%d %H:%M",
		"%Y/%m/%d %H",
		"%Y/%m/%d",
		"%Y.%m.%d %H:%M:%S",
		"%Y.%m.%d %H:%M",
		"%Y.%m.%d %H",
		"%Y.%m.%d",
		"%Y年%m月%d日 %H:%M:%S",
		"%Y年%m月%d日 %H:%M",
		"%Y年%m月%d日 %H",
		"%Y年%m月%d日",
		"%Y_%m_%d %H:%M:%S",
		"%Y_%m_%d %H:%M",
		"%Y_%m_%d %H",
		"%Y_%m_%d",
		"%Y%m%d%H:%M:%S",
		"%Y%m%d %H:%M:%S",
		"%Y%m%d %H:%M",
		"%Y%m%d %H",
		"%Y%m%d",
		"%Y%m%d%H%M%S",
		"%Y%m%d %H%M%S",
		"%Y%m%d %H%M",
		"%Y%m%d %H",
		"%Y%m%d",
		"%Y\%m\%d %H:%M:%S",
		"%Y\%m\%d %H:%M",
		"%Y\%m\%d %H",
		"%Y\%m\%d",
		"%Y年%m月%d日%H:%M:%S",
		"%Y年%m月%d日%H:%M",
		"%Y年%m月%d日%H",
		"%Y年%m月%d日",
	]
	for i in format_string:

		try:
			time_array = time.strptime(date, i)
		except:
			continue

	if not time_array:
		return None
	timeL1 = int(time.mktime(time_array))
	timeL = time.localtime(timeL1)
	if combdata:
		return time.strftime(outformat, timeL), timeL1
	else:
		return time.strftime(outformat, timeL)

def mysqlcon():
	MYSQLINFO = {
		"HOST": "183.6.136.67",
		"DBNAME": "jxtest",
		"USER": "jinxiao_67",
		"PASSWORD": "Qwer1234AQ",
		"PORT": 3306
	}
	conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
	                                                                                           PASSWORD=MYSQLINFO[
		                                                                                           'PASSWORD'],
	                                                                                           HOST=MYSQLINFO['HOST'],
	                                                                                           PORT=MYSQLINFO['PORT'],
	                                                                                           DBNAME=MYSQLINFO[
		                                                                                           'DBNAME'])
	mysqlcon = sqlalchemy.create_engine(conStr)
	return mysqlcon

def get_urlList():
	excWord = "SELECT page_url FROM listform10086;"
	alltoup = mysqlcon().execute(excWord)
	return tuple([x[0] for x in alltoup])

urlCut = get_urlList()

def readExcel(excelPath, sheetDict,readTime):
	countdf = []
	for keyName in sheetDict.keys():
		df = pd.read_excel(excelPath,
		                   sheet_name=sheetDict[keyName],
		                   usecols="A:B",
		                   names=['page_url', 'issue_time'],
		                   header=None)
		df['subclass'] = sheetDict[keyName]
		countdf.append(df)
	DF = pd.concat(countdf)
	if not readTime:
		DF.issue_time.fillna(datetime.datetime.now().strftime('%Y-%m-%d 00:00:00'), inplace=True)
	else:
		DF.issue_time.fillna(readTime, inplace=True)

	nullDF = pd.DataFrame()
	writer = pd.ExcelWriter(excelPath)
	for i in sheetDict.keys():
		nullDF.to_excel(writer, sheet_name=sheetDict[i], index=False)
	writer.save()

	return DF.reset_index(drop=True)


def applyTime(x):
	return get_timestr(x, '%Y-%m-%d %H:%M:%S')


def urldup(url):
	if url in urlCut:
		return 1
	else:
		return 0


if __name__ == '__main__':
	catName = {'caigou': '采购公告', 'zige': '资格预审公告', 'jieguo': '候选人公示', 'zhongxuan': '中选结果公示', 'danyi': '单一来源采购信息公告'}
	# readTime = ''
	readTime = '2021-11-08 00:00:00'
	# 				id号
	# //tr[@onmouseout = "cursorOut(this)"]/@onclick
	# 				时间和id
	# //tr[@onmouseout = "cursorOut(this)"]/@onclick|//tr[@onmouseout = "cursorOut(this)"]/td[4]/text()

	ePath = r"C:\Users\jinxx1\Desktop\10086hands.xlsx"
	
	exceldf = readExcel(excelPath=ePath, sheetDict=catName,readTime=readTime)

	exceldf['page_url'] = exceldf['page_url'].apply(lambda x: x.replace(splitA, splitB).replace(splitC, splitD))
	#
	exceldf['cut'] = exceldf['page_url'].apply(lambda x: urldup(x))
	exceldf.drop(exceldf[exceldf['cut'] == 1].index, inplace=True)
	exceldf.drop(['cut'], inplace=True, axis=1)
	exceldf.reset_index(drop=True, inplace=True)

	print(exceldf)
	print("共有  {}  篇文章未收录".format(len(exceldf)))
	insertInfo = exceldf.to_sql(name='listform10086', con=mysqlcon(), if_exists='append', index=False, chunksize=1000)
	print(insertInfo)
