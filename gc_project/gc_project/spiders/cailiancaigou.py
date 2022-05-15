# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/12
import os,json
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql
r = Redis('127.0.0.1',6379)

class CailiancaigouSpider(scrapy.Spider):
    name = 'gc_clcg'
    # allowed_domains = ['www.xxx.com']
    start_urls = [{'url': 'http://qy.chinapsp.cn:48882/api/services/app/AbpArticles/GetPaged?filter=a.ext2 == "74166" and a.isDispaly == "true"&sorting=a.creationTime+desc&maxResultCount=10&skipCount={}','page': 7}, # 2524
 # 招标公告
        {'url': 'http://qy.chinapsp.cn:48882/api/services/app/AbpArticles/GetPaged?filter=a.ext2+%3D%3D+%2274168%22+and+a.isDispaly+%3D%3D+%22true%22&sorting=a.creationTime+desc&maxResultCount=10&skipCount={}','page': 7}, # 2533
 # 结果公告
        {'url': 'http://qy.chinapsp.cn:48882/api/services/app/AbpArticles/GetPaged?filter=a.ext2+%3D%3D+%2274169%22+and+a.isDispaly+%3D%3D+%22true%22&sorting=a.creationTime+desc&maxResultCount=10&skipCount={}','page': 3}] # 474
  # 更正答疑

    def start_requests(self):
        for dic in self.start_urls:
            for page in range(0, dic['page']):
                url = dic['url'].format(page*10)
                yield scrapy.Request(url=url,callback=self.parse_list,dont_filter=True)

    def parse_list(self, response):
        res_list = response.json()['result']['items']
        for dic in res_list:
            item = GcProjectItem()
            item['site'] = 'www.chinapsp.cn'
            item['issue_time'] = dic['creationTime']
            item['subclass'] = dic['projectType']
            item['title'] = dic['title']
            item['page_url'] = 'http://www.chinapsp.cn/notice_content.html?itemid=%s'%dic['id']
            num = select_mysql("SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                import datetime
                print('该条信息一爬取。。。',datetime.datetime.now())


if __name__ == '__main__':
    os.system('scrapy crawl gc_clcg')







