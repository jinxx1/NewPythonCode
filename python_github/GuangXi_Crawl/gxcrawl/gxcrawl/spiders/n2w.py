# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
# from gxcrawl.Exist import *
from urllib import parse
from gxcrawl.items import GxcrawlItem


class N2wSpider(scrapy.Spider):
    name = 'n2w'
    allowed_domains = ['www.ccgp-guangxi.gov.cn']
    urlList =[{
		'catName': '广西省_市县级_成交公告',
		'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_cjgg/param_bulletin/20/page_{}.html',
		'allpageNum': 11249,
		'bei_10': 1124,
		'yu_10': 9,
		'code': 'sc8o'},{
		'catName': '广西省_市县级_采购公告',
		'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_cggg/param_bulletin/20/page_{}.html',
		'allpageNum': 19326,
		'bei_10': 1932,
		'yu_10': 6,
		'code': 'Wph0'}]



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

            elif isinstance(i['id'],int):
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
        item['ContentUrlList']=[]
        for i in range(0,len(link)+1):
            if i == len(link):
                meta['Num'] += 1
                if meta['Num'] < meta['nowMaxNum']:
                    yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta,
                                         dont_filter=True)
                else:
                    return None
            else:
                urlLINK = parse.urljoin(response.url,link[i])
                alist.append(urlLINK)


        item['ContentUrlList']=alist
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