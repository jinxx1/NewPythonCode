# -*- coding: utf-8 -*-
import scrapy
import pprint
import pandas as pd
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





class ZhiluSpider(scrapy.Spider):
    name = 'zhilu'
    allowed_domains = ['www.xoxo788.com','videodelivery.net','http://av1198.com/']

    a = mysqlcon.execute("select id,url from zhilu where title is null and artCode is null")
    start_urls = [{'id': i[0], 'url': i[1]} for i in a]

    HEA = {
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',

    }


    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['mysqlid'] = i['id']
            meta['url'] = i['url']

            meta['urlID'] = re.findall("id/(.*?)\.html", meta['url'])[0]
            artBaseUrl = 'http://www.xoxo788.com/api/payvideo.html'
            postDate = {'id': meta['urlID']}
            yield scrapy.FormRequest(url=artBaseUrl,formdata=postDate,callback=self.parseA,meta=meta,dont_filter=True,headers=self.HEA)

    def parseA(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)['data']['videoInfo']
        if not jsonT:
            return None

        meta['imgUrl'] = jsonT['thumbnail']
        meta['title'] = jsonT['title']
        meta['artID'] = jsonT['url'].replace('?sign=','')

        url = 'https://videodelivery.net/{}/manifest/video.m3u8'.format(meta['artID'])

        yield scrapy.Request(url=url,callback=self.parseM3u8,meta=meta,dont_filter=True)

    def parseM3u8(self,response):
        meta = response.meta

        listA = re.findall("stream_\d{1}", response.text)
        listB = ['stream_0', 'stream_1', 'stream_2', 'stream_3', 'stream_4', 'stream_5']

        meta['videoInfo'] = {
            'p128': 'stream_0',
            'p240': 'stream_1',
            'p360': 'stream_2',
            'p480': 'stream_3',
            'p720': 'stream_4',
            'p1080':'stream_5',

        }

        a1 = list(set(listB).difference(set(listA)))
        if a1:
            for nn in a1:
                keys = list(meta['videoInfo'].keys())[list(meta['videoInfo'].values()).index(nn)]
                del meta['videoInfo'][keys]

        for keyWords in meta['videoInfo'].keys():
            pUrl = 'https://videodelivery.net/{urlID}/manifest/{stream}.m3u8'.format(urlID = meta['artID'],stream = meta['videoInfo'][keyWords])
            try:
                acd = requests.get(url=pUrl,timeout=10)
            except:
                continue

            if acd.status_code == 200:
                listA = re.findall("seg_(\d{1,4})\.ts", acd.text)
                meta['videoInfo']['pageAll'] = len(listA)
                break
            else:
                meta['videoInfo']['pageAll'] = 0
                continue

        if meta['videoInfo']['pageAll'] == 0:
            return None
        # jsonVideoInfo = json.dumps(meta['videoInfo'])

        mysqlWord = "UPDATE zhilu SET title = '{title}',videoInfo = '{videoInfo}',imgUrl = '{imgUrl}',artCode = '{artCode}' WHERE id = '{mysqlID}'"
        execWord = mysqlWord.format(title = str(meta['title']),videoInfo = json.dumps(meta['videoInfo']),imgUrl = meta['imgUrl'],artCode = meta['artID'],mysqlID = meta['mysqlid'])

        mysqlcon.execute(execWord)


        # print(meta['title'])
        # print(meta['imgUrl'])
        # print(meta['url'])
        #
        # print(meta['artID'])
        # pprint.pprint(meta['videoInfo'])



        print('---------------------------------------------------------------------------')



