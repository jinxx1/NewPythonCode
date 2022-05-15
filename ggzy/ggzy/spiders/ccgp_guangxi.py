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


class CcgpGuangxiSpider(scrapy.Spider):
	name = 'ccgp_guangxi'
	allowed_domains = ['www.ccgp-guangxi.gov.cn']
	cname = '广西省政府采购网'

	# dupurl = []
	start_urls = [{'name': '公开招标公告', 'code': 'ZcyAnnouncement3001'}, {'name': '竞争性谈判公告', 'code': 'ZcyAnnouncement3002'},
	              {'name': '询价公告', 'code': 'ZcyAnnouncement3003'},
	              {'name': '公开招标资格预审公告', 'code': 'ZcyAnnouncement2001'},
	              {'name': '邀请招标资格预审公告', 'code': 'ZcyAnnouncement3008'},
	              {'name': '竞争性磋商公告', 'code': 'ZcyAnnouncement3011'},
	              {'name': '其他采购项目公告', 'code': 'ZcyAnnouncement2002'},
	              {'name': '允许采购进口产品公示', 'code': 'ZcyAnnouncement3013'},
	              {'name': '邀请招标公告', 'code': 'ZcyAnnouncement3020'},
	              {'name': '中标（成交）结果公告', 'code': 'ZcyAnnouncement3004'},
	              {'name': '中标公告', 'code': 'ZcyAnnouncement4005'}, {'name': '成交公告', 'code': 'ZcyAnnouncement4006'},
	              {'name': '邀请招标资格入围公告', 'code': 'ZcyAnnouncement3009'},
	              {'name': '废标公告', 'code': 'ZcyAnnouncement3007'}, {'name': '终止公告', 'code': 'ZcyAnnouncement3015'},
	              {'name': '公开招标资格入围公告', 'code': 'ZcyAnnouncement4004'},
	              {'name': '其他采购结果公告', 'code': 'ZcyAnnouncement4007'},
	              {'name': '采购合同公告', 'code': 'ZcyAnnouncement3010'}, {'name': '更正公告', 'code': 'ZcyAnnouncement3005'},
	              {'name': '澄清（修改）公告', 'code': 'ZcyAnnouncement3006'},
	              {'name': '采购结果变更公告', 'code': 'ZcyAnnouncement3017'},
	              {'name': '其他更正公告', 'code': 'ZcyAnnouncement3019'},
	              {'name': '中止（暂停）公告', 'code': 'ZcyAnnouncement3018'},
	              {'name': '采购文件需求公示', 'code': 'ZcyAnnouncement3014'},
	              {'name': '单一来源公示', 'code': 'ZcyAnnouncement3012'},
	              {'name': '在线询价合同公告', 'code': 'ZcyAnnouncement5001'},
	              {'name': '反向竞价合同公告', 'code': 'ZcyAnnouncement7001'},
	              {'name': '协议供货合同公告', 'code': 'ZcyAnnouncement8001'},
	              {'name': '反向竞价终止公告', 'code': 'ZcyAnnouncement8003'},
	              {'name': '电子卖场成交公告-采购成功', 'code': 'ZcyAnnouncement8013'},
	              {'name': '定点服务合同公告', 'code': 'ZcyAnnouncement9001'},
	              {'name': '网上超市合同公告', 'code': 'ZcyAnnouncement9005'},
	              {'name': '履约验收公告', 'code': 'ZcyAnnouncement3016'}, {'name': '其他公告', 'code': 'ZcyOtherAnnouncement'},
	              {'name': '建设工程招标公告', 'code': 'ZcyAnnouncement8031'},
	              {'name': '建设工程中标（成交）结果公告', 'code': 'ZcyAnnouncement8032'},
	              {'name': '建设工程更正公告', 'code': 'ZcyAnnouncement8033'}]

	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpGuangxiSpider, self).__init__(*args, **kwargs)
		self.pageS = 100
		self.goon = goon
		self.baseUrl = 'http://www.ccgp-guangxi.gov.cn/front/search/category'

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
		for num,x in enumerate(jsonT['hits']['hits']):
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
			# print('-'*50,meta['Num'])
			yield scrapy.Request(url=meta['page_url'],
			                     callback=self.parseA,
			                     meta=meta,
			                     headers=HEA,
			                     )
		if mark == len(jsonT['hits']['hits']) and self.goon == 'no':
			return None
		meta['Num'] += 1
		dataPost = {"categoryCode": str(meta['code']),"pageNo": str(meta['Num']),"pageSize": str(self.pageS)}
		yield scrapy.Request(url=self.baseUrl,method='POST',callback=self.parse,meta=meta,headers=HEA,body=json.dumps(dataPost))

	def parseA(self,response):
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
		try:
			item['attchment'] = []
			for nn in jsonT['attachmentVO']['attachments']:
				ddict = {}
				ddict['download_url'] = urlparse.urljoin(jsonT['attachmentVO']['domain'],nn['fileId'])
				ddict['name'] = nn['name']
				item['attchment'].append(ddict)
			if not item['attchment']:
				del item['attchment']
		except Exception as f:
			print('------------------attchment error')
			print(f)

		item['title'] = meta['title']
		item['subclass'] = meta['subclass']
		item['page_url'] = meta['page_url']
		item['issue_time'] = meta['issue_time']
		item['province_name'] = meta['province_name']
		item['site'] = self.allowed_domains[0]

		# item['content'] = len(item['content'])
		# pprint.pprint(item)
		# print('*-'*50)
		yield item