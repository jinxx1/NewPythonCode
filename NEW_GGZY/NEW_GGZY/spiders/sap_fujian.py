# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem




class SapFujianSpider(scrapy.Spider):
    name = 'sap_fujian'
    allowed_domains = ['www.fjgdwl.com']
    start_url = [
{'catName':'福建广电_招标公告','url':'https://www.fjgdwl.com/bids/18-{}.aspx'},
{'catName':'福建广电_招标公示','url':'https://www.fjgdwl.com/bids-37.aspx'},
{'catName':'福建广电_信息公开','url':'https://www.fjgdwl.com/bids-38.aspx'}
]

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        getTXTdict = getTXT(self.name, self.start_url)
        for i in getTXTdict['urlDict']:
            meta['catName'] = i['catName']
            meta['indexUrl'] = i['url']
            yield scrapy.Request(url=meta['indexUrl'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        linkList = response.xpath("//div[@class='rel csevtr']/div[@class='yondenc']/div[@class='encdg']/ul[@class='newcle coodet']/li/a/@href").extract()
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
        dict1['title'] = response.xpath("//div[@class='wrap']/div[@class='mrenvc']/div[@class='bkenc']/p[@class='p1']/text()").extract_first().strip()
        if not dict1['title']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 标题')
            print(response.url)
            return None

        dict1['content'] = response.xpath("//div[@class='wrap']/div[@class='mrenvc']/div[@class='tlsdet']").extract_first()
        if not dict1['content']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 内容')
            print(response.url)
            return None

        try:
            issueTime = response.xpath("//div[@class='wrap']/div[@class='mrenvc']/div[@class='bkenc']/p[@class='p2']/text()").extract_first()
            dict1['issueTime'] = timeReMark(re.findall("\d{2,4}-\d{1,2}-\d{1,2}",issueTime)[0])
        except:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 时间')
            print(response.url)
            return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['subclass'] = meta['catName']

        del meta
        yield dict1