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
header_raw = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Host: www.bidding.csg.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')

class BiddingSpider(scrapy.Spider):
    name = 'bidding'
    allowed_domains = ['www.bidding.csg.cn']
    siteName = '中国南方电网'

    start_urls = [
        {'business_type': '服务',
          'baseUrl': 'http://www.bidding.csg.cn/dbsearch.jspx?pageNo={}&channelId=309&q=&org=&types=%E6%9C%8D%E5%8A%A1'},
         {'business_type': '工程',
          'baseUrl': 'http://www.bidding.csg.cn/dbsearch.jspx?pageNo={}&channelId=309&q=&org=&types=%E5%B7%A5%E7%A8%8B'},
         {'business_type': '货物',
          'baseUrl': 'http://www.bidding.csg.cn/dbsearch.jspx?pageNo={}&channelId=309&q=&org=&types=%E8%B4%A7%E7%89%A9'}
         ]
    dupurl = get_dupurl(allowed_domains[0])
    def __init__(self, goon=None, *args, **kwargs):
        super(BiddingSpider, self).__init__(*args, **kwargs)
        self.goon = goon


    def start_requests(self):
        meta = {}
        meta['vertItem'] = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['vertItem']['business_type'] = i['business_type']
            meta['baseUrl'] = i['baseUrl']

            yield scrapy.Request(url=meta['baseUrl'].format(str(meta['Num'])),
                             callback=self.parse,
                             meta=meta,
                             dont_filter=True,
                                 headers=HEA)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='W1200 Center'][1]/div[@class='List2']/ul/li/a/@href").extract()
        # print(link)
        if not link:
            return None
        mark = 0
        for i in link:
            url = parse.urljoin(response.url,i)
            if url in self.dupurl:
                mark += 1
                continue
            meta['vertItem']['province_name'] = response.xpath("//*[@href = '{}']/../a[@class = 'Blue']/text()".format(i)).extract_first()
            if not meta['vertItem']['province_name']:
                return None
            meta['vertItem']['subclass'] = response.xpath("//*[@href = '{}']/../span[@class='Right']/a/text()".format(i)).extract_first()
            if not meta['vertItem']['subclass']:
                return None
            issue_time = response.xpath("//*[@href = '{}']/../span[@class='Right']/span/text()".format(i)).extract_first()
            if not issue_time:
                return None
            meta['vertItem']['issue_time'] = get_timestr(issue_time,"%Y-%m-%d %H:%M:%S")
            meta['vertItem']['site'] = self.allowed_domains[0]
            yield scrapy.Request(url=url,
                                 callback=self.parseA,
                                 meta=meta,
                                 dont_filter=True,
                                 headers=HEA
                                 )
            # print(url)
            # pprint.pprint(meta['vertItem'])
            # print('----------------------------',meta['Num'])


        if mark == len(link) and self.goon=='no':
            return None
        else:
            meta['Num'] += 1
            yield scrapy.Request(url=meta['baseUrl'].format(str(meta['Num'])),
                                 callback=self.parse,
                                 meta=meta,
                                 dont_filter=True,
                                 headers=HEA)

    def parseA(self,response):
        meta = response.meta
        item = GcprojectItem()
        for k in meta['vertItem'].keys():
            item[k] = meta['vertItem'][k]

        item['content'] = response.xpath("//div[@class = 'Section0']|//div[@class = 'Content']").extract_first()
        item['title'] = response.xpath("//h1/text()").extract_first()
        item['page_url'] = response.url

        if not item['content'] or not item['title']:
            print('NO CONTENT or title  ',response.url)
            return None
        if '附件下载' in response.text:
            item['attchment'] = []
            regx = re.findall("附件下载.*href=\"(.*?)\">", response.text)
            for reg in regx:
                ddict = {}
                ddict['download_url'] = parse.urljoin(response.url, reg)
                ddict['name'] = response.xpath("//a[@href='{}']/text()".format(reg)).extract_first()
                if not ddict['name']:
                    continue
                item['attchment'].append(ddict)
        # item['content'] = len(item['content'])
        # print(item)
        # print('--------------------------')
        yield item
