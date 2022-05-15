# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem

class SapShanhaiSpider(scrapy.Spider):
    name = 'sap_shanhai'
    allowed_domains = ['www.ocn.net.cn']
    start_urls = ['http://www.ocn.net.cn/gsgg_zhaobiao.html', 'http://www.ocn.net.cn/gsgg_zhaobiao2017.html', 'http://www.ocn.net.cn/gsgg_zhaobiao2016.html', 'http://www.ocn.net.cn/gsgg_zhaobiao2015.html', 'http://www.ocn.net.cn/gsgg_zhaobiao2014.html', 'http://www.ocn.net.cn/gsgg_zhaobiao2013.html']


    def parse(self, response):
        meta = {}
        meta['catName'] = '上海广电_公司采购公告'

        linkList = response.xpath("//a[@class='black']/@href").extract()
        if not linkList:
            return None

        link = duplicateUrl(linkList,response.url)

        del linkList

        if not link:
            return None

        for i in link:
            meta['title'] = response.xpath("//*[@href = '{}']/text()".format(i)).extract_first()
            meta['url'] = parse.urljoin(response.url, i)
            yield scrapy.Request(url=meta['url'],callback=self.parseA,meta=meta,dont_filter=True)

        del link


    def parseA(self,response):
        # print('进入文章了')
        meta = response.meta
        dict1 = GgzyItem()


        dict1['content'] = response.xpath("//td[@class='line18']").extract_first()
        if not dict1['content']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 内容')
            print(response.url)
            return None

        try:
            issueTime = re.findall("时间：(\d{2,4}年\d{1,2}月\d{1,2}日)",response.text.replace(' ',''))[0]
            dict1['issueTime'] = timeReMark(time_replace(issueTime, ['年', '月', '日']).strip('-'))

        except:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 时间')
            print(response.url)
            return None

        dict1['title'] = meta['title']
        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['subclass'] = meta['catName']

        del meta
        yield dict1