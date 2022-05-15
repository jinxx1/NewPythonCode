# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
import time
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())

class GdcdSpider(scrapy.Spider):
    name = 'gdcd'
    allowed_domains = ['gdcd.gov.cn']
    start_urls = ['http://www.gdcd.gov.cn/rss.jspx']

    def parse(self, response):
        Link = response.xpath("//item/link/text()").extract()
        Time1 = response.xpath("//item/pubDate/text()").extract()
        for i in range(len(Time1)):
            if Time1[i].split(' ')[0] == ToDayTime:
                yield scrapy.Request(url=Link[i], callback=self.parseA)

    def parseA(self,response):
        Title = response.xpath("//h1/text()").extract()[0]
        word1 = response.xpath("//div [@class = 'detail_content']//span//text()").extract()
        if word1:
            item = UxuepaiItem()
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '广东省交通运输厅公众网'
            item['TitleItem'] = Title
            item['LinkItem'] = response.url
            item['TimeItem'] = int(ToDayTime)
            item['WordItem'] = wo
            item['WebNameWord'] = 'gdcd.gov.cn'
            yield item
        else:
            return None


