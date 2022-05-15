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



class CniiSpider(scrapy.Spider):
    name = 'cnii'
    allowed_domains = ['www.cnii.gov.cn']
    dupcut = get_dbdupinfo(keysName=name)
    # dupcut = {}
    # dupcut['title']=[]
    # dupcut['ArtUrl'] = []

    start_urls = ['http://www.cnii.com.cn/gxyw/',
                      'http://www.cnii.com.cn/dtxw/',
                     'http://www.cnii.com.cn/xxtx/',
                    'http://www.cnii.com.cn/gyjj/',
                   'http://www.cnii.com.cn/zcfg/',
                  'http://www.cnii.com.cn/cygh/',
                  'http://www.cnii.com.cn/kjcx/',
                  'http://www.cnii.com.cn/zxqy/',
                  'http://www.cnii.com.cn/tjsj/',
                  'http://www.cnii.com.cn/lsjn/',
                  'http://www.cnii.com.cn/aqsc/',
                  'http://www.cnii.com.cn/djzc/',
                  'http://www.cnii.com.cn/rmydb/']


    def start_requests(self):
        meta = {}
        meta['weixinID'] = '中国信息产业网'
        for i in self.start_urls:
            meta['startUrl'] = i
            yield scrapy.Request(url=i,callback=self.parse,meta=meta,dont_filter=True)



    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='mainNews']//li/a/@href").extract()

        if not link:
            return None
        ddictList = []
        for num,i in enumerate(link):
            ddict = {}
            ddict['title'] = response.xpath("//*[@href = '{}']/text()".format(i)).extract_first()
            if ddict['title'] in self.dupcut['title']:
                continue
            ddict['type'] = get_type(ddict['title'], keysListall=catJson)
            if ddict['type'] == 5:
                continue
            ddict['url'] = parse.urljoin(response.url, i)
            if ddict['url'] in self.dupcut['ArtUrl']:
                continue
            ddict['time'] = response.xpath("//*[@href = '{}']/../span/text()".format(i)).extract_first().replace('.','-')
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



    def parseA(self, response):
        meta = response.meta

        item = U1WebcrwalItem()
        brow = response.xpath("//div[@id='divContent']").extract_first()


        item['body'] = get_html(brow).replace('新闻附件：','')

        if not meta['summary']:
            item['summary'] = precessSummary(item['body'])
        else:
            item['summary'] = meta['summary']

        ttime = response.xpath("//span[@class='detail_pubTime fl']/span/text()").extract_first()

        if ttime:
            try:
                publish = date_to_timestamp(ttime,format_string='%Y-%m-%d %H:%M')
                item['publish'] = publish['publish']
                item['created'] = publish['created']
                item['updated'] = publish['updated']
                item['timeYmd'] = publish['timeYmd']
            except:
                item['publish'] = meta['publish']
                item['created'] = meta['created']
                item['updated'] = meta['updated']
                item['timeYmd'] = meta['timeYmd']
        else:
            item['publish'] = meta['publish']
            item['created'] = meta['created']
            item['updated'] = meta['updated']
            item['timeYmd'] = meta['timeYmd']

        try:
            laiyuan = response.xpath("//div[@class='articleInfo']/span[@class='source fl']/text()").extract_first().split('：')[1]
            if laiyuan:
                item['weixinID'] = laiyuan
            else:
                item['weixinID'] = meta['weixinID']
        except:
            item['weixinID'] = meta['weixinID']


        item['title'] = meta['title']

        item['type'] = meta['type']
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
