# -*- coding: utf-8 -*-

import scrapy
import re
import time
import json
import ssl

from uxuepai.items import UxuepaiItem
ToDayTime = time.strftime("%Y-%m-%d", time.localtime()).split('-')
ToDayTime = '2018-11-19'
context = ssl._create_unverified_context()
class GdcaSpider(scrapy.Spider):
    name = 'gdca'
    allowed_domains = ['gdca.gov.cn']
    def start_requests(self):
        url = 'https://www.gdca.gov.cn/gdcmsnet/gdcms/content/getContentList'
        numAll = [101,54,56,236,62,61,60,57,58,59,75,78,316,119,122,64,125,128]
        # numAll = [101]
        for num in numAll:
            yield scrapy.FormRequest(url=url,formdata={'catogoryId':str(num)},
                callback = self.parse,
                meta={'cookiejar': 1}
            )

    def parse(self,response):
        jsonR = json.loads(response.body_as_unicode()).get('data')
        jsonY = jsonR['optData']['data']
        for i in jsonY:
            # timeT = i['publicTime']
            publicTIME = time.strftime("%Y-%m-%d",time.localtime(int(i['publicTime']) // 1000))
            if publicTIME == ToDayTime:
                url = response.urljoin(i['address'])
                pathurl = re.findall('path=(.*)', url, re.S)[0]
                yield scrapy.FormRequest(
                    url='https://www.gdca.gov.cn/gdcmsnet/gdcms/content/staticView?',
                    method='GET',
                    callback=self.parseA,
                    formdata={'path':pathurl},
                    meta = {'cookiejar':response.meta['cookiejar']})

    def parseA(self,response):
        Title = response.xpath("//title/text()").extract()[0]
        word1 = response.xpath("//p//text()").extract()
        if word1:
            item = UxuepaiItem()
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            # print(Title)
            # print(response.url)
            # print(int(ToDayTime.replace('-','')))
            # print(wo)

            item['NameTOTALItem'] = '广东省通信管理局'
            item['TitleItem'] = Title
            item['LinkItem'] = response.url
            item['TimeItem'] = int(ToDayTime.replace('-', ''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'gdca.gov.cn'
            yield item
        else:
            pass

