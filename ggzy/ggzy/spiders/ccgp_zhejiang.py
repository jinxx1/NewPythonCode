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
import pandas as pd
from ggzy.redis_dup import BloomFilter
bl = BloomFilter('uxue:url')
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

update_jxtest_exc = "UPDATE ccgp_zhejiang SET type=1 WHERE _id={};"

def getBetweenDay(begin_date):
	date_list = []
	begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
	end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
	while begin_date <= end_date:
		date_str = begin_date.strftime("%Y-%m-%d")
		date_list.append(date_str)
		begin_date += datetime.timedelta(days=1)
	return date_list
def get_jxtest():
	exc = "SELECT _id,id,title,url,districtName,typeName FROM ccgp_zhejiang WHERE type=0 ORDER BY pubDate DESC limit 100;"
	all = mysqlcon1.execute(exc)
	llist = []
	for i in all:
		ddict = {}
		ddict['_id'] = i[0]
		ddict['id'] = i[1]
		ddict['title'] = i[2]
		ddict['url'] = i[3]
		ddict['districtName'] = i[4]
		ddict['typeName'] = i[5]
		llist.append(ddict)
	if llist:
		return llist
	else:
		return None

class CcgpZhejiangSpider(scrapy.Spider):
	name = 'ccgp_zhejiang'
	cname = "浙江政府采购网"
	allowed_domains = ['www.ccgp-zhejiang.gov.cn']


	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpZhejiangSpider, self).__init__(*args, **kwargs)
		self.pageS = 100
		self.goon = goon
		self.baseUrl = "https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?pageSize={pageS}&pageNo={pageNum}&sourceAnnouncementType=10016%2C3012%2C1002%2C1003%2C3014%2C3013%2C3009%2C4004%2C3008%2C2001%2C3001%2C3020%2C3003%2C3002%2C3011%2C3017%2C3018%2C3005%2C3006%2C3004%2C4005%2C4006%2C3007%2C3015%2C3010%2C3016%2C6003%2C4002%2C4001%2C4003%2C8006%2C1995%2C1996%2C1997%2C8008%2C8009%2C8013%2C8014%2C9002%2C9003%2C808030100%2C7003%2C7004%2C7005%2C7006%2C7007%2C7008%2C7009&isGov=true&pubDate={startTime}+&endDate={endTime}+&isExact=1&url=notice"

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		if self.goon == 'no':
			meta['startTime'] = datetime.datetime.now().strftime("%Y-%m-%d")
			meta['endTime'] = meta['startTime']
			yield scrapy.Request(url=self.baseUrl.format(
				pageS=self.pageS,
				pageNum=meta['Num'],
				startTime=meta['startTime'],
				endTime=meta['endTime']),
				callback=self.parse,
				dont_filter=True,
				meta=meta
			)
		elif self.goon == 'yes':
			while True:
				aList = get_jxtest()
				if not aList:
					break
				for num, i in enumerate(aList):
					# if num > 1:
					# 	continue
					meta['_id'] = i['_id']
					if i['url'] in self.dupurl:
						mysqlcon1.execute(update_jxtest_exc.format(meta['_id']))
						continue
					meta['page_url'] = i['url']
					meta['title'] = i['title']
					meta['id'] = i['id']
					meta['province_name'] = i['districtName']
					meta['subclass'] = i['typeName']
					artcleBase = "https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?noticeId={}&url=noticeDetail"
					yield scrapy.Request(url=artcleBase.format(meta['id']),
						callback=self.parseA,
						dont_filter=True,
						meta=meta
					)
		else:
			return None

	def parse(self, response):
		meta = response.meta
		jsonT = json.loads(response.text)
		count = jsonT['count'] // self.pageS
		print('----------本页共有{}篇文章------------'.format(len(jsonT['articles'])))

		mark = 0
		for i in jsonT['articles']:

			if bl.exists(i['url']):
				mark += 1
				continue
			meta['page_url'] = i['url']
			meta['subclass'] = i['typeName']
			meta['province_name'] = i['districtName']
			artcleBase = "https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results?noticeId={}&url=noticeDetail"
			yield scrapy.Request(url=artcleBase.format(i['id']),
			                     callback=self.parseA,
			                     dont_filter=True,
			                     meta=meta
			                     )

		if mark == self.pageS:
			return None
		else:
			if meta['Num'] == count + 1:
				return None
			meta['Num'] += 1
			yield scrapy.Request(url=self.baseUrl.format(
				pageS=self.pageS,
				pageNum=meta['Num'],
				startTime=meta['startTime'],
				endTime=meta['endTime']),
				callback=self.parse,
				dont_filter=True,
				meta=meta
			)

	def parseA(self, response):
		meta = response.meta
		item = GgzyItem()
		try:
			jsonT = json.loads(response.text)
			item['content'] = jsonT['noticeContent']
			item['issue_time'] = get_timestr(jsonT['noticePubDate'].split('.')[0], "%Y-%m-%d %H:%M:%S")
			item['title'] = jsonT['noticeTitle']
		except:
			return None

		item['site'] = self.allowed_domains[0]
		item['page_url'] = meta['page_url']
		item['province_name'] = meta['province_name']
		item['subclass'] = meta['subclass']

		soup = BeautifulSoup(item['content'], 'lxml')
		hrefall = soup.find_all(href=re.compile("aliyuncs"))
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


		if self.goon=="yes":
			mysqlcon1.execute(update_jxtest_exc.format(meta['_id']))

		yield item

	def parseYES(self, response):
		meta = response.meta
		jsonT = json.loads(response.text)
		try:
			if not jsonT['articles']:
				return None
		except:
			return None

		df = pd.DataFrame(jsonT['articles'])
		count = jsonT['count'] // self.pageS
		df['type'] = 0

		a = df.to_sql(name='ccgp_zhejiang', con=mysqlcon1, if_exists='append', index=False, chunksize=1000)
		print(a)
		print('共有  ---',len(jsonT['articles']))
		print("------------------------------------------------------",meta['startTime'],meta['Num'])

		if meta['Num'] == count + 1:
			return None
		else:
			meta['Num'] += 1
			yield scrapy.Request(url=self.baseUrl.format(
				pageS=self.pageS,
				pageNum=meta['Num'],
				startTime=meta['startTime'],
				endTime=meta['endTime']),
				callback=self.parseYES,
				dont_filter=True,
				meta=meta
			)
