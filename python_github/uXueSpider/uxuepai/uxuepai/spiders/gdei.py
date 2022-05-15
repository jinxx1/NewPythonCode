# -*- coding: utf-8 -*-
import scrapy
from uxuepai.items import UxuepaiItem
from scrapy.linkextractors import LinkExtractor
import time
ToDayTime = time.strftime("%Y%m%d", time.localtime())

class GdeiSpider(scrapy.Spider):
    name = 'gdei'
    allowed_domains = ['gdei.gov.cn']
    start_urls = [
            'http://www.gdei.gov.cn/zwgk/tpxw/index.htm',
            'http://www.gdei.gov.cn/zwgk/tzgg/index.htm',
            'http://www.gdei.gov.cn/zwgk/mtbd/index.htm',
            'http://www.gdei.gov.cn/zwgk/dsdt/index.htm',
            'http://www.gdei.gov.cn/zwgk/jxgk/index.htm',
            'http://www.gdei.gov.cn/zwgk/xmzj/index.htm',
            'http://www.gdei.gov.cn/zwgk/zcfg/gjbm/index.htm',
            'http://www.gdei.gov.cn/zwgk/zcfg/gjbmgz/index.htm',
            'http://www.gdei.gov.cn/zwgk/zcfg/dfsf/index.htm',
            'http://www.gdei.gov.cn/zwgk/zcfg/szfgfxwj/index.htm',
            'http://www.gdei.gov.cn/zwgk/zcfg/jmwfg/index.htm',
            'http://www.gdei.gov.cn/zwgk/zcfg/fgjd/index.htm',
            'http://www.gdei.gov.cn/zwgk/gzdt/index.htm',
            'http://www.gdei.gov.cn/zwgk/bmfw/index.htm',
            'http://www.gdei.gov.cn/zwgk/zdjc/index.htm',
            'http://www.gdei.gov.cn/zwgk/zcgh/jsgz/index.htm',
            'http://www.gdei.gov.cn/zwgk/zcgh/xjzbzz/index.htm',
            'http://www.gdei.gov.cn/zwgk/zcgh/cyzyy/index.htm',
            'http://www.gdei.gov.cn/zwgk/5gk/jcgk/index.htm',
            'http://www.gdei.gov.cn/zwgk/5gk/zxgk/index.htm',
            'http://www.gdei.gov.cn/zwgk/5gk/jggk/index.htm'
]

    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'))
        links = link_extractor.extract_links(response)
        for url in links:
            urlYes = url.url.find(ToDayTime)
            if urlYes >= 0:
                yield scrapy.Request(url=url.url, callback=self.parseA)
    def parseA(self,response):
        item = UxuepaiItem()
        TitleTemp = response.xpath("//title/text()").extract()
        Title = TitleTemp[0].replace('<br>','')
        word1 = response.xpath("//p//text()").extract()
        if word1:
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            item['NameTOTALItem'] = '广东省工业和信息化厅'
            item['TitleItem'] = Title
            item['LinkItem'] = response.url
            item['TimeItem'] = int(ToDayTime)
            item['WordItem'] = wo
            item['WebNameWord'] = 'gdei.gov.cn'
            yield item
        else:
            pass

