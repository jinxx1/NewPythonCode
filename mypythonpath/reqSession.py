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
from ipProxies import IP_POOR


class req_session():
	# 从LOCAL_DB_ORM,py 或 UXUE_DB_ORM.py引入mysql库的orm对象。
	# 其中uxue_session()是正式库，local_session是本地测试库

	# ddict就是存储的json文件
	def __init__(self, ddict):

		self.mInfo = ddict

		self.req = requests.session()

		# IP池接口
		iporxies = IP_POOR()
		if iporxies:
			self.req.proxies = iporxies

		if ddict['cookies']:
			from requests.cookies import cookiejar_from_dict
			self.req.cookies = cookiejar_from_dict(ddict['cookies'])


		if ddict['HEA']:
			self.req.headers = creatHeader(ddict['HEA'])

		# requests超时重试四次
		self.req.mount('http://', HTTPAdapter(max_retries=3))
		self.req.mount('https://', HTTPAdapter(max_retries=3))

	def GetReHtml(self,url,html=True):
		# 主容器请求。self.req主容器，已经设置四次超时。超过四次，纪录超时信息，返回空值。
		try:
			brow = self.req.get(url=url, timeout=(20, 20))
		except Exception as ff:
			print(ff)
			errormsg = 'hub requestsException out：\n' + ff + '\n' + url + '\n'
			logging.error(msg=errormsg)
			return None
		if not html:
			return brow

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


	def PostResult(self,posturl='',postdate={},html=None,jsonT=None):
		if not html and not jsonT:
			raise 'not html or jsonT'
		if not postdate or not posturl:
			raise 'not postdate or posturl'

		try:
			brow = self.req.post(url=posturl,timeout=(20,20),data=postdate)
		except Exception as ff:
			print(ff)

			return None
		# print(brow.text)
		# print('----------------')

		browEnCode = brow.text.encode(encoding=brow.encoding, errors='ignore')
		# 先用 chardet监测页面的文字编码。
		self.hub_charset = chardet.detect(browEnCode)['encoding']
		# 如果 chardet没有检测出来，换cchardet再监测。。
		if not self.hub_charset or len(self.hub_charset) < 2:
			self.hub_charset = cchardet.detect(browEnCode)['encoding']
			# 如果 chardet和cchardet都没出来，直接用brow。encoding。
			if not self.hub_charset or len(self.hub_charset) < 2:
				self.hub_charset = brow.encoding

		hhtml = browEnCode.decode(self.hub_charset, 'ignore')


		if html:
			return hhtml
		if jsonT:
			try:
				return json.loads(hhtml)
			except:
				print(hhtml)

	def __closeSession__(self):
		self.req.close()
