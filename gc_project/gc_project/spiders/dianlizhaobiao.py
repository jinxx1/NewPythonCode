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

class DianlizhaobiaoSpider(scrapy.Spider):
    name = 'gc_dlzb'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        {'type':'VIP项目','url':'http://www.dlztb.com/xmxx/xiangmu/{}.html','page':702},# 702
        {'type':'拟在建项目','url':'http://www.dlztb.com/xmxx/nizaijian/{}.html','page':1208}, # 1208
        {'type':'独家项目','url':'http://www.dlztb.com/xmxx/dujiaxiangmu/{}.html','page':10},
        {'type':'工程中标','url':'http://www.dlztb.com/zbgg/158_{}.html','page':1158}, # 1158
        {'type':'设备中标','url':'http://www.dlztb.com/zbgg/157_{}.html','page':130}  #130
    ]
    def start_requests(self):
        for dic in self.start_urls:
            for page in range(1,dic['page']):
                url = dic['url'].format(page)
                yield scrapy.Request(url=url,callback=self.parse_list,dont_filter=True,meta={'dic':dic})

    def parse_list(self, response):
        li_list = response.xpath('/html/body/div[10]/div[1]/div/ul/li')
        dic = response.meta['dic']
        for li in li_list:
            item = GcProjectItem()
            try:
                item['site'] = 'www.dlztb.com'
                item['issue_time'] = li.xpath('./i/text()').get()
                item['subclass'] = dic['type']
                item['title'] = li.xpath('./a/text()').get()
                item['page_url'] = li.xpath('./a/@href').get()
                if item['page_url'] != None:
                    num = select_mysql(
                        "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
                    if num[0]['COUNT(*)'] == 1:
                        yield item
                    else:
                        print('该条信息一爬取。。。',datetime.datetime.now())
            except Exception as e:
                print('error:  ',e)
        # page_url = response.xpath('/html/body/div[10]/div[1]/div/div/a[10]/@href').get()
        # # if int(page_url[-6]) < 20:
        # yield scrapy.Request(url=page_url, callback=self.parse_list, dont_filter=True,meta={'dic':dic})

if __name__ == '__main__':
    os.system('scrapy crawl gc_dlzb')




