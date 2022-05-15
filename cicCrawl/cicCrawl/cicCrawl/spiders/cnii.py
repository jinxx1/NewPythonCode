# -*- coding: utf-8 -*-
import scrapy
from cicCrawl.mysql_processing import get_dupurl,get_type
from cicCrawl.scrapyParse import *
from cicCrawl.items import CiccrawlItem
from urllib import parse
from bs4 import BeautifulSoup
import re


class CniiSpider(scrapy.Spider):
    name = 'cnii'
    allowed_domains = ['paper.cnii.com.cn']
    source = '人民邮电报'
    start_urls = ['http://paper.cnii.com.cn/']
    dupurl = get_dupurl(source)


    def parse(self, response):
        meta = {}
        link = response.xpath("//div[@class='text']/ul/li/a/@href").extract()
        print('本期共有文章{}篇'.format(len(link)))
        print(response.url)
        print('---------------------------------------------------------------')
        if not link:
            return None

        for i in link:
            meta['actcleUrl'] = parse.urljoin(response.url, i)
            if meta['actcleUrl'] not in self.dupurl:
                yield scrapy.Request(url=meta['actcleUrl'],
                                     callback=self.parseA,
                                     meta=meta,
                                     dont_filter=True
                                     )

        # lastPage = response.xpath("//span[@class = 'periods']/a[contains(text(),'上一期')]/@href").extract_first()
        # lastPageAll = parse.urljoin(response.url, lastPage)
        # yield scrapy.Request(url=lastPageAll,
        #                      callback=self.parse,
        #                      dont_filter=True)




    def parseA(self,response):
        item = CiccrawlItem()
        item['title'] = response.xpath("//title/text()").extract_first()
        if not item['title']:
            return None

        Html = response.xpath("//div[@class = 'text']").extract()
        if not Html:
            return None
        item['body'] = no_script("".join(Html))

        try:
            item['publishTime'] = re.findall("出版时间：(\d{4}-\d{2}-\d{2})", response.text)[0]
            item['publishTime'] = get_timestr(item['publishTime'],'%Y-%m-%d %H:%M:%S')
            # print(item['publishTime'])
        except:
            return None

        item['url'] = response.url
        item['source'] = self.source
        item['summary'] = get_Summary(item['body'])
        item['programa_dictionaries'] = 1
        item['subtopic_dictionaries'] = 0



        soup = BeautifulSoup(item['body'], 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
            # print('发现头图+++++++++++++++++++++++++++++++')
            # print(item['cover'])
        except:
            item['cover'] = ''


        if not item['cover']:
            return None


        yield item