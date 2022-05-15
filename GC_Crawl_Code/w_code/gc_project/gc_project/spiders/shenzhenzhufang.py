# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/9
import json,os,datetime
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql
r = Redis('127.0.0.1',6379)

class ShenzhenzhufangSpider(scrapy.Spider):
    name = 'gc_szzf'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        {'url':'https://www.szjsjy.com.cn:8001/jyw/queryGongGaoList.do?rows=10&page=%s','type':'招标公告','page':20},# 420
        {'url':'https://www.szjsjy.com.cn:8001/jyw/queryBGList.do?page=%s&rows=10','type':'变更公示','page':50},#919
        {'url':'https://www.szjsjy.com.cn:8001/jyw/queryKongZhiJiaList.do?rows=10&page=%s','type':'招标控制价公示','page':20},#177
        {'url':'https://www.szjsjy.com.cn:8001/jyw/queryKBJiLuList.do?rows=10&page=%s','type':'开标情况公示','page':20},#375
        {'url':'https://www.szjsjy.com.cn:8001/jyw/queryPWList.do?rows=10&page=%s','type':'评标委员会公示','page':20},#287
        {'url':'https://www.szjsjy.com.cn:8001/jyw/queryPBJieGuoList.do?rows=10&page=%s','type':'评标报告公示','page':20},#287
        {'url':'https://www.szjsjy.com.cn:8001/jyw/queryDBJieGuoList.do?rows=10&page=%s','type':'定标结果公示','page':20},#443
        {'url':'https://www.szjsjy.com.cn:8001/jyw/queryZBJieGuoList.do?rows=10&page=%s','type':'中标结果公示','page':20},#384
    ]
    # custom_settings = {
    #     "REDIRECT_ENABLED": False,
    #     "ROBOTSTXT_OBEY": False,  # 关闭robot 协议
    #
    #     "DEFAULT_REQUEST_HEADERS": {
    #         'Cache-Control': 'no-cache',
    #         'Connection': 'keep-alive',
    #         'Cookie': 'user=null; user=null; JSESSIONID=1LyxaUETdJCtUX0fsYafgrkmwtR1J1N2yd9Yz_SktVjaos1QxYVU!-1203063273',
    #         'Referer': 'https://www.szjsjy.com.cn:8001/jyw/jyw/zbGongGao_View.do?ggguid=2c9e8ac275740a840175ab05cbad474f',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    #         'X-Requested-With': 'XMLHttpRequest',
    #     }
    # }
    def start_requests(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'user=null; JSESSIONID=SIOw0s_lE3WROPEeBFLTl90_raWApGB5A23BB5NZOzKKlPotYc6m!-1203063273',
            'Host': 'www.szjsjy.com.cn:8001',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }
        for dic in self.start_urls:
            if dic['type'] == '中标结果公示':
                for page in range(1,dic['page']):
                    url = dic['url']%str(page)
                    sleep(2)
                    yield scrapy.Request(url=url,callback=self.parse_zbjggs,dont_filter=True)
            if dic['type'] == '定标结果公示':
                for page in range(1,dic['page']):
                    url = dic['url']%str(page)
                    sleep(2)
                    yield scrapy.Request(url=url,callback=self.parse_dbjggs,dont_filter=True)
            if dic['type'] == '评标报告公示':
                for page in range(1,dic['page']):
                    url = dic['url']%str(page)
                    sleep(2)
                    yield scrapy.Request(url=url,callback=self.parse_pbbbgs,dont_filter=True)
            if dic['type'] == '评标委员会公示':
                for page in range(1,dic['page']):
                    url = dic['url']%str(page)
                    sleep(2)
                    yield scrapy.Request(url=url,callback=self.parse_pbwyhgs,dont_filter=True)
            if dic['type'] == '开标情况公示':
                for page in range(1,dic['page']):
                    url = dic['url']%str(page)
                    sleep(2)
                    yield scrapy.Request(url=url,callback=self.parse_kbqkgs,dont_filter=True)
            if dic['type'] == '招标控制价公示':
                for page in range(1,dic['page']):
                    url = dic['url']%str(page)
                    sleep(2)
                    yield scrapy.Request(url=url,callback=self.parse_kzjgs,dont_filter=True)
            if dic['type'] == '延期变更公示':
                for page in range(1,dic['page']):
                    url = dic['url']%str(page)
                    sleep(2)
                    yield scrapy.Request(url=url,callback=self.parse_yqbbgs,dont_filter=True)
            if dic['type'] == '招标公告':
                for page in range(1,dic['page']):
                    url = dic['url']%str(page)
                    sleep(2)
                    yield scrapy.Request(url=url,callback=self.parse_zbgg,dont_filter=True)
    def parse_zbjggs(self,response):
        res_obj = response.text[11:-1]
        dic = json.loads(res_obj)['rows']
        for row in dic:
            item = GcProjectItem()
            item['title'] = row['bdName']
            item['subclass'] = '中标结果公示'
            item['page_url'] = row['detailUrl']
            item['issue_time'] = row['fabuTime2']
            item['site'] = 'www.szjsjy.com.cn'
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
    def parse_dbjggs(self,response):
        res_obj = response.text[11:-1]
        dic = json.loads(res_obj)['rows']
        for row in dic:
            item = GcProjectItem()
            item['title'] = row['bdName']
            item['subclass'] = '定标结果公示'
            item['page_url'] = row['detailUrl']
            item['issue_time'] = row['createTime2']
            item['site'] = 'www.szjsjy.com.cn'
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
    def parse_pbbbgs(self,response):
        res_obj = response.text[11:-1]
        dic = json.loads(res_obj)['rows']
        for row in dic:
            item = GcProjectItem()
            item['title'] = row['bdName']
            item['subclass'] = '评标报告公示'
            item['page_url'] = row['detailUrl']
            item['issue_time'] = row['faBuTime2']
            item['site'] = 'www.szjsjy.com.cn'
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
    def parse_pbwyhgs(self,response):
        res_obj = response.text[11:-1]
        dic = json.loads(res_obj)['rows']
        for row in dic:
            item = GcProjectItem()
            item['title'] = row['bdName']
            item['subclass'] = '评标委员会公示'
            item['page_url'] = row['detailUrl']
            item['issue_time'] = row['createTime2']
            item['site'] = 'www.szjsjy.com.cn'
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
    def parse_kbqkgs(self,response):
        res_obj = response.text[16:-1]
        dic = json.loads(res_obj)['rows']
        for row in dic:
            item = GcProjectItem()
            item['title'] = row['bdName']
            item['subclass'] = '开标情况公示'
            item['page_url'] = row['detailUrl']
            item['issue_time'] = row['kbTime2']
            item['site'] = 'www.szjsjy.com.cn'
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
    def parse_kzjgs(self,response):
        res_obj = response.text[19:-1]
        dic = json.loads(res_obj)['rows']
        for row in dic:
            item = GcProjectItem()
            item['title'] = row['ggName']
            item['subclass'] = '招标控制价公示'
            item['page_url'] = row['detailUrl']
            item['issue_time'] = row['fbStartTime2']
            item['site'] = 'www.szjsjy.com.cn'
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
    def parse_yqbbgs(self,response):
        res_obj = response.text[11:-1]
        dic = json.loads(res_obj)['rows']
        for row in dic:
            item = GcProjectItem()
            item['title'] = row['bgBiaoTi']
            item['subclass'] = '延期变更公示'
            item['page_url'] = row['detailUrl']
            item['issue_time'] = row['faBuTime2']
            item['site'] = 'www.szjsjy.com.cn'
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
    def parse_zbgg(self, response):
        res_obj = response.text[16:-1]
        dic = json.loads(res_obj)['rows']
        for row in dic:
            item = GcProjectItem()
            item['title'] = row['ggName']
            item['subclass'] = '招标公告'
            item['page_url'] = row['detailUrl']
            item['issue_time'] = row['ggStartTime2']
            item['site'] = 'www.szjsjy.com.cn'
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
if __name__ == '__main__':
    os.system('scrapy crawl gc_szzf')






