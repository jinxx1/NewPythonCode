# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint
from urllib import parse as urlparse
from bs4 import BeautifulSoup
from ggzy.items import GgzyItem
from ggzy.parseScrpy import get_timestr
from ggzy.mysqlprecess import get_dupurl
import time
from dateutil.relativedelta import relativedelta
import datetime
import sqlalchemy
import os
from ggzy.redis_dup import BloomFilter
bl = BloomFilter('uxue:url')
header_raw = '''Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: close
Content-Type: application/json;charset=utf-8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')

class CcgpXizangSpider(scrapy.Spider):
    name = 'ccgp_xizang'
    cname = '西藏政府采购'
    allowed_domains = ['www.ccgp-xizang.gov.cn']
    start_urls = [{'urlid': '00101', 'subclass': '采购公告'}, {'urlid': '00102', 'subclass': '中标(成交)公告'}, {'urlid': '001003', 'subclass': '更正公告'}, {'urlid': '001031', 'subclass': '更正公告'}, {'urlid': '001032', 'subclass': '更正公告'}, {'urlid': '001004', 'subclass': '废标(终止)公告'}, {'urlid': '001006', 'subclass': '废标(终止)公告'}, {'urlid': '001052', 'subclass': '其他公告'}, {'urlid': '001053', 'subclass': '其他公告'}, {'urlid': '001055', 'subclass': '其他公告'}, {'urlid': '001056', 'subclass': '其他公告'}, {'urlid': '001057', 'subclass': '其他公告'}, {'urlid': '001058', 'subclass': '其他公告'}, {'urlid': '001059', 'subclass': '其他公告'}, {'urlid': '001051', 'subclass': '单一来源公示'}, {'urlid': '001009', 'subclass': '验收结果公告'}, {'urlid': '001054', 'subclass': '合同公告'}, {'urlid': '59', 'subclass': '采购意向公开'}]


    def __init__(self, goon=None, *args, **kwargs):
        super(CcgpXizangSpider, self).__init__(*args, **kwargs)
        self.pageS = 100
        self.goon = goon
        self.baseUrl = "http://www.ccgp-xizang.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=18de62f0-2fb0-4187-a6c1-cd8fcbfb4585&channel=b541ffff-03ee-4160-be64-b11ccf79660d&currPage={pageNum}&pageSize={pageS}&noticeType={urlid}&cityOrArea=&noticeName=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime"

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for num,i in enumerate(self.start_urls):
            if num > 0:
                continue
            meta['urlid'] = i['urlid']
            meta['subclass'] = i['subclass']
            yield scrapy.Request(url=self.baseUrl.format(pageNum = meta['Num'],urlid=meta['urlid'],pageS=self.pageS),
                                 callback=self.parse,
                                 dont_filter=True,
                                 meta=meta,
                                 headers=HEA)

    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)
        mark = 0
        for x in jsonT['data']:
            page_url = urlparse.urljoin('http://www.ccgp-xizang.gov.cn/',x['pageurl'])
            if bl.exists(page_url):
                mark += 1
                continue
            meta['page_url'] = page_url
            meta['title'] = x['title']
            meta['issue_time'] = get_timestr(x['addtimeStr'])
            meta['subclass'] = meta['subclass']
            meta['province_name'] = '西藏自治区'

            yield scrapy.Request(url=page_url,
                                 callback=self.parseA,
                                 dont_filter=True,
                                 meta=meta,
                                 headers=HEA)
        if mark == len(jsonT['data']) and self.goon == 'no':
            return None
        if jsonT['total']//self.pageS + 1 == meta['Num']:
            return None
        meta['Num'] += 1
        yield scrapy.Request(url=self.baseUrl.format(pageNum=meta['Num'], urlid=meta['urlid'], pageS=self.pageS),
                             callback=self.parse,
                             dont_filter=True,
                             meta=meta,
                             headers=HEA)

    def parseA(self, response):
        meta = response.meta
        item = GgzyItem()

        item['content'] = response.xpath("//div[@class='notice-con']").extract_first()
        if not item['content']:
            return None

        item['page_url'] = meta['page_url']
        item['title'] = meta['title']
        item['issue_time'] = meta['issue_time']
        item['subclass'] = meta['subclass']
        item['province_name'] = meta['province_name']
        item['site'] = self.allowed_domains[0]

        soup = BeautifulSoup(response.text, 'lxml')
        hrefall = soup.find_all(href=re.compile("/gpx-bid-file/"))
        item['attchment'] = []
        for nn in hrefall:
            ddict = {}
            ddict['download_url'] = nn.get('href')
            ddict['name'] = response.xpath("//*[@href = '{}']/text()".format(nn.get('href'))).extract_first()
            if not ddict['name']:
                continue
            item['attchment'].append(ddict)
        if not item['attchment']:
            del item['attchment']

        item['content'] = len(item['content'])
        pprint.pprint(item)
        print('--*'*50)
        # yield item
