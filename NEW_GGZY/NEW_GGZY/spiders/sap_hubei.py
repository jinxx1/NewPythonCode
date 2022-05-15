# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib

from urllib import parse
from NEW_GGZY.Breakpoint import *

from NEW_GGZY.items import GgzyItem



class SapHubeiSpider(scrapy.Spider):
    name = 'sap_hubei'
    allowed_domains = ['www.hrtn.com.cn']
    start_url = ['http://www.hrtn.com.cn/list/34.html?page={}']

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        meta['catName'] = '湖北广电_公示公告'
        getTXTdict = getTXT(self.name, self.start_url)
        for i in getTXTdict['urlDict']:
            meta['indexUrl'] = i
            yield scrapy.Request(url=meta['indexUrl'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        linkList = response.xpath("//div[@class='pwap cmain']/div[@class='crarea fr']/ul[@class='nlist']/li/a/@href").extract()
        if not linkList:
            return None
        link = duplicateUrl(linkList,response.url)
        del linkList
        if not link:
            return None
        print(len(link))
        print(meta['catName'])
        print(response.url)
        print('-------------------------------------')
        # for i in link:
        #     meta['url'] = parse.urljoin(response.url, i)
        #     yield scrapy.Request(url=meta['url'],callback=self.parseA,meta=meta,dont_filter=True)
        # del link

        meta['Num']+=1
        yield scrapy.Request(url=meta['indexUrl'].format(str(meta['Num'])),
                             callback=self.parse, meta=meta, dont_filter=True)



    def parseA(self,response):
        # print('进入文章了')
        meta = response.meta
        dict1 = GgzyItem()


        dict1['title'] = response.xpath("//div[@class='pwap cmain']/div[@class='crarea fr']/div[@class='zw']/div[@class='title']/text()").extract_first().strip()
        if not dict1['title']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 标题')
            print(response.url)
            return None

        dict1['content'] = response.xpath("//div[@class='pwap cmain']/div[@class='crarea fr']/div[@class='zw']").extract_first()
        if not dict1['content']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 内容')
            print(response.url)
            return None



        issueTime = response.xpath("/html/body/div[@class='pwap cmain']/div[@class='crarea fr']/div[@class='zw']/div[@class='about']/text()").extract_first()
        dict1['issueTime'] = timeReMark(issueTime)
        if not dict1['issueTime']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 时间')
            print(response.url)
            return None



        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['subclass'] = meta['catName']

        del meta

        yield dict1