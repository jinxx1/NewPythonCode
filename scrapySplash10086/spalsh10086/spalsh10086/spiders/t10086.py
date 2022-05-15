# -*- coding: utf-8 -*-
import joblib.externals.cloudpickle
import scrapy
from scrapy_splash import SplashRequest
import json, pprint, re
from bs4 import BeautifulSoup
from spalsh10086.scrapyParse import *
from spalsh10086.items import Spalsh10086Item
from spalsh10086.mysql_processing import *
import datetime
from getmysqlInfo import jsonInfo
from mkdir import mkdir
from redisBloomHash import *
from crawltools import *
from requests_obj import *
from uxue_orm import *
import platform, sys, os
import datetime, time


logroot = '/home/terry/10086log/monitoring/'
today = datetime.datetime.now()
year_month = str(today.year) + "-" + str(today.month) + "-" + str(today.day)
floder_ymd = os.path.join(logroot, year_month)

time_now = str(today.hour) + "-" + str(today.minute) + "-" + str(today.second)
floder_time = os.path.join(floder_ymd, time_now)

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

# today = "2022-03-08"
# yesterday = "2022-03-08"
class T10086Spider(scrapy.Spider):
	name = 't10086'
	allowed_domains = ['b2b.10086.cn']
	siteName = '移动'

	pageList = [
{"subclass":"采购公告", "url":"https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2"},
{"subclass":"候选人公示", "url":"https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=7"},
{"subclass":"中选结果公示", "url":"https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=16"},
{"subclass":"单一来源采购信息公告", "url":"https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=1"},
{"subclass":"资格预审公告", "url":"https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=3"},
	]
	lua_script_base = '''
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
    end''' % (str(yesterday), str(today))

	def __init__(self, goon=None, spiderName=None, *args, **kwargs):
		super(T10086Spider, self).__init__(*args, **kwargs)
		self.goon = goon
		self.lua_script = self.lua_script_base

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
			                    },
			                    )

	def parse(self, response):

		huburl = response.data['huburl']
		get_pageNum = int(response.data['get_pageNum'])

		# 获取本页subclass
		hubclass = ''
		for isub in self.pageList:
			if huburl == isub['url']:
				hubclass = isub['subclass']
				break
		if not hubclass:
			return None

		# 获取总页数
		try:
			allPage = re.findall("共.*条数据/(\d{1,2})页", response.data['html'])[0]
		except:
			return None

		# 获取hub列表
		artcle_urls = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id={}'
		resID = re.findall("selectResult\(\'(.*?)\'\)", response.data['html'])
		soup = BeautifulSoup(response.data['html'], 'lxml')
		article_info = []
		for id in resID:
			page_url = artcle_urls.format(id)
			all_tr = soup.find_all(attrs={'onclick': "selectResult('{id}')".format(id=id)})

			for i in all_tr:
				try:
					timeWord = re.findall("(\d{4}-\d{1,2}-\d{1,2})", str(i))[0]
					
					timeWord = get_timestr(timeWord)
					break
				except:
					continue
			ddict = {}
			ddict['id'] = id
			ddict['url'] = page_url+"&ux_" + timeWord.split(' ')[0]
			ddict['time'] = timeWord
			ddict['subclass'] = hubclass
			# print(ddict['url'])
			article_info.append(ddict)

		dupurl_original = [x['url'] for x in article_info]
		dupurl_List = urlIsExist(dupurl_original)

		noList = []
		if dupurl_List:
			for i in dupurl_List:
				for arti in article_info:
					if i == arti['url']:
						noList.append(arti)

		# 把本页信息存储到本地json
		filefolder = os.path.join(floder_time, hubclass)
		mkdir(filefolder)
		fileName = f'page{get_pageNum}.json'
		filePath = os.path.join(filefolder, fileName)
		with open(filePath, 'w', encoding='utf-8') as ff:
			json.dump(article_info, ff)

		print('《{}》中,第{}页，共有{}篇文章未录入，共{}页'.format(hubclass, get_pageNum, len(noList),allPage))

		if noList:
			pandas_insermysql(noList, hubclass)
			print('----------------------------------', get_pageNum)
		if int(get_pageNum) >= int(allPage):
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
