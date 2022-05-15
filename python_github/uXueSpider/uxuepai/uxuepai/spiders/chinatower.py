# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
import time
from uxuepai.filterHtml import filter_tags
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())


class ChinatowerSpider(scrapy.Spider):
    name = 'chinatower'
    allowed_domains = ['china-tower.com']
    start_urls = ['https://www.china-tower.com/news?nav=101000',
                  'https://www.china-tower.com/news?nav=102000',
                  'https://www.china-tower.com/news?nav=103000',
                  'https://www.china-tower.com/news?nav=104000',
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
    def parseB(self,response):
        word1 = response.xpath("//p").extract()
        if word1:
            item = UxuepaiItem()
            Title = response.xpath("//h2/text()").extract()[0]
            wo = ''
            for i1 in word1:
                if i1:
                    s = '<p>' + filter_tags(i1) + '</p>'
                    wo = wo + s
            # print(wo)
            item['NameTOTALItem'] = '中国铁塔官网'
            item['TitleItem'] = Title
            item['LinkItem'] = response.url
            item['TimeItem'] = int(ToDayTime.re('-',''))
            item['WordItem'] = wo
            item['WebNameWord'] = 'china-tower.com'
            yield item
        else:
            pass
