# -*- coding: utf-8 -*-
import scrapy,re,time,datetime,pprint,pymysql
from MidCrawl.SechMySql import *
from urllib import parse
from MidCrawl.items import MidcrawlItem
from MidCrawl.rexGetTime import *

def remarkList(list):
    newList = []
    for i in list:
        if 'javascript'in i:
            continue
        i = i.replace(' ','').replace('\n','').replace('\t','').replace('\r','')
        if i:
            newList.append(i)
    return newList


class AutospiderSpider(scrapy.Spider):
    name = 'autoSpider'

    MYSQLINFO = mysql_seach()

    def start_requests(self):
        for meta in self.MYSQLINFO:
            yield scrapy.Request(url=meta['startUrl'],callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        Xpath_link = response.xpath(meta['LinkList']).extract()
        if not Xpath_link:
            return None
        # 建立一个字典及包含该字典的list，用来存储去重后的链接和去重前该链接在Xpath_link数值中的位置
        linkDict_nonDeduplicationList = []
        for i, tempUrl in enumerate(Xpath_link):
            linkDict = {}
            linkDict['Num'] = i
            requUrl = parse.urljoin(response.url,tempUrl)# 构造链接
            linkDict['url'] = requUrl.strip()
            if meta['SiteUrl'] not in linkDict['url']:
                continue
            linkDict_nonDeduplicationList.append(linkDict)

        # 开始去重，返回[{},{}]的list
        new_link_List = mysql_Deduplication(linkDict_nonDeduplicationList)
        if not new_link_List:
            return None
        for i in new_link_List:
            getXpathUrl = Xpath_link[i['Num']]
            XpathTitle = response.xpath("//*[@href = '{}']//text()".format(getXpathUrl)).extract()
            try:
                meta['getListTitle'] = remarkList(XpathTitle)[0]
            except:
                meta['getListTitle'] = ''
            meta['requestUrl'] = i['url']
            yield scrapy.Request(url=meta['requestUrl'],callback=self.ContentGetParse,meta=meta,)

    def ContentGetParse(self, response):
        item = MidcrawlItem()
        meta = response.meta
        Content_Text = response.xpath(meta['Content_Text']).extract()
        if not Content_Text:
            return None
        try:
            Content_Title = response.xpath(meta['Content_Title']).extract()[0]
        except:
            Content_Title = ''

        TitleTure = meta['getListTitle'] or Content_Title

        if not TitleTure:
            return None



        item['SiteNameCha'] = meta['SiteName']
        item['SiteUrl'] = meta['SiteUrl']
        item['StartUrl'] = meta['startUrl']
        item['artTitle'] = TitleTure
        item['artContent'] = ''.join(['<p>'+i+'</p>' for i in Content_Text])
        item['artUrl'] = meta['requestUrl']
        item['Xpath_id'] = meta['id']
        item['artContentTime'] = rexTimeGet(str(response.text))
        yield item





