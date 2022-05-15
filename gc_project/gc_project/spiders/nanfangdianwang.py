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


class NanfangdianwangSpider(scrapy.Spider):
    name = 'gc_nfdw'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['http://www.bidding.csg.cn/zbcg/index_1.jhtml',] # 'http://www.bidding.csg.cn/tzgg/index_1.jhtml'
    def start_requests(self):
        for url in self.start_urls:
            if url == 'http://www.bidding.csg.cn/zbcg/index_1.jhtml':
                yield scrapy.Request(url=url,callback=self.parse_zbcg,dont_filter=True)
            if url == 'http://www.bidding.csg.cn/tzgg/index_1.jhtml':
                yield scrapy.Request(url=url,callback=self.parse_tzgg,dont_filter=True)

    def parse_zbcg(self, response):
        li_list = response.xpath('/html/body/section/div[3]/div[1]/ul/li')
        for li in li_list:
            item = GcProjectItem()
            try:
                item['site'] = 'www.bidding.csg.cn'
                item['issue_time'] = li.xpath('./span/span/text()').get()
                item['subclass'] = li.xpath('./span/a/text()').extract_first()
                item['title'] = li.xpath('./a[2]/text()').get()
                item['page_url'] = 'http://www.bidding.csg.cn' + li.xpath('./a/@href').extract_first()
                num = select_mysql(
                    "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
                if num[0]['COUNT(*)'] == 1:
                    yield item
                else:
                    print('该条信息一爬取。。。',datetime.datetime.now())
            except Exception as e:
                print('error:  ',e)
        try:
            page_url = 'http://www.bidding.csg.cn/zbcg/' + response.xpath('/html/body/section/div[3]/div[2]/div/a[3]/@href').get()
            if int(page_url[-7]) < 50:
                yield scrapy.Request(url=page_url, callback=self.parse_zbcg, dont_filter=True)
        except Exception as e:
            print('error:   ', e.__traceback__.tb_frame.f_globals["__file__"],
                  "--lineno:%s" % e.__traceback__.tb_lineno, e)


    def parse_tzgg(self, response):
        li_list = response.xpath('/html/body/section/div/div[2]/div[3]/ul/li')
        for li in li_list:
            item = GcProjectItem()
            try:
                item['site'] = 'www.bidding.csg.cn'
                item['issue_time'] = li.xpath('./span/span/text()').get()
                item['subclass'] = '通知公告'
                item['title'] = li.xpath('./a[2]/text()').get()
                item['page_url'] = 'http://www.bidding.csg.cn' + li.xpath('./a/@href').extract_first()
                num = select_mysql("SELECT COUNT(*) FROM `ztbRawInfoStatistics` WHERE page_url = '%s'" % item['page_url'])
                if num[0]['COUNT(*)'] == 0:
                    yield item
                else:
                    print('该条信息一爬取。。。',datetime.datetime.now())
            except Exception as e:
                print('error:  ',e)
        try:
            page_url = 'http://www.bidding.csg.cn/tzgg/' + response.xpath('/html/body/section/div/div[2]/div[4]/div/a[3]/@href').get()
            # if int(page_url[-7]) < 3:
            yield scrapy.Request(url=page_url, callback=self.parse_tzgg, dont_filter=True)
        except Exception as e:
            print('error:   ',e.__traceback__.tb_frame.f_globals["__file__"], "--lineno:%s" % e.__traceback__.tb_lineno,e)
if __name__ == '__main__':
    os.system('scrapy crawl gc_nfdw')






