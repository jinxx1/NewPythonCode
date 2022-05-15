# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib

from urllib import parse
from NEW_GGZY.Breakpoint import *

from NEW_GGZY.items import GgzyItem


class SapGdzjSpider(scrapy.Spider):
    name = 'sap_gdzj'
    allowed_domains = ['www.sapprft.gov.cn']
    start_url = ['http://www.sapprft.gov.cn/sapprft/govpublic/6669_{}.shtml']

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        meta['catName'] = '广电总局_政府采购'
        getTXTdict = getTXT(self.name, self.start_url)
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['indexUrl'] = i
            url = meta['indexUrl'].replace('_{}','')
            yield scrapy.Request(url=url,callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        linkList = response.xpath("//a[@class='extLink']/@href").extract()
        if not linkList:
            return None
        link = duplicateUrl(linkList,response.url)
        del linkList
        if not link:
            return None


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
        dict1['title'] = response.xpath("//p[@class='title']/text()").extract_first().strip()
        if not dict1['title']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 标题')
            print(response.url)
            return None

        dict1['content'] = response.xpath("//div[@class='kk content'][2]/div[@id='con']").extract_first()
        if not dict1['content']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 内容')
            print(response.url)
            return None

        issueTime = response.xpath("//div[@class='kk content'][1]/p[@class='info botLine']/span[1]/text()").extract_first()
        dict1['issueTime'] = timeReMark(time_replace(issueTime,['年','月','日']).strip('-'))
        if not dict1['issueTime']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 时间')
            print(response.url)
            return None



        attachLink = response.xpath("//div[@class='rightgov']/div[@class='kk content'][2]/div[@id='con']/p/a/@href").extract()
        if attachLink:
            attachmentListJsonList = []
            for i in attachLink:
                att_dict = {}
                att_dict['downloadUrl'] = parse.urljoin(response.url, i)
                attname = response.xpath("//*[@href = '{}']/text()".format(i)).extract()
                att_dict['name'] = ''.join(attname)
                attachmentListJsonList.append(att_dict)
            dict1['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)
            del attachmentListJsonList

        del attachLink

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['subclass'] = meta['catName']

        del meta

        yield dict1