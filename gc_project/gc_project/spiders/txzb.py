# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/30
# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/12
import os,json,datetime,pymysql
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql,insert_mysql
r = Redis('127.0.0.1',6379)


class TxzbSpider(scrapy.Spider):
    name = 'txzb'
    # allowed_domains = ['www.xxx.com']
    start_urls = 'http://txzb.miit.gov.cn/DispatchAction.do?reg=denglu&pagesize=11'
    headers = {
        'Origin': 'http://txzb.miit.gov.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    def start_requests(self):
        for page in range(1,3):  # 21634
            data = {'page': str(page),'efFormEname': 'POIX14'}
            yield scrapy.FormRequest(url=self.start_urls,
                                     method='POST',
                                     headers=self.headers,
                                     formdata=data,
                                     callback=self.parse_list,
                                     dont_filter=True,)
    def parse_list(self, response):
        tr_list = response.xpath('//*[@id="newsItem"]/tr')
        for tr in tr_list:
            try:
                item = {}
                item['title'] = tr.xpath('./td[3]/a/text()').get()
                item['issue_time'] = item['title'][-10::]
                item['page_url'] =  tr.xpath('./td[3]/a/@href').get()
                print(item)
            except Exception as e:
                print('error:  ',e)
    def parse_detail(self,response):
        item = response.meta['item']
        print(item)

if __name__ == '__main__':
    os.system('scrapy crawl txzb')



