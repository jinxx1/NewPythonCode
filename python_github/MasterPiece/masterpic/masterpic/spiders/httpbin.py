# -*- coding: utf-8 -*-
import scrapy


class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    # start_urls = ['http://httpbin.org/get']

    def start_requests(self):
        for i in range(0,6):
            yield scrapy.Request(url='http://httpbin.org/get',callback=self.parseA,dont_filter=True)

    # def parse(self, response):
    #     for i in range(0,6):
    #         yield scrapy.Request(url=self.start_urls[0],callback=self.parseA)

    def parseA(self,response):
        print(response.text)