#! /usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request,FormRequest

from uxuepai.items import UxuepaiItem
from scrapy.http.cookies import CookieJar
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())

class ZhaoqingSpider(scrapy.Spider):
    name = 'zhaoqing'
    allowed_domains = ['zhaoqing.gov.cn']
    start_urls = ['http://www.zhaoqing.gov.cn/xxgk/zcfg/zxwj/rss.xml',
                  'http://www.zhaoqing.gov.cn/xwzx/tzgg1/rss.xml',
                  'http://www.zhaoqing.gov.cn/xxgk/rsgz/rsrm/rss.xml',
                  'http://www.zhaoqing.gov.cn/xwzx/zqyw/rss.xml',

                  ]
    def parse(self, response):
        title = response.xpath("//item/title/text()").extract()
        link = response.xpath("//item/link/text()").extract()
        time = response.xpath("//item/pubDate/text()").extract()
        for i in range(len(time)):
            if time[i] == ToDayTime:
                url = link[i]
                yield scrapy.Request(url=url,callback=self.parseA,meta={'Title':title[i],'time1':time[i]})# 最后把生成的链接传递给pasreB做处理，同时传递两个参数

    def parseA(self, response):
        word1 = response.xpath("//p//text()").extract()
        if word1:
            item = UxuepaiItem()
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '肇庆市人民政府'
            item['TitleItem'] = response.meta['Title']
            item['LinkItem'] = response.url
            item['TimeItem'] = int(response.meta['time1'].replace('-',''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'zhaoqing'
            yield item
        else:
            pass




