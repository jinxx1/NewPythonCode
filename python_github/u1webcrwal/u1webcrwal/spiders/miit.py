# -*- coding: utf-8 -*-
import scrapy
import pprint
import json
import re
from u1webcrwal.u1parse import *
from u1webcrwal.items import U1WebcrwalItem
from urllib import parse
from bs4 import BeautifulSoup
catJson = get_catJson()



class MiitSpider(scrapy.Spider):
    name = 'miit'
    allowed_domains = ['www.miit.gov.cn']
    dupcut = get_dbdupinfo(keysName=name)
    start_urls = ['http://www.miit.gov.cn/n1146290/n1146392/index.html',
                  'http://www.miit.gov.cn/n1146290/n1146407/index.html']

    def start_requests(self):
        meta = {}
        meta['weixinID'] = '工信部'
        for i in self.start_urls:
            meta['startUrl'] = i
            yield scrapy.Request(url=i,callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='clist_con']/ul/li/span/a/@href").extract()
        if not link:
            return None
        ddictList = []
        for num,i in enumerate(link):
            ddict = {}
            ddict['url'] = parse.urljoin(response.url, i)
            if ddict['url'] in self.dupcut['ArtUrl']:
                continue
            ddict['time'] = response.xpath("//span/a[@href = '{}']/text()".format(i)).extract_first()
            ddictList.append(ddict)


        if len(ddictList) == 0:
            return None
        else:
            for i in ddictList:
                timedict = date_to_timestamp(date=i['time'])
                meta['publish'] = timedict['publish']
                meta['created'] = timedict['created']
                meta['updated'] = timedict['updated']
                meta['timeYmd'] = timedict['timeYmd']
                meta['summary'] = ''
                yield scrapy.Request(url=i['url'],callback=self.parseA,meta=meta,dont_filter=True)

    def parseA(self, response):
        meta = response.meta
        item = U1WebcrwalItem()
        item['title'] = response.xpath("//h1[@id='con_title']/text()|//title/text()").extract_first()
        if not item['title']:
            return None
        item['type'] = get_type(item['title'], keysListall=catJson)
        if item['type'] == 5:
            return None
        brow = response.xpath("//div[@id='con_con']").extract_first()

        item['body'] = get_html(brow)
        if not meta['summary']:
            item['summary'] = precessSummary(item['body'])
        else:
            item['summary'] = meta['summary']

        item['publish'] = meta['publish']
        item['created'] = meta['created']
        item['updated'] = meta['updated']
        item['timeYmd'] = meta['timeYmd']

        item['ArtUrl'] = response.url
        item['slug'] = getUrlCode() + '_{}'.format(self.name)

        try:
            laiyuan = response.xpath("//div[@class='cinfo center']/span[2]/text()").extract_first().split('：')[1]
            if laiyuan:
                item['weixinID'] = laiyuan
            else:
                item['weixinID'] = meta['weixinID']
        except:
            item['weixinID'] = meta['weixinID']



        item['media_id'] = self.name

        soup = BeautifulSoup(brow, 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
        except:
            item['cover'] = ''



        yield item