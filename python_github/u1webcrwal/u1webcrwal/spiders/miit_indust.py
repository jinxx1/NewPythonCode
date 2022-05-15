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

class MiitIndustSpider(scrapy.Spider):
    name = 'miit_indust'
    dupcut = get_dbdupinfo(keysName=name)
    allowed_domains = ['www.miit.gov.cn']
    start_urls = ['http://www.miit.gov.cn/n973401/n5993937/n5993953/index_5999141_{}.html',
'http://www.miit.gov.cn/n973401/n5993937/n5993958/index_5999141_{}.html',
'http://www.miit.gov.cn/n973401/n5993937/n5993963/index_5999141_{}.html',
'http://www.miit.gov.cn/n973401/n5993937/n5993973/index_5999141_{}.html',
'http://www.miit.gov.cn/n973401/n5993937/n5993968/index_5999141_{}.html']


    def start_requests(self):
        meta = {}
        meta['Num'] = 0

        meta['weixinID'] = '工信部-工业互联'
        for i in self.start_urls:
            meta['startUrl'] = i
            yield scrapy.Request(url=i.replace('index_5999141_{}.html','index.html'),callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='list center wryh14gray']/ul/li/a/@href").extract()
        if not link:
            return None
        ddictList = []
        for num,i in enumerate(link):
            ddict = {}
            ddict['url'] = parse.urljoin(response.url, i)
            if ddict['url'] in self.dupcut['ArtUrl']:
                continue
            ddict['title'] = response.xpath("//*[@href = '{}']/text()".format(i)).extract_first()
            if ddict['title'] in self.dupcut['title']:
                continue
            ddict['time'] = response.xpath("//*[@href = '{}']/../span/text()".format(i)).extract_first()
            ddict['type'] = get_type(ddict['title'], keysListall=catJson, input_id=6, next=True)
            if ddict['type'] == 5:
                continue
            ddictList.append(ddict)

        if len(ddictList) == 0:
            return None
        else:
            for i in ddictList:
                meta['title'] = i['title']
                meta['type'] = i['type']
                timedict = date_to_timestamp(date=i['time'])
                meta['publish'] = timedict['publish']
                meta['created'] = timedict['created']
                meta['updated'] = timedict['updated']
                meta['timeYmd'] = timedict['timeYmd']
                meta['summary'] = ''
                yield scrapy.Request(url=i['url'],callback=self.parseA,meta=meta,dont_filter=True)

        # meta['Num'] += 1
        # yield scrapy.Request(url=meta['startUrl'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)

    def parseA(self, response):
        meta = response.meta
        item = U1WebcrwalItem()
        brow = response.xpath("//div[@class='main center']/div[@class='content']/div[@class='center con']").extract_first()

        item['body'] = get_html(brow)
        if not meta['summary']:
            item['summary'] = precessSummary(item['body'])
        else:
            item['summary'] = meta['summary']
        item['title'] = meta['title']
        item['type'] = meta['type']
        item['publish'] = meta['publish']
        item['created'] = meta['created']
        item['updated'] = meta['updated']
        item['timeYmd'] = meta['timeYmd']
        item['weixinID'] = meta['weixinID']
        item['ArtUrl'] = response.url
        item['slug'] = getUrlCode() + '_{}'.format(self.name)
        item['media_id'] = self.name
        soup = BeautifulSoup(brow, 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
        except:
            item['cover'] = ''
        yield item


