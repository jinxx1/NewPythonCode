# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint
from urllib import parse as urlparse
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
header_raw = '''Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: close
Content-Type: application/json;charset=utf-8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


class CcgpHeilongjiangSpider(scrapy.Spider):
	name = 'ccgp_heilongjiang'
	allowed_domains = ['hljcg.hlj.gov.cn']

	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpHeilongjiangSpider, self).__init__(*args, **kwargs)
		self.pageS = 100
		self.goon = goon
		self.baseUrl = "https://hljcg.hlj.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=94c965cc-c55d-4f92-8469-d5875c68bd04&channel=c5bff13f-21ca-4dac-b158-cb40accd3035&currPage={pageNum}&pageSize={pageS}&noticeType=00101,00103,00102,001032,001004,001006&regionCode=&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime"

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		yield scrapy.Request(url=self.baseUrl.format(pageNum=meta['Num'], pageS=self.pageS),
		                     dont_filter=True,
		                     meta=meta,
		                     callback=self.parse,

		                     )

	def parse(self, response):
		meta = response.meta
		jsonT = json.loads(response.text)
		mark = 0
		for x in jsonT['data']:
			page_url = urlparse.urljoin('https://hljcg.hlj.gov.cn/', x['pageurl'])
			if bl.exists(page_url):
				mark += 1
				continue
			meta['page_url'] = page_url
			meta['title'] = x['title']
			meta['issue_time'] = get_timestr(x['addtimeStr'])
			try:
				meta['subclass'] = x['fieldValues']['f_noticeTypeName']
			except:
				meta['subclass'] = '招投标信息'
			meta['province_name'] = '西藏自治区'

			yield scrapy.Request(url=page_url,
			                     callback=self.parseA,
			                     dont_filter=True,
			                     meta=meta,
			                     headers=HEA)

			if mark == len(jsonT['data']) and self.goon == 'no':
				return None
			if jsonT['total'] // self.pageS + 1 == meta['Num']:
				return None
			meta['Num'] += 1
			yield scrapy.Request(url=self.baseUrl.format(pageNum=meta['Num'], pageS=self.pageS),
			                     dont_filter=True,
			                     meta=meta,
			                     callback=self.parse,
			                     )

	def parseA(self, response):
		meta = response.meta
		item = GgzyItem()

		item['content'] = response.xpath("//div[@id = 'content']").extract_first()
		if not item['content']:
			return None

		item['page_url'] = meta['page_url']
		item['title'] = meta['title']
		item['issue_time'] = meta['issue_time']
		item['subclass'] = meta['subclass']
		item['province_name'] = meta['province_name']
		item['site'] = self.allowed_domains[0]

		soup = BeautifulSoup(response.text, 'lxml')
		hrefall = soup.find_all(href=re.compile("freecms/download"))
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
		# print('--*'*50)
		yield item
