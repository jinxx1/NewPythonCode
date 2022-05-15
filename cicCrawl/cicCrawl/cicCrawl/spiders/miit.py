# -*- coding: utf-8 -*-
import scrapy
from cicCrawl.mysql_processing import *
from cicCrawl.scrapyParse import *
from cicCrawl.items import CiccrawlItem
from urllib import parse
from bs4 import BeautifulSoup
import pprint



class MiitSpider(scrapy.Spider):
    name = 'miit'
    source = '人民邮电报'
    allowed_domains = ['www.miit.gov.cn']

    base_info = [{'url': 'http://www.miit.gov.cn/n1146290/n1146392/index.html', 'programa_dictionaries': '行业动态', 'subtopic_dictionaries': 0}]

    start_urls = get_type(base_info)
    dupurl = get_dupurl(source)
    def start_requests(self):
        meta = {}
        for i in self.start_urls:
            meta['programa_dictionaries'] = i['programa_dictionaries']
            meta['subtopic_dictionaries'] = i['subtopic_dictionaries']
            yield scrapy.Request(url=i['url'],callback=self.parse,dont_filter=True,meta=meta)


    def parse(self,response):
        meta = response.meta
        link = response.xpath("//div[@class='clist_con']/ul/li/span/a/@href").extract()
        if not link:
            return None
        dupcount = 0
        diffcount = 0
        Artclcount = 0
        for num,i in enumerate(link):

            meta['url'] = parse.urljoin(response.url, i)
            if meta['url'] in self.dupurl:
                dupcount +=1
                continue
            meta['title'] = response.xpath("//a[@href = '{}']/text()".format(i)).extract_first()
            if not meta['title'] or not diff(meta['title']):
                diffcount +=1

                continue
            meta['publishTime'] = get_timestr(response.xpath("//span/a[@href = '{}']/text()".format(i)).extract_first(),"%Y-%m-%d %H:%M:%S")
            if not meta['publishTime']:
                continue
            print('符合文章--------')
            Artclcount +=1
            yield scrapy.Request(url=meta['url'], callback=self.parseB, meta=meta, dont_filter=True)

        print('被过滤掉文章总数{dupcount},其中{dup}是被去重，{diff}是被关键词过滤掉。本页共有{countArt}篇文章'.format(
            dupcount=diffcount + dupcount,
            dup=dupcount,
            diff=diffcount,
            countArt=num)
        )



        # temp_listLink = response.xpath("//div[@style = 'display:none']/a/@href").extract()
        # listLink = [parse.urljoin(response.url, i) for i in temp_listLink if i]
        # for i in reversed(listLink):
        #     yield scrapy.Request(url=i, callback=self.parse, meta=meta, dont_filter=True)

    def parseB(self, response):
        meta = response.meta
        item = CiccrawlItem()
        item['title'] = response.xpath("//h1[@id='con_title']/text()|//title/text()").extract_first()
        if not item['title']:
            return None
        print(item['title'])
        print(response.url)
        print('--------------------------------------')
        brow = response.xpath("//div[@id='con_con']").extract_first()

        # item['body'] = no_script(brow)
        item['body'] = no_Html(brow)
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