# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import quote, unquote
from newscrapy.scrapyParse import *
from newscrapy.items import NewscrapyItem
import pprint
HEA = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
    "Connection": "close",
    "Content-Length": "0",
    "Host": "www.gcable.com.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}
class GcableGuangdongSpider(scrapy.Spider):
    name = 'gcable_guangdong'
    allowed_domains = ['www.gcable.com.cn']
    start_urls = ['https://www.gcable.com.cn/about-us/purchase/?json=1']
    mysql_allurl = get_mysql_allurl(allowed_domains[0])

    def start_requests(self):
        meta = {}
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse,
                             dont_filter=True, meta=meta,
                             headers=HEA)
    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)
        if not jsonT:
            print('没有获取页面json数据')
            return None

        for num,i in enumerate(jsonT):
            i['link'] = unquote(i['link'], encoding='utf-8')
            if i['link'] in self.mysql_allurl:
                continue
            else:
                meta['issueTime'] = get_timestr(i['post-time'])
                if not i['title'] or not meta['issueTime']:
                    continue
                meta['title'] = i['title']
                meta['url'] = unquote(i['link'], encoding='utf-8')
                subclassList = [i['city'], i['type'], i['cate']]
                meta['subclass'] = '_'.join(subclassList)
                meta['pageNum'] = 1
                meta['contentNum'] = num
                yield scrapy.Request(url=meta['url'],callback=self.contentParse,
                                     headers=HEA,meta=meta)

    def contentParse(self,response):
        meta = response.meta
        item = NewscrapyItem()
        contentArticle = response.xpath("//div[@class = 'news-desc']").extract()
        item['content'] = ''.join(contentArticle)
        if not item['content']:
            return None

        item['issueTime'] = meta['issueTime']
        item['title'] = meta['title']
        item['url'] = meta['url']
        item['site'] = self.allowed_domains[0]
        item['subclass'] = meta['subclass']
        item['pageNum'] = meta['pageNum']
        item['contentNum'] = meta['contentNum']
        yield item








