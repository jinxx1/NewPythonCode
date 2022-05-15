# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,datetime
from urllib import parse
from gxcrawl.items import GxcrawlItem
from gxcrawl.rexGetTime import *
from gxcrawl.MongoTEST import *


class Getarticle01Spider(scrapy.Spider):
    name = 'getArticle01'
    allowed_domains = ['www.ccgp-guangxi.gov.cn']

    def start_requests(self):
        meta = {}
        MonGo_getContentUrl = MongoDB_guangxi_ContentUrl()
        find_code = {'inserTOMAINSQL': 0}

        getMongoDict = MonGo_getContentUrl.getMongoALLdate(find_code)

        # print(getMongoDict.count())
        for i in getMongoDict:
            meta['ContentUrl']=i['ContentUrl']
            meta['code'] = i['code']
            meta['inserTOMAINSQL'] = i['inserTOMAINSQL']
            meta['catName'] = i['catName']
            yield scrapy.Request(url=meta['ContentUrl'],callback=self.parse,meta=meta,dont_filter=True)


    def parse(self, response):
        meta = response.meta
        dict1 = GxcrawlItem()
        # 获取完整内容html代码
        try:
            html = response.xpath("//div[@class='frameReport']").extract()[0]
            dict1['content'] = html
        except:
            print('最终页未能获取到文章-内容', response.url)
            dict1['content'] = 0
            return None
        # 获取内容页标题
        try:
            html = response.xpath("//div[@class='frameReport']/div[@class='reportTitle']/h1/text()").extract()[0]
            dict1['title'] = html.strip()
        except:
            print('最终页未能获取到文章-标题', response.url)
            dict1['title'] = 0
            return None
        # 获取内容页时间
        try:
            html = response.xpath("//div[@class='frameReport']/div[@class='reportTitle']/span[@class='publishTime']/text()").extract()[0]
            dict1['issueTime'] = rexTimeGet(html)
        except:
            print('最终页未能获取到文章-时间', response.url)
            dict1['issueTime'] = 0
            return None

        attachments = []

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['subclass'] = meta['catName']
        dict1['attachments'] = json.dumps(attachments)


        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print(len(dict1['content']))
        print(dict1['attachments'])

        print('--------------------------------------------------------------------{}', format(datetime.datetime.now()))






