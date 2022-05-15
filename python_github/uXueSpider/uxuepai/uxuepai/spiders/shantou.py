#! /usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from Lagou.items import LagouJobItemLoader,LagouJobItem

from uxuepai.items import UxuepaiItem
# from items import UxuepaiItem
import time

ToDayTime = time.strftime("%Y-%m-%d", time.localtime())#全局变量，今天日期，整理成与网页对应的时间str格式
TimeStart = 20181021
TimeEnd = 20181022
class ShantouSpider(scrapy.Spider):
    name = 'shantou'
    allowed_domains = ['shantou.gov.cn']
    start_urls = ['http://www.shantou.gov.cn/cnst/dbdh/wzdt.shtml']
    denydomian = ['english.shantou.gov.cn','www.shantou.gov.cn/cnst/appxz/mapp.shtml']
    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href','text'),deny_domains=self.denydomian)#提取网站地图里的所有链接
        links = link_extractor.extract_links(response)#提取出来的链接整理成list
        for url in links:
            yield scrapy.Request(url=url.url,callback = self.parseA,meta = {'temurl':url.url})
    def parseA(self, response):
        TitelC = response.xpath("//div[@class = 'list_right']/ul/li/a/text() | //div[@class = ' wzlm_right ']/ul/li/a/text()").extract()
        time = response.xpath("//div[@class = 'list_right']/ul/li/span/text() | //div[@class = ' wzlm_right ']/ul/li/span/text()").extract()
        link = response.xpath("//div[@class = 'list_right']/ul/li/a/@href | //div[@class = ' wzlm_right ']/ul/li/a/@href").extract()
        for n in range(len(time)):
            if time[n] == ToDayTime:  # 如果今天时间对应
            # aa = int(time[n].replace('-', ''))  # 把爬到的时间str整理成int形式
            # if TimeStart <= aa <= TimeEnd:  # 如果在一个时间段内
                NowTimeOne = time[n].replace('-', '')
                if link[n].split('/')[0] != 'http:' or link[n].split('/')[0] != 'https:':

                    turl = 'http://www.shantou.gov.cn/' + link[n]
                    url1 = turl.replace('//', '/')  # 再把//全都搞成/
                    url = url1.replace('http:/', 'http://').replace('https:/', 'https://')
                    # print(url)
                    yield scrapy.Request(url=url,callback=self.parseB,meta={'TitleItem': TitelC[n],'TimeItem': NowTimeOne})  # 最后把生成的链接传递给pasreB做处理，同时传递两个参数
                else:
                    print(link[n] + '*************************')
                    yield scrapy.Request(url=link[n],callback=self.parseA,meta={'TitleItem': TitelC[n],'TimeItem': NowTimeOne})  # 最后把生成的链接传递给pasreB做处理，同时传递两个参数
    def parseB(self, response):
        # print(response.url)
        word1 = response.xpath("//p//text()").extract()
        if word1:
            item = UxuepaiItem()
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '汕头市人民政府'
            item['TitleItem'] = response.meta['TitleItem']
            item['LinkItem'] = response.url
            item['TimeItem'] = int(response.meta['TimeItem'])
            item['WordItem'] = wo
            item['WebNameWord'] = 'shantou'
            yield item
        else:
            pass




