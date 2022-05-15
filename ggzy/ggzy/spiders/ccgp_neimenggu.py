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

header_raw = '''
Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


class CcgpNeimengguSpider(scrapy.Spider):
	name = 'ccgp_neimenggu'
	allowed_domains = ['www.ccgp-neimenggu.gov.cn', '202.99.230.233']


	start_urls = ['http://202.99.230.233/zfcgwslave/web/index.php?r=pro%2Fanndata',
	              'http://www.ccgp-neimenggu.gov.cn/zfcgwslave/web/index.php?r=pro%2Fanndata']

	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpNeimengguSpider, self).__init__(*args, **kwargs)
		self.pageS = 18
		self.goon = goon
		self.urlList = [{'subclass': '招标公告', 'urlid': ' 1'}, {'subclass': '招标更正公告', 'urlid': '2'},
		                {'subclass': '中标(成交)公告', 'urlid': '3'}, {'subclass': '中标(成交)更正公告', 'urlid': '4'},
		                {'subclass': '废标公告', 'urlid': '5'}, {'subclass': '资格预审公告', 'urlid': '6'},
		                {'subclass': '资格预审更正公告', 'urlid': '7'}]

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		if self.goon == 'no':
			meta['postTime'] = datetime.datetime.now().strftime("%Y-%m-%d")
		elif self.goon == 'yes':
			meta['postTime'] = ''
		else:
			print('pls input yes no')
			return None
		for nnum, n in enumerate(self.urlList):
			# if nnum>0:
			#     continue
			meta['subclass'] = n['subclass']
			meta['urlid'] = n['urlid']

			for num, i in enumerate(self.start_urls):
				# if num > 0:
				#     continue
				meta['postUrl'] = i
				dataPost = {
					'type_name': meta['urlid'],
					'purmet': '',
					'keyword': '',
					'annstartdate_S': meta['postTime'],
					'annstartdate_E': meta['postTime'],
					'annenddate_S': '',
					'annenddate_E': '',
					'byf_page': str(meta['Num']),
					'fun': 'cggg',
					'page_size': str(self.pageS),
				}
				yield scrapy.FormRequest(url=meta['postUrl'],
				                         formdata=dataPost,
				                         callback=self.parse,
				                         meta=meta,
				                         dont_filter=True, headers=HEA
				                         )

	def parse(self, response):
		meta = response.meta
		jsonT = json.loads(response.text)
		if not jsonT[0]:
			return None
		mark = 0
		for num, x in enumerate(jsonT[0]):
			# if num > 0:
			#     continue
			baseArcUrl = 'http://202.99.230.233/category/cgggg?tb_id={tb_id}&p_id={p_id}&type={type}'
			meta['page_url'] = baseArcUrl.format(tb_id=x['ay_table_tag'], p_id=x['wp_mark_id'], type=x['type'])
			if bl.exists(meta['page_url']):
				mark += 1
				continue
			issue_time = re.findall("(\d{2,4}-\d{1,2}-\d{1,2})", x['SUBDATE'])
			meta['issue_time'] = get_timestr(''.join(issue_time))
			meta['title'] = x['TITLE']

			yield scrapy.Request(url=meta['page_url'], callback=self.parseA, meta=meta, dont_filter=True)

		try:
			if meta['Num'] == int(jsonT[1]) / self.pageS:
				return None
		except:
			pass
		if mark == len(jsonT[0]) and self.goon == 'no':
			return None

		meta['Num'] += 1
		dataPost = {
			'type_name': meta['urlid'],
			'purmet': '',
			'keyword': '',
			'annstartdate_S': meta['postTime'],
			'annstartdate_E': meta['postTime'],
			'annenddate_S': '',
			'annenddate_E': '',
			'byf_page': str(meta['Num']),
			'fun': 'cggg',
			'page_size': str(self.pageS),
		}
		yield scrapy.FormRequest(url=meta['postUrl'],
		                         formdata=dataPost,
		                         callback=self.parse,
		                         meta=meta,
		                         dont_filter=True, headers=HEA
		                         )

	def parseA(self, response):
		meta = response.meta
		item = GgzyItem()
		content = response.xpath("//div[@id= 'noticeArea']").extract()
		if not content:
			print('no content')
			return None
		item['content'] = ''.join(content)

		soup = BeautifulSoup(response.text, 'lxml')
		hrefall = soup.find_all(href=re.compile("gpx-bid-file"))
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

		item['page_url'] = meta['page_url']
		item['title'] = meta['title']
		item['issue_time'] = meta['issue_time']
		item['subclass'] = meta['subclass']
		item['province_name'] = '内蒙古自治区'
		item['site'] = self.allowed_domains[0]

		# item['content'] = len(item['content'])
		# pprint.pprint(item)
		# print('--*'*50)
		yield item
