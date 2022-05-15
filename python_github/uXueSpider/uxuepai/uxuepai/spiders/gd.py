# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
import time
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())
# ToDayTime = '2018-11-25'

class GdSpider(scrapy.Spider):
    name = 'gd'
    allowed_domains = ['gd.gov.cn']
    start_urls = [
        'http://www.gd.gov.cn/zwgk/gsgg/index.html',
        'http://www.gd.gov.cn/zwgk/zcjd/wjjd/index.html',
        'http://www.gd.gov.cn/zwgk/zcjd/gnzcsd/index.html',
        'http://www.gd.gov.cn/zwgk/zcjd/snzcsd/index.html',
        'http://www.gd.gov.cn/zwgk/zdlyxxgkzl/xzsp/index.html',
        'http://www.gd.gov.cn/gdywdt/ydylygd/index.html',
        'http://www.gd.gov.cn/gdywdt/dczl/gcls/index.html',
        'http://www.gd.gov.cn/gdywdt/dczl/dcxd/index.html',
        'http://www.gd.gov.cn/gdywdt/gdyw/index.html',
        'http://www.gd.gov.cn/gdywdt/dsdt/index.html',
        'http://www.gd.gov.cn/gdywdt/bmdt/index.html',
        'http://www.gd.gov.cn/gdywdt/zfjg/index.html',
        'http://www.gd.gov.cn/gdywdt/dczl/jcbs/index.html']
    def parse(self, response):
        Title = response.xpath("//div[@class = 'viewList']/ul/li/span[@class ='til']/a/text()").extract()
        Link = response.xpath("//div[@class = 'viewList']/ul/li/span[@class ='til']/a/@href").extract()
        Time1 = response.xpath("//div[@class = 'viewList']/ul/li/span[@class ='time']/text()").extract()
        for i in range(len(Title)):
            if Time1[i] == ToDayTime:
                yield scrapy.Request(url=Link[i], callback=self.parseA, meta={'title': Title[i], 'time1': Time1[i]})

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
            # print(response.meta['title'])
            # print(response.url)
            # print(response.meta['time1'].replace('-', ''))
            # print(wo)
            item['NameTOTALItem'] = '广东省人民政府'
            item['TitleItem'] = response.meta['title']
            item['LinkItem'] = response.url
            item['TimeItem'] = int(response.meta['time1'].replace('-', ''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'gd.gov.cn'
            yield item
        else:
            pass


