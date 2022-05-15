# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
import time

ToDayTime = time.strftime("%Y-%m-%d", time.localtime())
# ToDayTime = '2018-12-12'


class HuizhouSpider(scrapy.Spider):
    name = 'huizhou'
    allowed_domains = ['huizhou.gov.cn']
    start_urls = ['http://jxj.huizhou.gov.cn/pages/cms/hzjxj/html/artList.html?cataId=7d0e918d07d14293a86ee258e26434ec',
                  'http://jxj.huizhou.gov.cn/pages/cms/hzjxj/html/artList.html?cataId=64fcb241d5284bb484118e32c036e38f',
                  'http://jxj.huizhou.gov.cn/pages/cms/hzjxj/html/artList.html?cataId=28f61be915194319ba6aca7458fec7a4',
                  'http://jxj.huizhou.gov.cn/pages/cms/hzjxj/html/artList.html?cataId=38804c21b325474fa7551bdd5ada8a85',
                  'http://jxj.huizhou.gov.cn/pages/cms/hzjxj/html/artList.html?cataId=800821d853ad4f6da73894d050cde9c1',
                  'http://jxj.huizhou.gov.cn/pages/cms/hzjxj/html/artList.html?cataId=64ca78da3d054e90a6294126e1f26610',
                  'http://jxj.huizhou.gov.cn/pages/cms/hzjxj/html/artList.html?cataId=b0bf191443814387929b12df04b99ff8',
                  'http://jxj.huizhou.gov.cn/pages/cms/hzjxj/html/artList.html?cataId=2f9a089dce554295befcbe71638ac6ac',
                  ]

    def parse(self, response):
        xpathword1 = "//*[contains(text(),'{}')]/parent::*//@href".format(ToDayTime)
        xpathword2 = "//*[contains(text(),'{}')]/parent::*/parent::*//@href".format(ToDayTime)
        timeTemp = response.xpath(xpathword1).extract()
        if timeTemp:
            for i in timeTemp:
                url = response.urljoin(i)
                yield scrapy.Request(url=url, callback=self.parseB)
        else:
            timeTemp = response.xpath(xpathword2).extract()
            for i in timeTemp:
                url = response.urljoin(i)
                yield scrapy.Request(url=url, callback=self.parseB)

    def parseB(self, response):
        word1 = response.xpath("//p//text()").extract()
        if word1:
            item = UxuepaiItem()
            Title = response.xpath("//meta[@name = 'ArticleTitle']/@content").extract()[0]
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '惠州市经济和信息化局'
            item['TitleItem'] = Title
            item['LinkItem'] = response.url
            item['TimeItem'] = int(ToDayTime.replace('-', ''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'huizhou.gov.cn'
            yield item
            # print(Title)
            # print(response.url)
            # print(wo)
        else:
            pass
