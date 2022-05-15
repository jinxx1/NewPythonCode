# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint
from urllib import parse
from bs4 import BeautifulSoup
from gcproject.items import GcprojectItem
from gcproject.parseScrpy import get_location, get_timestr
from gcproject.mysqlprecess import get_dupurl, corren_getInfo, corren_updateInfo
from gcproject.sqlitedb_orm import sqlite_OBJ
import pandas as pd

subclass_list = [
	{'subclass': '招标公告', 'subclass_id': '1'},
	{'subclass': '招标变更', 'subclass_id': '2'},
	{'subclass': '中标公示', 'subclass_id': '3'}
]


class TobaccobidSpider(scrapy.Spider):
	name = 'tobaccobid'
	allowed_domains = ['www.tobaccobid.com']
	site = '烟草行业招投标信息平台'
	dupurl = get_dupurl(allowed_domains[0])
	start_urls = 'http://search.tobaccobid.com/searchTender.action?code=&area=0&type=0&date=0&keyName=&infoType={subclass}&pageNum={Num}'

	def __init__(self, goon=None, *args, **kwargs):
		super(TobaccobidSpider, self).__init__(*args, **kwargs)
		self.goon = goon
		if goon == 'correction':
			TableName = "atobaccobidTable"
			self.sqlitDB = sqlite_OBJ(dbName=TableName)

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		for subclass_unit in subclass_list:
			meta['subclass'] = subclass_unit['subclass']
			meta['subclass_id'] = subclass_unit['subclass_id']
			url = self.start_urls.format(subclass=meta['subclass_id'], Num=str(meta['Num']))
			if self.goon != 'correction':
				yield scrapy.Request(
					url=url,
					callback=self.parse,
					meta=meta,
					dont_filter=True
				)
			else:
				for i in self.sqlitDB.find_info(statusNum=4):
					meta['s_title'] = i['title']
					meta['s_page_url'] = i['page_url']
					meta['s_status'] = i['status']
					meta['s_id'] = i['id']
					cutWord = "http://www.tobaccobid.com/"
					truWord = "http://search.tobaccobid.com/"
					meta['url'] = meta['s_page_url'].replace(cutWord, truWord)


					yield scrapy.Request(
						url=meta['url'],
						callback=self.parse_correction,
						meta=meta,
						dont_filter=True
					)

	def parse(self, response):
		meta = response.meta
		link = response.xpath("//div[@class='righ2 fr']/ul[@class='lie1']/li/a/@href").extract()
		if not link:
			print('no link')
			return None
		mark = 0
		for num, i in enumerate(link):
			artUrl = parse.urljoin(response.url, i)
			if artUrl in self.dupurl:
				mark += 1
				continue

			titleCode = "//*[@href = '{}']/@title".format(i)
			Title = response.xpath(titleCode).extract_first()
			if not Title:
				continue
			meta['title'] = Title
			timeCode = "//*[@href = '{}']/../span[@class = 'fr']/text()".format(i)
			Time = response.xpath(timeCode).extract_first()
			if not Time:
				continue
			meta['issue_time'] = get_timestr(Time, "%Y-%m-%d %H:%M:%S")
			minorCode = "//*[@href = '{}']/../span/a/text()".format(i)
			meta['minor_business_type'] = response.xpath(minorCode).extract_first()
			if not meta['minor_business_type']:
				continue

			yield scrapy.Request(
				url=artUrl,
				meta=meta,
				callback=self.parseA,
				dont_filter=True
			)

		if mark == len(link) and self.goon == 'no':
			return None
		else:
			meta['Num'] += 1
			url = self.start_urls.format(subclass=meta['subclass_id'], Num=str(meta['Num']))
			yield scrapy.Request(
				url=url,
				callback=self.parse,
				meta=meta,
				dont_filter=True
			)

	def parseA(self, response):
		meta = response.meta
		item = GcprojectItem()

		item['page_url'] = response.url
		item['site'] = self.allowed_domains[0]
		item['title'] = meta['title']
		item['issue_time'] = meta['issue_time']
		item['minor_business_type'] = meta['minor_business_type']

		content = response.xpath("//div[@class = 'y4']|//div[@class='y4 detail-content']").extract()
		item['content'] = ''.join(content)

		yield item

	# item['content'] = len(item['content'])
	# pprint.pprint(item)
	# print('-----------------------------')

	def parse_correction(self, response):
		meta = response.meta
		titleError = False
		minorError = False
		endMark = False

		# status = 0 未处理
		# status = 1 已处理完毕
		# status = 2 测试数据，不用
		# status = 3 title获取错误
		# status = 4 Minor_business_type获取错误
		# status = 5 title和minorbusiness同时获取错误
		# status = 6 sqliteDB的title和网站原有title一样
		# status = 7 临时状态
		try:
			title = re.findall('''class="y3"><p><span>(.*?)</span>''', response.text, re.M | re.S)[0].replace('%','％')
			if not title:
				titleError = True
		except:
			titleError = True

		try:
			minor_business_type = re.findall("招标类型：</strong><span>(.*?)</span>", response.text, re.M | re.S)[0]
			if not minor_business_type:
				minorError = True
				minor_business_type = '其他类别'
		except:
			minor_business_type = '其他类别'
			minorError = True

		if titleError:
			self.sqlitDB.update_info(updateKey='status', updateValue=3, whereKey='id',
			                         whereValue=meta['s_id'])
			endMark = True

		# if minorError and titleError:
		# 	self.sqlitDB.update_info(updateKey='status', updateValue=5, whereKey='id',
		# 	                         whereValue=meta['s_id'])
		# 	endMark = True
		# if minorError and not titleError:
		# 	self.sqlitDB.update_info(updateKey='status', updateValue=4, whereKey='id',
		# 	                         whereValue=meta['s_id'])
		# 	endMark = True
		# if not minorError and titleError:
		# 	self.sqlitDB.update_info(updateKey='status', updateValue=3, whereKey='id',
		# 	                         whereValue=meta['s_id'])
		# 	endMark = True

		if title == meta['s_title']:
			self.sqlitDB.update_info(updateKey='status', updateValue=6, whereKey='id',
			                         whereValue=meta['s_id'])
			endMark = True

		if endMark:
			# print('本文出现错误')
			# print('title错误：', titleError)
			# print('minor错误：', minorError)
			# print('标题一样：', title == meta['s_title'])
			# print('文章链接：', meta['url'])
			# print('数据库ID：', meta['s_id'])
			# print('---------------------------------------ERROR')
			return None
		else:
			inserURL = meta['url'] + "&sd=" + str(meta['s_id'])
			# print(inserURL)
			# print(title)
			# print(minor_business_type)
			try:
				corren_updateInfo(updatePage_url=inserURL, updateTitle=title,
				                  updateMinor_business_type=minor_business_type, whereid=meta['s_id'])
				self.sqlitDB.update_info(updateKey='status', updateValue=1, whereKey='id',
				                         whereValue=meta['s_id'])
				# print('！！！！！！！！！！！！！！数据更新成功！！！！！！！！！！！！！！')

			except Exception as ff:
				self.sqlitDB.update_info(updateKey='status', updateValue=7, whereKey='id',
				                         whereValue=meta['s_id'])

				# print('++++++++++++++++++++++++++++++++++++++++++++++')
				# print(ff)
				# print('++++++++++++++++++++++++++++++++++++++++++++++')

				return None
