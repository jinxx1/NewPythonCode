# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint
from urllib import parse
from bs4 import BeautifulSoup
from gcproject.items import GcprojectItem
from gcproject.parseScrpy import get_location,get_timestr
from gcproject.mysqlprecess import get_dupurl
subclass_list = [{'subclass': '招标公告', 'subclass_id': '1'}, {'subclass': '招标变更', 'subclass_id': '2'}, {'subclass': '中标公示', 'subclass_id': '3'}]

# location_list = [{'location': '上海', 'location_id': '1'}]
# subclass_list = [{'subclass': '招标公告', 'subclass_id': '1'}]


class TobaccobidSpider(scrapy.Spider):
    name = 'tobaccobid'
    allowed_domains = ['www.tobaccobid.com']
    site = '烟草行业招投标信息平台'
    dupurl = get_dupurl(allowed_domains[0])
    start_urls = 'http://search.tobaccobid.com/searchTender.action?code=&area=0&type=0&date=0&keyName=&infoType={subclass}&pageNum={Num}'

    def __init__(self, goon=None, *args, **kwargs):
        super(TobaccobidSpider, self).__init__(*args, **kwargs)
        self.goon = goon

    def start_requests(self):
        meta = {}

        meta['Num'] = 1

        for subclass_unit in subclass_list:
            meta['vertItem'] = {}
            meta['vertItem']['subclass'] = subclass_unit['subclass']
            meta['subclass_id'] = subclass_unit['subclass_id']
            url = self.start_urls.format(subclass=meta['subclass_id'],Num=str(meta['Num']))
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta=meta,
                dont_filter=True
            )

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='righ2 fr']/ul[@class='lie1']/li/a/@href").extract()
        if not link:
            print('no link')
            return None

        mark = 0
        for num,i in enumerate(link):
            artUrl = parse.urljoin(response.url,i)
            if artUrl in self.dupurl:
                # print('dupcut')
                mark += 1
                continue
            meta['vertItem']['title'] = ''
            meta['vertItem']['issue_time'] = ''
            meta['vertItem']['minor_business_type'] = ''

            xpathCode = "//*[@href = '{}']/@title".format(i)
            Title = response.xpath(xpathCode).extract_first()
            if not Title:
                continue
            meta['vertItem']['title'] = Title

            xpathCode = "//*[@href = '{}']/../span[@class = 'fr']/text()".format(i)
            Time = response.xpath(xpathCode).extract_first()
            if not Time:
                continue
            meta['vertItem']['issue_time'] = get_timestr(Time,"%Y-%m-%d %H:%M:%S")

            xpathCode = "//*[@href = '{}']/../span/a/text()".format(i)

            meta['vertItem']['minor_business_type'] = response.xpath(xpathCode).extract_first()
            if not meta['vertItem']['minor_business_type']:
                continue

            yield scrapy.Request(
                url=artUrl,
                meta=meta,
                callback=self.parseA,
                dont_filter=True
            )

        if mark == len(link) and self.goon == 'no':
            return None
        else:
            meta['Num'] += 1
            url = self.start_urls.format(subclass=meta['subclass_id'],Num=str(meta['Num']))
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta=meta,
                dont_filter=True
            )


    def parseA(self,response):
        meta = response.meta
        item = GcprojectItem()

        item['page_url'] = response.url
        item['site'] = self.allowed_domains[0]

        for k in meta['vertItem'].keys():
            item[k] = meta['vertItem'][k]
        content = response.xpath("//div[@class = 'y4']|//div[@class='y4 detail-content']").extract()
        item['content'] = ''.join(content)

        yield item
        # item['content'] = len(item['content'])
        #
        # pprint.pprint(item)
        # print('-----------------------------')







