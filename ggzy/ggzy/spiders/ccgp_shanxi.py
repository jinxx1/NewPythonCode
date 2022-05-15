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
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: close
Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36
'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')

def timestamp_to_timestr(stamp):
	import time
	# 转换成localtime
	time_local = time.localtime(stamp // 1000)
	# 转换成新的时间格式(2016-05-05 20:28:54)
	dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
	return dt

class CcgpShanxiSpider(scrapy.Spider):
	name = 'ccgp_shanxi'
	allowed_domains = ['www.ccgp-shanxi.gov.cn']
	cname = '山西省政府采购网'
	start_urls = [{'name': '公开招标公告', 'code': 'ZcyAnnouncement3001'}, {'name': '邀请招标公告', 'code': 'ZcyAnnouncement3020'},
	              {'name': '竞争性谈判公告', 'code': 'ZcyAnnouncement3002'},
	              {'name': '竞争性磋商公告', 'code': 'ZcyAnnouncement3011'}, {'name': '询价公告', 'code': 'ZcyAnnouncement3003'},
	              {'name': '公开招标资格预审公告', 'code': 'ZcyAnnouncement2001'},
	              {'name': '邀请招标资格预审公告', 'code': 'ZcyAnnouncement3008'},
	              {'name': '中标（成交）结果公告', 'code': 'ZcyAnnouncement3004'},
	              {'name': '终止公告', 'code': 'ZcyAnnouncement3015'}, {'name': '废标公告', 'code': 'ZcyAnnouncement3007'},
	              {'name': '采购结果变更公告', 'code': 'ZcyAnnouncement3017'},
	              {'name': '更正（变更）公告', 'code': 'ZcyAnnouncement3005'},
	              {'name': '澄清（修改）公告', 'code': 'ZcyAnnouncement3006'},
	              {'name': '中止（暂停）公告', 'code': 'ZcyAnnouncement3018'}, {'name': '合同公示', 'code': 'ZcyAnnouncement3010'},
	              {'name': '履约验收公告', 'code': 'ZcyAnnouncement3016'}, {'name': '采购需求公示', 'code': 'ZcyAnnouncement3014'},
	              {'name': '单一来源公示', 'code': 'ZcyAnnouncement3012'},
	              {'name': '进口产品论证意见公示', 'code': 'ZcyAnnouncement3013'},
	              {'name': '采购意向公开', 'code': 'ZcyAnnouncement10016'}]

	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpShanxiSpider, self).__init__(*args, **kwargs)
		self.pageS = 100
		self.goon = goon
		self.baseUrl = "http://www.ccgp-shanxi.gov.cn/front/search/category"

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		for num, i in enumerate(self.start_urls):
			# if num > 0:
			# 	continue
			meta['subclass'] = i['name']
			meta['code'] = i['code']
			dataPost = {
				"categoryCode": str(meta['code']),
				"districtCode": ["149900", "140100", "140200", "140300", "140400", "140500", "140600", "140700",
				                 "140800", "140900", "141000", "141100"],
				"pageNo": str(meta['Num']),
				"pageSize": str(self.pageS)
			}
			yield scrapy.Request(url=self.baseUrl,
			                     method='POST',
			                     callback=self.parse,
			                     meta=meta,
			                     headers=HEA,
			                     body=json.dumps(dataPost),
			                     )

	def parse(self, response):
		meta = response.meta
		jsonT = json.loads(response.text)
		if not jsonT['hits']['hits']:
			return None
		mark = 1
		for num, x in enumerate(jsonT['hits']['hits']):
			# if num >0:
			# 	continue
			page_url = urlparse.urljoin(response.url, x['_source']['url'])
			if bl.exists(page_url):
				mark += 1
				continue
			meta['title'] = x['_source']['title']
			try:
				meta['subclass'] = x['_source']['procurementMethod']
			except:
				meta['subclass'] = x['_source']['pathName']
			meta['page_url'] = page_url
			meta['issue_time'] = timestamp_to_timestr(x['_source']['publishDate'])
			meta['province_name'] = '广西省'
			# pprint.pprint(meta)
			# print('-'*50,meta['Num'],'___________parse')
			yield scrapy.Request(url=meta['page_url'],
			                     callback=self.parseA,
			                     meta=meta,
			                     headers=HEA,
			                     )
		if mark == len(jsonT['hits']['hits']) and self.goon == 'no':
			return None
		meta['Num'] += 1
		dataPost = {"categoryCode": str(meta['code']), "pageNo": str(meta['Num']), "pageSize": str(self.pageS)}
		yield scrapy.Request(url=self.baseUrl, method='POST', callback=self.parse, meta=meta, headers=HEA,
		                     body=json.dumps(dataPost))

	def parseA(self, response):
		meta = response.meta
		item = GgzyItem()

		jsonValue = response.xpath("//input[@name = 'articleDetail']/@value").extract_first()
		jsonT = json.loads(jsonValue)


		# 内容获取
		try:
			item['content'] = jsonT['content']
		except Exception as f:
			print('---------------- content error ----------------')
			print(f)
			return None
		if not item['content']:
			print('---------------- not content ----------------')
			return None
		# 附件获取

		soup = BeautifulSoup(item['content'], 'lxml')
		hrefall = soup.find_all(href=re.compile("sx2gov2open2"))
		item['attchment'] = []
		for nn in hrefall:
			ddict = {}
			ddict['download_url'] = nn.get('href')
			ddict['name'] = nn.get_text()
			if not ddict['name']:
				continue
			item['attchment'].append(ddict)
		if not item['attchment']:
			del item['attchment']

		item['title'] = meta['title']
		item['subclass'] = meta['subclass']
		item['page_url'] = meta['page_url']
		item['issue_time'] = meta['issue_time']
		item['province_name'] = meta['province_name']
		item['site'] = self.allowed_domains[0]

		# item['content'] = len(item['content'])
		# pprint.pprint(item)
		# print('*-' * 50)
		yield item
