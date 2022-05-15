#! /usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
import random
from scrapy.spiders import CrawlSpider, Rule
from scrapy.link import Link
import time

from uxuepai.items import UxuepaiItem
# from items import UxuepaiItem
ToDayTime = time.strftime("%Y/%m/%d", time.localtime())#全局变量，今天日期，整理成与网页对应的时间str格式
TimeStart = 20181001
TimeEnd = 20181023
class NdrcSpider(scrapy.Spider):


    name = 'ndrc'
    allowed_domains = ['ndrc.gov.cn']
    start_urls = ['http://www.ndrc.gov.cn/jsfb/wzdt/']#网站地图


    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href','text'))#提取网站地图里的所有链接
        links = link_extractor.extract_links(response)#提取出来的链接整理成list
        for url in links:
            yield scrapy.Request(url=url.url,callback = self.parseA)


    def parseA(self,response):
        Title = response.xpath("//div[@class ='box1 ']/ul[@class = 'list_02 clearfix']/li/a/text()").extract()#查看网页list表中的文章标题
        Link  = response.xpath("//div[@class ='box1 ']/ul[@class = 'list_02 clearfix']/li/a/@href").extract()#查看网页list表中的文章标题对应的链接
        Time  = response.xpath("//div[@class ='box1 ']/ul[@class = 'list_02 clearfix']/li/font/text()").extract()#查看网页list表中的文章标题对应的发布时间
        for n in range(len(Time)):
            if Time[n] == ToDayTime:#如果今天时间对应
            # aa = int(Time[n].replace('/',''))#把爬到的时间str整理成int形式
            # if TimeStart <= aa <= TimeEnd:#如果在一个时间段内
                NowTimeOne = int(Time[n].replace('/',''))#获取文章发布的时间，整理成int，传递给item，并最终存储到sql。用来做去重参考
                if Link[n].split('/')[0] == ".":#如果抓取到的链接开头为   ./ 的话
                    turl = response.url + Link[n].replace('./','/')#先把链接头加上，再把./搞成/
                    url1 = turl.replace('//','/')#再把//全都搞成/
                    url = url1.replace('http:/', 'http://').replace('https:/', 'https://')#再把http:/变成http://或https
                    yield scrapy.Request(url=url,callback = self.parseB,meta={'TitleItem':Title[n],'TimeItem':NowTimeOne})#最后把生成的链接传递给pasreB做处理，同时传递两个参数
        tempLink = response.xpath("//h3/a/@href").extract()#页面左边list的链接抓取到
        if tempLink:#如果页面左边list有链接
            for tempurl1 in tempLink:
                if tempurl1.split('/')[0] == "..":
                    a1 = response.url.split('/')
                    a2 = a1[0] + '//' + a1[2] + '/' + a1[3] + '/'
                    tURL = a2 + tempurl1.replace('../','')
                    url1 = tURL.replace('/','/')
                    url = url1.replace('http:/','http://').replace('https:/','https://')
                    yield scrapy.Request(url=url,callback = self.parseA)


    def parseB(self,response):
        item = UxuepaiItem()
        # word1 = response.xpath("//p/span/text() | //p/text() | //p/span/font/text()").extract()
        word1 = response.xpath("//p//text()").extract()
        wo = ''
        for i1 in range(len(word1)):
            ss = word1[i1].strip()
            if len(ss) > 0:
                s = '<p>' + str(ss) + '</p>'
                wo = wo + s
        item['Pageid'] = random.randrange(10000001, 99999999, 1)
        item['NameTOTALItem'] = '发改委'
        item['TitleItem'] = response.meta['TitleItem']
        item['LinkItem'] = response.url
        item['TimeItem'] = response.meta['TimeItem']
        item['WordItem'] = wo
        item['WebNameWord'] = 'ndrc'
        yield item