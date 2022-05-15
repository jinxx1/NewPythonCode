# -*- coding: utf-8 -*-
import scrapy
from cicCrawl.mysql_processing import get_dupurl,get_type
from cicCrawl.scrapyParse import *
from cicCrawl.items import CiccrawlItem
from urllib import parse
from bs4 import BeautifulSoup
import pprint
import json,time

class GdcaMiitSpider(scrapy.Spider):
    name = 'gdca_miit'
    allowed_domains = ['gdca.miit.gov.cn']
    start_urls = ['https://gdca.miit.gov.cn/gdcmsnet/gdcms/content/getContentList']
    source = '广东通信管理局'
    dupurl = get_dupurl(source)
    def start_requests(self):
        meta = {}
        meta['programa_dictionaries'] = 1
        meta['subtopic_dictionaries'] = 0
        formDate = {'catogoryId':'54'}
        for i in self.start_urls:
            yield scrapy.FormRequest(url=i,
                                     formdata=formDate,
                                     meta=meta,
                                     callback=self.parse,
                                     dont_filter=True)


    def parse(self, response):

        meta = response.meta
        jsonT = json.loads(response.text)['data']['optData']['data']
        dupcount = 0
        diffcount = 0
        Artclcount = 0
        for i in jsonT:
            meta['url'] = parse.urljoin(response.url, i['address']).replace('gdcms','gdcmsnet/gdcms')
            if meta['url'] in self.dupurl:
                dupcount += 1
                continue
            meta['title'] = i['title']
            if not diff(meta['title']):
                diffcount += 1
                continue
            meta['publishTime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(i['publicTime']//1000))
            Artclcount += 1
            yield scrapy.Request(url=meta['url'],callback=self.parseA,dont_filter=True,meta=meta)

        print('被过滤掉文章总数{dupcount},其中{dup}是被去重，{diff}是被关键词过滤掉。本页共有{countArt}篇文章'.format(
                dupcount = diffcount+dupcount,
                dup = dupcount,
                diff = diffcount,
                countArt = len(jsonT))
        )

    def parseA(self,response):
        item = CiccrawlItem()
        meta = response.meta
        Html = response.xpath("//div[@id='page-content-mainText']").extract()

        # item['body'] = no_script("".join(Html))
        item['body'] = no_Html("".join(Html))
        if not item['body']:
            print(meta['title'])
            print('no HTML')
            return None

        item['url'] = response.url
        item['title'] = meta['title']
        item['publishTime'] = meta['publishTime']
        item['programa_dictionaries'] = meta['programa_dictionaries']
        if isinstance(meta['subtopic_dictionaries'], int):
            item['subtopic_dictionaries'] = meta['subtopic_dictionaries']
        else:
            item['subtopic_dictionaries'] = 0
        item['source'] = self.source
        item['summary'] = get_Summary(item['body'])

        # item['body'] = item['body'].replace('data-src','dddsss')
        # item['body'] = item['body'].replace('src','nonononono')
        # item['body'] = item['body'].replace('dddsss','src')

        soup = BeautifulSoup(item['body'], 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
        except:
            item['cover'] = ''

        yield item


