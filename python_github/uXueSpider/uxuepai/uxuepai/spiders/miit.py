#! /usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
import time

from uxuepai.items import UxuepaiItem

ToDayTime = time.strftime("%Y-%m-%d", time.localtime())

class MiitSpider(scrapy.Spider):
    name = 'miit'
    allowed_domains = ['miit.gov.cn']
    start_urls = ['http://miit.gov.cn/n1146322/n3733725/index.html']

    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'))  # 提取网站地图里的所有链接
        links = link_extractor.extract_links(response)  # 提取出来的链接整理成list
        for url in links:
            yield scrapy.Request(url=url.url, callback=self.parseA)

    def parseA(self,response):
        Link = response.xpath("//li/a/@href").extract()
        Title = response.xpath("//li/a/text()").extract()
        Time = response.xpath("//li/span/a/text()").extract()
        for i in range(len(Time)):
            if Time[i] == ToDayTime:
                TitleT = Title[i]
                LinkT = Link[i].replace('../../', 'http://miit.gov.cn/')
                yield scrapy.Request(url = LinkT,callback=self.parseB,meta={'Title':TitleT,'time1':Time[i].replace('-','')})

    def parseB(self,response):
        item = UxuepaiItem()
        word1 = response.xpath("//p//text()").extract()
        wo = ''
        for i1 in range(len(word1)):
            ss = word1[i1].strip()
            if len(ss) > 0:
                s = '<p>' + str(ss) + '</p>'
                wo = wo + s
        item['NameTOTALItem'] = '工信部'
        item['TitleItem'] = response.meta['Title']
        item['LinkItem'] = response.url
        item['TimeItem'] = int(response.meta['time1'])
        item['WordItem'] = wo
        item['WebNameWord'] = 'miit'
        yield item

