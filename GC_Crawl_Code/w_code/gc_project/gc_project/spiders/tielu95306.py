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


class TieluSpider(scrapy.Spider):
    name = 'gc_tl'
    # allowed_domains = ['www.xxx.com']
    # start_urls = 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&curPage=%s'
    start_urls = [{'type':'项目公告','url':'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&noticeType=01&extend=1&curPage={}','page':100},#14534
                    {'type':'变更公告','url':'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&noticeType=02&extend=1&curPage={}','page':30}, #248
                    {'type':'答疑补漏','url':'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&noticeType=03&extend=1&curPage={}','page':30}, #322
                    {'type':'结果公告','url':'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&noticeType=04&extend=1&curPage={}','page':100}] #6704
    def start_requests(self):
        for dic in self.start_urls:  # 21634
            for i in range(1,dic['page']):  # dic['page']
                url = dic['url'].format(i)
                yield scrapy.Request(url=url,callback=self.parse_list,dont_filter=True,meta={'dic':dic})

    def parse_list(self, response):
        tr_list = response.xpath('/html/body/div[3]/div/table/tr')
        for tr in tr_list:
            try:
                item = GcProjectItem()
                dic_info = response.meta['dic']
                item['site'] = 'wzcgzs.95306.cn'
                item['issue_time'] = tr.xpath('./td[6]/text()').get()
                if item['issue_time'] == None:item['issue_time'] = datetime.datetime.now()
                item['purchase_type'] = tr.xpath('./td[4]/text()').get()
                item['subclass'] = dic_info['type']
                item['title'] = tr.xpath('./td[2]/a/text()').get()
                link = tr.xpath('./td[2]/a/@href').get()
                if link == None:
                    continue
                item['page_url'] = 'http://wzcgzs.95306.cn' + link
                num = select_mysql(
                    "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
                if num[0]['COUNT(*)'] == 1:
                    yield item
                else:
                    print('该条信息一爬取。。。',datetime.datetime.now())
            except Exception as e:
                print('error:  ',e)

if __name__ == '__main__':
    os.system('scrapy crawl gc_tl')



