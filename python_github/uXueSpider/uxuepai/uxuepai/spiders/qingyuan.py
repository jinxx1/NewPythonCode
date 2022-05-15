#! /usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
import time
from bs4 import BeautifulSoup
from uxuepai.items import UxuepaiItem
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())

class QingyuanSpider(scrapy.Spider):
    name = 'qingyuan'
    allowed_domains = ['gdqy.gov.cn']
    start_urls = ['http://www.gdqy.gov.cn/gdqy/RSS/RSS.shtml']

    def parse(self, response):
        urls = response.xpath("//div[@class = 'right_rss2']/table//@href").extract()
        for urlt in urls:
            url = 'http://www.gdqy.gov.cn' + urlt
            yield scrapy.Request(url=url,callback=self.parseA)
    #
    def parseA(self, response):
        xmlWord1 = BeautifulSoup(response.text,'lxml-xml')#.prettify()
        xmlWord2 = xmlWord1.findAll('item')
        for xmlWord in xmlWord2:
            time1 = xmlWord.pubDate.string
            timeT = time1.split(' ')[0]
            if timeT == ToDayTime:
                title = xmlWord.title.string
                link1 = xmlWord.link.string
                yield scrapy.Request(url = link1,callback=self.parseB,meta={'Title':title,'time1':timeT})

    def parseB(self, response):
        word1 = response.xpath("//span//text()").extract()
        if word1:
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item = UxuepaiItem()
            item['NameTOTALItem'] = '清远市人民政府'
            item['TitleItem'] = response.meta['Title']
            item['LinkItem'] = response.url
            item['TimeItem'] = int(response.meta['time1'].replace('-',''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'qingyuan'
            yield item
        else:
            pass



