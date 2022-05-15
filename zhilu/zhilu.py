# -*- coding: utf-8 -*-
import scrapy


class ZhiluSpider(scrapy.Spider):
    name = 'zhilu'
    allowed_domains = ['www.xoxo788.com']
    start_urls = ['http://www.xoxo788.com/']

    def parse(self, response):
        pass
