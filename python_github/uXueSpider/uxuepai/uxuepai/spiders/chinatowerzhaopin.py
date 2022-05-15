# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
import time
from uxuepai.filterHtml import filter_tags
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())
# ToDayTime = '2018-10-31'

class ChinatowerzhaopinSpider(scrapy.Spider):
    name = 'chinatowerzhaopin'
    allowed_domains = ['zhaopin.chinatowercom.cn']
    start_urls = ['http://zhaopin.chinatowercom.cn/social',
                  'http://zhaopin.chinatowercom.cn/campus',
                  'http://zhaopin.chinatowercom.cn/trainee']

    def parse(self, response):
        xpathword1 = "//*[contains(text(),'{}')]/parent::*//@href".format(ToDayTime)
        xpathword2 = "//*[contains(text(),'{}')]/parent::*/parent::*//@href".format(ToDayTime)
        timeTemp = response.xpath(xpathword1).extract()
        if timeTemp:
            for i in timeTemp:
                url = response.urljoin(i)
                yield scrapy.Request(url=url, callback=self.parseB)
        else:
            timeTemp = response.xpath(xpathword2).extract()
            for i in timeTemp:
                url = response.urljoin(i)
                yield scrapy.Request(url=url, callback=self.parseB)

    def parseB(self, response):
        word1 = response.xpath("//ul/li | //p").extract()
        if word1:
            item = UxuepaiItem()
            Title = response.xpath("//h1/text()").extract()[0]
            wo = ''
            for i1 in word1:
                if i1:
                    s = '<p>' + filter_tags(i1) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '铁塔招聘'
            item['TitleItem'] = Title
            item['LinkItem'] = response.url
            item['TimeItem'] = int(ToDayTime.re('-', ''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'chinatowercom'
            yield item
            # print(Title)
            # print(response.url)
            # print(wo)
        else:
            pass