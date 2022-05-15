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

header_raw = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Cache-Control: max-age=0
Host: www.szzfcg.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


def attmenSTR(downLoad):
    from urllib.parse import unquote
    import requests
    ddict = {}
    ddict['download_url'] = downLoad
    brow = requests.get(url=downLoad)
    try:
        soureAttachment = re.findall('''attachment; filename=\"(.*?)\"''',brow.headers['Content-Disposition'])[0]
    except:
        return None
    ddict['name'] = unquote(soureAttachment,'utf-8')
    return ddict

allNum = 100

class SzzfcgSpider(scrapy.Spider):
    name = 'szzfcg'
    allowed_domains = ['www.szzfcg.cn']
    baseUrl = '&ec_i=topicChrList_20070702&topicChrList_20070702_crd={allNum}&topicChrList_20070702_p={Num}'
    start_urls =[
                {'subclass': '采购需求公示', 'baseUrl': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=2719966'},
                {'subclass': '采购公告', 'baseUrl': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660'},
                {'subclass': '采购公告', 'baseUrl': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=10001'},
                {'subclass': '采购公告', 'baseUrl': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660&agencyType=1'},
                {'subclass': '采购公告', 'baseUrl': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=1660&agencyType=2'},
                {'subclass': '采购公告', 'baseUrl': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=201902'},
                {'subclass': '采购公告', 'baseUrl': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=201901'},
                {'subclass': '采购结果公示', 'baseUrl': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=2014'},
                {'subclass': '采购结果公示', 'baseUrl': 'http://www.szzfcg.cn/portal/topicView.do?method=view&id=10002'}
                 ]
    dupurl = get_dupurl(allowed_domains[0])
    def __init__(self, goon=None, *args, **kwargs):
        super(SzzfcgSpider, self).__init__(*args, **kwargs)
        self.goon = goon
    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['vertItem'] = {}
            meta['vertItem']['subclass'] = i['subclass']
            meta['baseUrl'] = i['baseUrl'] + self.baseUrl
            yield scrapy.Request(url=meta['baseUrl'].format(allNum=allNum,Num=meta['Num']),
                                 callback=self.parse,
                                 meta=meta,
                                 dont_filter=True,
                                 headers=HEA)
    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='eXtremeTable']//tbody/tr/td[3]/a/@href").extract()
        if not link:
            return None
        mark = 0
        for i in link:
            try:
                regx = re.findall("id=(.*)", i)[0]
                url = 'http://www.szzfcg.cn/portal/documentView.do?method=view&id=' + regx
            except:
                continue
            if url in self.dupurl:
                mark += 1
                continue
            meta['vertItem']['title'] = response.xpath("///*[@href = '{}']/text()".format(i)).extract_first().strip()
            if not meta['vertItem']['title']:
                continue
            issue_time = response.xpath("//*[@href='{}']/../../td[5]/text()".format(i)).extract_first().strip()
            if not issue_time:
                continue
            meta['vertItem']['issue_time'] = get_timestr(issue_time,"%Y-%m-%d %H:%M:%S")
            business_type = response.xpath("//*[@href = '{}']/../../td[4]/text()".format(i)).extract_first().strip()
            if business_type:
                meta['vertItem']['business_type'] = business_type

            meta['vertItem']['site'] = self.allowed_domains[0]

            yield scrapy.Request(url=url,
                                 callback=self.parseA,
                                 meta=meta,
                                 dont_filter=True,
                                 headers=HEA
                                 )

        if len(link) < 100:
            return None
        if mark == len(link) and self.goon == 'no':
            return None
        else:
            meta['Num'] += 1
            yield scrapy.Request(url=meta['baseUrl'].format(allNum=allNum,Num=meta['Num']),
                                 callback=self.parse,
                                 meta=meta,
                                 dont_filter=True,
                                 headers=HEA)

    def parseA(self,response):
        meta = response.meta
        item = GcprojectItem()
        for k in meta['vertItem'].keys():
            item[k] = meta['vertItem'][k]
        item['content'] = response.xpath("//table").extract_first()
        item['page_url'] = response.url
        if not item['content']:
            return None
        soup = BeautifulSoup(item['content'], 'lxml')
        hrefall = soup.find_all(href=re.compile("fileDown"))
        if hrefall:
            item['attchment'] = []
            for i in hrefall:
                downloadurl = i.get('href')
                item['attchment'].append(attmenSTR(downloadurl))

        yield item
