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
today_str = datetime.date.today().strftime('%Y%m%d')
today_str1 = datetime.date.today().strftime('%Y-%m-%d')

class CpnnSpider(scrapy.Spider):
    name = 'cpnn'
    allowed_domains = ['cpnn.com.cn']
    start_urls = ['http://www.cpnn.com.cn/zdyw/default.htm']
    dupcut = get_dbdupinfo(keysName=name)


    def start_requests(self):
        meta = {}
        meta['weixinID'] = '中国电力新闻网'
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
            ddict['type'] = get_type(ddict['title'], keysListall=catJson,input_id=4,next=False)
            if ddict['type'] == 5:
                continue
            ddictList.append(ddict)
        if len(ddictList) == 0:
            return None
        else:
            for num,i in enumerate(ddictList):
                # if num >0:
                #     return None
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
        bodyList = response.xpath("//div[@class = 'cpnn-con-zhenwen']//p[not(@style)]").extract()
        item['body'] = ''.join(bodyList)

        summary = response.xpath("//meta[@name = 'Description']/@content").extract_first()
        if summary:
            item['summary'] = summary[0:60] + "..."
        else:
            item['summary'] = precessSummary(item['body'])

        item['publish'] = meta['created']
        item['created'] = meta['created']
        item['updated'] = meta['updated']
        item['timeYmd'] = meta['timeYmd']

        item['ArtUrl'] = response.url
        item['slug'] = getUrlCode() + '_{}'.format(self.name)
        item['title'] = meta['title']
        item['type'] = meta['type']
        item['media_id'] = self.name



        xpathcode = "//div[@class='cpnn-zhengwen-time']/p/text()"
        wword = response.xpath(xpathcode).extract_first()
        if wword:
            try:
                b = re.findall("来源：(.*?)日期", wword)[0]
                a = b.strip().replace('&nbsp;', '').replace(' ', '')
                item['weixinID'] = a
            except:
                item['weixinID'] = meta['weixinID']
        else:
            item['weixinID'] = meta['weixinID']


        soup = BeautifulSoup(item['body'], 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
        except:
            item['cover'] = ''

        yield item