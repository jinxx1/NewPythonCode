# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint
from urllib import parse
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
Content-Type: application/json;charset=UTF-8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


class CcgpGuangdongSpider(scrapy.Spider):
    name = 'ccgp_guangdong'
    allowed_domains = ['gdgpo.czt.gd.gov.cn']
    # allowed_domains = ['www.gdgpo.gov.cn','gdgpo.czt.gd.gov.cn']
    # 'www.gdgpo.gov.cn'自2021年2月开始就不更新了。
    # 'gdgpo.czt.gd.gov.cn'还在更新，使用这个
    cname = '广东省政府采购网'

    start_urls = [
                    {'subclass': '采购意向公开', 'urlid': '59'},
                    {'subclass': '单一来源公示', 'urlid': '001051'},
                    {'subclass': '采购计划 ', 'urlid': '001101'},
                    {'subclass': '采购需求', 'urlid': '001059'},
                    {'subclass': '资格预审公告', 'urlid': '001052,001053'},
                    {'subclass': '采购公告', 'urlid': '00101'},
                    {'subclass': '中标（成交）结果公告', 'urlid': '00102'},
                    {'subclass': '更正公告', 'urlid': '00103'},
                    {'subclass': '终止公告', 'urlid': '001004,001006'},
                    {'subclass': '合同公告', 'urlid': '001054'},
                    {'subclass': '验收公告', 'urlid': '001009,00105A'}
                  ]

    def __init__(self, goon=None, *args, **kwargs):
        super(CcgpGuangdongSpider, self).__init__(*args, **kwargs)
        self.goon = goon
        self.pageS = 100
        if self.goon == 'yes':
            self.baseUrl = "https://gdgpo.czt.gd.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=cd64e06a-21a7-4620-aebc-0576bab7e07a&channel=fca71be5-fc0c-45db-96af-f513e9abda9d&currPage={pageNum}&pageSize={pageSize}&noticeType={subclass}&regionCode=&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=&operationEndTime=&selectTimeName=noticeTime"
        elif self.goon == 'no':
            aa = '789nowTime789'
            nowTime = datetime.datetime.now().strftime("%Y-%m-%d")
            # nowTime = '2021-07-22'
            self.baseUrl = "https://gdgpo.czt.gd.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=cd64e06a-21a7-4620-aebc-0576bab7e07a&channel=fca71be5-fc0c-45db-96af-f513e9abda9d&currPage={pageNum}&pageSize={pageSize}&noticeType={subclass}&regionCode=&purchaseManner=&title=&openTenderCode=&purchaser=&agency=&purchaseNature=&operationStartTime=789nowTime789%2000:00:00&operationEndTime=789nowTime789%2023:59:59&selectTimeName=noticeTime".replace(aa,nowTime)
        else:
            print('pls input yes or no ')


    def start_requests(self):
        meta = {}
        meta['Num'] = 1

        for num,i in enumerate(self.start_urls):
            # if num >3:
            #     continue
            meta['subclass'] = i['subclass']
            meta['subclass_id'] = i['urlid']
            yield scrapy.Request(url=self.baseUrl.format(
                                                        pageNum=meta['Num'],
                                                        pageSize=self.pageS,
                                                        subclass=meta['subclass_id'],
                                                    ),
                                callback=self.parse,
                                meta=meta,
                                headers=HEA,
                                dont_filter=True)

    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)
        if len(jsonT['data']) == 0:
            return None
        mark = 0
        for num,i in enumerate(jsonT['data']):
            AricleUrl = 'https://gdgpo.czt.gd.gov.cn' + i['pageurl']
            if bl.exists(AricleUrl):
                mark += 1
                continue
            item = GgzyItem()
            item['page_url'] = AricleUrl
            content = BeautifulSoup(i['content'],'lxml')
            item['content'] = content.find("div",class_="noticeArea").prettify()
            item['site'] = self.allowed_domains[0]
            item['title'] = i['title']
            item['subclass'] = meta['subclass']
            item['province_name'] = '广东省'
            item['issue_time'] = i['noticeTime']

            # item['content'] = len(item['content'])
            # pprint.pprint(item)
            # print('----------------------')
            yield item
            print('----------------------',item['subclass'],meta['Num'])



        if meta['Num'] == jsonT['total'] // self.pageS + 1:
            return None
        if mark == len(jsonT['data']) and self.goon == 'no':
            return None

        meta['Num'] += 1
        yield scrapy.Request(url=self.baseUrl.format(
            pageNum=meta['Num'],
            pageSize=self.pageS,
            subclass=meta['subclass_id'],
        ),
            callback=self.parse,
            meta=meta,
            headers=HEA,
            dont_filter=True)
