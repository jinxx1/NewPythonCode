# -*- coding: utf-8 -*-
import scrapy


class Grade1Spider(scrapy.Spider):
    name = 'grade1'
    allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.xxx.com/']

    def parse(self, response):
        pass
