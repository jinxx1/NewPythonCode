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

class DlztbSpider(scrapy.Spider):
    name = 'dlztb'
    allowed_domains = ['www.dlztb.com']
    site = '中国电力招标采购网'
    start_urls = [
        {'subclass': '设备中标', 'baseUrl': 'http://www.dlztb.com/zbgg/157_{}.html'},
                  {'subclass': '工程中标', 'baseUrl': 'http://www.dlztb.com/zbgg/158_{}.html'},
                  {'subclass': 'VIP项目', 'baseUrl': 'http://www.dlztb.com/xmxx/xiangmu/{}.html'},
                  {'subclass': '拟在建项目', 'baseUrl': 'http://www.dlztb.com/xmxx/nizaijian/{}.html'},
                  {'subclass': '独家项目', 'baseUrl': 'http://www.dlztb.com/xmxx/dujiaxiangmu/{}.html'}
    ]

    dupurl = get_dupurl(allowed_domains[0])
    def __init__(self, goon=None, *args, **kwargs):
        super(DlztbSpider, self).__init__(*args, **kwargs)
        self.goon = goon

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['baseUrl'] = i['baseUrl']
            yield scrapy.Request(
                url=meta['baseUrl'].format(str(meta['Num'])),
                callback=self.parse,
                meta=meta,
                dont_filter=True,

            )

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class ='catlist']/ul/li/a/@href").extract()
        # print('{}页，共有{}篇文章'.format(meta['vertItem']['subclass'],len(link)))

        if not link:
            return None
        mark = 0
        for num,i in enumerate(link):
            # if num >1:
            #     continue
            url = parse.urljoin(response.url,i)
            if url in self.dupurl:
                mark += 1
                continue
            yield scrapy.Request(url=url,
                                 callback=self.parseA,
                                 meta=meta,
                                 dont_filter=True
                                 )
        if mark == len(link) and self.goon=='no':
            return None
        else:
            meta['Num'] += 1
            yield scrapy.Request(url=meta['baseUrl'].format(str(meta['Num'])),
                             callback=self.parse,
                             meta=meta,
                             dont_filter=True
                             )

    def parseA(self,response):
        meta = response.meta
        item = GcprojectItem()
        Timet = response.xpath("//div[@class='m m3']/div[@class='m3l']/div[@class='info']").extract()
        Timet = ''.join(Timet)
        try:
            timerex = re.findall("\d{4}-\d{2}-\d{2}",Timet)[0]
        except:
            return None
        meta['issue_time'] = get_timestr(timerex, "%Y-%m-%d %H:%M:%S")
        item['subclass'] = response.xpath("//div[@class='m']/div[@class='nav']/a[3]/text()").extract_first()
        item['title'] = response.xpath("//h1[@id='title']/text()").extract_first()
        cutgif = "http://www.zgdlzb.org.cn/member/editor/fckeditor/editor/css/images/fck_anchor.gif"
        item['content'] = response.xpath("//div[@id='article']").extract_first().replace(cutgif,'')
        item['page_url'] = response.url
        item['site'] = self.allowed_domains[0]
        if not item['content']:
            return None
        yield item

        # item['content'] = len(item['content'])
        # pprint.pprint(item)
        # print('----------------------------------------------')