# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem

class SapJiangsuSpider(scrapy.Spider):
    name = 'sap_jiangsu'
    allowed_domains = ['supplier.jscnnet.com']
    start_url = [
{'catName':'江苏广电_招标采购公告','url':'https://supplier.jscnnet.com/column/col1463/index.html'},
{'catName':'江苏广电_招标采购结果','url':'https://supplier.jscnnet.com/column/col1464/index.html'}
]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.start_url)
        for i in getTXTdict['urlDict']:
            meta['indexUrl'] = i['url']
            meta['catName'] = i['catName']
            yield scrapy.Request(url=meta['indexUrl'],callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        linkList = re.findall("urls\[i\]=\'(.*?)\'",response.text)

        if not linkList:
            return None
        link = duplicateUrl(linkList,response.url)
        del linkList
        if not link:
            return None
        # print(len(link))
        # print(meta['catName'])
        # print(response.url)
        # print('-------------------------------------')

        for i in link:
            meta['url'] = parse.urljoin(response.url, i)
            yield scrapy.Request(url=meta['url'],callback=self.parseA,meta=meta,dont_filter=True)
        del link


    def parseA(self,response):
        # print('进入文章了')
        meta = response.meta
        dict1 = GgzyItem()
        dict1['title'] = response.xpath("//title/text()").extract_first()
        if not dict1['title']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 标题')
            print(response.url)
            # print(response.text)
            return None

        dict1['content'] = response.xpath("//div[@class='tabig_left']").extract_first()
        if not dict1['content']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 内容')
            print(response.url)
            return None

        try:
            dict1['issueTime'] = timeReMark(re.findall("发表时间: (\d{2,4}-\d{1,2}-\d{1,2})",dict1['content'])[0])
        except:
            try:
                dict1['issueTime'] = timeReMark(re.findall("article/(\d{2,4}-\d{1,2}-\d{1,2}/)", response.url)[0])
            except:
                print('没有 》》》》》》》》》》》》》》》》》》》》》》 时间')
                print(response.url)
                return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['subclass'] = meta['catName']

        del meta
        yield dict1