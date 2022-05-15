# -*- coding: utf-8 -*-
import sys

import json, os
import sqlalchemy
from sqlalchemy.engine import reflection
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, inspect, create_engine
import requests, datetime,time
from redis_dup import BloomFilter
bl = BloomFilter('uxue:url')

def encode64_forDonload(s):
	import base64
	s1 = s.encode('utf-8')
	a = base64.b64encode(s1)
	baseUrl = 'http://www.ccgp-hubei.gov.cn:8090/gpmispub/download?id={}'.format(a.decode('utf-8'))
	return baseUrl


def getBetweenDay(begin_date):
	date_list = []
	begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
	end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
	while begin_date <= end_date:
		date_str = begin_date.strftime("%Y-%m-%d")
		date_list.append(date_str)
		begin_date += datetime.timedelta(days=1)
	return date_list



def urlIsExist(urllist):

	return [x for x in urllist if not bl.exists(x)]
	# posturlapi = 'http://183.6.136.70:8035/pc/api/caijiApi/urlIsExist'
	# str_c = json.dumps(urllist)
	# dataApi = {"urlListJson": str_c}
	# try:
	# 	a = requests.post(url=posturlapi, data=dataApi, headers={"Connection": "close"})
	# 	# print(a.status_code)
	# 	jsonT = json.loads(a.text)
	# 	return jsonT['data']
	# except Exception as f:
	# 	print(f)
	# 	return 'error'

def save_api(dict1):

	try:
		dict1['attachmentListJson'] = json.dumps(dict1['attachmentListJson'], ensure_ascii=False)
	except:
		pass

	HEA = {
		"Connection": "close",
	}
	try:
		a = requests.post(url='http://183.6.136.70:8035/pc/api/caijiApi/save', data=dict1, headers=HEA)
		return json.loads(a.text)
	except Exception as f:
		print('save ERROR ---')
		return f


def get_timestr(date, outformat="%Y-%m-%d", combdata=False):
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


if __name__ == '__main__':
	url = 'xxxx'
	a = urlIsExist([url])
	print(a)