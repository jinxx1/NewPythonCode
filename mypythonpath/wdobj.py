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

import platform, sys, os, json
mysystem = platform.system()
if mysystem == 'Windows':
	rootpath = r"D:/PythonCode/mypythonpath"
elif mysystem == "Linux":
	rootpath = r"/home/terry/anaconda3/lib/python3.7/site-packages/mtools"
else:
	raise 'not Windows or Linux'

class wdriver():
	def __init__(self,ua):
		from selenium.webdriver import Chrome
		from selenium.webdriver.chrome.options import Options
		import os
		stealthPath = os.path.join(rootpath, "wd/stealth.min.js")
		chrodriverPath = os.path.join(rootpath, "wd/chromedriver")
		self.chrome_options = Options()
		self.chrome_options.add_argument("--headless")
		self.chrome_options.add_argument(
			'user-agent={}'.format(ua))
		self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
		self.chrome_options.add_argument('--no-sandbox')
		self.chrome_options.add_argument('blink-settings=imagesEnabled=false')
		self.chrome_options.add_argument('--disable-gpu')
		self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

		self.driver = Chrome(chrodriverPath, options=chrome_options)
		self.driver.set_page_load_timeout(60)
		self.driver.set_script_timeout(60)
		with open(stealthPath, 'r') as f:
			js = f.read()
		self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})


	def get_driver(self):
		return self.driver

	def get_driverCookies(self,pageUrl):
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




