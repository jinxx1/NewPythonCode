# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/18
import os,json,datetime
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql
r = Redis('127.0.0.1',6379)

class ZhengfucaigouSpider(scrapy.Spider):
    name = 'gc_zfcg'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        {
            'url':'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type':'采购公告','page':90  # 9000
        },
        {
            'url':'http://www.szzfcg.cn/portal/topicView.do?method=view&id=2719966&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '采购公示', 'page': 3
        },
        {
            'url': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=10001&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '采购公告', 'page': 2
        },
        {
            'url': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=201901&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '采购公告', 'page': 30  # 310
        },
        {
            'url': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=201902&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '采购公告', 'page': 20  # 20
        },
        {
            'url': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660&agencyType=2&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '采购公告', 'page': 30  # 3350
        },
        {
            'url': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=2014&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '采购结果公示', 'page': 70  # 7000
        },
        {
            'url': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=10002&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '采购结果公示', 'page': 20  # 20
        },
        {
            'url': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=518010&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '采购公告', 'page': 22  # 22
        },
        {
            'url': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=518014&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '结果公告', 'page': 21  # 21
        },
        {
            'url': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660&agencyType=1&topicChrList_20070702_crd=20&ec_i=topicChrList_20070702&topicChrList_20070702_p=%s',
            'type': '采购公告', 'page': 20  # 1688
        },
    ]
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
        for dic in self.start_urls:
            for page in range(1,dic['page']):
                url = dic['url']%(page)
                yield scrapy.Request(url=url,
                                     headers=headers,
                                     callback=self.parse_list,
                                     dont_filter=True,
                                     meta={'dic':dic})

    def parse_list(self, response):
        tr_list = response.xpath('//*[@id="topicChrList_20070702_table"]/tbody/tr')
        dic = response.meta['dic']
        for tr in tr_list:
            item = GcProjectItem()
            try:
                item['site'] = 'www.szzfcg.cn'
                item['issue_time'] = tr.xpath('./td[5]/text()').get()
                item['subclass'] = dic['type']
                item['title'] = tr.xpath('./td[3]/a/text()').get()
                d = tr.xpath('./td[3]/a/@href').get()
                item['page_url'] = 'http://www.szzfcg.cn/portal/documentView.do?method=view&id=' + d.split('=')[1]
                num = select_mysql(
                    "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
                if num[0]['COUNT(*)'] == 1:
                    yield item
                else:
                    print('该条信息一爬取。。。',datetime.datetime.now())
            except Exception as e:
                print('error:  ',e)

if __name__ == '__main__':
    os.system('scrapy crawl gc_zfcg')





