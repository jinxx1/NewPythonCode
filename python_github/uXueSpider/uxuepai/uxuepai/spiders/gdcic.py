# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
from scrapy.linkextractors import LinkExtractor
import time
ToDayTime = time.strftime("%Y%m%d", time.localtime())


class GdcicSpider(scrapy.Spider):
    name = 'gdcic'
    allowed_domains = ['gdcic.gov.cn']
    start_urls = ['http://www.gdcic.gov.cn/About/Sitemap_CN']


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

    def parseB(self, response):
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
            # item['NameTOTALItem'] = '广东省住房和城乡建设厅'
            # item['TitleItem'] = Title
            # item['LinkItem'] = response.url
            # item['TimeItem'] = int(ToDayTime)
            # item['WordItem'] = wo
            # item['WebNameWord'] = 'gdcic.gov.cn'
            # yield item
            print(Title)
            print(response.url)
            print(int(ToDayTime))
            print(wo)
        else:
            pass
