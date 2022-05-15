# -*- coding: utf-8 -*-
# coding=utf-8
import scrapy
from uxuepai.items import UxuepaiItem
from uxuepai.filterHtml import filter_tags
import time

ToDayTime = time.strftime("%Y-%m-%d", time.localtime()).split('-')
nowTime = time.strftime("%Y%m%d", time.localtime())
Tyear = ToDayTime[0]
Tmouth = ToDayTime[1]
Tday = ToDayTime[2]


class C114Spider(scrapy.Spider):
    name = 'c114'
    allowed_domains = ['c114.com.cn']
    intourl ='http://www.c114.com.cn/news/roll.asp?y={}&m={}&d={}&o='.format(Tyear,Tmouth,Tday)
    start_urls = [intourl]

    def parse(self, response):
        Title = response.xpath("//div[@class ='content_c_list']/div/h6/a/text()").extract()
        Link = response.xpath("//div[@class ='content_c_list']/div/h6/a/@href").extract()
        for i in range(len(Title)):
            yield scrapy.Request(url=Link[i], callback=self.parseA, meta={'Title': Title[i]})

    def parseA(self,response):
        word1 = response.xpath("//div[@class ='text']/p").extract()
        if word1:
            item = UxuepaiItem()
            wo = ''
            for i1 in word1:
                if i1:
                    try:
                        s = '<p>' + filter_tags(i1) + '</p>'
                        wo = wo + s
                    except:
                        continue
            item['NameTOTALItem'] = 'c114通信网'
            item['TitleItem'] = response.meta['Title']
            item['LinkItem'] = response.url
            item['TimeItem'] = int(nowTime)
            item['WordItem'] = wo
            item['WebNameWord'] = 'c114'
            yield item
        else:
            pass
