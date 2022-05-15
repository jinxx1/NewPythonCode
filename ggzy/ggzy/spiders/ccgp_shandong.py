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


header_raw = '''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: close
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


def shandong_regex_content(HTML):
	reg = re.findall("<style.*?</style>", HTML, re.M | re.S)
	for i in reg:
		HTML = HTML.replace(i, '')
	return HTML


class CcgpShandongSpider(scrapy.Spider):
	name = 'ccgp_shandong'
	allowed_domains = ['www.ccgp-shandong.gov.cn']
	cname = "山东政府采购网"


	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpShandongSpider, self).__init__(*args, **kwargs)
		self.pageS = 100
		self.goon = goon
		self.base_url = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp'
		self.urlList = [
			{'catName': '山东省_采购公告', 'url': '0301', 'grade': 'province'},
			{'catName': '山东省_单一来源公示', 'url': '2102', 'grade': 'province'},
			{'catName': '山东省_结果公告', 'url': '0302', 'grade': 'province'},
			{'catName': '山东省_废标公告', 'url': '0306', 'grade': 'province'},
			{'catName': '山东省_合同公开', 'url': '2502', 'grade': 'province'},
			{'catName': '山东省_验收公开', 'url': '2503', 'grade': 'province'},
			{'catName': '山东省_意向公开', 'url': '2500', 'grade': 'province'},
			{'catName': '山东省_信息更正', 'url': '0305', 'grade': 'province'},

			{'catName': '山东省_市县需求(意向)公开', 'url': '2504', 'grade': 'city'},
			{'catName': '山东省_市县采购公告', 'url': '0303', 'grade': 'city'},
			{'catName': '山东省_市县单一来源公示', 'url': '2106', 'grade': 'city'},
			{'catName': '山东省_信息更正', 'url': '0305', 'grade': 'city'},
			{'catName': '山东省_市县结果公告', 'url': '0304', 'grade': 'city'},
			{'catName': '山东省_废标公告', 'url': '0306', 'grade': 'city'},
			{'catName': '山东省_市县合同公开', 'url': '2505', 'grade': 'city'},
			{'catName': '山东省_市县验收公开', 'url': '2506', 'grade': 'city'},

		]

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		if self.goon == 'no':
			for i in self.urlList:
				meta['catName'] = i['catName']
				meta['url'] = i['url']
				meta['datapost'] = {}
				meta['datapost']['colcode'] = meta['url']
				meta['datapost']['grade'] = i['grade']
				meta['datapost']['curpage'] = str(meta['Num'])
				yield scrapy.FormRequest(url=self.base_url,
				                         formdata=meta['datapost'],
				                         callback=self.parse,
				                         meta=meta,
				                         dont_filter=True,
				                         headers=HEA
				                         )
		elif self.goon == 'yes':
			pass
		else:
			print('pls input yes or no')
			return None

	def parse(self, response):
		meta = response.meta
		link = response.xpath("//span[@class='title']//a/@href").extract()
		# print(response.text)
		if not link:
			print('-----------------------------not link')
			return None
		mark = 0
		for i in link:
			page_url = parse.urljoin(response.url, i)
			if bl.exists(page_url):
				mark += 1
				continue

			meta['title'] = response.xpath("//*[@href = '{}']/@title".format(i)).extract_first()
			issueTime = response.xpath(
				"//*[@href = '{ul}']/../../span[@class='hits']/text()|//*[@href = '{ul}']/../../../span[@class='hits']/text()".format(
					ul=i)).extract_first()

			meta['issueTime'] = get_timestr(issueTime, "%Y-%m-%d %H:%M:%S")
			meta['page_url'] = parse.urljoin(response.url, i)


			yield scrapy.Request(url=meta['page_url'],
			                     callback=self.parseA,
			                     meta=meta,
			                     dont_filter=True,
			                     headers=HEA
			                     )

		if mark == len(link):
			return None
		meta['Num'] += 1
		meta['datapost']['curpage'] = str(meta['Num'])
		yield scrapy.FormRequest(url=self.base_url,
		                         formdata=meta['datapost'],
		                         callback=self.parse,
		                         meta=meta,
		                         dont_filter=True,
		                         headers=HEA
		                         )

	def parseA(self, response):
		meta = response.meta
		item = GgzyItem()
		html1 = response.xpath("//div[@id= 'textarea']").extract()
		if not html1:
			# print('-----------not html1')
			return None
		item['content'] = shandong_regex_content(''.join(html1))

		try:
			item['issue_time'] = get_timestr(
				re.findall("发布时间：(\d{2,4}年\d{1,2}月\d{1,2}日 \d{1,2}时\d{1,2}分\d{1,2}秒)", response.text)[0],
				outformat="%Y-%m-%d %H:%M:%S")
			if not item['issue_time']:
				item['issue_time'] = meta['issueTime']
		except:
			item['issue_time'] = meta['issueTime']

		if not item['issue_time']:
			# print('-------------not issue_time')
			return None

		item['page_url'] = meta['page_url']
		item['site'] = self.allowed_domains[0]
		item['title'] = meta['title']
		item['subclass'] = meta['catName']
		item['province_name'] = '山东省'

		soup = BeautifulSoup(item['content'], 'lxml')
		hrefall = soup.find_all(href=re.compile("attach"))
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
		# print('-------------------------------------------',meta['Num'])
		yield item
