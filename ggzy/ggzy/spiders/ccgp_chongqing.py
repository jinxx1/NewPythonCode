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
import sqlalchemy
from ggzy.redis_dup import BloomFilter
bl = BloomFilter('uxue:url')
ROOT = '../pageNum/ccgp_chongqing/'

MYSQLINFO1 = {
	"HOST": "183.6.136.67",
	"DBNAME": "jxtest",
	"USER": "jinxiao_67",
	"PASSWORD": "Qwer1234AQ",
	"PORT": 3306
}
conStr1 = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO1['USER'],
                                                                                            PASSWORD=MYSQLINFO1[
	                                                                                            'PASSWORD'],
                                                                                            HOST=MYSQLINFO1['HOST'],
                                                                                            PORT=MYSQLINFO1['PORT'],
                                                                                            DBNAME=MYSQLINFO1[
	                                                                                            'DBNAME'])
mysqlcon1 = sqlalchemy.create_engine(conStr1)

update_jxtest_exc = "UPDATE cqslq SET status=1 WHERE id={};"


def get_jxtest():
	exc = "SELECT id,articleId FROM cqslq WHERE status=0 ORDER BY issueTime DESC;"
	all = mysqlcon1.execute(exc)
	llist = []
	for i in all:
		ddict = {}
		ddict['id'] = i[0]
		ddict['artid'] = i[1]
		llist.append(ddict)
	if llist:
		return llist
	else:
		return None


class CcgpChongqingSpider(scrapy.Spider):
	name = 'ccgp_chongqing'
	cname="重庆市政府采购网"
	allowed_domains = ['www.ccgp-chongqing.gov.cn']
	baseUrl = "https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/new?__platDomain__=www.ccgp-chongqing.gov.cn&endDate={todaytime}&pi={pi}&ps={pageS}&startDate={todaytime}"


	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpChongqingSpider, self).__init__(*args, **kwargs)
		self.pageS = 200
		self.goon = goon


	def start_requests(self):

		if self.goon == 'no':
			meta = {}
			meta['startTime'] = datetime.datetime.now().strftime("%Y-%m-%d")
			meta['endTime'] = meta['startTime']
			# meta['startTime'] = "2021-05-21"
			# meta['endTime'] = "2021-05-25"
			meta['Num'] = 1

			yield scrapy.Request(url=self.baseUrl.format(
				todaytime=meta['startTime'],
	            pi=meta['Num'],
	            pageS=self.pageS),
			                     callback=self.parseYES,
			                     meta=meta,
			                     dont_filter=True
			                     )
		else:
			meta = {}
			allInfo = get_jxtest()
			for num,i in enumerate(allInfo):
				artcleBaseUrl = "https://www.ccgp-chongqing.gov.cn/notices/detail/{}"
				postUrlbase = "https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/{}?__platDomain__=www.ccgp-chongqing.gov.cn"
				page_url = artcleBaseUrl.format(i['artid'])
				if page_url in self.dupurl:
					mysqlcon1.execute(update_jxtest_exc.format(i['id']))
					continue
				meta['page_url'] = page_url
				meta['mysqlid'] = i['id']
				meta['artid'] = i['artid']
				postUrl = postUrlbase.format(i['artid'])
				yield scrapy.Request(url=postUrl,
				                     callback=self.parseA,
				                     meta=meta,
				                     dont_filter=True)


	def parseYES(self, response):
		meta = response.meta
		artcleBaseUrl = "https://www.ccgp-chongqing.gov.cn/notices/detail/{}"
		postUrlbase = "https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/{}?__platDomain__=www.ccgp-chongqing.gov.cn"
		jsonT = json.loads(response.text)
		try:
			if len(jsonT['notices']) == 0:
				return None
		except:
			return None
		mark = 0
		for i in jsonT['notices']:
			meta['page_url'] = ''
			meta['page_url'] = artcleBaseUrl.format(i['id'])
			if bl.exists(meta['page_url']):
				mark += 1
				continue
			postUrl = postUrlbase.format(i['id'])
			yield scrapy.Request(url=postUrl,
			                     callback=self.parseA,
			                     meta=meta,
			                     dont_filter=True
			                     )

		if mark == len(jsonT['notices']):
			return None
		else:
			meta['Num'] += 1
			yield scrapy.Request(url=self.baseUrl.format(
				todaytime=meta['startTime'],
				pi=meta['Num'],
				pageS=self.pageS),
								callback=self.parseYES,
								meta=meta,
								dont_filter=True)


	def parse(self, response):
		meta = response.meta
		if meta['status'] == meta['Num']:
			return None
		artcleBaseUrl = "https://www.ccgp-chongqing.gov.cn/notices/detail/{}"
		postUrlbase = "https://www.ccgp-chongqing.gov.cn/gwebsite/api/v1/notices/stable/{}?__platDomain__=www.ccgp-chongqing.gov.cn"
		jsonT = json.loads(response.text)
		try:
			if len(jsonT['notices']) == 0:
				return None
		except:
			return None
		notices = []
		for n in jsonT['notices']:
			n['crawlStatus'] = 0
			notices.append(n)
		fileName = ROOT + meta['startTime'] + '_' + meta['endTime'] + '_' + str(meta['Num']) + ".json"
		with open(fileName, 'w', encoding='utf-8') as f:
			json.dump(notices, f, ensure_ascii=False)
		print('{}已经保存到本地'.format(fileName))

		mark = 0


		if mark == self.pageS and self.goon == 'no':
			for num, n in enumerate(self.allTime):
				if meta['startTime'] == n['begin']:
					self.allTime[num]['pageNum'] = meta['Num']
			with open('../pageNum/ccgp_chongqing_allTime.json', 'w') as f:
				json.dump(self.allTime, f)
			return None

		else:
			meta['Num'] += 1
			for num, n in enumerate(self.allTime):
				if meta['startTime'] == n['begin']:
					self.allTime[num]['pageNum'] = meta['Num']
			with open('../pageNum/ccgp_chongqing_allTime.json', 'w') as f:
				json.dump(self.allTime, f)

			yield scrapy.Request(
				url=self.start_urls['1'].format(startime=meta['startTime'], endtime=meta['endTime'],
				                                pageS=self.pageS, pi=meta['Num']),
				callback=self.parse,
				dont_filter=True,
				meta=meta)


	def parseA(self, response):
		meta = response.meta
		item = GgzyItem()

		item['site'] = self.allowed_domains[0]
		item['page_url'] = meta['page_url']
		item['province_name'] = '重庆市'

		jsonT = json.loads(response.text)
		if '成功' not in jsonT['msg']:
			print('-----msg没有成功---------------{}---------{}------{}'.format(meta['startTime'], meta['endTime'],
			                                                                meta['Num']))
			return None

		item['title'] = jsonT['notice']['title'][0:199]
		try:
			item['subclass'] = jsonT['notice']['projectPurchaseWayName']
		except:
			item['subclass'] = '无分类'
		item['content'] = jsonT['notice']['html']
		item['issue_time'] = get_timestr(jsonT['notice']['issueTime'], "%Y-%m-%d %H:%M:%S")
		try:
			if len(jsonT['notice']['attachments']) > 2:
				json_attach = json.loads(jsonT['notice']['attachments'])
				item['attchment'] = []
				for i in json_attach:
					ddict = {}
					ddict['download_url'] = "https://www.ccgp-chongqing.gov.cn/" + i['value']
					ddict['name'] = i['name']
					item['attchment'].append(ddict)
		except:
			pass

		# item['content'] = len(item['content'])
		# pprint.pprint(item)
		# print('-------------------------------{}---------{}------{}'.format(meta['startTime'],meta['endTime'],meta['Num']))
		if self.goon=="yes":
			mysqlcon1.execute(update_jxtest_exc.format(meta['mysqlid']))
			

		yield item
