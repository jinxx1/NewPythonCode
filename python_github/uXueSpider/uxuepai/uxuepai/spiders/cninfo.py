# -*- coding: utf-8 -*-
import scrapy
import pprint
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lxml import html
import re
import json
from uxuepai.items import UxuepaiItem
import time,datetime
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
print(tomorrow)
class CninfoSpider(scrapy.Spider):
    name = 'cninfo'
    allowed_domains = ['cninfo.com.cn']
    start_urls = ['http://www.cninfo.com.cn/new/disclosure?']

    def start_requests(self):
        url = 'http://www.cninfo.com.cn/new/disclosure?'
        for i in range(1,2):
            yield scrapy.FormRequest(url=url,
                                     method='POST',
                                     formdata={'column': 'szse_latest','pageNum': str(i)},
                                     meta={'cookiejar': 1},
                                     callback=self.parse)

    def parse(self, response):
        jsonR = json.loads(response.body_as_unicode()).get('classifiedAnnouncements')
        for LabelOne in jsonR:
            for LabelTwo in LabelOne:
                if str(tomorrow) in LabelTwo['adjunctUrl']:
                    pprint.pprint('http://www.cninfo.com.cn/' + LabelTwo['adjunctUrl'])
