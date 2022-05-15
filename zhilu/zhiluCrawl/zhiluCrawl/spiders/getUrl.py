# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import pprint
import re,json
import pprint
import requests
from urllib import parse
from zhiluCrawl.items import ZhilucrawlItem
from zhiluCrawl.config import MYSQLINFO
import sqlalchemy

conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(
    USER=MYSQLINFO['USER'], PASSWORD=MYSQLINFO['PASSWORD'], HOST=MYSQLINFO['HOST'], PORT=MYSQLINFO['PORT'],
    DBNAME=MYSQLINFO['DBNAME'])

mysqlcon = sqlalchemy.create_engine(conStr)



class GeturlSpider(scrapy.Spider):
    name = 'getUrl'
    allowed_domains = ['www.xoxo788.com','videodelivery.net','http://av1198.com/']
    start_urls = [{'cat': '精选无码', 'code': '2'}, {'cat': '中文字幕', 'code': '9'}, {'cat': '大奶辣妹', 'code': '10'}, {'cat': '熟女人妻', 'code': '57'}, {'cat': '国产自拍', 'code': '61'}, {'cat': '制服诱惑', 'code': '59'}, {'cat': '强奸乱伦', 'code': '60'}, {'cat': '欧美精品', 'code': '64'}, {'cat': 'AI换脸', 'code': '66'}, {'cat': '经典三级', 'code': '67'}]
    baseUrl = 'http://www.xoxo788.com/video/lists/orderCode/lastTime.html?orderCode=lastTime&tag_id=0&sub_cid=0&cid={}&page={}'

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['cat'] = i['cat']
            meta['code'] = i['code']
            meta['formLink'] = self.baseUrl.format(meta['code'],str(meta['Num']))

            yield scrapy.Request(url=meta['formLink'],callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        linkList = response.xpath("//div[@class='sort-box']/ul[@class='panel']/li[@class='sort-cel']/a/@href").extract()
        pdList = []

        if not linkList:
            return None

        for i in linkList:
            ddict = {}
            ddict['cat'] = meta['cat']
            ddict['url'] = i
            ddict['formLink'] = meta['formLink']
            ddict['pageNum'] = meta['Num']
            pdList.append(ddict)

        DF = pd.DataFrame(pdList)
        print(DF)
        # DF.to_sql(name='zhilu',con=mysqlcon, if_exists='append', index=False, chunksize=1000)




        meta['Num'] += 1
        meta['formLink'] = self.baseUrl.format(meta['code'],str(meta['Num']))
        yield scrapy.Request(url=meta['formLink'], callback=self.parse, meta=meta, dont_filter=True)
