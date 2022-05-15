import scrapy
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
from ggzy.redis_dup import BloomFilter
bl = BloomFilter('uxue:url')
pageNumPath = r"../ggzy/pageNum/"


def shandong_regex_content(HTML):
	reg = re.findall("<style.*?</style>", HTML, re.M | re.S)
	for i in reg:
		HTML = HTML.replace(i, '')
	return HTML


class DealggzySpider(scrapy.Spider):
	name = 'dealggzy'
	allowed_domains = ['deal.ggzy.gov.cn']
	siteName = "全国公共资源交易中心"


	def __init__(self, goon=None, timeBegin="2020-12-22", timeEnd="2021-03-22", *args, **kwargs):
		super(DealggzySpider, self).__init__(*args, **kwargs)
		self.baseUrl = "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp"
		self.goon = goon
		if goon == "no":
			timeEnd = datetime.datetime.now().strftime("%Y-%m-%d")
			timeBegin = timeEnd
		if goon == 'yes':
			timeEnd_unix = datetime.datetime.today()
			timeBegin_3monthsBefore = timeEnd_unix - relativedelta(months=3)
			timeBegin = timeBegin_3monthsBefore.strftime("%Y-%m-%d")
			timeEnd = timeEnd_unix.strftime("%Y-%m-%d")

		self.ListformData = {
			"TIMEBEGIN_SHOW": timeBegin,
			"TIMEEND_SHOW": timeEnd,
			"TIMEBEGIN": timeBegin,
			"TIMEEND": timeEnd,
			"SOURCE_TYPE": "1",
			"DEAL_TIME": "06",
			"DEAL_CLASSIFY": "00",
			"DEAL_STAGE": "0000",
			"DEAL_PROVINCE": "0",
			"DEAL_CITY": "0",
			"DEAL_PLATFORM": "0",
			"BID_PLATFORM": "0",
			"DEAL_TRADE": "0",
			"isShowAll": "1",
			"FINDTXT": ""
		}

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		for i in ['1', '2']:
			if self.goon == 'yes':
				meta['pageNumFile'] = pageNumPath + self.name + "_" + i + ".txt"
				with open(meta['pageNumFile'], 'r') as f:
					infoPageNum = f.read()
				meta['Num'] = int(infoPageNum)

			meta['SOURCE_TYPE'] = i
			if meta['SOURCE_TYPE'] == '2':
				self.ListformData['DEAL_CLASSIFY'] = '01'
			self.ListformData['SOURCE_TYPE'] = meta['SOURCE_TYPE']
			self.ListformData['PAGENUMBER'] = str(meta['Num'])
			yield scrapy.FormRequest(url=self.baseUrl,
			                         formdata=self.ListformData,
			                         callback=self.parse,
			                         dont_filter=True,
			                         meta=meta)

	def parse(self, response):
		meta = response.meta
		try:
			jsonT = json.loads(response.text)
			jsonList = jsonT['data']
		except:
			return None
		mark = 0
		for i in jsonList:
			if bl.exists(i['url']):
				mark += 1
				continue
			meta['page_url'] = i['url']
			try:
				meta['issue_time'] = get_timestr(i['timeShow'], "%Y-%m-%d %H:%M:%S")
				meta['title'] = i['title']
			except:
				continue

			try:
				meta['subclass'] = i['stageShow']
			except:
				meta['subclass'] = 'No SubClass'

			try:
				meta['business_type'] = i['classifyShow']
			except:
				meta['business_type'] = ''

			try:
				meta['source'] = i['platformName']
			except:
				meta['source'] = ''

			try:
				meta['province_name'] = i['districtShow']
			except:
				meta['province_name'] = ''

			try:
				meta['industry'] = i['tradeShow']
			except:
				meta['industry'] = ''

			request_url = meta['page_url'].replace('/a/', '/b/')

			yield scrapy.Request(url=request_url,
			                     dont_filter=True,
			                     callback=self.parseA,
			                     meta=meta)
		if self.goon == 'yes':
			with open(meta['pageNumFile'], 'w') as f:
				f.write(str(meta['Num']))
				f.flush()
				f.close()

		if mark == len(jsonT['data']) and self.goon == 'no':
			return None
		elif meta['Num'] >= jsonT['ttlpage']:
			return None
		else:
			meta['Num'] += 1
			if meta['SOURCE_TYPE'] == '2':
				self.ListformData['DEAL_CLASSIFY'] = '01'
			self.ListformData['SOURCE_TYPE'] = meta['SOURCE_TYPE']
			self.ListformData['PAGENUMBER'] = str(meta['Num'])
			yield scrapy.FormRequest(url=self.baseUrl,
			                         formdata=self.ListformData,
			                         callback=self.parse,
			                         dont_filter=True,
			                         meta=meta
			                         )

	def parseA(self, response):
		meta = response.meta
		item = GgzyItem()

		content = response.xpath("//div[@id = 'mycontent']").extract()
		if not content:
			return None
		item['content'] = ''.join(content)

		try:
			timeRex = re.findall("<span>发布时间：(.*?)</span>", response.text)[0]
			item['issue_time'] = get_timestr(timeRex, "%Y-%m-%d %H:%M:%S")
		except:
			item['issue_time'] = meta['issue_time']

		item['site'] = self.allowed_domains[0]
		item['page_url'] = meta['page_url']
		item['title'] = meta['title']
		item['subclass'] = meta['subclass']

		item['business_type'] = meta['business_type']
		item['source'] = meta['source']
		item['province_name'] = meta['province_name']
		item['industry'] = meta['industry']

		if '山东' in item['province_name']:
			item['content'] = shandong_regex_content(item['content'])

		soup = BeautifulSoup(item['content'], 'lxml')
		hrefall = soup.find_all(href=re.compile("download"))
		item['attchment'] = []
		for nn in hrefall:

			ddict = {}
			ddict['download_url'] = nn.get('href')
			ddict['name'] = response.xpath("//*[@href = '{}']/text()".format(nn.get('href'))).extract_first()
			if not ddict['name']:
				continue
			item['attchment'].append(ddict)

		if not item['attchment']:
			del item['attchment']

		# item['content'] = len(item['content'])
		# pprint.pprint(item)
		# print('------------------------')
		yield item
