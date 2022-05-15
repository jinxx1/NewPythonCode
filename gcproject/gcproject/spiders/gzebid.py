# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint,datetime
from urllib import parse
from bs4 import BeautifulSoup
from gcproject.items import GcprojectItem
from gcproject.parseScrpy import get_location,get_timestr
from gcproject.mysqlprecess import get_dupurl


# 网站接口更换。需要重新做。
class GzebidSpider(scrapy.Spider):
    name = 'gzebid'
    allowed_domains = ['www.gzebid.cn']
    start_urls = 'https://www.gzebid.cn/web-list/articles?categoryId={catID}&pageNumber={Num}&pageSize=1000&title=&pushTime='

    catName = [
                {'subclass': '招标公告', 'catID': 'b66478f0930d4162be8df579268b39a7'},
                {'subclass': '采购公告', 'catID': 'ead7af9fccec46aaa91797fc218dcdd0'},
                {'subclass': '其他公告', 'catID': '67ece36282d0465f8352283f34bc9123'},
                {'subclass': '变更澄清', 'catID': '3aa62ebb9ad948899521b7c0466f789c'},
                {'subclass': '项目答疑', 'catID': '0717bd7ad0c64ed4b5c1252806bb355d'},
                {'subclass': '中标公示', 'catID': '83d3368a846745c09536b77227a3d76f'},
                {'subclass': '中标公告', 'catID': '833749ccca314d05a9ca19440c63af48'},
                {'subclass': '其他公示', 'catID': 'ff2962347e664004afabab75d7787731'}
               ]

    dupurl = get_dupurl(allowed_domains[0])


    def __init__(self, goon=None, *args, **kwargs):
        super(GzebidSpider, self).__init__(*args, **kwargs)
        self.goon = goon

    def start_requests(self):
        meta = {}
        meta['Num'] = 1

        for i in self.catName:
            meta['subclass'] = i['subclass']
            meta['catID'] = i['catID']
            yield scrapy.Request(url=self.start_urls.format(catID=meta['catID'],Num=meta['Num']),
                                 callback=self.parse,
                                 meta=meta,
                                 dont_filter=True
                                 )

    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)
        jsonT_2 = json.loads(jsonT['data'])
        if len(jsonT_2['rows']) == 0:
            return None
        mark = 0
        for i in jsonT_2['rows']:

            meta['vertItem'] = {}
            meta['vertItem']['site'] = self.allowed_domains[0]
            meta['vertItem']['subclass'] = meta['subclass']

            meta['vertItem']['page_url'] = 'https://www.gzebid.cn/web-detail/frontDetail?articleId=' + i['id']
            if meta['vertItem']['page_url'] in self.dupurl:
                mark += 1
                continue
            meta['articleUrl'] = 'https://www.gzebid.cn/web-detail/noticeDetail?id=' + i['id']
            meta['vertItem']['title'] = i['noticeName']
            if not meta['vertItem']['title']:
                continue
            meta['vertItem']['issue_time'] = get_timestr(i['publishTime'], "%Y-%m-%d %H:%M:%S")
            if not meta['vertItem']['issue_time']:
                continue

            yield scrapy.Request(url=meta['articleUrl'],
                                 callback=self.parseA,
                                 meta = meta,
                                 dont_filter=True
                                 )


        if len(jsonT_2['rows']) < 1000:
            return None
        if mark == len(jsonT_2['rows']) and self.goon == 'no':
            return None
        else:
            meta['Num'] += 1
            yield scrapy.Request(url=self.start_urls.format(catID=meta['catID'],Num=meta['Num']),
                                 callback=self.parse,
                                 meta=meta,
                                 dont_filter=True
                                 )

    def parseA(self, response):
        meta = response.meta
        item = GcprojectItem()
        for k in meta['vertItem'].keys():
            item[k] = meta['vertItem'][k]

        jsonT = json.loads(response.text)

        if not jsonT['success']:
            return None

        jsonContent = json.loads(jsonT['data'])

        item['content'] = jsonContent['context']

        yield item
        # item['content'] = len(item['content'])
        # pprint.pprint(item)
        #
        # print('-----------------------------')


