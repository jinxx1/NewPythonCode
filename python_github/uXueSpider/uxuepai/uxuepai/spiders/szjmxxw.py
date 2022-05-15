# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
from scrapy.linkextractors import LinkExtractor
import time
ToDayTime = time.strftime("%Y%m%d", time.localtime())


class SzjmxxwSpider(scrapy.Spider):
    name = 'szjmxxw'
    allowed_domains = ['szjmxxw.gov.cn']
    start_urls = ['http://www.szjmxxw.gov.cn/fzlm/wzdt/']

    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'))
        links = link_extractor.extract_links(response)
        for url in links:
            yield scrapy.Request(url=url.url, callback=self.parseA)

    def parseA(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'))
        links = link_extractor.extract_links(response)
        for url in links:
            urlYes = url.url.find(ToDayTime)
            if urlYes >= 0:
                yield scrapy.Request(url=url.url, callback=self.parseB)

    def parseB(self,response):
        item = UxuepaiItem()
        Title = response.xpath("//meta[@name = 'ArticleTitle']/@content").extract()[0].strip()
        word1 = response.xpath("//p//text()").extract()
        if word1:
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '深圳市经济贸易和信息化委员会'
            item['TitleItem'] = Title
            item['LinkItem'] = response.url
            item['TimeItem'] = int(ToDayTime)
            item['WordItem'] = wo
            item['WebNameWord'] = 'szjmxxw.gov.cn'
            yield item
            # print(Title)
            # print(response.url)
            # print(int(ToDayTime))
            # print(wo)
        else:
            pass
