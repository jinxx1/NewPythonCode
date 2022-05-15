# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint
from urllib import parse
from bs4 import BeautifulSoup
from ggzy.items import GgzyItem
from ggzy.parseScrpy import get_timestr
from ggzy.mysqlprecess import get_dupurl
import time
from dateutil.relativedelta import relativedelta
import datetime
import sqlalchemy
import os
from ggzy.redis_dup import BloomFilter

bl = BloomFilter('uxue:url')
header_raw = '''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Content-Type: application/json;charset=UTF-8
Host: www.ccgp-jiangsu.gov.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36
X-Requested-With: XMLHttpRequest'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


def stmeTime(time_str, today=True):
	import time
	timeArray = time.strptime(time_str, "%Y-%m-%d")

	ddict = {}

	ddict['sd'] = time.mktime(timeArray)
	if today:
		ddict['ed'] = ddict['sd'] + (60 * 60 * 23.999)
	else:
		ddict['ed'] = ddict['sd'] + 86400
	ddict['sd'] = int(ddict['sd']) * 1000
	ddict['ed'] = int(ddict['ed']) * 1000
	return ddict


def file_name_walk(file_dir):
	import os
	listpath = []
	for root, dirs, files in os.walk(file_dir):
		dictTemp = {}
		dictTemp['root'] = root  # 当前目录路径
		dictTemp['dirs'] = dirs  # 当前路径下所有子目录
		dictTemp['files'] = files  # 当前路径下所有非目录子文件
		listpath.append(dictTemp)
	llistpath = []
	for i in listpath:
		if i['files']:
			for n in i['files']:
				pathName = os.path.join(i['root'], n)
				llistpath.append(pathName)
	return llistpath


root1 = os.getcwd()
root = os.path.join(root1, 'jiangsu')

subclass = {"cgyx": "采购意向",
            "dyly": "单一来源公示",
            "zgys": "资格预审",
            "cggg": "采购公告",
            "gkzb": "采购公告",
            "zbgg": "中标公告",
            "cjgg": "成交公告",
            "xjgg": "项目公告",
            "zzgg": "终止公告",
            "gzgg": "更正公告",
            "htgg": "合同公告",
            "jzcs": "竞争性磋商",
            "qtgg": "其它公告"}


class CcgpJiangsuSpider(scrapy.Spider):
	name = 'ccgp_jiangsu'
	cname = '江苏省政府采购'
	allowed_domains = ['www.ccgp-jiangsu.gov.cn']
	start_urls = ['2021-07-19', '2021-07-20']

	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpJiangsuSpider, self).__init__(*args, **kwargs)
		self.pageS = 200
		self.baseUrl = 'http://www.ccgp-jiangsu.gov.cn/pss/jsp/search_cggg.jsp?cgr=&xmbh=&pqy=&sd={sd}&ed={ed}&dljg=&cglx=&bt=&nr=&cgfs=&page={pageNum}'
		self.artcleBase = "http://www.ccgp-jiangsu.gov.cn/jiangsu/js_cggg/details.html?gglb={gglb}&ggid={ggid}"
		self.artclePostUrl = "http://www.ccgp-jiangsu.gov.cn/pss/jsp/relevantCgggGetById.jsp"
		self.goon = goon

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		if self.goon == 'yes':
			for i in self.start_urls:
				timesteam = stmeTime(i, today=False)
				meta['sd'] = timesteam['sd']
				meta['ed'] = timesteam['ed']
				yield scrapy.Request(url=self.baseUrl.format(sd=meta['sd'], ed=meta['ed'], pageNum=meta['Num']),
				                     dont_filter=True,
				                     callback=self.parse,
				                     meta=meta,
				                     headers=HEA)

		elif self.goon == 'no':
			Times = datetime.datetime.now().strftime("%Y-%m-%d")
			timesteam = stmeTime(Times, today=True)
			meta['sd'] = timesteam['sd']
			meta['ed'] = timesteam['ed']
			yield scrapy.Request(url=self.baseUrl.format(sd=meta['sd'], ed=meta['ed'], pageNum=meta['Num']),
			                     dont_filter=True,
			                     callback=self.parse,
			                     meta=meta,
			                     headers=HEA)

		elif self.goon == 'history':

			alljson = file_name_walk(root)
			for num, ifile in enumerate(alljson):

				# if num > 3:
				# 	continue
				file = open(ifile, 'r')
				papers = []
				for line in file.readlines():
					dic = json.loads(line)
					papers.append(dic)
				for ini in papers:
					jsonT = ini['result']['list']
					for ii in jsonT:
						meta = {}
						if jsonT:
							try:
								if not ii['ggCode'] or not ii['id']:
									continue
							except:
								continue

							meta['page_url'] = self.artcleBase.format(gglb=ii['ggCode'], ggid=ii['id'])
							if meta['page_url'] in self.dupurl:
								continue
							meta['ggid'] = ii['id']
							meta['issue_time'] = ii['publishDate']
							meta['title'] = ii['title']
							try:
								meta['subclass'] = subclass[ii['ggCode']]
							except:
								meta['subclass'] = '信息公告'
							postdate = {"ggid": meta['ggid']}
							HEAacrt = '''Accept: application/json, text/javascript, */*; q=0.01
							Accept-Encoding: gzip, deflate
							Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
							Connection: keep-alive
							Content-Length: 37
							Content-Type: application/x-www-form-urlencoded; charset=UTF-8
							Host: www.ccgp-jiangsu.gov.cn
							Origin: http://www.ccgp-jiangsu.gov.cn
							User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36
							X-Requested-With: XMLHttpRequest'''
							HEAacrt = dict(line.split(": ", 1) for line in HEAacrt.split("\n") if line != '')
							HEAacrt['Referer'] = ''
							HEAacrt['Referer'] = meta['page_url']
							# print(ii)
							# print('--------------------------------')
							yield scrapy.FormRequest(url=self.artclePostUrl,
							                         formdata=postdate,
							                         dont_filter=True,
							                         callback=self.parseA,
							                         meta=meta)
		else:
			print('pls input goon yes or no ')
			return None

	def parse(self, response):
		meta = response.meta
		jsonT = json.loads(response.text)['result']['list']

		if not jsonT:
			return None
		mark = 0
		for i in jsonT:
			try:
				if not i['ggCode'] or not i['id']:
					continue
			except:
				continue
			meta['page_url'] = self.artcleBase.format(gglb=i['ggCode'], ggid=i['id'])
			if bl.exists(meta['page_url']):
				mark += 1
				continue
			meta['ggid'] = i['id']
			meta['issue_time'] = i['publishDate']
			meta['title'] = i['title']
			try:
				meta['subclass'] = subclass[i['ggCode']]
			except:
				meta['subclass'] = '信息公告'
			postdate = {"ggid": meta['ggid']}
			HEAacrt = '''Accept: application/json, text/javascript, */*; q=0.01
			Accept-Encoding: gzip, deflate
			Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
			Connection: keep-alive
			Content-Length: 37
			Content-Type: application/x-www-form-urlencoded; charset=UTF-8
			Host: www.ccgp-jiangsu.gov.cn
			Origin: http://www.ccgp-jiangsu.gov.cn
			User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36
			X-Requested-With: XMLHttpRequest'''
			HEAacrt = dict(line.split(": ", 1) for line in HEAacrt.split("\n") if line != '')
			HEAacrt['Referer'] = ''
			HEAacrt['Referer'] = meta['page_url']

			yield scrapy.FormRequest(url=self.artclePostUrl,
			                         formdata=postdate,
			                         dont_filter=True,
			                         callback=self.parseA,
			                         meta=meta)

		meta['Num'] += 1
		if mark == len(jsonT) and self.goon == 'no':
			return None
		else:
			yield scrapy.Request(url=self.baseUrl.format(sd=meta['sd'], ed=meta['ed'], pageNum=meta['Num']),
			                     dont_filter=True,
			                     callback=self.parse,
			                     meta=meta,
			                     headers=HEA)

	def parseA(self, response):
		print('----into  parseA-------')
		meta = response.meta
		jsonT = json.loads(response.text)['data']
		item = GgzyItem()

		item['page_url'] = meta['page_url']
		item['site'] = self.allowed_domains[0]
		item['title'] = meta['title']
		item['subclass'] = meta['subclass']
		item['province_name'] = '江苏省'
		try:
			item['content'] = jsonT['content']
			if not item['content']:
				return None
		except:
			item['content'] = '''<p>本文无内容</p>'''

		item['issue_time'] = get_timestr(meta['issue_time'], outformat="%Y-%m-%d %H:%M:%S")
		if not item['issue_time']:
			item['issue_time'] = get_timestr(jsonT['publishDate'], outformat="%Y-%m-%d %H:%M:%S")
		if not item['issue_time']:
			return None

		try:
			item['attchment'] = []
			for nn in jsonT['files']:
				ddict = {}
				ddict['download_url'] = nn['url']
				ddict['name'] = nn['name']
				item['attchment'].append(ddict)
			if not item['attchment']:
				del item['attchment']
		except:
			pass

		# item['content'] = len(item['content'])
		# pprint.pprint(item)
		# print('-------------------------------------------')
		yield item

	def parse_yes(self, response):
		meta = response.meta
		pathName = str(meta['sd']) + "_" + str(meta['Num']) + ".json"
		filepath = os.path.join(root, pathName)

		jsonT = json.loads(response.text)
		if jsonT['result']['count'] < 1:
			return None
		else:
			with open(filepath, 'w') as f:
				json.dump(jsonT, f, ensure_ascii=False)
				f.flush()
				f.close()
				print('保存成功：', filepath)

		if jsonT['result']['totalPage'] == meta['Num']:
			return None
		else:
			meta['Num'] += 1
			yield scrapy.Request(url=self.baseUrl.format(sd=meta['sd'], ed=meta['ed'], pageNum=meta['Num']),
			                     dont_filter=True,
			                     callback=self.parse,
			                     meta=meta,
			                     headers=HEA)
