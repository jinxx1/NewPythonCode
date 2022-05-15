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
import pandas as pd
from ggzy.redis_dup import BloomFilter
bl = BloomFilter('uxue:url')

def attmenSTR(downLoad):
	import cgi
	from urllib.parse import unquote
	import requests
	ddict = {}
	ddict['download_url'] = downLoad
	iii = 0
	response = None
	while iii < 2:
		try:
			response = requests.head(url=downLoad,timeout=(15,15))
			break
		except:
			try:
				response = requests.get(url=downLoad, timeout=(15, 15))
				break
			except:
				iii += 1
	if not response:
		return None

	try:
		value, params = cgi.parse_header(response.headers['Content-Disposition'])
		name = params['filename'].encode('ISO-8859-1').decode('utf8')
		ddict['name'] = unquote(name, 'utf-8')
	except:
		ddict['name'] = downLoad.split('/')[-1]

	return ddict


class CcgpSichuanSpider(scrapy.Spider):
	name = 'ccgp_sichuan'
	allowed_domains = ['www.ccgp-sichuan.gov.cn']
	start_urls = ['www.ccgp-sichuan.gov.cn']
	cname = "四川政府采购网"

	def __init__(self, goon=None, *args, **kwargs):
		super(CcgpSichuanSpider, self).__init__(*args, **kwargs)
		self.pageS = 100
		self.goon = goon
		self.base_url = 'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=search&years=&chnlNames=\u6240\u6709&chnlCodes=&title=&tenderno=&agentname=&buyername=&startTime=&endTime=&distin_like=510000&city=&town=&cityText=\u8BF7\u9009\u62E9&townText=\u8BF7\u9009\u62E9&searchKey=&distin=&type=&beginDate=&endDate=&str1=&str2=&pageSize=10&curPage={}&searchResultForm=search_result_anhui.ftl'

	def start_requests(self):
		meta = {}
		if self.goon == 'yes' or self.goon == 'no':
			meta['Num'] = 1
		else:
			meta['Num'] = int(self.goon)

		yield scrapy.Request(url=self.base_url.format(str(meta['Num'])),
		                     callback=self.parse,
		                     meta=meta,
		                     dont_filter=True)

	def parse(self, response):
		meta = response.meta
		link = response.xpath("//div[@class = 'info']/ul/li/a/@href").extract()

		if not link:
			print('-----------------------------not link')
			return None
		mark = 0
		for i in link:
			page_url = urlparse.urljoin(response.url, i)
			if bl.exists(page_url):
				mark += 1
				continue
			meta['page_url'] = page_url

			issTime = response.xpath("//*[@href = '{hreff}']/../div[@class = 'time curr']/text()|//*[@href = '{hreff}']/../div[@class = 'time curr']/span/text()".format(hreff=i)).extract()
			issTiem_labeList = [x.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ','') for x in issTime if x.replace(' ','').replace('\r', '').replace('\n', '').replace('\t', '')]
			issTiem_labe1 = issTiem_labeList[1] + '-' + issTiem_labeList[0]
			meta['issueTime'] = get_timestr(issTiem_labe1,outformat='%Y-%m-%d %H:%M:%S')
			yield scrapy.Request(url=meta['page_url'],
			                     callback=self.parseA,
			                     meta=meta,
			                     dont_filter=True
			                     )

		if mark == len(link) and self.goon == 'no':
			return None

		meta['Num'] += 1
		if meta['Num'] == 30000:
			return None
		yield scrapy.Request(url=self.base_url.format(str(meta['Num'])),
		                     callback=self.parse,
		                     meta=meta,
		                     dont_filter=True)

	def parseA(self, response):

		meta = response.meta
		item = GgzyItem()
		html1 = response.xpath(
			"//div[@id= 'myPrintArea']|//table[@class ='public-table']|//div[@class='cont-info']").extract()
		if not html1:
			print('-----------not html1')
			return None
		item['content'] = ''.join(html1)

		item['title'] = response.xpath("//h1/text()").extract_first()
		if not item['title']:
			print('-----------not title')
			return None

		try:
			catAll = response.xpath("//div[@class='siteBox']/a/@title").extract()
			lbword = ''
			for i in range(len(catAll) - 1):
				lbword = lbword + '_' + catAll[i]
			catName1 = '四川省_' + lbword.replace(' ', '').replace('\t', '').strip()
			catName2 = catName1.replace('__首页', '')
		except:
			return None
		item['subclass'] = catName2

		try:
			item['issue_time'] = get_timestr(
				re.findall("系统发布时间：(\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})", response.text)[0],
				outformat="%Y-%m-%d %H:%M:%S")
			if not item['issue_time']:
				item['issue_time'] = meta['issueTime']
		except:
			item['issue_time'] = meta['issueTime']

		if not item['issue_time']:
			print('no  -----------  issue time')
			return None
		item['page_url'] = meta['page_url']
		item['site'] = self.allowed_domains[0]
		item['province_name'] = '四川省'

		soup = BeautifulSoup(item['content'], 'lxml')
		attch_strList = [
			'download', 'pload', 'open-doc', 'Attach',
		]
		item['attchment'] = []
		for attchWord in attch_strList:
			hrefall = soup.find_all(href=re.compile(attchWord))
			for nn in hrefall:
				print('--------------nn--------------')
				print(nn.get('href'))
				download_url = urlparse.urljoin('http://www.ccgp-sichuan.gov.cn', nn.get('href'))
				ddict = attmenSTR(download_url)
				if not ddict:
					continue
				item['attchment'].append(ddict)
		if not item['attchment']:
			del item['attchment']

		# item['content'] = len(item['content'])
		# pprint.pprint(item)
		# print('-------------------------------------------',meta['Num'])
		yield item
