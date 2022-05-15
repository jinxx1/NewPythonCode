# -*- coding: utf-8 -*-
import scrapy

import sys, re, os, json, pprint, chardet, cchardet, time, datetime, lxml, requests
import lxml.html
from lxml.html import HtmlComment
from lxml import etree
from lxml import html as htmlstr
from shangQing.items import ShangqingItem, ShangqingHubItem, ShangqingArticleItem
from requests.adapters import HTTPAdapter
from urllib import parse as urlpase
from bs4 import BeautifulSoup
import platform

sys_code = platform.system()
if sys_code == 'Windows':
    sys.path.append(r"D:\PythonCode\mypythonpath")
from mkdir import mkdir
from redisBloomHash import bl, bh
from getmysqlInfo import jsonInfo
from crawltools import *
from reqSession import *
from uxue_orm import *

hub_HeadersWord = '''Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Content-Type: application/json;charset=utf-8
Cookie: JSESSIONID=75899EBAFAC946064C88E2A02F644C56
Host: www.ccgp-shaanxi.gov.cn
Referer: http://www.ccgp-shaanxi.gov.cn/freecms/site/shanxi/xxgg/index.html?xxggType=123&noticeType=00101
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36
X-Requested-With: XMLHttpRequest'''


def get_urlList():
    wword = '''采购公告	00101
中标(成交)公告	00102
更正公告	001003,001031,001032
废标(终止)公告	001004,001006
其他公告	001052,001053,001055,001056,001057,001058,001059
单一来源公示	001051
验收结果公告	001009
合同公告	001054
采购意向公开	59'''.split('\n')
    llist = []
    for i in wword:
        cut = i.split('\t')
        ddict = {}
        ddict['catName'] = cut[0]
        ddict['code'] = cut[1]
        llist.append(ddict)
    return llist


class XizangCcgpSpider(scrapy.Spider):
    name = 'xizang_ccgp'
    allowed_domains = ['www.ccgp-xizang.gov.cn']
    urlList = [{'catName': '采购公告', 'code': '00101'},
               {'catName': '中标(成交)公告', 'code': '00102'},
               {'catName': '更正公告', 'code': '001003,001031,001032'},
               {'catName': '废标(终止)公告', 'code': '001004,001006'},
               {'catName': '其他公告', 'code': '001052,001053,001055,001056,001057,001058,001059'},
               {'catName': '单一来源公示', 'code': '001051'},
               {'catName': '验收结果公告', 'code': '001009'},
               {'catName': '合同公告', 'code': '001054'},
               {'catName': '采购意向公开', 'code': '59'}]
    baseUrl = "http://www.ccgp-xizang.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=18de62f0-2fb0-4187-a6c1-cd8fcbfb4585&channel=b541ffff-03ee-4160-be64-b11ccf79660d&currPage={pageNum}&pageSize={pageS}&noticeType={catNameCode}&cityOrArea=&noticeName=&operationStartTime={startTime}&operationEndTime={endTime}&selectTimeName=noticeTime"

    def __init__(self, goon=None, startTime=None, endTime=None, *args, **kwargs):
        super(XizangCcgpSpider, self).__init__(*args, **kwargs)
        self.pageS = 100
        self.goon = goon
        self.timeoutformat = "%Y-%m-%d %H:%M:%S"
        if goon == 'hub':
            if not startTime and not endTime:
                self.startT = get_timestr(str(datetime.date.today()), outformat=self.timeoutformat)
                self.endT = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            elif startTime and not endTime:
                print('have startTime and not endTime')

                self.startT = get_timestr(startTime, outformat=self.timeoutformat)
                self.endT = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            elif startTime and endTime:
                a = datetime.datetime.now() + datetime.timedelta(days=-1)
                self.startT = get_timestr(startTime, outformat=self.timeoutformat)
                self.endT = get_timestr(endTime, outformat=self.timeoutformat).replace("00:00:00", "23:59:59")
            else:
                raise 'startTime or endTime INPUT ERROR'

        if goon != 'article' and goon != 'hub':
            raise 'pls input goon = hub  or  article'

    def start_requests(self):
        meta = {}
        meta['breakMark'] = 0
        meta['pageNum'] = 1
        if self.goon == 'hub':
            for num, i in enumerate(self.urlList):
                # if num >0:
                #     continue

                meta['subclass'] = i['catName']
                meta['subclass_code'] = i['code']
                apiurl = self.baseUrl.format(
                    pageS=self.pageS,
                    pageNum=meta['pageNum'],
                    catNameCode=meta['subclass_code'],
                    startTime=self.startT,
                    endTime=self.endT)

                yield scrapy.Request(url=apiurl,
                                     callback=self.parse_hub,
                                     meta=meta,
                                     dont_filter=True,
                                     headers=creatHeader(hub_HeadersWord)
                                     )

        # 抓取ARTICLE页
        if self.goon == 'article':
            self.mysession = mysql_orm()
            urlList = self.mysession.get_ztbhubinfo(self.allowed_domains[0])
            # print('======================================',len(urlList))
            for num, i in enumerate(urlList):
                # if num >0:
                #     continue
                if bl.exists(i.page_url):
                    self.mysession.update_ztbHubInfo(update_dict={"craw_status": 1}, hubInfo_id=i.id)
                    continue
                meta['page_url'] = i.page_url
                meta['hubinfo'] = i

                yield scrapy.Request(url=meta['page_url'],
                                     callback=self.parse_article,
                                     meta=meta,
                                     dont_filter=True,
                                     headers=creatHeader(hub_HeadersWord)
                                     )

    def parse_hub(self, response):

        meta = response.meta
        jsonT = json.loads(response.text)

        print(meta['subclass'], self.startT)
        print(response.url)
        print('本页共有 ----------------------------', jsonT['total'])
        if jsonT['total'] == 0:
            return None
        allpage = get_pagecount(articlecount=jsonT['total'], pageS=self.pageS)

        mark = 0
        for num, pageInfo in enumerate(jsonT['data']):
            try:
                page_url = urlpase.urljoin(base="http://www.ccgp-xizang.gov.cn/", url=pageInfo['pageurl'])
            except:
                print('not get url')
                continue

            if bl.exists(page_url) or bh.exists(page_url):
                mark += 1
                print('exists')
                continue

            info_dict = ShangqingHubItem()
            info_dict['site'] = self.allowed_domains[0]
            info_dict['purchase_type'] = meta['subclass']
            info_dict['subclass'] = meta['subclass']
            info_dict['page_url'] = page_url

            try:
                # 标题
                info_dict['title'] = pageInfo['title']
                # 发布时间
                info_dict['issue_time'] = pageInfo['addtimeStr']
            except:
                continue

            province_name_dict = tureLocation(localName='西藏', title=info_dict['title'])
            info_dict['province_name'] = province_name_dict['province_name']
            if province_name_dict['city_name']:
                info_dict['city_name'] = province_name_dict['city_name']
                if len(province_name_dict['city_name']) <= 2:
                    info_dict['city_name'] = ''
            else:
                info_dict['city_name'] = ''

            # pprint.pprint(info_dict)
            # print('----------------------------------')

            yield info_dict

        if mark == len(jsonT['data']):
            meta['breakMark'] += 1
            print("breakMark += 1", meta['breakMark'])
        else:
            meta['breakMark'] = 0

        if meta['breakMark'] == 3:
            return None

        if meta['pageNum'] >= allpage:
            return None

        meta['pageNum'] += 1
        apiurl = self.baseUrl.format(
            pageS=self.pageS,
            pageNum=meta['pageNum'],
            catNameCode=meta['subclass_code'],
            startTime=self.startT,
            endTime=self.endT)

        yield scrapy.Request(url=apiurl,
                             callback=self.parse_hub,
                             meta=meta,
                             dont_filter=True,
                             headers=creatHeader(hub_HeadersWord)
                             )

    def parse_article(self, response):
        meta = response.meta

        if response.status == 404:
            print('ERROR 404')
            self.mysession.update_ztbHubInfo(update_dict={"craw_status": 2}, hubInfo_id=meta['hubinfo'].id)
            return None

        articleInfo = ShangqingArticleItem()
        articleInfo['hubid'] = meta['hubinfo'].id
        if not meta['hubinfo'].id:
            print(meta['hubinfo'])
            return None

        dict_HUBINFO = meta['hubinfo'].__dict__
        for i in dict_HUBINFO.keys():
            if i == 'id' or i == '_sa_instance_state':
                continue
            articleInfo[i] = dict_HUBINFO[i]

        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find('div', attrs={"class": "notice-con"})

        articleInfo['content'] = content.prettify()

        attch_soupall = soup.find_all(href=re.compile("upload"))
        if attch_soupall:
            attchments = []
            for attch in attch_soupall:
                attchDict = {}
                try:
                    attchDict['download_url'] = attch.get('href')
                    download_filename = attch.get_text()
                    attchDict['download_filename'] = download_filename.split('/')[-1]
                    if len(attchDict['download_url']) < 2 or len(attchDict['download_filename']) < 1:
                        continue

                except:
                    continue
                attchments.append(attchDict)

            if attchments:
                articleInfo['attchments'] = attchments
        articleInfo['page_url'] = response.url

        yield articleInfo
