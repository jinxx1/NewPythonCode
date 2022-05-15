# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/18
import os,json
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql
r = Redis('127.0.0.1',6379)
ll = []
class ZhengfucaigouSpider(scrapy.Spider):
    name = '111'
    # allowed_domains = ['www.xxx.com']
    start_urls = 'https://www.89ip.cn/index_%s.html'
    def start_requests(self):
        headers = {
            # 'POST /portal/topicView.do?method=view&id=1660 HTTP/1.1
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        for page in range(1,101):
            url = self.start_urls%(page)
            yield scrapy.Request(url=url,headers=headers,callback=self.parse_list,dont_filter=True)

    def parse_list(self, response):
        tr_list = response.xpath('/html/body/div[3]/div[1]/div/div[1]/table/tbody/tr')
        for tr in tr_list:
            item = GcProjectItem()
            try:
                p  = tr.xpath('./td[1]/text()').extract_first().strip()+':'+tr.xpath('./td[2]/text()').extract_first().strip()
                ll.append(p)
            except Exception as e:
                print('error:  ',e)
        print(ll)

if __name__ == '__main__':
    os.system('scrapy crawl 111')








