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

class BjxSpider(scrapy.Spider):
    name = 'bjx'
    allowed_domains = ['www.bjx.com.cn']
    dupcut = get_dbdupinfo(keysName=name)
    start_urls = ['http://news.bjx.com.cn/list?page={}',
                  'http://news.bjx.com.cn/list?catid=100&page={}',
                  'http://news.bjx.com.cn/zt.asp?topic=%b5%e7%c1%a6%cd%a8%d0%c5&page={}',
                  'http://shupeidian.bjx.com.cn/dwjs/?page={}'
                  ]


    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        meta['weixinID'] = '北极星电力网'
        for i in self.start_urls:
            meta['startUrl'] = i
            yield scrapy.Request(url=i.format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):

        meta = response.meta
        link = response.xpath("//div[@class='list_left']/ul[@class='list_left_ztul']/li/a/@href|//div[@class='list_left']/ul[@class='list_left_ul']/li/a/@href").extract()

        if not link:
            return None
        ddictList = []
        for num, i in enumerate(link):
            ddict = {}
            ddict['url'] = parse.urljoin(response.url, i)
            if ddict['url'] in self.dupcut['ArtUrl']:
                continue
            ddict['title'] = response.xpath("//*[@href = '{}']/@title".format(i)).extract_first()
            if ddict['title'] in self.dupcut['title']:
                continue
            ddict['time'] = response.xpath("//*[@href = '{}']/../span/text()".format(i)).extract_first().replace('.','-')
            ddict['type'] = get_type(ddict['title'], keysListall=catJson, input_id=4, next=False)
            if ddict['type'] == 5:
                continue
            ddictList.append(ddict)

        if len(ddictList) == 0:
            return None
        else:

            for i in ddictList:
                meta['type'] = i['type']
                meta['title'] = i['title']
                timedict = date_to_timestamp(date=i['time'])
                meta['publish'] = timedict['publish']
                meta['created'] = timedict['created']
                meta['updated'] = timedict['updated']
                meta['timeYmd'] = timedict['timeYmd']
                meta['summary'] = ''
                yield scrapy.Request(url=i['url'], callback=self.parseA, meta=meta, dont_filter=True)


    def parseA(self, response):
        meta = response.meta
        item = U1WebcrwalItem()
        brow = response.xpath("//div[@id='content']/p").extract()
        item['body'] = get_html(''.join(brow))
        item['body'] = item['body'].replace('src','sssss')
        item['body'] = item['body'].replace('data-echo', 'src')
        if len(item['body'])<10:
            return None
        if not meta['summary']:
            item['summary'] = precessSummary(item['body'])
        else:
            item['summary'] = meta['summary']


        item['publish'] = meta['publish']
        item['created'] = meta['created']
        item['updated'] = meta['updated']
        item['timeYmd'] = meta['timeYmd']


        ttime = response.xpath("//div[@class='list_copy']/b[2]/text()").extract_first()
        if ttime:
            try:
                publish = date_to_timestamp(ttime,format_string='%Y/%m/%d %H:%M')
                item['publish'] = publish['publish']
                item['created'] = publish['created']
                item['updated'] = publish['updated']
                item['timeYmd'] = publish['timeYmd']
            except:
                item['publish'] = meta['created']
                item['created'] = meta['created']
                item['updated'] = meta['updated']
                item['timeYmd'] = meta['timeYmd']
        else:
            item['publish'] = meta['created']
            item['created'] = meta['created']
            item['updated'] = meta['updated']
            item['timeYmd'] = meta['timeYmd']


        try:
            laiyuan = response.xpath("//div[@class='list_copy']/b[1]/text()").extract_first().split(':')[1]
            if laiyuan:
                item['weixinID'] = laiyuan
            else:
                item['weixinID'] = meta['weixinID']
        except:
            item['weixinID'] = meta['weixinID']




        item['title'] = meta['title']
        item['ArtUrl'] = response.url
        item['slug'] = getUrlCode() + '_{}'.format(self.name)
        item['cover'] = ''
        item['type'] = meta['type']


        item['media_id'] = self.name

        # soup = BeautifulSoup(item['body'], 'lxml')
        # try:
        #     imgSrc = soup.img.get('src')
        #     item['cover'] = parse.urljoin(response.url, imgSrc)
        # except:
        #     item['cover'] = ''

        yield item