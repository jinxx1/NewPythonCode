# -*- coding: utf-8 -*-
import time
from redisBloomHash import bl
import json,requests,datetime




def creatHeader(header_raw):
	'''

	:param :将浏览器中拷贝出来的header信息，整理成dict格式。并只保留
	 ['accept', 'connection', 'accept-encoding', 'accept-control', 'accept-language', 'user-agent']
	 这些字段，同时将connection变为close
	:return: 一个可供requests调用的dict格式的headers
	'''

	headers = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')
	keys = ['content-type','accept', 'connection', 'accept-encoding', 'accept-control', 'accept-language', 'user-agent']
	ddict = {}
	for key in headers.keys():
		if key.lower() in keys:

			if key.lower() == 'connection':
				ddict[key] = 'close'
			else:
				ddict[key] = headers[key]
	return ddict


def get_timestr(date, outformat="%Y-%m-%d %H:%M:%S", combdata=False):
	import time
	time_array = ''
	format_string = [
		"%Y-%m-%d %H:%M:%S",
		"%Y-%m-%d %H:%M",
		"%Y-%m-%d %H",
		"%Y-%m-%d",
		"（%Y-%m-%d %H:%M:%S）",
		"（%Y-%m-%d %H:%M）",
		"（%Y-%m-%d %H）",
		"（%Y-%m-%d）",
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
			time_array = time.strptime(date.strip(), i)

		except:
			continue
	if not time_array:
		return None
	timeL1 = int(time.mktime(time_array))
	timeL = time.localtime(timeL1)
	if combdata:
		return time.strftime(outformat, timeL), timeL1
	else:
		# return timeL
		return time.strftime(outformat, timeL)


def sleepSec(one, two):
	'''
	:one和two是两个int。比如要生成1到9之间任意一个数字。 sleepSec（1,9）

	:return: 随机生成从one到two的任意一个int
	'''
	import random
	sleeptime = random.uniform(one, two)
	rou = 1
	times = round(sleeptime, rou)
	return times

def timestampREtimestr(timestamp):
	import time
	if len(str(timestamp)) == 13:
		time_stamp = float(timestamp/1000)
	if len(str(timestamp)) == 12:
		time_stamp = float(timestamp/100)
	if len(str(timestamp)) == 11:
		time_stamp = float(timestamp/10)
	if len(str(timestamp)) == 10:
		time_stamp = float(timestamp)
	if len(str(timestamp)) == 9:
		time_stamp = float(timestamp*10)
	if len(str(timestamp)) == 8:
		time_stamp = float(timestamp*100)
	if len(str(timestamp)) == 7:
		time_stamp = float(timestamp*1000)
	if len(str(timestamp)) == 6:
		time_stamp = float(timestamp*10000)

	timeArray = time.localtime(time_stamp)
	timestr = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
	return timestr


def getBetweenDayList(begin_date):
	'''
	:begin_date 早于今天的某一个时间，时间格式中必须带有%Y-%m-%d
	:return: 一个列表，排列从begin_date到今天的所有时间%Y-%m-%d
	'''
	import datetime, time
	date_list = []
	begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
	end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
	while begin_date <= end_date:
		date_str = begin_date.strftime("%Y-%m-%d")
		date_list.append(date_str)
		begin_date += datetime.timedelta(days=1)
	return date_list


def openJson(path):
	import json
	with open(path, 'rb') as ff:
		jsonT = json.load(ff)
		ff.close()
	return jsonT



def writeJson(path, jsonT):
	import json
	with open(path, 'w',encoding='utf-8') as ff:
		json.dump(jsonT, ff,ensure_ascii=False)
		ff.flush()
		ff.close()



def urlIsExist(urllist):
	HEA = {
		"Connection": "close",
	}
	posturlapi = 'http://183.6.136.70:8035/pc/api/caijiApi/urlIsExist'
	str_c = json.dumps(urllist)
	dataApi = {"urlListJson": str_c}
	try:
		a = requests.post(url=posturlapi, data=dataApi, headers=HEA)
		jsonT = json.loads(a.text)
		return jsonT['data']
	except:
		return None


def save_api(dict1):
	import requests, json
	HEA = {"Connection": "close"}
	try:
		a = requests.post(
			url='http://183.6.136.70:8035/pc/api/caijiApi/save',
			data=dict1,
			headers=HEA
		)
		if not bl.exists(dict1['url']):
			bl.insert(dict1['url'])
		return json.loads(a.text)
	except Exception as ff:
		print(ff)
		return None


def get_pagecount(articlecount,pageS):
	if articlecount % pageS == 0:
		allPage = articlecount // pageS
	else:
		allPage = articlecount // pageS + 1
	return allPage


def get_location(strword):
	'''

	:param strword: 根据strword分析其中蕴含的地理位置信息
	:return: 一个dict。
	'''
	import cpca
	item_return = {}
	if not isinstance(strword, str):
		return ''
	a = cpca.transform([strword], pos_sensitive=True)
	item_return['province'] = a.iloc[0]['省']
	item_return['country'] = a.iloc[0]['市']
	item_return['district'] = a.iloc[0]['区']
	item_return['address'] = a.iloc[0]['地址']
	item_return['adcode'] = a.iloc[0]['adcode']
	item_return['original'] = strword
	return item_return


def tureLocation(localName, title):
	'''

	:param localName: 给定一个地理名词，比如广东省。然后跟title中分析出来的地理信息做对比
	:param title: 从标题中分析地理信息
	:return: 如果localname和title中都没有出现地理信息。则返回空字段
			如果
	'''

	finalDict = {}
	finalDict['province_name'] = ''
	finalDict['city_name'] = ''
	finalDict['str1'] = ''

	title_l = get_location(title)
	localName_l = get_location(localName)

	if not title_l['province'] and not localName_l['province']:
		return finalDict

	if localName_l['province']:
		if title_l['province'] != localName_l['province']:
			finalDict['province_name'] = localName_l['province']
			finalDict['city_name'] = localName_l['country']
			finalDict['str1'] = localName_l['adcode']
			return finalDict

		if title_l['province'] == localName_l['province']:
			finalDict['province_name'] = title_l['province']
			finalDict['city_name'] = title_l['country']
			finalDict['str1'] = title_l['adcode']
			return finalDict

	if title_l['province']:
		finalDict['province_name'] = title_l['province']
		finalDict['city_name'] = title_l['country']
		finalDict['str1'] = title_l['adcode']
		return finalDict

if __name__ == '__main__':
	hub_HeadersWord = '''Accept: */*
	Accept-Encoding: gzip, deflate
	Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
	Connection: keep-alive
	Content-Length: 162
	Content-Type: application/json
	Host: www.ccgp-guizhou.gov.cn
	Origin: http://www.ccgp-guizhou.gov.cn
	User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36
	X-Requested-With: XMLHttpRequest'''
	a = creatHeader(hub_HeadersWord)
	print(a)