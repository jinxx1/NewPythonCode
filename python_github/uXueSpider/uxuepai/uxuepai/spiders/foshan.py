#! /usr/bin/python

# -*- coding: utf-8 -*-

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from Lagou.items import LagouJobItemLoader,LagouJobItem

from uxuepai.items import UxuepaiItem
import time

ToDayTime = time.strftime("%Y-%m-%d", time.localtime())#全局变量，今天日期，整理成与网页对应的时间str格式
TimeStart = 20181021
TimeEnd = 20181031
dict1 = {'quchword': ''}


class FoshanSpider(scrapy.Spider):
    name = 'foshan'
    allowed_domains = ['www.foshan.gov.cn']
    start_urls = ['http://www.foshan.gov.cn/wzbz/wzdt/']
    otherUrls = ['http://www.foshan.gov.cn/zwgk/zwdt/wqdt/ccq/',
                 'http://www.foshan.gov.cn/zwgk/zwdt/wqdt/nhq/',
                 'http://www.foshan.gov.cn/zwgk/zwdt/wqdt/sdq/',
                 'http://www.foshan.gov.cn/zwgk/zwdt/wqdt/gmq/',
                 'http://www.foshan.gov.cn/zwgk/zwdt/wqdt/ssq/',
                 'http://www.foshan.gov.cn/zwgk/zwdt/bmdt/'
                 ]


    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'),allow_domains=self.allowed_domains)  # 提取网站地图里的所有链接
        links = link_extractor.extract_links(response)  # 提取出来的链接整理成list
        for url in links:
            yield scrapy.Request(url=url.url, callback=self.parseA,dont_filter=False)
        for urlother in self.otherUrls:
            yield scrapy.Request(url=urlother, callback=self.parseA, dont_filter=False)

    def parseA(self, response):
        times = response.xpath("//li[@class = 'clearfix']/span/text()").extract()
        links = response.xpath("//li[@class = 'clearfix']/a/@href").extract()
        for n in range(len(times)):
            # aa = times[n].replace('-','')
            # if TimeStart <=int(aa) <= TimeEnd:
            if times[n] == ToDayTime:
                url = response.url + links[n].replace('./','')
                yield scrapy.Request(url=url, callback=self.parseB, dont_filter=False)
    def parseB(self, response):
        word1 = response.xpath("//p//text() | //div/text()").extract()
        if word1:
            item = UxuepaiItem()
            time = response.xpath("//meta[@name ='PubDate']/@content").extract()
            title = response.xpath("//meta[@name ='ArticleTitle']/@content").extract()
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '佛山市人民政府'
            item['TitleItem'] = title[0]
            item['LinkItem'] = response.url
            item['TimeItem'] = int(time[0].replace('-',''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'foshan'
            yield item
        else:
            pass