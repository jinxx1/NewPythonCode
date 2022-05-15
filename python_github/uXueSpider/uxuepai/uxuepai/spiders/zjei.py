# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
from scrapy.linkextractors import LinkExtractor
import time
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())


class ZjeiSpider(scrapy.Spider):
    name = 'zjei'
    allowed_domains = ['zjei.gov.cn']
    start_urls = ['http://www.zjei.gov.cn/single_page/rss.shtml']

    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'))
        links = link_extractor.extract_links(response)
        for url in links:
            yield scrapy.Request(url=url.url, callback=self.parseA)

    def parseA(self,response):
        Links = response.xpath("//item/link/text()").extract()
        Time1 = response.xpath("//item/pubDate/text()").extract()
        # print(len(Links),len(Time1))
        # print(response.url)
        if len(Time1) > 0:
            for i in range(len(Time1)):
                if Time1[i].split(" ")[0] == ToDayTime:
                    yield scrapy.Request(url=Links[i].strip(), callback=self.parseB)

    def parseB(self, response):
        item = UxuepaiItem()
        Title = response.xpath("//h2//text()").extract()[0].strip()
        word1 = response.xpath("//p//text()").extract()
        if word1:
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '湛江市经济和信息化局'
            item['TitleItem'] = Title
            item['LinkItem'] = response.url
            item['TimeItem'] = int(ToDayTime.replace('-',''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'zjei.gov.cn'
            yield item

        else:
            pass
