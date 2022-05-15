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

class GuoepingtaiSpider(scrapy.Spider):
    name = 'gc_gept'
    # allowed_domains = ['www.xxx.com']
    start_urls = 'https://www.ebidding.com/portal/announcement/ebd?type=&df=&department=&industry=&bidType=&guanjianzi=&openMode=&showDateSort=1&platformType=&_=1605168039749&on=false&page=%s'
    def start_requests(self):
        for i in range(1,100):#1605
            url = self.start_urls%str(i)
            yield scrapy.Request(url=url,callback=self.parse_list,dont_filter=True)

    def parse_list(self, response):
        dic_list = response.json()['result']['content']
        for dic in dic_list:
            item = GcProjectItem()
            item['site'] = 'www.ebidding.com'
            item['issue_time'] = dic['showDate']
            item['subclass'] = dic['type']
            item['title'] = dic['title']
            item['page_url'] = 'https://www.ebidding.com/portal/html/index.html#page=main:notice_details?&' \
                               'tenderType=2&etId=%s&type=%s&htmlContentId=%s'%(dic['etId'],dic['type'],dic['htmlContentId'])
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())

if __name__ == '__main__':
    os.system('scrapy crawl gc_gept')
