# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
import time
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())


class GzjtSpider(scrapy.Spider):
    name = 'gzjt'
    allowed_domains = ['gzjt.gov.cn']
    start_urls = [
                    'http://www.gzjt.gov.cn/gzjt/gzdt/list.shtml',
                    'http://www.gzjt.gov.cn/gzjt/xwdt_hygk/list.shtml',
                    'http://www.gzjt.gov.cn/gzjt/xwdt_wgk/list.shtml',
                    'http://www.gzjt.gov.cn/gzjt/tzgg/list.shtml',
                    'http://www.gzjt.gov.cn/gzjt/zbgg/list.shtml'
    ]

    def parse(self, response):
        Link = response.xpath("//ul[@class ='News_list']/li/a/@href").extract()
        Time1 = response.xpath("//ul[@class ='News_list']/li/span/text()").extract()
        for i in range(len(Time1)):
            if Time1[i] == ToDayTime:
                url = Link[i].replace('../../','http://www.gzjt.gov.cn/')
                yield scrapy.Request(url = url,callback=self.parseA)

    def parseA(self,response):
        item = UxuepaiItem()
        Title = response.xpath("//meta[@name = 'ArticleTitle']/@content").extract()[0].strip()
        word1 = response.xpath("//p//text()").extract()
        wo = ''
        for i1 in range(len(word1)):
            ss = word1[i1].strip()
            if len(ss) > 0:
                s = '<p>' + str(ss) + '</p>'
                wo = wo + s
        item['NameTOTALItem'] = '广州市交通委员会'
        item['TitleItem'] = Title
        item['LinkItem'] = response.url
        item['TimeItem'] = int(ToDayTime.replace('-',''))
        item['WordItem'] = wo
        item['WebNameWord'] = 'gzjt.gov.cn'
        yield item