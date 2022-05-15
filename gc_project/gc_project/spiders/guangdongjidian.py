import os,json,datetime
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql
r = Redis('127.0.0.1',6379)

class GuangdongjidianSpider(scrapy.Spider):
    name = 'gc_gdjd'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        {'type': '招标信息公告', 'url': 'https://www.gdebidding.com/zbxxgg/index_1.jhtml','head':'https://www.gdebidding.com/zbxxgg/'},
        {'type': '澄清更正公告', 'url': 'https://www.gdebidding.com/cqgzgg/index_1.jhtml','head':'https://www.gdebidding.com/cqgzgg/'},
        {'type': '招标结果公示', 'url': 'https://www.gdebidding.com/zbjggs/index_1.jhtml','head':'https://www.gdebidding.com/zbjggs/'},
        {'type': '招标结果公告', 'url': 'https://www.gdebidding.com/zbjggg/index_1.jhtml','head':'https://www.gdebidding.com/zbjggg/'},
        {'type': '招标信息预告', 'url': 'https://www.gdebidding.com/zbyg/index_1.jhtml','head':'https://www.gdebidding.com/zbyg/'},
        {'type': '电子招标投标信息', 'url': 'https://www.gdebidding.com/dzzbtbxx/index_1.jhtml','head':'https://www.gdebidding.com/dzzbtbxx/'},
        # {'type': '采购信息公告', 'url': 'https://www.gdebidding.com/cgxxgg/index_1.jhtml','head':'https://www.gdebidding.com/cgxxgg/'},
        # {'type': '采购结果公告', 'url': 'https://www.gdebidding.com/cgjggg/index_1.jhtml','head':'https://www.gdebidding.com/cgjggg/'}
    ]
    def start_requests(self):
        for dic in self.start_urls:
            url = dic['url']
            yield scrapy.Request(url=url,callback=self.parse_list,dont_filter=True,meta={'dic':dic})

    def parse_list(self, response):
        div_list = response.xpath('/html/body/div[7]/div/div[2]/div[2]/div')
        dic = response.meta['dic']
        for div in div_list:
            try:
                item = GcProjectItem()
                item['site'] = 'www.gdebidding.com'
                item['issue_time'] = div.xpath('./span/text()').get()
                item['subclass'] = dic['type']
                item['title'] = div.xpath('./a/text()').get()
                link = div.xpath('./a/@href').get()
                if link == None:
                    continue
                type_list = ['电子招标投标信息', '采购信息公告', '采购结果公告']
                if item['subclass'] in type_list:
                    item['page_url'] = link
                else:
                    item['page_url'] = 'https://www.gdebidding.com' + link
                num = select_mysql(
                    "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
                if num[0]['COUNT(*)'] == 1:
                    yield item
                else:
                    print('该条信息一爬取。。。',datetime.datetime.now())
            except Exception as e:
                print('error>>>>',e)
                print(e.__traceback__.tb_frame.f_globals["__file__"], "--lineno:%s" % e.__traceback__.tb_lineno,e)
        p = response.xpath('/html/body/div[7]/div/div[2]/div[2]/div[16]/div/a[3]/@href').get()
        # if p != None and int(p[-7]) < 10:
        if p != None and int(p[-7]) < 20:
            next_page_link = dic['head'] + p
            yield scrapy.Request(url=next_page_link,callback=self.parse_list,dont_filter=True,meta={'dic':dic})
    def parse_detail(self,response):
        pass
if __name__ == '__main__':
    os.system('scrapy crawl gc_gdjd')








