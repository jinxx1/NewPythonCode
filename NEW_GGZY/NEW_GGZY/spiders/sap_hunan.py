# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib

from urllib import parse
from NEW_GGZY.Breakpoint import *

from NEW_GGZY.items import GgzyItem


class SapHunanSpider(scrapy.Spider):
    name = 'sap_hunan'
    allowed_domains = ['www.hunancatv.com']
    start_url = [{'catName':'湖南广电_商务招标_招标公告','url':'http://www.hunancatv.com/tender.aspx?pageindex={}&class=64&channel=57'},
                 {'catName':'湖南广电_商务招标_候选公示','url':'http://www.hunancatv.com/tender.aspx?pageindex={}&class=65&channel=57'}]

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        getTXTdict = getTXT(self.name, self.start_url)
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['indexUrl'] = i['url']

            yield scrapy.Request(url=meta['indexUrl'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)



    def parse(self, response):
        meta = response.meta
        linkList = response.xpath("//div[@class='mian']/div[@class='ny_group']/div[@class='ny_group_right']/div[@class='ny_group_right_txt']/div[@class='ny_group_right_Zi']/div[@class='ny_tender']/a/@href").extract()
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


        dict1['title'] = response.xpath("//div[@class='news_deta']/div[@class='news_Wen_Tit']/h1/text()").extract_first().strip()
        if not dict1['title']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 标题')
            print(response.url)
            return None

        dict1['content'] = response.xpath("//div[@class='news_deta']/div[@class='news_Wen_Txt']").extract_first()
        if not dict1['content']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 内容')
            print(response.url)
            return None


        try:
            issueTime = response.xpath("//div[@class='news_deta']/div[@class='news_Wen_Tit']/span/text()").extract_first()
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