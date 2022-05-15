# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
from scrapy.linkextractors import LinkExtractor
import time
import re
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())
ToDayTime = '2018-11-21'


class JieyangSpider(scrapy.Spider):
    name = 'jieyang'
    allowed_domains = ['jieyang.net']
    start_urls = ['http://www.jieyang.net/zdmap.php']

    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'))
        links = link_extractor.extract_links(response)
        for url in links:
            yield scrapy.Request(url=url.url, callback=self.parseA)

    def parseA(self, response):
        xpathword1 = "//*[contains(text(),'{}')]/parent::*//@href".format(ToDayTime)
        xpathword2 = "//*[contains(text(),'{}')]/parent::*/parent::*//@href".format(ToDayTime)
        timeTemp = response.xpath(xpathword1).extract()
        if timeTemp:
            for i in timeTemp:
                url = response.urljoin(i)
                regex = re.findall('id=(.*?)\',',url)
                yield scrapy.Request(url='http://www.jieyang.net/news_detail.php?id=' + regex[0], callback=self.parseB)
        else:
            timeTemp = response.xpath(xpathword2).extract()
            for i in timeTemp:
                url = response.urljoin(i)
                regex = re.findall('id=(.*?)\',', url)
                yield scrapy.Request(url='http://www.jieyang.net/news_detail.php?id=' + regex[0], callback=self.parseB)

    def parseB(self, response):
        Title = response.xpath("//title//text()").extract()[0].split(',')[0].strip()
        word1 = response.xpath("//p//text()").extract()
        if word1:
            item = UxuepaiItem()
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '揭阳市经济和信息化局'
            item['TitleItem'] = Title
            item['LinkItem'] = response.url
            item['TimeItem'] = int(ToDayTime.replace('-', ''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'jieyang.net'
            yield item
            # print(Title)
            # print(response.url)
            # print(wo)
        else:
            pass