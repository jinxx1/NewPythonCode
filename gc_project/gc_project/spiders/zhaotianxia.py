# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/12
import os,json,datetime
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql
r = Redis('127.0.0.1',6379)

class ZhaotianxiaSpider(scrapy.Spider):
    name = 'gc_ztx'
    # allowed_domains = ['www.xxx.com']
    start_urls = 'https://www.zhaotx.cn/searchlist.htm?type=&page=%s'
    def start_requests(self):
        for page in [i for i in range(1,300)]:#[i for i in range(1,24970)][::-1]
            url = self.start_urls%(page)
            yield scrapy.Request(url=url,callback=self.parse_list,dont_filter=True)

    def parse_list(self, response):
        li_list = response.xpath('/html/body/div[6]/div[2]/div[2]/ul/li')
        for li in li_list:
            item = GcProjectItem()
            try:
                item['site'] = 'www.zhaotx.cn'
                item['issue_time'] = li.xpath('./a/p[5]/text()').get()
                item['subclass'] = li.xpath('./a/p/text()').extract_first()
                item['title'] = li.xpath('./a/p[4]/text()').get()
                item['business_type'] = li.xpath('./a/p[2]/text()').get()
                if item['business_type'] == '\xa0':
                    item['business_type'] = ''
                item['city_name'] = li.xpath('./a/p[3]/text()').get()
                link = li.xpath('./a/@href').extract_first()
                if link == None:
                    continue
                item['page_url'] = 'https://www.zhaotx.cn' + link
                num = select_mysql(
                    "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
                if num[0]['COUNT(*)'] == 1:
                    yield item
                else:
                    print('该条信息一爬取。。。',datetime.datetime.now())
            except Exception as e:
                print('error:  ',e)


if __name__ == '__main__':
    os.system('scrapy crawl gc_ztx')

