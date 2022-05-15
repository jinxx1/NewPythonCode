# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lxml import html
import re
import json
import time
from uxuepai.items import UxuepaiItem

ToDayTime = time.strftime("%Y-%m-%d", time.localtime())


class ZsSpider(scrapy.Spider):
    name = 'zs'
    allowed_domains = ['zs.gov.cn']
    start_urls = ['http://www.zs.gov.cn/main/zwgk/list/town/index.action']

    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'))
        links = link_extractor.extract_links(response)
        for url in links:
            urlcut = re.findall('did=(\d*)', url.url)
            if len(urlcut) > 0:
                urlid = urlcut[0]
                data1 = {
                    'did': urlid,
                    'curPage': '1',
                    'pageSize': '22',
                    'ts': '1537952595837',
                }
                url = 'http://www.zs.gov.cn/ajax/infoPage.action?did=' + str(urlid)
                yield scrapy.FormRequest(url=url,
                                         method='GET',
                                         formdata=data1,
                                         meta={'cookiejar': 1},
                                         callback=self.parseA)
            else:


                yield scrapy.Request(url=url.url, callback=self.parseNOID,meta = {'cookiejar':1},dont_filter=False)

    def parseNOID(self,response):
        # print(response.headers.getlist('Set-Cookie'))
        regex = re.findall('getOpenData\(\'(.*?)\'\, \'(.*?)\'', response.text, re.S)
        try:
            tokentype = re.findall('token=(.*?)\';', response.text, re.S)[0]
        except:
            pass
        for i in range(len(regex)):
            pubcode = regex[i][0]
            codetype = regex[i][1]
            base0_url = 'http://www.zs.gov.cn/ajax/openInfoPage.action?'
            data2 = {
                'curPage': '1',
                'pageSize': '22',
                'pubcode': pubcode,
                'type': 'scatcode',
                'code': codetype,
                'token': tokentype,
            }
            yield scrapy.FormRequest(url=base0_url,
                                     method='GET',
                                     formdata=data2,
                                     meta={'cookiejar': response.meta['cookiejar']},
                                     callback=self.parseA)


    def parseA(self,response):
        jsonR = json.loads(response.body_as_unicode()).get('rows')
        if jsonR:
            for jsonY in jsonR:
                timeT = jsonY.get('date')
                # if timeT :
                if timeT == ToDayTime:
                    titleT = jsonY.get('title')
                    indexID = jsonY.get('id')
                    try:
                        Link = jsonY.get('link')
                    except:
                        pass
                    if Link:
                        Link1 = 'http://www.zs.gov.cn' + jsonY.get('link')
                        yield scrapy.Request(url=Link1, callback=self.parseRade, meta={'title': titleT, 'time1': timeT})
                    else:
                        aa = 'http://www.zs.gov.cn/main/zwgk/newsview/index.action?id='
                        Link2 = aa + str(indexID)
                        yield scrapy.Request(url=Link2, callback=self.parseRade, meta={'title': titleT, 'time1': timeT})
    def parseRade(self,response):
        word1 = response.xpath("//p/span/text() | //p//text() | //div[@class = 'xs_cnt']/text()").extract()
        if word1:
            item = UxuepaiItem()
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            # print(response.meta['title'])
            # print(int(response.meta['time1'].replace('-','')))
            # # print(wo)
            # print(response.url)
            item['NameTOTALItem'] = '中山市人民政府'
            item['TitleItem'] = response.meta['title']
            item['LinkItem'] = response.url
            item['TimeItem'] = int(response.meta['time1'].replace('-',''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'zs'
            yield item
        else:
            pass