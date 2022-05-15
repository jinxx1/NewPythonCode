# -*- coding: utf-8 -*-
import scrapy
from cicCrawl.mysql_processing import *
from cicCrawl.scrapyParse import *
from cicCrawl.items import CiccrawlItem
from urllib import parse
from bs4 import BeautifulSoup
import pprint

HEA = {
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"zh-CN,zh;q=0.9,zh-TW;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Host":"jsca.miit.gov.cn",
"If-None-Match":'W/"eb8551-8e6a-2e8f8c00"',
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}


class JscaMiitSpider(scrapy.Spider):
    name = 'jsca_miit'
    allowed_domains = ['jsca.miit.gov.cn/']
    source = '江苏通信管理局'
    base_info = [{'url': 'http://jsca.miit.gov.cn/zxzx/xwdt/hyyw/index_{}.html', 'programa_dictionaries': '行业动态',
                  'subtopic_dictionaries': 0}]
    start_urls = get_type(base_info)
    dupurl = get_dupurl(source)

    def start_requests(self):
        meta = {}
        meta['Num'] = 0
        for i in self.start_urls:
            meta['listurl'] = i['url']
            meta['programa_dictionaries'] = i['programa_dictionaries']
            meta['subtopic_dictionaries'] = i['subtopic_dictionaries']
            yield scrapy.Request(url=meta['listurl'].replace('index_{}','index'),
                                 callback=self.parse,dont_filter=True,meta=meta,
                                 headers=HEA)


    def parse(self,response):
        meta = response.meta
        link = response.xpath("//a[@class='hui']/@href").extract()
        if not link:
            print('no link')
            print(response.url)
            return None

        dupcount = 0
        diffcount = 0
        Artclcount = 0

        for num,i in enumerate(link):
            meta['url'] = parse.urljoin(response.url, i)
            if meta['url'] in self.dupurl:
                dupcount += 1
                continue
            meta['title'] = response.xpath("//*[@href = '{}']/text()".format(i)).extract_first()
            if not meta['title'] or not diff(meta['title']):
                diffcount += 1
                continue
            meta['publishTime'] = get_timestr(response.xpath("//*[@href = '{}']/../../td/text()".format(i)).extract_first(),"%Y-%m-%d %H:%M:%S")
            if not meta['publishTime']:
                continue

            Artclcount += 1
            yield scrapy.Request(url=meta['url'], callback=self.parseB, meta=meta, dont_filter=True,headers=HEA)

        print('\n本页共有{countArt}篇文章。\n被过滤掉文章总数{dupcount},其中{dup}是被去重，{diff}是被关键词过滤掉。\n{Artclcount}篇文章未录入。'.format(
            dupcount=diffcount + dupcount,
            dup=dupcount,
            Artclcount = Artclcount,
            diff = diffcount,
            countArt=len(link))
        )
        print('响应页面地址为：',response.url)
        print('--------------------')
        # meta['Num'] += 1
        # yield scrapy.Request(url=meta['listurl'].format(str(meta['Num'])),
        #                      callback=self.parse, meta=meta, dont_filter=True,
        #                      headers=HEA
        #                      )

    def parseB(self,response):
        meta = response.meta
        item = CiccrawlItem()
        HHtml = response.xpath("//div[@class = 'Custom_UnionStyle']|//td[@class = 'con14']").extract_first()
        item['body'] = no_Html(HHtml)
        if not item['body']:
            print(meta['title'])
            print(response.url)
            print('no HTML')
            return None
        item['title'] = response.xpath("//td[@class = 'un']/text()").extract_first()
        if not item['title']:
            return None
        item['url'] = response.url
        item['publishTime'] = meta['publishTime']
        item['programa_dictionaries'] = meta['programa_dictionaries']
        if isinstance(meta['subtopic_dictionaries'],int):
            item['subtopic_dictionaries'] = meta['subtopic_dictionaries']
        else:
            item['subtopic_dictionaries'] = 0

        item['source'] = self.source
        item['summary'] = get_Summary(item['body'])
        soup = BeautifulSoup(item['body'], 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
        except:
            item['cover'] = ''
        yield item

