# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import json, os, sys, pprint
from urllib import parse as urlparse
import pandas as pd
import datetime, time
import random
import lxml
import lxml.html
from lxml.html import HtmlComment
from lxml import etree
from lxml import html as htmlstr
import cchardet, chardet
from requests.adapters import HTTPAdapter
from redisBloomHash import bl
import logging
from crawltools import tureLocation, get_location, save_api, writeJson, openJson, getBetweenDayList, sleepSec, \
	get_timestr, creatHeader


class request_hub_OBJ():
	# 从LOCAL_DB_ORM,py 或 UXUE_DB_ORM.py引入mysql库的orm对象。
	# 其中uxue_session()是正式库，local_session是本地测试库

	# ddict就是存储的json文件
	def __init__(self, ddict):

		self.mInfo = ddict
		# '''没有列表页和最终页的method报错'''
		if not self.mInfo['hub_method']:
			logging.critical('Have not hub_method')
		# ''' 列表页为get，而没有hub xpath报错'''
		if self.mInfo['hub_method'] == 'GET' and not self.mInfo['hub_xpath']:
			logging.critical('pls input hub_xpath')
		# ''' 列表页为post而没有字典规范和传参表格，报错'''
		if self.mInfo['hub_method'] == 'POST' and not self.mInfo['hub_postdate'] and not self.mInfo['hub_dictKeys']:
			logging.critical('pls input both hub_postdate and hub_dictKeys')

		# 构建requests容器
		self.req = requests.session()

		# ''' 定义全局headers'''
		if ddict['HEA']:
			self.HEA = creatHeader(ddict['HEA'])
			self.req.headers = self.HEA
		else:
			self.req.headers = ''

		# IP池接口
		self.req.proxies = None
		# 设置requests请求头文件

		# requests超时重试四次
		self.req.mount('http://', HTTPAdapter(max_retries=3))
		self.req.mount('https://', HTTPAdapter(max_retries=3))
		# self.req.cookies = None

		# ''' 如果需要传递cookies则打开无头浏览器获取cookies '''
		if self.mInfo['transmitCookies']:
			self.req.cookies = self.webdriver_getCookie(self.mInfo['hub_url'][0])
			# ''' 如果无头浏览器超时，无返回cookies，报错 '''
			if not self.req.cookies:
				logging.critical('The cookies fail to get')

	def webdriver_getCookie(self, url,):
		# 启动webdrviver仿真，获取cookies用。使用chrmedrvier
		pageUrl = url
		from selenium.webdriver import Chrome
		from selenium.webdriver.chrome.options import Options
		import os
		root = os.getcwd()
		stealthPath = os.path.join(root, "wd/stealth.min.js")
		chrodriverPath = os.path.join(root, "wd/chromedriver")
		# proxIP = "118.24.219.151:16818"

		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument(
			'user-agent={}'.format(self.HEA['User-Agent']))
		chrome_options.add_argument("--disable-blink-features=AutomationControlled")
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('blink-settings=imagesEnabled=false')
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

		driver = Chrome(chrodriverPath, options=chrome_options)
		driver.set_page_load_timeout(60)
		driver.set_script_timeout(60)
		with open(stealthPath, 'r') as f:
			js = f.read()
		driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
		try:
			driver.get(pageUrl)
			time.sleep(3)
			driver.refresh()
			c = driver.get_cookies()

			cookies = {}
			# 获取cookie中的name和value,转化成requests可以使用的形式
			for cookie in c:
				cookies[cookie['name']] = cookie['value']
			driver.quit()
			return cookies
		except Exception as ff:
			driver.quit()
			errormag = 'webdriver error---\t' + ff
			logging.error(msg=errormag)
			return None

	def get_hub_html(self, url):
		# 主容器请求。self.req主容器，已经设置四次超时。超过四次，纪录超时信息，返回空值。
		try:
			# 如果请求方式为POST，需要有hub_postdate这个字典
			if self.mInfo['hub_method'].upper() == 'POST':
				brow = self.req.post(url=url, data=self.mInfo['hub_postdate'], timeout=(20, 20))
			else:
				# 否则，请求方式就是GET，无需其他字典。
				brow = self.req.get(url=url, timeout=(20, 20))
		except Exception as ff:
			print(ff)
			print('122page')
			errormsg = 'hub requestsException out：\n' + ff + '\n' + url + '\n'
			logging.error(msg=errormsg)
			return None

		browEnCode = brow.text.encode(encoding=brow.encoding, errors='ignore')
		# 先用 chardet监测页面的文字编码。
		self.hub_charset = chardet.detect(browEnCode)['encoding']
		# 如果 chardet没有检测出来，换cchardet再监测。。
		if not self.hub_charset or len(self.hub_charset) < 2:
			self.hub_charset = cchardet.detect(browEnCode)['encoding']
			# 如果 chardet和cchardet都没出来，直接用brow。encoding。
			if not self.hub_charset or len(self.hub_charset) < 2:
				self.hub_charset = brow.encoding

		html = browEnCode.decode(self.hub_charset, 'ignore')
		return html

	def get_hubInfo_list(self, url=None, baseUrl=None, location=None,subclass=None,timeL=None):
		mark = 0
		html = self.get_hub_html(url)
		llist = []

		if self.mInfo['hub_method'].upper() != 'POST' and self.mInfo['hub_method'].upper() != 'GET':
			raise 'hub_method must GET or POST'
		if self.mInfo['hub_method'].upper() == 'POST':
			if self.mInfo['hub_postmainKey']:
				jsonInfo = json.loads(html)[self.mInfo['hub_postmainKey']]
			else:
				jsonInfo = json.loads(html)
			for i in jsonInfo:
				ddict = {}
				ddict['site'] = self.mInfo['site']
				try:
					for key in self.mInfo['hub_dictKeys'].keys():
						if key == 'page_url':
							ddict[key] = urlparse.urljoin(baseUrl, i[self.mInfo['hub_dictKeys']])
						elif key == 'issue_time':
							ddict[key] = get_timestr(i[self.mInfo['hub_dictKeys']])
						else:
							ddict[key] = i[self.mInfo['hub_dictKeys']]
				except Exception as fff:
					msgerror = 'keys error\nweb keys\t' + ','.join(jsonInfo.keys()) + '\nmy keys\t' + ','.join(
						self.mInfo['hub_dictKeys'].keys()) + '\n' + fff
					logging.error(msg=msgerror)

				if bl.exists(ddict['page_url']):
					mark += 1
					continue
				llist.append(ddict)
			return llist, mark == len(jsonInfo)

		if self.mInfo['hub_method'].upper() == 'GET':
			doc = lxml.html.fromstring(html)
			link = doc.xpath(self.mInfo['hub_xpath']['page_url'])
			if not link:

				return 'no link',True
			for i in link:
				ddict = {}
				nowTime = datetime.datetime.now()
				ddict['create_time'] = nowTime
				ddict['update_time'] = nowTime
				ddict['subclass'] = subclass
				ddict['page_url'] = urlparse.urljoin(url, i)
				ddict['title'] = doc.xpath(self.mInfo['hub_xpath']['title'].format(i))[0].strip()
				if bl.exists(ddict['page_url']):
					mark += 1
					continue
				ddict['site'] = self.mInfo['site']
				ddict['craw_id'] = self.mInfo['craw_id']

				if self.mInfo['hub_xpath']['issus_time']:
					timeT = doc.xpath(self.mInfo['hub_xpath']['issus_time'].format(i))[0].strip()
					ddict['issus_time'] = get_timestr(timeT)
				else:
					ddict['issus_time'] = ''

				if location:
					province_name_dict = tureLocation(localName=location, title=ddict['title'])
					ddict['province_name'] = province_name_dict['province_name']
					ddict['city_name'] = province_name_dict['city_name']
					ddict['str1'] = province_name_dict['str1']
				else:
					if self.mInfo['hub_xpath']['location']:
						try:
							province_name = doc.xpath(self.mInfo['hub_xpath']['location'].format(i))[0].strip()
							province_name_dict = tureLocation(localName=province_name, title=ddict['title'])
							ddict['province_name'] = province_name_dict['province_name']
							ddict['city_name'] = province_name_dict['city_name']
							ddict['str1'] = province_name_dict['str1']
						except Exception as f4:
							province_name_dict = tureLocation(localName='NULL', title=ddict['title'])
							ddict['province_name'] = province_name_dict['province_name']
							ddict['city_name'] = province_name_dict['city_name']
							ddict['str1'] = province_name_dict['str1']
							if not ddict['province_name']:
								ddict['province_name'] = ''
					else:
						ddict['province_name'] = ''
						ddict['city_name'] = ''
						ddict['str1'] = ''
				llist.append(ddict)

			return llist, mark == len(link)


class request_article_OBJ():
	# 从LOCAL_DB_ORM,py 或 UXUE_DB_ORM.py引入mysql库的orm对象。
	# 其中uxue_session()是正式库，local_session是本地测试库

	# ddict就是存储的json文件
	def __init__(self, ddict):

		self.mInfo = ddict
		# '''没有列表页和最终页的method报错'''
		if not self.mInfo['hub_method']:
			logging.critical('Have not hub_method')
		# ''' 列表页为get，而没有hub xpath报错'''
		if self.mInfo['hub_method'] == 'GET' and not self.mInfo['hub_xpath']:
			logging.critical('pls input hub_xpath')
		# ''' 列表页为post而没有字典规范和传参表格，报错'''
		if self.mInfo['hub_method'] == 'POST' and not self.mInfo['hub_postdate'] and not self.mInfo['hub_dictKeys']:
			logging.critical('pls input both hub_postdate and hub_dictKeys')
		# ''' 定义全局headers'''
		self.HEA = creatHeader(ddict['HEA'])



		# 构建requests容器
		self.req = requests.session()

		# IP池接口
		# self.req.proxies = ''
		# 设置requests请求头文件
		self.req.headers = self.HEA

		# requests超时重试四次
		self.req.mount('http://', HTTPAdapter(max_retries=3))
		self.req.mount('https://', HTTPAdapter(max_retries=3))
		# self.req.cookies = None

		# ''' 如果需要传递cookies则打开无头浏览器获取cookies '''
		if self.mInfo['transmitCookies']:
			self.req.cookies = self.webdriver_getCookie(self.mInfo['hub_url'][0])
			# ''' 如果无头浏览器超时，无返回cookies，报错 '''


	def webdriver_getCookie(self, url):
		# 启动webdrviver仿真，获取cookies用。使用chrmedrvier
		pageUrl = url
		from selenium.webdriver import Chrome
		from selenium.webdriver.chrome.options import Options
		import os
		root = os.getcwd()
		stealthPath = os.path.join(root, "crawlfile/wd/stealth.min.js")
		chrodriverPath = os.path.join(root, "wd/chromedriver")
		# proxIP = "118.24.219.151:16818"

		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument(
			'user-agent={}'.format(self.HEA['User-Agent']))
		chrome_options.add_argument("--disable-blink-features=AutomationControlled")
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('blink-settings=imagesEnabled=false')
		chrome_options.add_argument('--disable-gpu')
		chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

		driver = Chrome(chrodriverPath, options=chrome_options)
		driver.set_page_load_timeout(60)
		driver.set_script_timeout(60)
		with open(stealthPath, 'r') as f:
			js = f.read()
		driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
		try:
			driver.get(pageUrl)
			time.sleep(3)
			driver.refresh()
			c = driver.get_cookies()

			cookies = {}
			# 获取cookie中的name和value,转化成requests可以使用的形式
			for cookie in c:
				cookies[cookie['name']] = cookie['value']
			driver.quit()
			return cookies
		except Exception as ff:
			driver.quit()
			errormag = 'webdriver error---\t' + ff
			logging.error(msg=errormag)
			return None

	def get_article_html(self, url):
		# 主容器请求。self.req主容器，已经设置四次超时。超过四次，纪录超时信息，返回空值。
		try:
			# 如果请求方式为POST，需要有hub_postdate这个字典
			if self.mInfo['hub_method'].upper() == 'POST':
				brow = self.req.post(url=url, data=self.mInfo['hub_postdate'], timeout=(20, 20))
			else:
				# 否则，请求方式就是GET，无需其他字典。
				brow = self.req.get(url=url, timeout=(20, 20))
		except Exception as ff:
			print(ff)
			return None

		browEnCode = brow.text.encode(encoding=brow.encoding, errors='ignore')
		# 先用 chardet监测页面的文字编码。
		self.hub_charset = chardet.detect(browEnCode)['encoding']
		# 如果 chardet没有检测出来，换cchardet再监测。。
		if not self.hub_charset or len(self.hub_charset) < 2:
			self.hub_charset = cchardet.detect(browEnCode)['encoding']
			# 如果 chardet和cchardet都没出来，直接用brow。encoding。
			if not self.hub_charset or len(self.hub_charset) < 2:
				self.hub_charset = brow.encoding

		html = browEnCode.decode(self.hub_charset, 'ignore')
		return html

	def replaceHtml(self, html):
		p = re.compile(r"<table(.*?)>")
		html = p.sub('<table border="1">', html)
		p = re.compile(r"<tr(.*?)>")
		html = p.sub('<tr>', html)
		p = re.compile(r"<td(.*?)>")
		html = p.sub('<td>', html)
		p = re.compile(r"<th(.*?)>")
		html = p.sub('<th>', html)
		p = re.compile(r"<input(.*?)>")
		html = p.sub('', html)
		return html.replace(u'&#13;', u'').replace(u'\xa0', u'')

	def get_text(self, html, encoding):
		doc = lxml.html.fromstring(html)
		lxml.etree.strip_elements(doc, 'script')
		lxml.etree.strip_elements(doc, 'style')
		for ch in doc.iterdescendants():
			if not isinstance(ch.tag, str):
				continue
			if ch.tag in ['div', 'h1', 'h2', 'h3', 'p', 'br', 'table', 'tr', 'dl', 'img']:
				if not ch.tail:
					ch.tail = '\n'
				else:
					ch.tail = '\n' + ch.tail.strip() + '\n'

			# if ch.tag in ['th', 'td','tr','table']:
			if ch.tag in ['table']:
				enHtml = etree.tostring(ch, encoding=encoding, pretty_print=True)
				cleanTable = self.replaceHtml(enHtml.decode(encoding))
				ch.text = cleanTable.replace('\n', '')

		lines_a = doc.text_content().split('\n')
		lines = []
		for l in lines_a:
			strWord = l.replace('\t', '').strip()
			if strWord:
				lines.append('<p>' + strWord + '</p>')
		return ''.join(lines).replace('\u3000', '')


if __name__ == '__main__':
	all_xiangtong = 0
	all_butong = 0
	mark = 0
	sezi = [1, 2, 3, 4, 5, 6]
	doup = []
	for s1 in sezi:
		for s2 in sezi:
			for s3 in sezi:
				for s4 in sezi:
					for s5 in sezi:
						mark += 1
						doup.append([s1, s2, s3, s4, s5])

	pprint.pprint(doup)
	print(mark, len(doup))
