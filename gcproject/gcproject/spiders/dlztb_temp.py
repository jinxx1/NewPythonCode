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
import sqlalchemy
import pandas as pd

from urllib.parse import quote_plus
MYSQLINFO = {
    "HOST": "172.16.10.99",
    "DBNAME": "shangqing",
    "USER": "xey",
    "PASSWORD": quote_plus("Xey123456!@#$%^"),
    "PORT":3306
}

conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
                                                                                               'DBNAME'])

mysqlcon = sqlalchemy.create_engine(conStr)

def getmysqlInfo():
    exc = "select page_url from ztbRawInfo_copy1;"
    a = mysqlcon.execute(exc)
    return [x[0] for x in a]



class DlztbSpider(scrapy.Spider):
    name = 'dlztb_temp'
    allowed_domains = ['www.dlztb.com']
    site = '中国电力招标采购网'
    start_urls = [
# {'subclass': '设备中标', 'baseUrl': 'http://www.dlztb.com/zbgg/157_{}.html','allpage':129},
# {'subclass': '工程中标', 'baseUrl': 'http://www.dlztb.com/zbgg/158_{}.html','allpage':1157},#932
{'subclass': 'VIP项目', 'baseUrl': 'http://www.dlztb.com/xmxx/xiangmu/{}.html','allpage':1772},#400
# {'subclass': '拟在建项目', 'baseUrl': 'http://www.dlztb.com/xmxx/nizaijian/{}.html','allpage':1308},
# {'subclass': '独家项目', 'baseUrl': 'http://www.dlztb.com/xmxx/dujiaxiangmu/{}.html','allpage':60}
    ]
    tempUrl = getmysqlInfo()
    def __init__(self, goon=None, *args, **kwargs):
        super(DlztbSpider, self).__init__(*args, **kwargs)
        self.goon = goon

    def start_requests(self):
        meta = {}
        meta['Num'] = 1101
        meta['handle_httpstatus_all'] = True

        for i in self.start_urls:
            meta['baseUrl'] = i['baseUrl']
            meta['subclass'] = i['subclass']
            meta['allpage'] = i['allpage']
            yield scrapy.Request(
                url=meta['baseUrl'].format(str(meta['Num'])),
                callback=self.only_list,
                meta=meta,dont_filter=True)

    def only_list(self,response):
        meta = response.meta
        if response.status in [404,403,402,500]:
            print('=================404错误了啊===============')
            meta['Num'] += 1
            if meta['Num'] > meta['allpage']:
                return None
            else:
                yield scrapy.Request(url=meta['baseUrl'].format(str(meta['Num'])),
                                     callback=self.only_list,
                                     meta=meta,
                                     dont_filter=True
                                     )


        link = response.xpath("//div[@class ='catlist']/ul/li/a/@href").extract()
        print('《{}》-----{}页，共有{}篇文章,'.format(meta['subclass'],meta['Num'],len(link)))
        if not link:
            return None
        llist = []
        for i in link:
            url = parse.urljoin(response.url, i)
            if url in self.tempUrl:
                continue
            self.tempUrl.append(url)
            item = {}
            item['subclass'] = meta['subclass']
            item['page_url'] = url

            item['title'] = response.xpath("//*[@href='{}']/@title".format(i)).extract_first()
            if not item['title']:
                continue
            issue_time = response.xpath("//*[@href='{}']/../i/text()".format(i)).extract_first()
            if not issue_time:
                continue
            item['issue_time'] = get_timestr(issue_time, "%Y-%m-%d %H:%M:%S")
            item['site'] = self.allowed_domains[0]
            llist.append(item)
        df = pd.DataFrame(llist)
        print('《{}》-----{}页，入库{},'.format(meta['subclass'], meta['Num'], len(llist)))
        df.to_sql(name='ztbRawInfo_copy1', con=mysqlcon, if_exists='append', index=False)
        with open('pageNum.txt','w') as f:
            f.write(str(meta['Num']))
            f.flush()
            f.close()

        if self.goon == 'no':
            return None
        else:
            meta['Num'] += 1
            if meta['Num'] > meta['allpage']:
                return None
            else:
                yield scrapy.Request(url=meta['baseUrl'].format(str(meta['Num'])),
                                     callback=self.only_list,
                                     meta=meta,
                                     dont_filter=True
                                     )