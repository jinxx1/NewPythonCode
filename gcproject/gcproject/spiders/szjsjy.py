# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint,datetime
from urllib import parse
from bs4 import BeautifulSoup
from gcproject.items import GcprojectItem
from gcproject.parseScrpy import get_location,get_timestr
from gcproject.mysqlprecess import get_dupurl


def attmenSTR(downLoad):
    from urllib.parse import unquote
    import requests
    ddict = {}
    ddict['download_url'] = downLoad
    brow = requests.get(url=downLoad)
    ddict['name'] = unquote(brow.headers['Content-Disposition'],'utf-8')
    return ddict


class SzjsjySpider(scrapy.Spider):
    name = 'szjsjy'
    allowed_domains = ['www.szjsjy.com.cn']
    start_urls = [
                    {'subclass': '招标公告', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryGongGaoList.do?rows=10&page={}'},
                    {'subclass': '延期变更公示', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryBGList.do?rows=10&page={}'},
                    {'subclass': '招标控制价公示', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryKongZhiJiaList.do?rows=10&page={}'},
                    {'subclass': '截标信息', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryJBList.do?rows=10&page={}'},
                    {'subclass': '会议信息', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryHYList.do?rows=10&page={}'},
                    {'subclass': '开标情况公示', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryKBJiLuList.do?rows=10&page={}'},
                    {'subclass': '评标委员会公示', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryPWList.do?rows=10&page={}'},
                    {'subclass': '评标报告公示', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryPBJieGuoList.do?rows=10&page={}'},
                    {'subclass': '定标结果公示', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryDBJieGuoList.do?rows=10&page={}'},
                    {'subclass': '中标结果公示', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryZBJieGuoList.do?rows=10&page={}'},
                    {'subclass': '资审及业绩公示', 'baseUrl': 'https://www.szjsjy.com.cn:8001/jyw/queryYeJiList.do?rows=10&page={}'},
                    {'subclass': '合同公示', 'baseUrl': 'http://zjj.sz.gov.cn/jsjy/jyxx/htgs/index.html'}
                  ]

    dupurl = get_dupurl(allowed_domains[0])
    def __init__(self, goon=None, *args, **kwargs):
        super(SzjsjySpider, self).__init__(*args, **kwargs)
        self.goon = goon

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['subclass'] = i['subclass']
            meta['baseUrl'] = i['baseUrl']
            if i['subclass'] == '合同公示':
                yield scrapy.Request(url=meta['baseUrl'],
                                     meta = meta,
                                     callback=self.parse_hetong,
                                     dont_filter=True
                                     )
            else:
                yield scrapy.Request(url=meta['baseUrl'].format(meta['Num']),
                                     meta=meta,
                                     callback=self.parse,
                                     dont_filter=True
                                     )

    def parse(self, response):
        meta = response.meta
        hhtml = response.text.replace('var gongGaoList=','')[:-1]
        jsonT = json.loads(hhtml)
        if len(jsonT['rows']) == 0:
            return None
        mark = 0
        for i in jsonT['rows']:
            if i['detailUrl'] in self.dupurl:
                mark += 1
                continue
            meta['vertItem'] = {}
            meta['vertItem']['subclass'] = meta['subclass']
            meta['vertItem']['site'] = self.allowed_domains[0]
            meta['vertItem']['page_url'] = i['detailUrl']
            meta['vertItem']['title']= i['ggName']
            meta['vertItem']['issue_time'] = get_timestr(i['ggStartTime2'], "%Y-%m-%d %H:%M:%S")
            meta['articleUrl'] = 'https://www.szjsjy.com.cn:8001/jyw/showGongGao.do?ggGuid={}&gcbh=&bdbhs='.format(i['ggGuid'])
            yield scrapy.Request(url=meta['articleUrl'],
                                 meta = meta,
                                 callback=self.parseA,
                                 dont_filter=True
                                 )
            # pprint.pprint(meta['vertItem'])
            # print('--------------------------',meta['Num'])



        if len(jsonT['rows']) < 10:
            return None
        if mark == len(jsonT['rows']) and self.goon == 'no':
            return None
        else:
            meta['Num'] += 1
            yield scrapy.Request(url=meta['baseUrl'].format(meta['Num']),
                                 meta=meta,
                                 callback=self.parse,
                                 dont_filter=True
                                 )

    def parseA(self, response):
        meta = response.meta
        item = GcprojectItem()
        for k in meta['vertItem'].keys():
            item[k] = meta['vertItem'][k]

        jsonT = json.loads(response.text)
        item['content'] = jsonT['html']
        soup = BeautifulSoup(item['content'], 'lxml')
        hrefall = soup.find_all(href=re.compile("downloadFile"))
        item['attchment'] = []
        for nn in hrefall:
            ddict = {}
            ddict['download_url'] = nn.get('href')
            ddict['name'] = response.xpath("//*[@href = '{}']/text()".format(nn.get('href'))).extract_first()
            item['attchment'].append(ddict)

        if not item['attchment']:
            del item['attchment']

        yield item

        # item['content'] = len(item['content'])
        # pprint.pprint(item)
        # print('---------------------------')












    def parse_hetong(self, response):
        meta = response.meta
        item = GcprojectItem()
        item['site'] = self.allowed_domains[0]
        item['subclass'] = meta['subclass']

        links = response.xpath("//div[@class='listcontent_right']/ul[@class='ftdt-list']/li/a/@href").extract()

        for i in links:
            if i in self.dupurl:
                continue
            item['title'] = response.xpath("//*[@href = '{}']/@title".format(i)).extract_first()
            issue_time = response.xpath("//*[@href = '{}']/../span/text()".format(i)).extract_first()
            item['issue_time'] = get_timestr('20'+issue_time, "%Y-%m-%d %H:%M:%S")
            item['content'] = "<p>" + item['title'] + "---合同下载</p>"
            item['page_url'] = i
            item['attchment'] = []
            ddict = {}
            ddict['download_url'] = i
            ddict['name'] = i.split('/')[-1]
            item['attchment'].append(ddict)


            yield item