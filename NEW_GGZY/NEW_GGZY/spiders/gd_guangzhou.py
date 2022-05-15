# -*- coding: utf-8 -*-
import scrapy, re, json, pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *

TEMPPATH = TMEPTEST()


class GuangzhouSpider(scrapy.Spider):
	name = 'gd_guangzhou'
	allowed_domains = ['www.gzggzy.cn']

	urlDict = [
		{'catName': '广州市_政府采购_采购公告',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/zfcglist.jsp?page={}&siteId=1&channelId=456',
		 'allowModel': 'get'},
		{'catName': '广州市_政府采购_预公告',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/zfcglist.jsp?page={}&siteId=1&channelId=448',
		 'allowModel': 'get'},
		{'catName': '广州市_政府采购_更正公告',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/zfcglist.jsp?page={}&siteId=1&channelId=457',
		 'allowModel': 'get'},
		{'catName': '广州市_政府采购_结果公告',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/zfcglist.jsp?page={}&siteId=1&channelId=458',
		 'allowModel': 'get'},
		{'catName': '广州市_土地_信息公告',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/tdlist.jsp?page={}&siteId=1&channelId=391',
		 'allowModel': 'get'},
		{'catName': '广州市_土地_成交公示',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/tdlist.jsp?page={}&siteId=1&channelId=393',
		 'allowModel': 'get'},
		{'catName': '广州市_矿产_信息公告',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/kclist.jsp?page={}&siteId=1&channelId=397',
		 'allowModel': 'get'},
		{'catName': '广州市_矿产_成交公示',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/kclist.jsp?page={}&siteId=1&channelId=399',
		 'allowModel': 'get'},
		{'catName': '广州市_房建市政_招标公告',
		                        'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=503&pchannelid=466&curgclb=01,02,14&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=1&cIndex=1',
		                        'allowModel': 'post'},
		{'catName': '广州市_房建市政_资审结果公示',
		                                                'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=504&pchannelid=466&curgclb=01,02,14&curxmlb=01,02,03,04,05,14&curIndex=2&pcurIndex=1&cIndex=1',
		                                                'allowModel': 'post'},
		{'catName': '广州市_房建市政_中标候选人公示',
		                                                                        'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=506&pchannelid=466&curgclb=01,02,14&curxmlb=01,02,03,04,05,14&curIndex=3&pcurIndex=1&cIndex=1',
		                                                                        'allowModel': 'post'},
		{'catName': '广州市_房建市政_投标文件公开',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=519&pchannelid=466&curgclb=01,02,14&curxmlb=01,02,03,04,05,14&curIndex=4&pcurIndex=1&cIndex=1',
		 'allowModel': 'post'},
		{'catName': '广州市_房建市政_中标信息',
		                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=505&pchannelid=466&curgclb=01,02,14&curxmlb=01,02,03,04,05,14&curIndex=5&pcurIndex=1&cIndex=1',
		                         'allowModel': 'post'},
		{'catName': '广州市_交通_招标公告',
		                                                 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=510&channelids=15&pchannelid=467&curgclb=03&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=2',
		                                                 'allowModel': 'post'},
		{'catName': '广州市_交通_资审结果公示',
		                                                                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=511&channelids=16&pchannelid=467&curgclb=03&curxmlb=01,02,03,04,05,14&curIndex=2&pcurIndex=2',
		                                                                         'allowModel': 'post'},
		{'catName': '广州市_交通_中标候选人公示',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=513&channelids=17&pchannelid=467&curgclb=03&curxmlb=01,02,03,04,05,14&curIndex=3&pcurIndex=2',
		 'allowModel': 'post'},
		{'catName': '广州市_交通_中标信息',
		                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=512&pchannelid=467&curgclb=03&curxmlb=01,02,03,04,05,14&curIndex=4&pcurIndex=2&cIndex=1',
		                         'allowModel': 'post'},
		{'catName': '广州市_电力_招标公告',
		                                                 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=515&channelids=15&pchannelid=468&curgclb=05&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=3',
		                                                 'allowModel': 'post'},
		{'catName': '广州市_电力_中标候选人公示',
		                                                                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=518&channelids=17&pchannelid=468&curgclb=05&curxmlb=01,02,03,04,05,14&curIndex=2&pcurIndex=3',
		                                                                         'allowModel': 'post'},
		{'catName': '广州市_电力_中标信息',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=517&pchannelid=468&curgclb=05&curxmlb=01,02,03,04,05,14&curIndex=3&pcurIndex=3&cIndex=1',
		 'allowModel': 'post'},
		{'catName': '广州市_铁路_招标公告',
		                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=520&channelids=15&pchannelid=469&curgclb=06&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=4',
		                         'allowModel': 'post'},
		{'catName': '广州市_铁路_中标候选人公示',
		                                                 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=523&channelids=17&pchannelid=469&curgclb=06&curxmlb=01,02,03,04,05,14&curIndex=2&pcurIndex=4',
		                                                 'allowModel': 'post'},
		{'catName': '广州市_铁路_中标信息',
		                                                                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=522&pchannelid=469&curgclb=06&curxmlb=01,02,03,04,05,14&curIndex=3&pcurIndex=4&cIndex=1',
		                                                                         'allowModel': 'post'},
		{'catName': '广州市_水利_招标公告',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=525&channelids=15&pchannelid=470&curgclb=04&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=5',
		 'allowModel': 'post'},
		{'catName': '广州市_水利_资审结果公示',
		                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=526&channelids=16&pchannelid=470&curgclb=04&curxmlb=01,02,03,04,05,14&curIndex=2&pcurIndex=5',
		                         'allowModel': 'post'},
		{'catName': '广州市_水利_中标候选人公示',
		                                                 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=528&channelids=17&pchannelid=470&curgclb=04&curxmlb=01,02,03,04,05,14&curIndex=3&pcurIndex=5',
		                                                 'allowModel': 'post'},
		{'catName': '广州市_水利_投标文件公开',
		                                                                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=529&channelids=17&pchannelid=470&curgclb=04&curxmlb=01,02,03,04,05,14&curIndex=4&pcurIndex=5',
		                                                                         'allowModel': 'post'},
		{'catName': '广州市_水利_中标信息',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=527&channelids=18&pchannelid=470&curgclb=04&curxmlb=01,02,03,04,05,14&curIndex=5&pcurIndex=5',
		 'allowModel': 'post'},
		{'catName': '广州市_园林_招标公告',
		                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=543&channelids=15&pchannelid=472&curgclb=08&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=6',
		                         'allowModel': 'post'},
		{'catName': '广州市_园林_资审结果公示',
		                                                 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=544&channelids=16&pchannelid=472&curgclb=08&curxmlb=01,02,03,04,05,14&curIndex=2&pcurIndex=6',
		                                                 'allowModel': 'post'},
		{'catName': '广州市_园林_中标候选人公示',
		                                                                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=546&channelids=17&pchannelid=472&curgclb=08&curxmlb=01,02,03,04,05,14&curIndex=3&pcurIndex=6',
		                                                                         'allowModel': 'post'},
		{'catName': '广州市_园林_投标文件公开',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=547&channelids=17&pchannelid=472&curgclb=08&curxmlb=01,02,03,04,05,14&curIndex=4&pcurIndex=6',
		 'allowModel': 'post'},
		{'catName': '广州市_园林_中标信息',
		                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=545&channelids=18&pchannelid=472&curgclb=08&curxmlb=01,02,03,04,05,14&curIndex=5&pcurIndex=6',
		                         'allowModel': 'post'},
		{'catName': '广州市_民航_招标公告',
		                                                 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=539&channelids=15&pchannelid=471&curgclb=07&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=7',
		                                                 'allowModel': 'post'},
		{'catName': '广州市_民航_中标候选人公示',
		                                                                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=542&channelids=17&pchannelid=471&curgclb=07&curxmlb=01,02,03,04,05,14&curIndex=2&pcurIndex=7',
		                                                                         'allowModel': 'post'},
		{'catName': '广州市_民航_中标信息',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=541&channelids=18&pchannelid=471&curgclb=07&curxmlb=01,02,03,04,05,14&curIndex=3&pcurIndex=7',
		 'allowModel': 'post'},
		{'catName': '广州市_军队_招标公告',
		                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=1033&channelids=9999&pchannelid=475&curgclb=&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=8',
		                         'allowModel': 'post'},
		{'catName': '广州市_军队_资审结果公示',
		                                                 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=1034&channelids=9999&pchannelid=475&curgclb=&curxmlb=01,02,03,04,05,14&curIndex=2&pcurIndex=8',
		                                                 'allowModel': 'post'},
		{'catName': '广州市_军队_中标候选人公示',
		                                                                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=1036&channelids=9999&pchannelid=475&curgclb=&curxmlb=01,02,03,04,05,14&curIndex=3&pcurIndex=8',
		                                                                         'allowModel': 'post'},
		{'catName': '广州市_军队_中标信息',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=1035&channelids=9999&pchannelid=475&curgclb=&curxmlb=01,02,03,04,05,14&curIndex=4&pcurIndex=8',
		 'allowModel': 'post'},
		{'catName': '广州市_其他_招标公告',
		                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=535&channelids=15&pchannelid=474&curgclb=13&curxmlb=01,02,03,04,05,14&curIndex=1&pcurIndex=10',
		                         'allowModel': 'post'},
		{'catName': '广州市_其他_资审结果公示',
		                                                 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=536&channelids=16&pchannelid=474&curgclb=13&curxmlb=01,02,03,04,05,14&curIndex=2&pcurIndex=10',
		                                                 'allowModel': 'post'},
		{'catName': '广州市_其他_中标候选人公示',
		                                                                         'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=538&channelids=17&pchannelid=474&curgclb=13&curxmlb=01,02,03,04,05,14&curIndex=3&pcurIndex=10',
		                                                                         'allowModel': 'post'},
		{'catName': '广州市_其他_中标信息',
		 'url': 'http://www.gzggzy.cn/cms/wz/view/index/layout2/szlist.jsp?siteId=1&channelId=537&channelids=18&pchannelid=474&curgclb=13&curxmlb=01,02,03,04,05,14&curIndex=4&pcurIndex=10',
		 'allowModel': 'post'}]

	def start_requests(self):
		meta = {}
		getTXTdict = getTXT(self.name, self.urlDict)
		meta['Num'] = int(getTXTdict['Num'])
		for i in getTXTdict['urlDict']:
			meta['Breakpoint'] = i
			meta['key'] = i['catName']
			meta['url'] = i['url']
			meta['allowModel'] = i['allowModel']
			if meta['allowModel'] == 'get':
				yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parseget, meta=meta)
			else:
				yield scrapy.FormRequest(url=meta['url'], formdata={'page': str(meta['Num'])}, callback=self.parse,
				                         meta=meta)

	def parse(self, response):
		meta = response.meta
		link = response.xpath("//div[@class = 'infor_lb']//td[2]/a/@href").extract()
		if len(link) > 0:
			urlListTemp = []
			for i in link:
				urlTemp = parse.urljoin(response.url, i)
				urlListTemp.append(urlTemp + TEMPPATH)
			urllist = urlIsExist(urlListTemp)
			n = 0
			if len(urllist) > 0 and str(type(urllist)) == r"<class 'list'>":
				for url in urllist:
					n += 1
					if n == len(urllist):
						meta['pageTune'] = 1
					else:
						meta['pageTune'] = 0
					yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA,
					                     meta=meta)
			else:
				return None
		else:
			return None

	def parseA(self, response):
		meta = response.meta
		dict1 = {}
		selectWord = '点击查询日程安排'
		if selectWord in response.text:
			html = response.xpath("//div[@class = 'xx-text']/div[4]").extract()
		else:
			html = response.xpath(
				"//div[@class = 'xx-text']/div[3] |//div[@class = 'xx-text']/div[2] | //div[@class='xx-main']/div[@class='xx-text']//p").extract()
		titleT = response.xpath("//meta[@name = 'ArticleTitle']/@content").extract()
		timeT = response.xpath("//meta[@name = 'PubDate']/@content").extract()
		nonword1 = '附：交易中心位置图'
		nonword2 = '''<img alt="" src="http://www.gzggzy.cn/file/zfcg/zxdt.jpeg" width="535" height="352" data-bd-imgshare-binded="1">"'''
		if html and titleT and timeT:
			dict1['url'] = response.url
			dict1['site'] = self.allowed_domains[0]
			dict1['title'] = titleT[0]
			dict1['issueTime'] = timeReMark(timeT[0])
			dict1['content'] = html[0].replace(nonword1, '').replace(nonword2, '')
			dict1['subclass'] = meta['key']
			requestsAPI = save_api(dict1)
			tempDict = meta['Breakpoint']
			tempDict['Num'] = meta['Num']
			writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

			print(dict1['title'])
			print(dict1['url'])
			print(dict1['issueTime'])
			print(dict1['subclass'])
			print(len(dict1['content']))
			print(requestsAPI.text)
			print('------------------------------------')

			if meta['pageTune'] == 1:
				meta['Num'] += 1
				if meta['allowModel'] == 'get':
					yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta)
				else:
					yield scrapy.FormRequest(url=meta['url'], formdata={'page': str(meta['Num'])}, callback=self.parse,
					                         meta=meta)
		else:
			return None

	def parseget(self, response):
		# def parseid(self, response):
		meta = response.meta
		titleT = response.xpath(
			"//div[@class = 'infor_lb']//td[2]/a/text() | //div[@class = 'infor_lb']//td[3]/a/text()").extract()
		link = response.xpath(
			"//div[@class = 'infor_lb']//td[2]/a/@href | //div[@class = 'infor_lb']//td[3]/a/@href").extract()
		timeT = response.xpath(
			"//div[@class = 'infor_lb']//td[3]/text() | //div[@class = 'infor_lb']//td[4]/text()").extract()
		titleT = remarkList(titleT)
		link = remarkList(link)

		if len(link) != len(titleT) or len(titleT) != len(timeT):
			print("列表页，文章、链接、时间。规则数量不同", response.url)
			print(len(link), len(titleT), len(timeT))
			print(meta['allowModel'])
			print(link)
			print(titleT)
			print(timeT)
			print('********************************************************************')
			return None

		GotArtcl = 0
		notGotArtcl = 0
		if len(link) > 0:

			for i in range(len(link) + 1):
				urlListTemp = []
				# print('进入List循环体了')
				if notGotArtcl == 0 and GotArtcl == len(link):
					# print('notGotArtcl == 0 and GotArtcl == len(link)-------------------------------没有新文章退出')
					return None
				elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(link):
					# print('notGotArtcl !=0 and notGotArtcl + GotArtcl == len(link)--------------------翻页')
					meta['Num'] += 1
					if meta['allowModel'] == 'get':
						yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta)
					else:
						yield scrapy.FormRequest(url=meta['url'], formdata={'page': str(meta['Num'])},
						                         callback=self.parse,
						                         meta=meta)
				else:
					# print('urlTemp = parse.urljoin(response.url, link[i])--------------------最终进入文章')
					urlTemp = parse.urljoin(response.url, link[i])
					urlListTemp.append(urlTemp + TEMPPATH)
					urllist = urlIsExist(urlListTemp)
					if len(urllist) < 1:
						GotArtcl += 1
						continue
					else:
						notGotArtcl += 1
						for url in urllist:
							meta['articleTitle'] = titleT[i]
							meta['articleTime'] = timeT[i]
							if not meta['articleTitle']:
								meta['articleTitle'] = '本文暂无标题'
							if not meta['articleTime']:
								meta['articleTime'] = '2000-01-01 00:00:00'
							meta['ListPageNow'] = '本页第{}条，共{}条'.format(notGotArtcl + GotArtcl, len(link))
							# yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseAid, meta=meta)
							yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseAget, meta=meta)
		else:
			return None

	def parseAget(self, response):
		meta = response.meta
		dict1 = {}
		selectWord = '点击查询日程安排'
		if selectWord in response.text:
			html = response.xpath("//div[@class = 'xx-text']/div[4]").extract()
		else:
			html = response.xpath(
				"//div[@class = 'xx-text']/div[3] | //div[@class = 'xx-text']/div[2] | //div[@class='xx-main']/div[@class='xx-text']").extract()

		nonword1 = '附：交易中心位置图'
		nonword2 = '''<img alt="" src="http://www.gzggzy.cn/file/zfcg/zxdt.jpeg" width="535" height="352" data-bd-imgshare-binded="1">"'''
		if html:
			dict1['url'] = response.url
			dict1['site'] = self.allowed_domains[0]
			dict1['title'] = meta['articleTitle']
			dict1['issueTime'] = timeReMark(meta['articleTime'])
			dict1['content'] = html[0].replace(nonword1, '').replace(nonword2, '')
			dict1['subclass'] = meta['key']
			requestsAPI = save_api(dict1)

			tempDict = meta['Breakpoint']
			tempDict['Num'] = meta['Num']
			writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

			print(dict1['title'])
			print(dict1['url'])
			print(dict1['issueTime'])
			print(dict1['subclass'])
			print(len(dict1['content']))
			print(requestsAPI.text)
			print(' ')
			print(meta)
			print('------------------------------------')


		else:
			meta['error'] = '没有正文'
			meta['errorUrl'] = response.url
			errorLOG(meta)

			return None
