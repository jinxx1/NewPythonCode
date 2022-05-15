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

class YancaohangyeSpider(scrapy.Spider):
    name = 'gc_yc'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        {'type':'招标公告','url':'http://search.tobaccobid.com/list.action?type=1&tenderType=0&pageNum=1'},
        {'type':'招标变更','url':'http://search.tobaccobid.com/list.action?type=2&tenderType=0&pageNum=1'},
        {'type':'中标公示','url':'http://search.tobaccobid.com/list.action?type=3&tenderType=0&pageNum=1'}
    ]

    def start_requests(self):
        for dic in self.start_urls:
            yield scrapy.Request(url=dic['url'],
                                 callback=self.parse_list,
                                 dont_filter=True,
                                 meta={'dic':dic})

    def parse_list(self, response):
        dic = response.meta['dic']
        li_list = response.xpath('//*[@id="mainbody1"]/div/div[2]/ul/li')
        for li in li_list:
            try:
                item = GcProjectItem()
                item['site'] = 'www.tobaccobid.com'
                item['issue_time'] = li.xpath('./span/text()').get()
                item['subclass'] = dic['type']
                item['title'] = li.xpath('./a/@title').get()
                link = li.xpath('./a/@href').get()
                if link == None:
                    continue
                item['page_url'] = 'http://search.tobaccobid.com/' + link
                num = select_mysql(
                    "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
                if num[0]['COUNT(*)'] == 1:
                    yield item
                else:
                    print('该条信息一爬取。。。', datetime.datetime.now())
            except Exception as e:
                print(e,"---")
        u = response.xpath('//*[@id="myForm"]/div/p/a[3]/@href').get()
        if u != None:
            page_url = 'http://search.tobaccobid.com/' + u
            if int(page_url[-1]) < 20:
                yield scrapy.Request(url=page_url, callback=self.parse_list, dont_filter=True, meta={'dic': dic})

if __name__ == '__main__':
    os.system('scrapy crawl gc_yc')
'''未入库'''

