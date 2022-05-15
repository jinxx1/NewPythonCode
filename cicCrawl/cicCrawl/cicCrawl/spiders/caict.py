# -*- coding: utf-8 -*-
import scrapy
from cicCrawl.mysql_processing import *
from cicCrawl.scrapyParse import *
from cicCrawl.items import CiccrawlItem
from urllib import parse

import emoji,io
from bs4 import BeautifulSoup
import pprint


class CaictSpider(scrapy.Spider):
    name = 'caict'
    allowed_domains = ['caict.ac.cn']
    source = '中国信通院'
    base_info = [{'url': 'http://www.caict.ac.cn/xwdt/hyxw/index_{}.htm', 'programa_dictionaries': '行业动态',
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
                                 )

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//a[@class='main_t_list']/@href").extract()
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
            meta['title'] = response.xpath("//*[@href = '{}']/@title".format(i)).extract_first()
            if not meta['title'] or not diff(meta['title']):
                diffcount += 1
                continue
            puTime = response.xpath("//*[@href = '{}']/../../td/text()".format(i)).extract()
            puTime = ''.join(puTime).strip()
            meta['publishTime'] = get_timestr(puTime,"%Y-%m-%d %H:%M:%S")
            if not meta['publishTime']:
                continue

            Artclcount += 1
            yield scrapy.Request(url=meta['url'], callback=self.parseB, meta=meta, dont_filter=True)

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
        #                      )

    def parseB(self,response):
        item = CiccrawlItem()
        meta = response.meta
        if 'weixin' in response.url:
            item['body'] = response.xpath("//div[@class = 'rich_media_content ']|//div[@id = 'js_content']").extract_first()
            item['body'] = item['body'].replace('visibility: hidden;','')
            if not item['body']:
                return None
            item['body'] = emoji.demojize(item['body'])
            item['cover'] = response.xpath("//meta[@property = 'og:image']/@content").extract_first()
            item['summary'] = response.xpath("//meta[@name = 'description']/@content").extract_first().replace(r'\x0a','').replace(r'\x26','')

        if 'caict.ac.cn' in response.url:
            item['body'] = response.xpath("//div[@class = 'Custom_UnionStyle']").extract_first()
            if not item['body']:
                return None
            item['body'] = no_Html(item['body'])
            item['summary'] = get_Summary(item['body'])
            soup = BeautifulSoup(item['body'], 'lxml')
            try:
                imgSrc = soup.img.get('src')
                item['cover'] = parse.urljoin(response.url, imgSrc)
            except:
                item['cover'] = ''


        item['url'] = response.url
        item['title'] = meta['title']
        item['publishTime'] = meta['publishTime']
        item['programa_dictionaries'] = meta['programa_dictionaries']
        if isinstance(meta['subtopic_dictionaries'],int):
            item['subtopic_dictionaries'] = meta['subtopic_dictionaries']
        else:
            item['subtopic_dictionaries'] = 0
        item['source'] = self.source

        yield item

