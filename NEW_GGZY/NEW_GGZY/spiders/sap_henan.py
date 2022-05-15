# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib

from urllib import parse
from NEW_GGZY.Breakpoint import *

from NEW_GGZY.items import GgzyItem

class SapHenanSpider(scrapy.Spider):
    name = 'sap_henan'
    allowed_domains = ['http://www.henancatv.com']
    start_url = ['http://www.henancatv.com/zbxx/index_{}.jhtml']

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        meta['catName'] = '河南广电_招标信息'
        getTXTdict = getTXT(self.name, self.start_url)
        for i in getTXTdict['urlDict']:
            meta['indexUrl'] = i
            url = meta['indexUrl'].replace('_{}','')
            yield scrapy.Request(url=url,callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        linkList = response.xpath("//ul[@class='news_ul']/li/a/@href").extract()
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

        meta['Num']+=1
        yield scrapy.Request(url=meta['indexUrl'].format(str(meta['Num'])),
                             callback=self.parse, meta=meta, dont_filter=True)


    def parseA(self,response):
        # print('进入文章了')
        meta = response.meta
        dict1 = GgzyItem()
        dict1['title'] = response.xpath("//td[@class='newtxttitle']/text()").extract_first().strip()
        if not dict1['title']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 标题')
            print(response.url)
            return None

        dict1['content'] = response.xpath("//td[@class='new_txt2']").extract_first()
        if not dict1['content']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 内容')
            print(response.url)
            return None

        try:
            issueTime = response.xpath("//td[@class='new_txt_time1']/center/p/text()").extract_first()
            dict1['issueTime'] = timeReMark(re.findall("\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}",issueTime)[0])
        except:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 时间')
            print(response.url)
            return None


        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['subclass'] = meta['catName']

        del meta

        yield dict1