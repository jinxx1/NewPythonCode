# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint
from urllib import parse as urlParse
from bs4 import BeautifulSoup
from ggzy.items import GgzyItem
from ggzy.parseScrpy import get_timestr
from ggzy.mysqlprecess import get_dupurl
import requests
import time
from dateutil.relativedelta import relativedelta
import datetime
import sqlalchemy
import os
from ggzy.redis_dup import BloomFilter
bl = BloomFilter('uxue:url')

header_raw = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: close
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36
'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')

class CcgpHenanSpider(scrapy.Spider):
    name = 'ccgp_henan'
    allowed_domains = ['www.hngp.gov.cn']

    start_urls = [{'subclass': '省级_采购意向', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=9102&pageNo={}&pageSize=16&bz=1&gglx=0'}, {'subclass': '省级_采购公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=0101&pageNo={}&pageSize=16&bz=1&&gglx=0'}, {'subclass': '省级_更正公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=0103&pageNo={}&pageSize=16&bz=1&gglx=0'}, {'subclass': '省级_结果公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=0102&pageNo={}&pageSize=16&bz=1&gglx=0'}, {'subclass': '省级_废标公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=0190&pageNo={}&pageSize=16&bz=1&gglx=0'}, {'subclass': '省级_合同公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=1401&pageNo={}&pageSize=16&bz=1&gglx=0'}, {'subclass': '省级_验收结果公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=1402&pageNo={}&pageSize=16&bz=1&gglx=0'}, {'subclass': '省级_单一来源公示', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=1301&pageNo={}&pageSize=16&bz=1&gglx=0'}, {'subclass': '省级_非政府采购', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=9101&pageNo={}&pageSize=16&bz=1&gglx=0'}, {'subclass': '省级_其他', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=1304&pageNo={}&pageSize=16&bz=1&gglx=0'}, {'subclass': '市区县级_采购意向', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=9102&pageNo={}&pageSize=16&bz=2&gglx=0'}, {'subclass': '市区县级_采购公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=0101&pageNo={}&pageSize=16&bz=2&gglx=0'}, {'subclass': '市区县级_更正公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=0103&pageNo={}&pageSize=16&bz=2&gglx=0'}, {'subclass': '市区县级_结果公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=0102&pageNo={}&pageSize=16&bz=2&gglx=0'}, {'subclass': '市区县级_废标公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=0190&pageNo={}&pageSize=16&bz=2&gglx=0'}, {'subclass': '市区县级_合同公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=1401&pageNo={}&pageSize=16&bz=2&gglx=0'}, {'subclass': '市区县级_验收结果公告', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=1402&pageNo={}&pageSize=16&bz=2&gglx=0'}, {'subclass': '市区县级_单一来源公示', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=1301&pageNo={}&pageSize=16&bz=2&gglx=0'}, {'subclass': '市区县级_非政府采购', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=9101&pageNo={}&pageSize=16&bz=2&gglx=0'}, {'subclass': '市区县级_其他', 'url': 'http://www.hngp.gov.cn/henan/list2?channelCode=1304&pageNo={}&pageSize=16&bz=2&gglx=0'}]

    def __init__(self, goon=None, *args, **kwargs):
        super(CcgpHenanSpider, self).__init__(*args, **kwargs)
        self.pageS = 200
        self.goon = goon
    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for num,i in enumerate(self.start_urls):
            if num > 2:
                continue
            meta['subclass'] = i['subclass']
            meta['url'] = i['url']
            yield scrapy.Request(
                url=meta['url'].format(meta['Num']),
                callback=self.parse,
                dont_filter=True,
                meta=meta,
            )

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='List2']/ul/li/a/@href").extract()
        if not link:
            return None

        mark = 0
        for x in link:
            page_url = urlParse.urljoin(response.url,x)
            if bl.exists(page_url):
                mark += 1
                continue
            meta['page_url'] = page_url
            meta['title'] = response.xpath("//*[@href = '{}']/text()".format(x)).extract_first()
            timeT = response.xpath("//*[@href = '{}']/../p/span[@class = 'Gray Right']/text()".format(x)).extract_first()
            meta['issue_time'] = get_timestr(timeT,"%Y-%m-%d %H:%M:%S")
            if not meta['issue_time'] or not meta['title']:
                continue
            yield scrapy.Request(url=page_url,
                                 callback=self.parseA,
                                 meta=meta,
                                 )


        if mark == len(link) and self.goon == 'no':
            return None
        meta['Num'] += 1
        yield scrapy.Request(
            url=meta['url'].format(meta['Num']),
            callback=self.parse,
            dont_filter=True,
            meta=meta,
        )
    def parseA(self,response):
        meta = response.meta
        item = GgzyItem()
        item['page_url'] = meta['page_url']
        item['site'] = self.allowed_domains[0]
        item['title'] = meta['title']
        item['subclass'] = meta['subclass']
        item['province_name'] = '河南省'
        item['issue_time'] = meta['issue_time']

        reg = re.findall('''get\("(.*?)", function''', response.text)
        if not reg:
            return None
        artUrl = urlParse.urljoin('http://www.hngp.gov.cn/',''.join(reg))
        contentBrow = requests.get(url=artUrl,headers=HEA)
        if contentBrow.status_code > 300:
            return None
        hhtml = contentBrow.text.encode(contentBrow.encoding).decode('utf-8')
        soup = BeautifulSoup(hhtml,'lxml')
        content = soup.find('table',class_='Content').prettify()

        if not content:
            return None

        item['content'] = ''.join(content)
        attchment = response.xpath("//div[@class='List1 Top5']//a/@href").extract()

        if attchment:
            item['attchment'] = []
            for nn in attchment:
                ddict = {}
                ddict['download_url'] = urlParse.urljoin('http://www.hngp.gov.cn/',nn)
                ddict['name'] = response.xpath("//*[@href='{}']/text()".format(nn)).extract_first()
                item['attchment'].append(ddict)

        # item['content'] = len(item['content'])
        # pprint.pprint(item)
        # print('-------------------------------------------')
        yield item

