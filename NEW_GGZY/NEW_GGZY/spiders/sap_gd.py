# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem


class SapGdSpider(scrapy.Spider):
    name = 'sap_gd'
    allowed_domains = ['www.gcable.com.cn']
    start_url = ['https://www.gcable.com.cn/about-us/purchase/?json=1']

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        meta['catName'] = '广东广电网络_'
        getTXTdict = getTXT(self.name, self.start_url)
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['indexUrl'] = i
            yield scrapy.Request(url=meta['indexUrl'],callback=self.parse,meta=meta,dont_filter=True)


    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)
        linkList = [x['link'] for x in jsonT]
        if not linkList:
            return None

        link = duplicateUrl(linkList,response.url)

        del linkList

        if not link:
            return None

        for i in link:
            for x in  jsonT:
                if i == x['link']:
                    meta['title'] = x['title']
                    meta['issueTime'] = timeReMark(x['post-time'].strip())
                    meta['url'] = x['link']
                    meta['subclass'] = meta['catName'] + x['city'] + '_' + x['type'] + '_' + x['cate']
                    yield scrapy.Request(url=x['link'],callback=self.parseA,meta=meta,dont_filter=True)
        del link

    def parseA(self,response):
        # print('进入文章了')
        meta = response.meta
        dict1 = GgzyItem()
        dict1['content'] = response.xpath("//div[@class='xwzx']/div[@class='content clearfix']/div[@class='news-desc']").extract_first()
        if not dict1['content']:
            print('没有 》》》》》》》》》》》》》》》》》》》》》》 内容')
            print(response.url)
            return None


        attachLink = response.xpath("//div[@class='xwzx']/div[@class='content clearfix']/div[@class='news-desc']/div[@class='attachment']/div[@class='download-link']/a/@href").extract()
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

        dict1['title'] = meta['title']
        dict1['issueTime'] = meta['issueTime']
        dict1['url'] = meta['url']
        dict1['subclass'] = meta['subclass']
        dict1['site'] = self.allowed_domains[0]

        del meta

        yield dict1