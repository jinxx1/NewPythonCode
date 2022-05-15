import csv
import os
import xlsxwriter
import pandas as pd
import datetime, time, pymysql
import pandas as pd
import numpy as np
from pandas import Series
import pprint,json

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.width', 5000)
# pd.set_option('display.unicode.ambiguous_as_wide', True)
# pd.set_option('display.unicode.east_asian_width', True)

from jzsc_mohurd2016.settings import MYSQLINFO
import sqlalchemy
from jzsc_mohurd2016.jzsc import JZSC
from jzsc_mohurd2016.decrypt import AESDecrypt


def get_Company_api(qyid='', keyWord=None):
	if not qyid:
		raise 'pls input qyid str'
	item = {}
	item['caDetailList'] = {}
	item['caDetailList']['id'] = 'caDetailList'
	item['caDetailList']['name'] = '企业资格认证汇总'
	item['caDetailList'][
		'url'] = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/caDetailList?qyId={}&pg=0&pgsz=15".format(
		qyid)
	item['compDetail'] = {}
	item['compDetail']['id'] = 'compDetail'
	item['compDetail']['name'] = '企业主要信息'
	item['compDetail'][
		'url'] = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/compDetail?compId={}".format(qyid)
	item['regStaffList'] = {}
	item['regStaffList']['id'] = 'regStaffList'
	item['regStaffList']['name'] = '企业注册人员信息'
	item['regStaffList'][
		'url'] = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/regStaffList?qyId={}&pg=0&pgsz=15".format(
		qyid)
	item['compPerformanceListSys'] = {}
	item['compPerformanceListSys']['id'] = 'compPerformanceListSys'
	item['compPerformanceListSys']['name'] = '企业主要参与的工程项目'
	item['compPerformanceListSys'][
		'url'] = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/compPerformanceListSys?qy_id={}&pg=0&pgsz=15".format(
		qyid)
	item['compCreditRecordList_mark_0'] = {}
	item['compCreditRecordList_mark_0']['id'] = 'compCreditRecordList_mark_0'
	item['compCreditRecordList_mark_0']['name'] = '企业不良行为'
	item['compCreditRecordList_mark_0'][
		'url'] = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/compCreditRecordList?compId={}&mark=0&pg=0&pgsz=15".format(
		qyid)
	item['compCreditRecordList_mark_1'] = {}
	item['compCreditRecordList_mark_1']['id'] = 'compCreditRecordList_mark_1'
	item['compCreditRecordList_mark_1']['name'] = '企业良好行为'
	item['compCreditRecordList_mark_1'][
		'url'] = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/compCreditRecordList?compId={}&mark=1&pg=0&pgsz=15".format(
		qyid)
	item['compCreditBlackList'] = {}
	item['compCreditBlackList']['id'] = 'compCreditBlackList'
	item['compCreditBlackList']['name'] = '企业黑名单纪录'
	item['compCreditBlackList'][
		'url'] = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/compCreditBlackList?compId={}&pg=0&pgsz=15".format(
		qyid)
	item['compPunishList'] = {}
	item['compPunishList']['id'] = 'compPunishList'
	item['compPunishList']['name'] = '企业失信联合惩戒记录'
	item['compPunishList'][
		'url'] = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/compPunishList?corpId={}&pg=0&pgsz=15".format(
		qyid)
	item['aptChange'] = {}
	item['aptChange']['id'] = 'aptChange'
	item['aptChange']['name'] = '企业变更记录'
	item['aptChange']['url'] = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/aptChange?qyId={}".format(
		qyid)
	if not keyWord:
		return item
	else:
		keys = ['caDetailList', 'compDetail', 'regStaffList', 'compPerformanceListSys', 'compCreditRecordList_mark_0',
		        'compCreditRecordList_mark_1', 'compCreditBlackList', 'compPunishList', 'aptChange']
		if keyWord not in keys:
			print(keys)
			raise 'pls input keyWord must into keys'
		else:
			return item[keyWord]

def path_walk_urlall(path):
	import os, json
	for roots, dirs, files in os.walk(path):
		if len(files) > 1:
			for file in files:
				filePath = os.path.join(roots, file)
				with open(filePath, 'r', encoding='utf-8') as ff:
					jsonT = json.load(ff)
				# meta['jsonInfo']['status']  0 未处理 1处理中  2 处理完毕
				if jsonT['status'] == 2:
					continue
				else:
					jsonT['filePath'] = filePath
					yield jsonT

def path_walk_hubSave(path):
	import os, json
	for roots, dirs, files in os.walk(path):
		if len(files) > 1:
			for file in files:
				filePath = os.path.join(roots, file)
				with open(filePath, 'r', encoding='utf-8') as ff:
					jsonT = json.load(ff)
				if jsonT['hub_crawl_status'] == 0:
					jsonT['hubfilePath'] = filePath
					yield jsonT

def get_fileCreatTime_nowTime_diff(path):
	import os, time, datetime
	datetimet = time.localtime(os.stat(path).st_ctime)
	tY = int(time.strftime('%Y', datetimet))
	tm = int(time.strftime('%m', datetimet))
	td = int(time.strftime('%d', datetimet))
	tH = int(time.strftime('%H', datetimet))
	tM = int(time.strftime('%M', datetimet))
	tS = int(time.strftime('%S', datetimet))
	nowTime = datetime.datetime.now()
	fileTime = datetime.datetime(tY, tm, td, tH, tM, tS)
	return abs((nowTime - fileTime).days)

def clearDebugLog(folder):
	import os
	for roots, dirs, files in os.walk(folder):
		if len(files) > 0:
			for file in files:
				filePath = os.path.join(roots, file)
				fileTimeDiff = get_fileCreatTime_nowTime_diff(filePath)
				if fileTimeDiff >= 10:
					os.remove(filePath)

def timeT():
	import time
	t = time.time()
	nowTime = lambda: int(round(t * 1000))
	return int(nowTime())

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def messageCreat(meta, message, filePath):
	if filePath:
		msgtemp = '''
\t......................({message})......................
\t|城市名称：{reg_Name}，
\t|城市编号：{reg_id}，
\t|apt名称：{apt_Name}，
\t|apt代码：{apt_id}，
\t|本页多少篇文章：{total}，
\t|当前页码：{pageNum},
\t|文件存储路径：{filepath}。
'''
		msg = msgtemp.format(
			message=message,
			reg_Name=meta['jsonInfo']['reg_Name'],
			reg_id=meta['jsonInfo']['reg_id'],
			apt_Name=meta['jsonInfo']['apt_Name'],
			apt_id=meta['jsonInfo']['apt_id'],
			total=meta['jsonInfo']['total'],
			pageNum=meta['jsonInfo']['crawled_pageNum'],
			filepath=filePath
		)
	else:
		msgtemp = '''
\t===========================({message})===========================
\t|城市名称：{reg_Name}，
\t|城市编号：{reg_id}，
\t|apt名称：{apt_Name}，
\t|apt代码：{apt_id}，
\t|本页多少篇文章：{total}，
\t|当前页码：{pageNum}。
		'''
		msg = msgtemp.format(
			message=message,
			reg_Name=meta['jsonInfo']['reg_Name'],
			reg_id=meta['jsonInfo']['reg_id'],
			apt_Name=meta['jsonInfo']['apt_Name'],
			apt_id=meta['jsonInfo']['apt_id'],
			total=meta['jsonInfo']['total'],
			pageNum=meta['jsonInfo']['crawled_pageNum']
		)
	return msg

if __name__ == "__main__":
	obj = JZSC()
	token = 'jkFXxgu9TcpocIyCKmJ+tfpxe/45B9dbWMUXhdY7vLWyqIWoTqxtJJiP93YFvaWLhpUUKvcMtoMqfGfwdLCb8g=='
	# token = 'jkFXxgu9TcpocIyCKmJ+tfpxe/45B9dbWMUXhdY7vLWyqIWoTqxtJJiP93YFvaWLhpUUKvcMtoMqfGfwdLC='

	qyid = '002105291254749233'
	keyStr = 'compDetail'
	companyAPI = get_Company_api(qyid, keyStr)

	decDate = obj.artinfo(apiUrl=companyAPI['url'], token=token)
	getdate = json.loads(decDate)
	pprint.pprint(getdate)

	print(companyAPI)
	# print(item.keys())

	exit()
