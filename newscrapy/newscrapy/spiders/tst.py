# -*- coding: utf-8 -*-
import scrapy
from ..settings import *

class TstSpider(scrapy.Spider):
    name = 'tst'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com/']
    # custom_settings = custom_settings_for_spider1

    def parse(self, response):
        print(SPIDERTYPE)
        # print(LOG_FILE)

class TstSpider1(scrapy.Spider):
    name = 'tst1'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com/']
    # custom_settings = custom_settings_for_spider1

    def parse(self, response):
        print(SPIDERTYPE)
        # print(LOG_FILE)