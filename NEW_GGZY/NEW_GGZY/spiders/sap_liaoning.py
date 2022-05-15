# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem

class SapLiaoningSpider(scrapy.Spider):
    name = 'sap_liaoning'
    allowed_domains = ['http://wzcg.bfgd.com.cn']
    start_url = [{'catName': '辽宁广电_招标和询价公告', 'url': 'http://wzcg.bfgd.com.cn:8066/ForePage/Skin3/Notice.aspx?pagesize=50&page={}'},
                  {'catName': '辽宁广电_结果公示', 'url': 'http://wzcg.bfgd.com.cn:8066/ForePage/Skin3/ZBList.aspx?pagesize=50&page={}'}]


    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        getTXTdict = getTXT(self.name, self.start_url)
        for i in getTXTdict['urlDict']:
            meta['indexUrl'] = i['url']
            meta['catName'] = i['catName']
            yield scrapy.Request(url=meta['indexUrl'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta

        linkList = response.xpath("//div[@class='cont newslist']/ul/li/a/@href").extract()
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
            title = response.xpath("//*[@href = '{}']/text()".format(i)).extract()
            meta['title'] = ''.join(title).strip()
            if not meta['title']:
                print('没有 》》》》》》》》》》》》》》》》》》》》》》 标题')
                print(i)
                return None
            try:
                issueTime = response.xpath("//*[@href = '{}']/../i/text()".format(i)).extract_first()

                meta['issueTime'] = timeReMark(re.findall("\d{2,4}-\d{1,2}-\d{1,2}",issueTime)[0])
            except:
                print('没有 》》》》》》》》》》》》》》》》》》》》》》 时间')
                print(i)
                return None

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

        content = response.xpath("//div[@id='autocontent']|//div[@class = 'infocontent']").extract()
        dict1['content'] = ''.join(content)
        if not dict1['content']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 内容')
            print(response.url)
            return None
        dict1['title'] = meta['title']
        dict1['issueTime'] = meta['issueTime']

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['subclass'] = meta['catName']

        del meta
        yield dict1