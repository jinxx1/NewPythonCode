#! /usr/bin/python
# -*- coding: utf-8 -*-
from uxuepai.filterHtml import filter_tags
import scrapy
import time

from uxuepai.items import UxuepaiItem
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())


class ChaozhouSpider(scrapy.Spider):
    name = 'chaozhou'
    allowed_domains = ['chaozhou.gov.cn']
    start_urls = ['http://www.chaozhou.gov.cn/rss.jspx']

    def parse(self, response):
        title = response.xpath("//item/title/text()").extract()
        link = response.xpath("//item/link/text()").extract()
        time = response.xpath("//item/pubDate/text()").extract()
        for i in range(len(time)):
            timeT = time[i].split(' ')[0]
            if timeT == ToDayTime:
                url = link[i]
                yield scrapy.Request(url=url,callback=self.parseA,meta={'Title':title[i],'time1':timeT})# 最后把生成的链接传递给pasreB做处理，同时传递两个参数

    def parseA(self, response):
        word1 = response.xpath("//p").extract()
        if word1:
            wo = ''
            for i1 in word1:
                if i1:
                    s = '<p>' + filter_tags(i1) + '</p>'
                    wo = wo + s
            # print(wo)
            item = UxuepaiItem()
            item['NameTOTALItem'] = '潮州市人民政府'
            item['TitleItem'] = response.meta['Title']
            item['LinkItem'] = response.url
            item['TimeItem'] = int(response.meta['time1'].replace('-',''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'chaozhou'
            yield item
        else:
            pass
