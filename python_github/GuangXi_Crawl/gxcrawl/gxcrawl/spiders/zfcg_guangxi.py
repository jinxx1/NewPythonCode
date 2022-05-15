# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
# from gxcrawl.Exist import *
from urllib import parse
from gxcrawl.items import GxcrawlItem



class ZfcgGuangxiSpider(scrapy.Spider):
	name = 'zfcg_guangxi'
	allowed_domains = ['www.ccgp-guangxi.gov.cn']
	urlList = [{'catName': '广西省_区本级_中标公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_zbgg/param_bulletin/20/page_{}.html', 'allpageNum': 950, 'bei_10': 95, 'yu_10': 0, 'code': 'wlRj'}, {'catName': '广西省_区本级_采购公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_cggg/param_bulletin/20/page_{}.html', 'allpageNum': 1990, 'bei_10': 199, 'yu_10': 0, 'code': 'oQVC'}, {'catName': '广西省_区本级_更正公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_gzgg/param_bulletin/20/page_{}.html', 'allpageNum': 482, 'bei_10': 48, 'yu_10': 2, 'code': 'tqp3'}, {'catName': '广西省_区本级_成交公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_cjgg/param_bulletin/20/page_{}.html', 'allpageNum': 1056, 'bei_10': 105, 'yu_10': 6, 'code': 'Q98I'}, {'catName': '广西省_区本级_其他公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_qtgg/param_bulletin/20/page_{}.html', 'allpageNum': 210, 'bei_10': 21, 'yu_10': 0, 'code': 'ZB2F'}, {'catName': '广西省_区本级_单一来源公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_dylygg/param_bulletin/20/page_{}.html', 'allpageNum': 147, 'bei_10': 14, 'yu_10': 7, 'code': 'bf1Q'}, {'catName': '广西省_区本级_招标文件预公示', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_zbwjygg/param_bulletin/20/page_{}.html', 'allpageNum': 634, 'bei_10': 63, 'yu_10': 4, 'code': 'Mh9c'}, {'catName': '广西省_市县级_其他公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_qtgg/param_bulletin/20/page_{}.html', 'allpageNum': 2138, 'bei_10': 213, 'yu_10': 8, 'code': 'zYGd'}, {'catName': '广西省_市县级_单一来源公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_dylygg/param_bulletin/20/page_{}.html', 'allpageNum': 382, 'bei_10': 38, 'yu_10': 2, 'code': '2h96'}, {'catName': '广西省_市县级_更正公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_gzgg/param_bulletin/20/page_{}.html', 'allpageNum': 4810, 'bei_10': 481, 'yu_10': 0, 'code': 'mU9J'}, {'catName': '广西省_市县级_中标公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_zbgg/param_bulletin/20/page_{}.html', 'allpageNum': 7078, 'bei_10': 707, 'yu_10': 8, 'code': 'YoHR'}, {'catName': '广西省_市县级_招标文件预公示', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_zbwjygs/param_bulletin/20/page_{}.html', 'allpageNum': 1946, 'bei_10': 194, 'yu_10': 6, 'code': '7Xfo'}]

	def start_requests(self):
		meta = {}
		BPt = breakPoint(self.urlList)
		for i in BPt:
			meta['catName'] = i['catName']
			meta['url'] = i['url']
			meta['code'] = i['code']
			meta['arrange'] = 0
			meta['allpageNum'] = i['allpageNum']
			meta['bei_10'] = i['bei_10']
			meta['yu_10'] = i['yu_10']

			if i['id'] == 'null':
				for n in range(1, i['bei_10'] + 1):
					meta['nowMaxNum'] = n * 10 + 1
					meta['nowMinNum'] = meta['nowMaxNum'] - 10
					meta['Num'] = meta['nowMinNum']
					if n == i['bei_10']:
						meta['nowMaxNum'] = n * 10 + i['yu_10'] + 1
						meta['nowMinNum'] = n * 10 + 1
					yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta,
										 dont_filter=True)
			elif isinstance(i['id'], int):
				meta['nowMaxNum'] = i['nowMaxNum']
				meta['nowMinNum'] = i['nowMinNum']
				meta['Num'] = i['Num']
				yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta,
									 dont_filter=True)

			else:
				continue

	def parse(self, response):
		meta = response.meta
		link = response.xpath("//div[@class='rowContainer']//a[@onclick = 'updatenoticemore(id)']/@href").extract()
		if not link:
			return None
		item = GxcrawlItem()
		alist = []
		item['ContentUrlList'] = []
		for i in range(0, len(link) + 1):
			if i == len(link):
				meta['Num'] += 1
				if meta['Num'] < meta['nowMaxNum']:
					yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta,
										 dont_filter=True)
				else:
					return None
			else:
				urlLINK = parse.urljoin(response.url, link[i])
				alist.append(urlLINK)

		item['ContentUrlList'] = alist
		item['code'] = meta['code']
		item['allpageNum'] = meta['allpageNum']
		item['bei_10'] = meta['bei_10']
		item['yu_10'] = meta['yu_10']
		item['Num'] = meta['Num']
		item['arrange'] = meta['arrange']
		item['nowMaxNum'] = meta['nowMaxNum']
		item['nowMinNum'] = meta['nowMinNum']
		# pprint.pprint(item)
		yield item



