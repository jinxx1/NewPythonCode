# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json, pprint, re
from bs4 import BeautifulSoup
from spalsh10086.scrapyParse import *
from spalsh10086.items import Spalsh10086Item
from spalsh10086.mysql_processing import *
import datetime

import platform, sys, os

mysystem = platform.system()
if mysystem == 'Windows':
	sys.path.append(r"D:\PythonCode\mypythonpath")
	logroot = r"D:\PythonCode\scrapySplash10086\spalsh10086\spalsh10086\10086log\monitoring"

elif mysystem == "Linux":
	sys.path.append("/home/terry/i139/mypythonpath")
	logroot = "/home/terry/10086log/monitoring"
else:
	logroot = os.getcwd()
	pass
from mkdir import mkdir

import datetime, time

today = datetime.datetime.now()
year_month = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
floder_ymd = os.path.join(logroot, year_month)
mkdir(floder_ymd)
time_now = str(today.hour) + "-" + str(today.minute) + "-" + str(today.second)
floder_time = os.path.join(floder_ymd, time_now)
mkdir(floder_time)

print("开始spalsh抓取中国移动：", datetime.datetime.now())


class A100862Spider(scrapy.Spider):
	name = 'cmcrawlformtime'
	allowed_domains = ['b2b.10086.cn']
	siteName = '移动'

	pageList = [
		{"subclass": "采购公告", "url": "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2"},
		{"subclass": "候选人公示", "url": "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=7"},
		{"subclass": "中选结果公示", "url": "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=16"},
		{"subclass": "单一来源采购信息公告", "url": "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=1"},
		{"subclass": "资格预审公告", "url": "https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=3"},
	]


	def __init__(self, startime=None,endtime=None, spiderName=None, *args, **kwargs):
		super(A100862Spider, self).__init__(*args, **kwargs)
		if not startime and not endtime:
			raise 'input startime and endtime'


		self.lua_script = '''
		    function main(splash, args)
		        function focus(sel)
		            splash:select(sel):focus()
		        end
		        splash.resource_timeout = 20
		        splash.images_enabled = false
		        splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko")
		        assert(splash:go(args.url))
		        assert(splash:wait(3))

		        focus('input[id=startDate]')
		        splash:send_text("%s")
		        assert(splash:wait(1))
		        focus('input[id=endDate]')
		        splash:send_text("%s")
		        assert(splash:wait(3))




		        focus('input[id=pageNumber]')
		        splash:send_text(args.pageNum)
		        assert(splash:wait(3))

		        splash:select('input[value=GO]'):mouse_click()
		        assert(splash:wait(5))

		        return {
		            html = splash:html(),
		            huburl=args.url,
		            get_pageNum = args.pageNum

		            }
		    end''' % (str(startime), str(endtime))

	def start_requests(self):
		for i in self.pageList:
			yield SplashRequest(url=i['url'], endpoint="execute", callback=self.parse,
			                    args={
				                    "wait": 0.5,
				                    "timeout": 90,
				                    "resource_timeout": 10,
				                    "images": 0,
				                    "lua_source": self.lua_script,
				                    "pageNum": str(1)
			                    }, )

	def parse(self, response):

		huburl = response.data['huburl']
		get_pageNum = int(response.data['get_pageNum'])
		try:
			allPage = re.findall("共.*条数据/(\d{1,2})页", response.data['html'])[0]
		except:
			return None

		article_info = get_IDandTIME(response.data['html'])
		if not article_info or len(article_info) == 0:
			return None

		hubclass = ''
		for isub in self.pageList:
			if huburl == isub['url']:
				hubclass = isub['subclass']
		if not hubclass:
			return None

		filefolder = os.path.join(floder_time, hubclass)
		mkdir(filefolder)
		fileName = f'page{get_pageNum}.json'
		filePath = os.path.join(filefolder, fileName)
		with open(filePath, 'w', encoding='utf-8') as ff:
			json.dump(article_info, ff)
		try:
			noList = depcut(article_info)
		except:
			return None
		print(article_info[0])
		print('第{}页，共有{}篇文章未录入。本类别共{}页'.format(get_pageNum, len(noList),str(allPage)))
		print('----------------------------------', hubclass,get_pageNum)
		if noList:
			pandas_insermysql(noList, hubclass)
		if int(get_pageNum) >= int(allPage):
			print('=======end=======', hubclass,get_pageNum)
			return None
		else:
			get_pageNum += 1
			yield SplashRequest(url=huburl, endpoint="execute", callback=self.parse,
			                    args={
				                    "wait": 0.5,
				                    "timeout": 90,
				                    "resource_timeout": 10,
				                    "images": 0,
				                    "lua_source": self.lua_script,
				                    "pageNum": str(get_pageNum)
			                    }, )
