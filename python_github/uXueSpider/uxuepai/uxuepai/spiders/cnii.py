# -*- coding: utf-8 -*-
import scrapy

from uxuepai.items import UxuepaiItem
import time
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())

class CniiSpider(scrapy.Spider):
    name = 'cnii'
    allowed_domains = ['cnii.com.cn']
    start_urls = ['http://www.cnii.com.cn/node_33989.htm']

    def parse(self, response):
        # print(response.text)
        Time = response.xpath("//ul[@class = 'list2']/li/span/text()").extract()
        Title = response.xpath("//ul[@class = 'list2']/li/a/text()").extract()
        Link = response.xpath("//ul[@class = 'list2']/li/a/@href").extract()
        for i in range(len(Title)):
            if Time[i] == ToDayTime:
                TitleT = Title[i]
                LinkT = 'http://www.cnii.com.cn/' + Link[i]
                yield scrapy.Request(url=LinkT, callback=self.parseA,
                                     meta={'Title': TitleT, 'time1': Time[i].replace('-', '')})
    def parseA(self,response):
        word1 = response.xpath("//p//text()").extract()
        if word1:
            item = UxuepaiItem()
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = 'cnii中国信息产业网'
            item['TitleItem'] = response.meta['Title']
            item['LinkItem'] = response.url
            item['TimeItem'] = int(response.meta['time1'])
            item['WordItem'] = wo
            item['WebNameWord'] = 'cnii'
            yield item
        else:
            pass
