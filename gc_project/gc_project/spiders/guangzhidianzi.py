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

class GuangzhidianziSpider(scrapy.Spider):
    name = 'gc_gzdz'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
    {
'type':'招标公告','page':50,#464,
'url':'https://www.gzebid.cn/web-list/articles?categoryId=b66478f0930d4162be8df579268b39a7&pageNumber=%s&pageSize=15'},
    {
'type':'采购公告','page':20,#101,
'url':'https://www.gzebid.cn/web-list/articles?categoryId=ead7af9fccec46aaa91797fc218dcdd0&pageNumber=%s&pageSize=15'
    },
    {
'type':'其他公告','page':30,#34,
'url':'https://www.gzebid.cn/web-list/articles?categoryId=67ece36282d0465f8352283f34bc9123&pageNumber=%s&pageSize=15'
    },
    {
'type':'变更澄清','page':20,#112,
'url':'https://www.gzebid.cn/web-list/articles?categoryId=3aa62ebb9ad948899521b7c0466f789c&pageNumber=%s&pageSize=15'
    },
    {
'type':'项目答疑','page':5,
'url':'https://www.gzebid.cn/web-list/articles?categoryId=0717bd7ad0c64ed4b5c1252806bb355d&pageNumber=%s&pageSize=15'
    },
    {
'type':'中标公示','page':50,#302,
'url':'https://www.gzebid.cn/web-list/articles?categoryId=83d3368a846745c09536b77227a3d76f&pageNumber=%s&pageSize=15'
    },
    {
'type':'中标公告','page':30,#206,
'url':'https://www.gzebid.cn/web-list/articles?categoryId=833749ccca314d05a9ca19440c63af48&pageNumber=%s&pageSize=15'
    },
    {
'type':'其他公示','page':5,#4,
'url':'https://www.gzebid.cn/web-list/articles?categoryId=ff2962347e664004afabab75d7787731&pageNumber=%s&pageSize=15'
    }
]
    def start_requests(self):
        for dic in self.start_urls:  # 21634
            for j in range(0,dic['page']):
                url = dic['url']%(str(j))
                yield scrapy.Request(url=url,callback=self.parse_list,dont_filter=True,meta={'dic':dic})

    def parse_list(self, response):
        text_obj = response.text
        dic_info = response.meta['dic']
        res_dic = json.loads(text_obj)
        res_list = json.loads(res_dic['data'])['rows']
        for i in res_list:
            item = GcProjectItem()
            item['site'] = 'www.gzebid.cn'
            item['issue_time'] = i['publishTime']
            item['subclass'] = dic_info['type']
            item['title'] = i['noticeName']
            item['page_url'] = 'https://www.gzebid.cn/web-detail/frontDetail?articleId='+i['id']
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())

if __name__ == '__main__':
    os.system('scrapy crawl gc_gzdz')








