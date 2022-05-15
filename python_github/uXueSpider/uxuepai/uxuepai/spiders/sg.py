#! /usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.link import Link
import time
import re

from uxuepai.items import UxuepaiItem
# from items import UxuepaiItem
ToDayTime = time.strftime("[%Y-%m-%d]", time.localtime())
ToDayTime1 = time.strftime("[%m-%d]", time.localtime())



class SgSpider(scrapy.Spider):
    name = 'sg'
    allowed_domains = ['sg.gov.cn']
    start_urls = ['http://www.sg.gov.cn/fzgn/wzdt/']

    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'))
        links = link_extractor.extract_links(response)
        for url in links:
            yield scrapy.Request(url=url.url, callback=self.parseA,meta = {'temurl':url.url},dont_filter=False)

    def parseA(self, response):
        Time = response.xpath("//ul/li/span/text()").extract()
        Title = response.xpath("//ul/li/span/preceding-sibling::a/text()").extract()
        Link = response.xpath("//ul/li/span/preceding-sibling::a/@href").extract()
        # print('来自parse的   d 链接：',response.meta['temurl'])
        # print('parseA正在浏览的链接：',response.url)
        for n in range(len(Time)):
            if Time[n] == ToDayTime or Time[n] == ToDayTime1:
            # if Time[n] == '2018-09-30':
                NowTimeOne = int(Time[n].replace('-', '').replace('[', '').replace(']', ''))
                if Link[n].split('/')[0] == ".":
                    url1 = response.url + Link[n].replace('./', '')
                    url2 = url1.replace('//', '/')  # 再把//全都搞成/
                    url = url2.replace('http:/', 'http://').replace('https:/', 'https://')  # 再把http:/变成http://或https
                    yield scrapy.Request(url=url, callback=self.parseB,meta={'TitleItem':Title[n],'TimeItem':NowTimeOne})


    def parseB(self, response):
        word1 = response.xpath("//p/span/text()").extract()
        if word1:
            item = UxuepaiItem()
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '韶关市人民政府'
            item['TitleItem'] = response.meta['TitleItem']
            item['LinkItem'] = response.url
            item['TimeItem'] = response.meta['TimeItem']
            item['WordItem'] = wo
            item['WebNameWord'] = 'sgsrmzf'
            yield item
        else:
            pass
