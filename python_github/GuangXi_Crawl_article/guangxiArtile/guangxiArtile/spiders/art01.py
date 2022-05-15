# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,datetime
from guangxiArtile.items import GuangxiartileItem
from guangxiArtile.rexGetTime import *
from guangxiArtile.MongoTEST import *
from urllib import parse


MonGo_getContentUrl = MongoDB_guangxi_ContentUrl()
find_code = {'inserTOMAINSQL': 0}

class Art01Spider(scrapy.Spider):
    name = 'art01'
    allowed_domains = ['www.ccgp-guangxi.gov.cn']

    def start_requests(self):
        meta = {}
        getMongoDict = MonGo_getContentUrl.getMongoALLdate(find_code)
        for i in getMongoDict:
            meta['ContentUrl']=i['ContentUrl']
            meta['code'] = i['code']
            meta['inserTOMAINSQL'] = i['inserTOMAINSQL']
            meta['catName'] = i['catName']
            yield scrapy.Request(url=meta['ContentUrl'],callback=self.parse,meta=meta,dont_filter=True)


        # url = 'http://www.ccgp-guangxi.gov.cn/view/staticpags/shengji_zbgg/8ab8a09065fba46d01666239f73e0f05.html'
        # meta = {'ContentUrl': url,'code':'testcode','inserTOMAINSQL':0,'catName':'testcode'}
        # yield scrapy.Request(url=meta['ContentUrl'], callback=self.parse, meta=meta, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        dict1 = GuangxiartileItem()
        # 获取完整内容html代码
        try:
            html = response.xpath("//div[@class='frameReport']").extract()[0]
            dict1['content'] = html
        except:
            print('最终页未能获取到文章-内容', response.url)
            ERROR_DICT = {'ErrorCrawl':'Not articleHTML'}
            MonGo_getContentUrl.insert_error(response.url,ERROR_DICT)
            return None
        # 获取内容页标题
        try:
            html = response.xpath("//div[@class='frameReport']/div[@class='reportTitle']/h1/text()").extract()[0]
            dict1['title'] = html.strip()
        except:
            print('最终页未能获取到文章-标题', response.url)
            ERROR_DICT = {'ErrorCrawl': 'Not articleTitle'}
            MonGo_getContentUrl.insert_error(response.url, ERROR_DICT)
            return None
        # 获取内容页时间
        try:
            html = response.xpath("//div[@class='frameReport']/div[@class='reportTitle']/span[@class='publishTime']/text()").extract()[0]
            dict1['issueTime'] = rexTimeGet(html)
        except:
            print('最终页未能获取到文章-时间', response.url)
            ERROR_DICT = {'ErrorCrawl': 'Not articleTime'}
            MonGo_getContentUrl.insert_error(response.url, ERROR_DICT)
            return None

        # 获取内容页附件信息
        dict1['attachments'] = []
        attchmentsLink = response.xpath("//div[@class='frameReport']/div[@class='file']/ul/li/a/@href").extract()
        if attchmentsLink:
            for attlink in attchmentsLink:
                attDict ={}
                attDict['url'] = parse.urljoin(response.url, attlink)
                attDict['name'] = ''.join(response.xpath("//*[@href = '{}']/text()".format(attlink)).extract())
                if not attDict['name']:
                    attDict['name'] = 'unknow_name'
                attDict['type'] = getfiletype(attDict['url'])
                attDict['status'] = 0
                attDict['docId'] = 'null'
                dict1['attachments'].append(attDict)

        dict1['url'] = response.url
        dict1['site'] = '广西壮族自治区政府采购网'
        dict1['domain'] = self.allowed_domains[0]
        dict1['subclass'] = meta['catName']

        yield dict1



