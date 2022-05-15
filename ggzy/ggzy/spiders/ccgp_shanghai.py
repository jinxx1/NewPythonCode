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
HEA = {
	"Accept": "*/*",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
	# "Connection": "keep-alive",
	# "Content-Length": "162",
	"Content-Type": "application/json"
}


def timeuniTOstr(timecode):
	import time
	time_local = time.localtime(int(timecode) / 1000)
	return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


class CcgpShanghaiSpider(scrapy.Spider):
	name = 'ccgp_shanghai'
	allowed_domains = ['www.zfcg.sh.gov.cn']
	cname = "上海政府采购网"
	urlList = [{'subclass': '上海市_上海市本级_采购意向公开', 'districtCode': '319900', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_其他区_采购意向公开', 'districtCode': '310099', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_黄浦区_采购意向公开', 'districtCode': '310101', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_徐汇区_采购意向公开', 'districtCode': '310104', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_长宁区_采购意向公开', 'districtCode': '310105', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_静安区_采购意向公开', 'districtCode': '310106', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_普陀区_采购意向公开', 'districtCode': '310107', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_虹口区_采购意向公开', 'districtCode': '310109', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_杨浦区_采购意向公开', 'districtCode': '310110', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_闵行区_采购意向公开', 'districtCode': '310112', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_宝山区_采购意向公开', 'districtCode': '310113', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_嘉定区_采购意向公开', 'districtCode': '310114', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_浦东新区_采购意向公开', 'districtCode': '310115', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_金山区_采购意向公开', 'districtCode': '310116', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_松江区_采购意向公开', 'districtCode': '310117', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_青浦区_采购意向公开', 'districtCode': '310118', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_奉贤区_采购意向公开', 'districtCode': '310120', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_崇明区_采购意向公开', 'districtCode': '310151', 'categoryCode': 'ZcyAnnouncement10016'}, {'subclass': '上海市_上海市本级_单一来源公示', 'districtCode': '319900', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_其他区_单一来源公示', 'districtCode': '310099', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_黄浦区_单一来源公示', 'districtCode': '310101', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_徐汇区_单一来源公示', 'districtCode': '310104', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_长宁区_单一来源公示', 'districtCode': '310105', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_静安区_单一来源公示', 'districtCode': '310106', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_普陀区_单一来源公示', 'districtCode': '310107', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_虹口区_单一来源公示', 'districtCode': '310109', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_杨浦区_单一来源公示', 'districtCode': '310110', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_闵行区_单一来源公示', 'districtCode': '310112', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_宝山区_单一来源公示', 'districtCode': '310113', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_嘉定区_单一来源公示', 'districtCode': '310114', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_浦东新区_单一来源公示', 'districtCode': '310115', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_金山区_单一来源公示', 'districtCode': '310116', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_松江区_单一来源公示', 'districtCode': '310117', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_青浦区_单一来源公示', 'districtCode': '310118', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_奉贤区_单一来源公示', 'districtCode': '310120', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_崇明区_单一来源公示', 'districtCode': '310151', 'categoryCode': 'ZcyAnnouncement1'}, {'subclass': '上海市_上海市本级_采购公告', 'districtCode': '319900', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_其他区_采购公告', 'districtCode': '310099', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_黄浦区_采购公告', 'districtCode': '310101', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_徐汇区_采购公告', 'districtCode': '310104', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_长宁区_采购公告', 'districtCode': '310105', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_静安区_采购公告', 'districtCode': '310106', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_普陀区_采购公告', 'districtCode': '310107', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_虹口区_采购公告', 'districtCode': '310109', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_杨浦区_采购公告', 'districtCode': '310110', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_闵行区_采购公告', 'districtCode': '310112', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_宝山区_采购公告', 'districtCode': '310113', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_嘉定区_采购公告', 'districtCode': '310114', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_浦东新区_采购公告', 'districtCode': '310115', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_金山区_采购公告', 'districtCode': '310116', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_松江区_采购公告', 'districtCode': '310117', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_青浦区_采购公告', 'districtCode': '310118', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_奉贤区_采购公告', 'districtCode': '310120', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_崇明区_采购公告', 'districtCode': '310151', 'categoryCode': 'ZcyAnnouncement2'}, {'subclass': '上海市_上海市本级_更正公告', 'districtCode': '319900', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_其他区_更正公告', 'districtCode': '310099', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_黄浦区_更正公告', 'districtCode': '310101', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_徐汇区_更正公告', 'districtCode': '310104', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_长宁区_更正公告', 'districtCode': '310105', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_静安区_更正公告', 'districtCode': '310106', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_普陀区_更正公告', 'districtCode': '310107', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_虹口区_更正公告', 'districtCode': '310109', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_杨浦区_更正公告', 'districtCode': '310110', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_闵行区_更正公告', 'districtCode': '310112', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_宝山区_更正公告', 'districtCode': '310113', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_嘉定区_更正公告', 'districtCode': '310114', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_浦东新区_更正公告', 'districtCode': '310115', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_金山区_更正公告', 'districtCode': '310116', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_松江区_更正公告', 'districtCode': '310117', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_青浦区_更正公告', 'districtCode': '310118', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_奉贤区_更正公告', 'districtCode': '310120', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_崇明区_更正公告', 'districtCode': '310151', 'categoryCode': 'ZcyAnnouncement3'}, {'subclass': '上海市_上海市本级_采购结果公告', 'districtCode': '319900', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_其他区_采购结果公告', 'districtCode': '310099', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_黄浦区_采购结果公告', 'districtCode': '310101', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_徐汇区_采购结果公告', 'districtCode': '310104', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_长宁区_采购结果公告', 'districtCode': '310105', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_静安区_采购结果公告', 'districtCode': '310106', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_普陀区_采购结果公告', 'districtCode': '310107', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_虹口区_采购结果公告', 'districtCode': '310109', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_杨浦区_采购结果公告', 'districtCode': '310110', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_闵行区_采购结果公告', 'districtCode': '310112', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_宝山区_采购结果公告', 'districtCode': '310113', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_嘉定区_采购结果公告', 'districtCode': '310114', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_浦东新区_采购结果公告', 'districtCode': '310115', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_金山区_采购结果公告', 'districtCode': '310116', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_松江区_采购结果公告', 'districtCode': '310117', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_青浦区_采购结果公告', 'districtCode': '310118', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_奉贤区_采购结果公告', 'districtCode': '310120', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_崇明区_采购结果公告', 'districtCode': '310151', 'categoryCode': 'ZcyAnnouncement4'}, {'subclass': '上海市_上海市本级_采购合同公告', 'districtCode': '319900', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_其他区_采购合同公告', 'districtCode': '310099', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_黄浦区_采购合同公告', 'districtCode': '310101', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_徐汇区_采购合同公告', 'districtCode': '310104', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_长宁区_采购合同公告', 'districtCode': '310105', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_静安区_采购合同公告', 'districtCode': '310106', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_普陀区_采购合同公告', 'districtCode': '310107', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_虹口区_采购合同公告', 'districtCode': '310109', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_杨浦区_采购合同公告', 'districtCode': '310110', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_闵行区_采购合同公告', 'districtCode': '310112', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_宝山区_采购合同公告', 'districtCode': '310113', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_嘉定区_采购合同公告', 'districtCode': '310114', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_浦东新区_采购合同公告', 'districtCode': '310115', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_金山区_采购合同公告', 'districtCode': '310116', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_松江区_采购合同公告', 'districtCode': '310117', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_青浦区_采购合同公告', 'districtCode': '310118', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_奉贤区_采购合同公告', 'districtCode': '310120', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_崇明区_采购合同公告', 'districtCode': '310151', 'categoryCode': 'ZcyAnnouncement5'}, {'subclass': '上海市_上海市本级_终止公告', 'districtCode': '319900', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_其他区_终止公告', 'districtCode': '310099', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_黄浦区_终止公告', 'districtCode': '310101', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_徐汇区_终止公告', 'districtCode': '310104', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_长宁区_终止公告', 'districtCode': '310105', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_静安区_终止公告', 'districtCode': '310106', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_普陀区_终止公告', 'districtCode': '310107', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_虹口区_终止公告', 'districtCode': '310109', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_杨浦区_终止公告', 'districtCode': '310110', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_闵行区_终止公告', 'districtCode': '310112', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_宝山区_终止公告', 'districtCode': '310113', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_嘉定区_终止公告', 'districtCode': '310114', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_浦东新区_终止公告', 'districtCode': '310115', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_金山区_终止公告', 'districtCode': '310116', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_松江区_终止公告', 'districtCode': '310117', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_青浦区_终止公告', 'districtCode': '310118', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_奉贤区_终止公告', 'districtCode': '310120', 'categoryCode': 'ZcyAnnouncement6'}, {'subclass': '上海市_崇明区_终止公告', 'districtCode': '310151', 'categoryCode': 'ZcyAnnouncement6'}]
	#urlList = [{'subclass': '上海市_上海市本级_采购公告', 'districtCode': '319900', 'categoryCode': 'ZcyAnnouncement2'}]

	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpShanghaiSpider, self).__init__(*args, **kwargs)
		self.pageS = 100
		self.goon = goon
		self.base_url = 'http://www.zfcg.sh.gov.cn/front/search/category'

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		for i in self.urlList:
			meta['subclass1'] = i['subclass']
			meta['districtCode'] = i['districtCode']
			meta['categoryCode'] = i['categoryCode']
			datepost = {
				"districtCode": [str(meta['districtCode']), ],
				"utm": "sites_group_front.5b1ba037.0.0.876326d0df9711eb8a905d1e2bc2a29f",
				"categoryCode": str(meta['categoryCode']),
				"pageSize": str(self.pageS),
				"pageNo": str(meta['Num'])}

			yield scrapy.Request(url=self.base_url,
			                     method='POST',
			                     callback=self.parse,
			                     dont_filter=True,
			                     meta=meta,
			                     body=json.dumps(datepost), headers=HEA)

	def parse(self, response):
		meta = response.meta
		jsonT = json.loads(response.text)['hits']
		allPage = int(jsonT['total']) // self.pageS + 1
		mark = 0
		for num, i in enumerate(jsonT['hits']):
			# if num > 10:
			# 	continue
			meta['page_url'] = parse.urljoin(response.url, i['_source']['url'])
			if bl.exists(meta['page_url']):
				mark += 1
				continue
			meta['issueTime'] = timeuniTOstr(int(i['_source']['publishDate']))
			meta['title'] = i['_source']['title']
			try:
				meta['subclass'] = meta['subclass1'] + "_" + i['_source']['procurementMethod']
			except:
				meta['subclass'] = meta['subclass1']
			yield scrapy.Request(url=meta['page_url'],
			                     callback=self.parseA,
			                     meta=meta,
			                     dont_filter=True)

		if meta['Num'] == allPage:
			return None
		if mark == self.pageS and self.goon == 'no':
			return None
		else:
			meta['Num'] += 1
			datepost = {
				"districtCode": [str(meta['districtCode']), ],
				"utm": "sites_group_front.5b1ba037.0.0.876326d0df9711eb8a905d1e2bc2a29f",
				"categoryCode": str(meta['categoryCode']),
				"pageSize": str(self.pageS),
				"pageNo": str(meta['Num'])}

			yield scrapy.Request(url=self.base_url, method='POST', callback=self.parse, dont_filter=True, meta=meta,
			                     body=json.dumps(datepost), headers=HEA)

	def parseA(self, response):
		meta = response.meta
		item = GgzyItem()
		try:
			contentJsonStr = response.xpath("//input[@name='articleDetail']/@value").extract_first()
			item['content'] = json.loads(contentJsonStr)['content']
		except Exception as ff:
			return None
		if not item['content']:
			return None
		item['issue_time'] = meta['issueTime']
		item['page_url'] = meta['page_url']
		item['site'] = self.allowed_domains[0]
		item['title'] = meta['title']
		item['subclass'] = meta['subclass']
		item['province_name'] = '上海市'

		# item['content'] = len(item['content'])
		# pprint.pprint(item)
		# print('--' * 50)
		yield item
