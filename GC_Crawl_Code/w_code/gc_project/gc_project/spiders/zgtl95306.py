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


class TieluSpider(scrapy.Spider):

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.max = 0
    name = 'tielu95306'
    # allowed_domains = ['www.xxx.com']
    # start_urls = 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&curPage=%s'
    start_urls = [{'type':'项目公告','url':'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&noticeType=01&extend=1&curPage={}','page':50},#314501
                    {'type':'变更公告','url':'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&noticeType=02&extend=1&curPage={}','page':20}, #247
                    {'type':'答疑补漏','url':'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&noticeType=03&extend=1&curPage={}','page':30}, #321
                    {'type':'结果公告','url':'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&noticeType=04&extend=1&curPage={}','page':50}] #6666
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
                item['page_url'] = 'http://wzcgzs.95306.cn' + tr.xpath('./td[2]/a/@href').get()
                num = select_mysql(
                    "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
                if num[0]['COUNT(*)'] == 0:
                    yield scrapy.Request(url=item['page_url'],callback=self.parse_detail,dont_filter=True,meta={'item': item})
                else:
                    self.max += 1
                    print(self.max,"---")
                    if self.max > 20:return
            except Exception as e:
                print('error:  ',e)
    def parse_detail(self,response):
        item = response.meta['item']
        item['content']=response.xpath('/html/body/form/div[1]/div[2]').get()
        now_time = datetime.datetime.now()
        if item.get('business_type') == None:
            item['business_type'] = ''
        if item.get('city_name') == None:
            item['city_name'] = ''
        if item.get('purchase_type') == None:
            item['purchase_type'] = ''
        sql = "INSERT INTO ztbRawInfo (subclass,site,page_url,title,issue_time,creation_time,end_time,business_type,city_name,purchase_type) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
              % (item['subclass'], item['site'], item['page_url'], item['title'], item['issue_time'],
                 now_time,
                 now_time, item['business_type'], item['city_name'], item['purchase_type'])
        insert_id = insert_mysql(sql)
        c = pymysql.escape_string(item['content'])
        print(insert_id, '***')
        if insert_id != None:
            insert_mysql("INSERT INTO ztbRawInfoContent (raw_data_id,content) VALUES (%s,'%s')" % (insert_id, c))
if __name__ == '__main__':
    os.system('scrapy crawl tielu95306')



