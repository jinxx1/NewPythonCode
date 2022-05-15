# -*- coding: utf-8 -*-
import scrapy
import pprint
import json
import re
from u1webcrwal.u1parse import *
from u1webcrwal.items import U1WebcrwalItem
from urllib import parse
from bs4 import BeautifulSoup
import datetime
catJson = get_catJson()
today_str = datetime.date.today().strftime('%Y/%m%d')
today_str1 = datetime.date.today().strftime('%Y-%m-%d')

class PeopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['people.com']
    dupcut = get_dbdupinfo(keysName=name)
    start_urls = ['http://finance.people.com.cn/GB/70846/index.html',
                  'http://society.people.com.cn/GB/136657/index.html',
                  'http://industry.people.com.cn/GB/413887/index.html',
                  'http://industry.people.com.cn/GB/413888/index.html',
                  'http://industry.people.com.cn/GB/413888/index.html',
                  'http://it.people.com.cn/GB/243510/index.html',
                  'http://edu.people.com.cn/GB/1053/index.html',
                  'http://scitech.people.com.cn/GB/1057/index.html',
                  'http://kpzg.people.com.cn/'
                  ]

    def start_requests(self):
        meta = {}
        meta['weixinID'] = '人民网'
        for i in self.start_urls:
            meta['startUrl'] = i
            yield scrapy.Request(url=i,callback=self.parse,meta=meta,dont_filter=True)
    def parse(self, response):
        meta = response.meta
        link1 = response.xpath("//*[contains(@href,'{}')]/@href".format(today_str)).extract()
        link = list(set(link1))
        if not link:
            return None
        ddictList = []
        for num, i in enumerate(link):
            ddict = {}
            ddict['url'] = parse.urljoin(response.url, i)
            if ddict['url'] in self.dupcut['ArtUrl']:
                continue
            ddict['title'] = response.xpath("//a[@href = '{}']/text()".format(i)).extract_first()
            ddict['type'] = get_type(ddict['title'], keysListall=catJson)
            if ddict['type'] == 5:
                continue
            ddictList.append(ddict)
        if len(ddictList) == 0:
            return None
        else:
            for i in ddictList:
                meta['title'] = i['title']
                meta['type'] = i['type']
                timedict = date_to_timestamp(date=today_str1)
                meta['publish'] = timedict['publish']
                meta['created'] = timedict['created']
                meta['updated'] = timedict['updated']
                meta['timeYmd'] = timedict['timeYmd']
                yield scrapy.Request(url=i['url'], callback=self.parseA, meta=meta, dont_filter=True)

    def parseA(self, response):
        item = U1WebcrwalItem()
        meta = response.meta
        item['body'] = response.xpath("//div[@id = 'rwb_zw']").extract_first().replace('\n','').replace('\t','').replace('\r','').replace(r'\xa0','')
        if len(item['body']) < 100:
            return None
        summary = response.xpath("//meta[@name = 'description']/@content").extract_first()
        if summary:
            item['summary'] = summary[0:60] + "..."
        else:
            item['summary'] = precessSummary(item['body'])


        ttime = response.xpath("//div[@class='box01']/div[@class='fl']/text()").extract_first().replace('来源：','').replace('&nbsp;','').replace('日','日 ')

        if ttime:
            try:
                publish = date_to_timestamp(ttime,format_string='%Y年%m月%日 %H:%M')
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
            laiyuan = response.xpath("//div[@class='box01']/div[@class='fl']/a/text()").extract_first()
            if laiyuan:
                item['weixinID'] = laiyuan
            else:
                item['weixinID'] = meta['weixinID']
        except:
            item['weixinID'] = meta['weixinID']


        item['ArtUrl'] = response.url
        item['slug'] = getUrlCode() + '_{}'.format(self.name)
        item['title'] = meta['title']
        item['type'] = meta['type']

        item['media_id'] = self.name


        soup = BeautifulSoup(item['body'], 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
        except:
            item['cover'] = ''

        yield item