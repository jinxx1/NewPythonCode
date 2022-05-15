# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint
from urllib import parse
from bs4 import BeautifulSoup
from gcproject.items import GcprojectItem
from gcproject.parseScrpy import get_location,get_timestr
from gcproject.mysqlprecess import get_dupurl


class GdebiddingSpider(scrapy.Spider):
    name = 'gdebidding'
    site = '广东省机电设备招标中心有限公司'
    allowed_domains = ['www.gdebidding.com']
    dupurl = get_dupurl(allowed_domains[0])
    start_urls = [
                {'catName': '招标信息公告', 'baseurl': 'https://www.gdebidding.com/zbxxgg/index_{}.jhtml'},
                {'catName': '电子招投标信息', 'baseurl': 'https://www.gdebidding.com/dzzbtbxx/index_{}.jhtml'},
                # {'catName': '电子采购信息', 'baseurl': 'https://www.gdebidding.com/cgxx/index_{}.jhtml.jhtml'},
                {'catName': '澄清更正公告', 'baseurl': 'https://www.gdebidding.com/cqgzgg/index_{}.jhtml'},
                {'catName': '招标结果公告', 'baseurl': 'https://www.gdebidding.com/zbjggg/index_{}.jhtml'},
                {'catName': '招标结果公示', 'baseurl': 'https://www.gdebidding.com/zbjggs/index_{}.jhtml'},
                {'catName': '招标信息预告', 'baseurl': 'https://www.gdebidding.com/zbyg/index_{}.jhtml'}
                  ]

    def __init__(self, goon=None, *args, **kwargs):
        super(GdebiddingSpider, self).__init__(*args, **kwargs)
        self.goon = goon

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['catName'] = i['catName']
            meta['baseurl'] = i['baseurl']
            yield scrapy.Request(
                url=meta['baseurl'].format('index_{}.jhtml','index.jhtml'),
                callback=self.parse,
                meta=meta,
                dont_filter=True
            )

    def parse(self, response):
        meta = response.meta
        xpath_str = "//div[@class='container']/div[@class='line-big']/div[@class='xs9 xm9']/div[@class='padding-big']/div/a/@href"
        link = response.xpath(xpath_str).extract()
        if not link:
            return None
        mark = 0
        for i in link:
            url = parse.urljoin(response.url,i)
            if url in self.dupurl:
                mark+=1
                continue
            meta['speceUrl'] = url
            Time = response.xpath("//*[@href='{}']/../span/text()".format(i)).extract_first()
            meta['issue_time'] = get_timestr(Time,"%Y-%m-%d %H:%M:%S")
            if not meta['issue_time']:
                continue
            if meta['catName'] == "电子采购信息":
                artilebaseUrl = 'https://eps.gdebidding.com/gdjd-xunjia/gonggaoxinxi/jieGuo_view.html?guid={}&callBackUrl=https://eps.gdebidding.com/html/crossDomainForFeiZhaoBiao.html'
                try:
                    regx = re.findall("guid=(.*?)&&", meta['speceUrl'])[0]
                except:
                    print('except')
                    continue
                yield scrapy.Request(url=artilebaseUrl.format(regx),
                                     callback=self.parseB,
                                     meta=meta,
                                     dont_filter=True
                                     )
            else:
                yield scrapy.Request(url=url,
                                 callback=self.parseA,
                                 meta=meta,
                                 dont_filter=True
                                 )
                # break


        # 翻页
        if mark == len(link) and self.goon == 'no':
            return None
        else:
            meta['Num'] += 1
            yield scrapy.Request(
                url=meta['baseurl'].format(meta['Num']),
                callback=self.parse,
                meta=meta,
                dont_filter=True
            )

    def parseA(self, response):
        meta = response.meta
        item = GcprojectItem()
        item['title'] = response.xpath("//h1/text()").extract_first()
        if not item['title']:
            return None
        item['content'] = response.xpath('//p').extract()
        item['content'] = ''.join(item['content'])
        if not item['content']:
            return None


        item['issue_time'] = meta['issue_time']
        item['page_url'] = response.url
        item['site'] = self.allowed_domains[0]
        item['subclass'] = meta['catName']
        # print('----------------------------------',meta['Num'])
        yield item

    def parseB(self, response):
        meta = response.meta
        item = GcprojectItem()
        print(response.text)
        print('--------------------------------------------------------------')
        return None


        item['title'] = response.xpath("//h1/text()").extract_first()
        if not item['title']:
            return None
        item['content'] = response.xpath('//p').extract()
        item['content'] = ''.join(item['content'])
        if not item['content']:
            return None


        item['issue_time'] = meta['issue_time']
        item['page_url'] = response.url
        item['site'] = self.allowed_domains[0]
        item['subclass'] = meta['catName']

        item['content'] = len(item['content'])
        import pprint
        pprint.pprint(item)
        print('----------------------------------',meta['Num'])

'''


subclass = scrapy.Field()  # 子类型
site = scrapy.Field()  # 来源站点,域名
page_url = scrapy.Field()  # 链接地址
title = scrapy.Field()  # 标题
issue_time = scrapy.Field()  # 发布时间

content = scrapy.Field()#公告内容

download_url = scrapy.Field()#原始网站的附件下载地址
name = scrapy.Field()#文件对应的名称,如文件名为123.xls,name为广州招标
'''


