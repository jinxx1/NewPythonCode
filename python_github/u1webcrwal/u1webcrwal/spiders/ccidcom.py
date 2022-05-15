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


class CcidcomSpider(scrapy.Spider):
    name = 'ccidcom'
    allowed_domains = ['www.ccidcom.com']
    dupcut = get_dbdupinfo(keysName=name)
    start_urls = ['http://www.ccidcom.com/yaowen/index.html']

    def start_requests(self):
        meta = {}
        meta['Num'] = 0
        meta['weixinID'] = '通信产业网'
        for i in self.start_urls:
            meta['startUrl'] = i
            yield scrapy.Request(url=i,callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        meta['postUrl'] = 'http://www.ccidcom.com/getcolumnarts.do'
        try:
            regex = re.findall("(csrf.*)\'}", response.text)[0].replace("'", "").split(':')
        except:
            return ''
        meta['postDate'] = {
            'colnum_name': 'yaowen',
            'start': '1',
            'page': '1',
            regex[0]: regex[1]
        }
        yield scrapy.FormRequest(url=meta['postUrl'],formdata=meta['postDate'],callback=self.parseA,meta=meta,dont_filter=True)

    def parseA(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)['arts']


        for i in jsonT:

            meta['type'] = get_type(i['title'], keysListall=catJson, input_id=2, next=True)
            if meta['type'] == 5:
                continue
            meta['title'] = i['title']
            if meta['title'] in self.dupcut['title']:
                continue
            meta['ArtUrl'] = parse.urljoin(response.url, i['art_url'])
            if meta['ArtUrl'] in self.dupcut['ArtUrl']:
                continue
            timedict = timeall(ctime=i['create_at'])
            meta['weixinID'] = i['source']
            meta['publish'] = timedict['publish']
            meta['created'] = timedict['created']
            meta['updated'] = timedict['updated']
            meta['timeYmd'] = timedict['timeYmd']
            meta['summary'] = i['summary'][0:97] + '...'
            meta['cover'] = i['firstimg']
            meta['ArtUrl'] = parse.urljoin(response.url, i['art_url'])
            # yield scrapy.Request(url=meta['ArtUrl'],callback=self.parseB,meta=meta,dont_filter=True)


    def parseB(self, response):

        meta = response.meta
        item = U1WebcrwalItem()
        brow = response.xpath("//div[@class='content']").extract_first()
        item['body'] = get_html(brow)

        if not meta['summary']:
            item['summary'] = precessSummary(item['body'])
        else:
            item['summary'] = meta['summary']
        item['title'] = meta['title']
        item['cover'] = meta['cover']
        item['publish'] = meta['publish']
        item['created'] = meta['created']
        item['updated'] = meta['updated']
        item['timeYmd'] = meta['timeYmd']
        item['weixinID'] = meta['weixinID']
        item['ArtUrl'] = meta['ArtUrl']
        item['type'] = meta['type']
        item['slug'] = getUrlCode() + '_{}'.format(self.name)
        item['media_id'] = self.name

        yield item



