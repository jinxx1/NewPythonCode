import os
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql
r = Redis('127.0.0.1',6379)

class YancaohangyeSpider(scrapy.Spider):
    name = 'junduicaigou'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        # {'type':'单一来源公示','page':10,'url':'https://www.plap.cn/index/selectAllByTabs.html?page={}&articleTypeId=87&secondArticleTypeId=93&tab=%25E7%2589%25A9%25E8%25B5%2584'},
        # {'type':'中标结果公告公示','page':10,'url':'https://www.plap.cn/index/selectAllByTabs.html?page={}&articleTypeId=44&secondArticleTypeId=66&tab=%25E7%2589%25A9%25E8%25B5%2584'},
        {'type':'中标结果公告公示','page':10,'url':'https://www.plap.cn/index/selectAllByTabs.html?page={}&articleTypeId=1&secondArticleTypeId=23&tab=%25E7%2589%25A9%25E8%25B5%2584'},
    ]

    def start_requests(self):
        for dic in self.start_urls:
            for i in range(1,dic['page']):
                url = dic['url'].format(i)
                yield scrapy.Request(url=url,callback=self.parse_list,dont_filter=True,meta={'dic':dic})

    def parse_list(self, response):
        dic = response.meta['dic']
        li_list = response.xpath('/html/body/form/div/div[3]/ul/li')
        for li in li_list:
            item = GcProjectItem()
            item['site'] = 'www.plap.cn'
            item['issue_time'] = li.xpath('./span[2]/text()').get()
            item['subclass'] = dic['type']
            item['title'] = li.xpath('./a/text()').get()
            item['page_url'] = 'https://www.plap.cn' + li.xpath('./a/@href').get()
            num = select_mysql("SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。')
if __name__ == '__main__':
    os.system('scrapy crawl junduicaigou')


