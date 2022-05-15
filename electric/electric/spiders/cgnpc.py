import scrapy
from urllib import parse
import pprint
import re, json, requests
from electric.scrapyParse import *
from bs4 import BeautifulSoup
from electric.items import ElectricItem


class CgnpcSpider(scrapy.Spider):
	name = 'cgnpc'
	allowed_domains = ['ecp.cgnpc.com.cn']
	start_urls = [
		{'catName': '招标信息_招标公告', 'baseUrl': 'https://ecp.cgnpc.com.cn/zbgg.html?pageIndex={}', 'allPage': 275,
		 'dataid': "65e43b2fbc914f7e98d966d85f78d5de", 'listUrl': "350ea2d859f7a2797c9be4b6cb3b5ebe"},
		# {'catName': '招标信息_资格预审公告', 'baseUrl': 'https://ecp.cgnpc.com.cn/zgysgg.html?pageIndex={}', 'allPage': 36,'dataid':"0e7755722d294001bf41f467ddfe04b2",'listUrl':"350ea2d859f7a2797c9be4b6cb3b5ebe"},
		# {'catName': '招标信息_中标候选人公示', 'baseUrl': 'https://ecp.cgnpc.com.cn/zbhxrgs.html?pageIndex={}', 'allPage': 199,'dataid':"aa2e86adfa624027b1cf9d1598fb90b6",'listUrl':"350ea2d859f7a2797c9be4b6cb3b5ebe"},
		# {'catName': '招标信息_中标结果公示', 'baseUrl': 'https://ecp.cgnpc.com.cn/zbjggs.html?pageIndex={}', 'allPage': 60,'dataid':"c5ef47bc30844c4683639c66325ec0d7",'listUrl':"350ea2d859f7a2797c9be4b6cb3b5ebe"},
		# {'catName': '招标信息_变更公告', 'baseUrl': 'https://ecp.cgnpc.com.cn/bggg.html?pageIndex={}', 'allPage': 45,'dataid':"85381e89a85d4e019475e4e6d025f681",'listUrl':"350ea2d859f7a2797c9be4b6cb3b5ebe"},
		# {'catName': '非招标采购信息_采购启动公示', 'baseUrl': 'https://ecp.cgnpc.com.cn/cgqdgs.html?pageIndex={}', 'allPage': 2125,'dataid':"bbf3c0e849e042459392b379c4fb343b",'listUrl':"6aafa6a8a2acaf9c12afc657db3a5b18"},
		# {'catName': '非招标采购信息_采购结果公示', 'baseUrl': 'https://ecp.cgnpc.com.cn/cgjggs.html?pageIndex={}', 'allPage': 406,'dataid':"924e0e09dd90451ba1394cae3e06f326",'listUrl':"6aafa6a8a2acaf9c12afc657db3a5b18"}
	]
	jsonRequestUrl = "https://ecp.cgnpc.com.cn/content/{pageId}/{listUrl}/{num}.json?pageIndex={num}"
	ArtcleRequestUrl = "https://ecp.cgnpc.com.cn/detail/{dataid}/{detailid}.json"

	def __init__(self, goon=None, *args, **kwargs):
		super(CgnpcSpider, self).__init__(*args, **kwargs)
		self.goon = goon

	def start_requests(self):
		meta = {}
		meta['Num'] = 1
		for i in self.start_urls:
			meta['catName'] = i['catName']
			meta['baseUrl'] = i['baseUrl']
			meta['allPage'] = i['allPage']
			meta['dataid'] = i['dataid']
			meta['listUrl'] = i['listUrl']

			yield scrapy.Request(url=meta['baseUrl'].format(meta['Num']),
			                     callback=self.parse,
			                     meta=meta,
			                     dont_filter=True
			                     )

	def parse(self, response):
		meta = response.meta
		meta['pageId'] = re.findall("window.pageId.\=.\'(.*?)\'\;", response.text)[0]
		yield scrapy.Request(
			url=self.jsonRequestUrl.format(pageId=meta['pageId'], listUrl=meta['listUrl'], num=meta['Num']),
			callback=self.parseList,
			dont_filter=True,
			meta=meta
			)

	def parseList(self, response):
		meta = response.meta
		jsonT = json.loads(response.text)['list']

		artcleUrl = "https://ecp.cgnpc.com.cn/Details.html?dataId={dataId}&detailId={detailId}"
		nodupJson = []
		for i in jsonT:
			ddict = {}
			ddict['detailId'] = i['Id']
			ddict['artcleUrl'] = artcleUrl.format(detailId=ddict['detailId'], dataId=meta['dataid'])
			ddict['CreateTime'] = i['CreateTime']
			ddict['Title'] = i['Title']
			nodupJson.append(ddict)
		nodupUrlList = [x['artcleUrl'] for x in nodupJson]
		nogetUrlList = urlIsExist(nodupUrlList)
		print("《{}》第{}页，一共有{}篇幅，{}未收录".format(meta['catName'], meta['Num'], len(jsonT), len(nogetUrlList)))
		print('---------------------------------------------------')

		if not nogetUrlList and self.goon == 'no':
			return None
		if nogetUrlList:
			for i in nodupJson:
				if i['artcleUrl'] not in nogetUrlList:
					continue
				meta['ArtcleRequestUrl'] = self.ArtcleRequestUrl.format(detailid=i['detailId'], dataid=meta['dataid'])
				meta['CreateTime'] = i['CreateTime']
				meta['Title'] = i['Title']
				meta['artcleUrl'] = i['artcleUrl']
				yield scrapy.Request(url=meta['ArtcleRequestUrl'],
				                     dont_filter=True,
				                     meta=meta,
				                     callback=self.parseA)

		meta['Num'] += 1
		if meta['Num'] >= meta['allPage'] + 1:
			return None
		yield scrapy.Request(
			url=self.jsonRequestUrl.format(pageId=meta['pageId'], listUrl=meta['listUrl'], num=meta['Num']),
			callback=self.parseList,
			dont_filter=True,
			meta=meta
			)

	def parseA(self, response):
		meta = response.meta
		item = ElectricItem()
		print('--------------------------------------------------',type(response.text))
		jsonT = json.loads(response.text)
		item['content'] = jsonT['Body']
		Attachment = ''
		if 'BodyAttachment' in jsonT.keys():
			Attachment = jsonT['BodyAttachment']
		if 'Attachment' in jsonT.keys():
			Attachment = jsonT['Attachment']

		if len(Attachment) > 5:
			attJson = json.loads(Attachment)
			item['attachmentListJson'] = []
			for n in attJson:
				ddict = {}
				ddict['name'] = n['name']
				ddict['download_url'] = n['url']
				item['attachmentListJson'].append(ddict)
			item['attachmentListJson'] = json.dumps(item['attachmentListJson'], ensure_ascii=False)

		item['url'] = meta['artcleUrl']
		item['site'] = self.allowed_domains[0]
		item['subclass'] = meta['catName']
		item['issueTime'] = get_timestr(meta['CreateTime'], '%Y-%m-%d %H:%M:%S')
		item['title'] = meta['Title']

		# item['content'] = len(item['content'])
		# pprint.pprint(item)
		# print('----------------------------------------')
		yield item
