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
Content-Type: application/json
Host: www.ccgp-anhui.gov.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'''

headers = dict(line.split(": ", 1) for line in hub_HeadersWord.split("\n") if line != '')

codeList = [
    {'subclassName': '采购文件需求公示', 'code': 'ZcyAnnouncement3014', 'purchaseName': '采购文件需求公示'},
    {'subclassName': '单一来源公示', 'code': 'ZcyAnnouncement3012', 'purchaseName': '单一来源公示'},
    {'subclassName': '采购意向公开', 'code': 'ZcyAnnouncement10016', 'purchaseName': '采购意向公开'},
    {'subclassName': '采购公告', 'code': 'ZcyAnnouncement3008', 'purchaseName': '资格预审公告'},
    {'subclassName': '采购公告', 'code': 'ZcyAnnouncement3001', 'purchaseName': '公开招标公告'},
    {'subclassName': '采购公告', 'code': 'ZcyAnnouncement3020', 'purchaseName': '邀请招标公告'},
    {'subclassName': '采购公告', 'code': 'ZcyAnnouncement3002', 'purchaseName': '竞争性谈判公告'},
    {'subclassName': '采购公告', 'code': 'ZcyAnnouncement3011', 'purchaseName': '竞争性磋商公告'},
    {'subclassName': '采购公告', 'code': 'ZcyAnnouncement3003', 'purchaseName': '询价公告'},
    {'subclassName': '结果公告', 'code': 'ZcyAnnouncement3015', 'purchaseName': '终止公告'},
    {'subclassName': '结果公告', 'code': 'ZcyAnnouncement4005', 'purchaseName': '中标公告'},
    {'subclassName': '结果公告', 'code': 'ZcyAnnouncement4006', 'purchaseName': '成交公告'},
    {'subclassName': '结果公告', 'code': 'ZcyAnnouncement3017', 'purchaseName': '采购结果变更公告'},
    {'subclassName': '合同公告', 'code': 'ZcyAnnouncement3010', 'purchaseName': '合同公告'},
    {'subclassName': '更正公告', 'code': 'ZcyAnnouncement3018', 'purchaseName': '中止（暂停）公告'},
    {'subclassName': '更正公告', 'code': 'ZcyAnnouncement3005', 'purchaseName': '更正公告'},
    {'subclassName': '商城采购公告', 'code': 'ZcyAnnouncement9003', 'purchaseName': '商城采购信息、竞价公告'},
    {'subclassName': '商城采购公告', 'code': 'ZcyAnnouncement8013', 'purchaseName': '商城成交信息公告'},
    {'subclassName': '其他公告', 'code': 'ZcyAnnouncement9001', 'purchaseName': '定点成交信息公告'},
    {'subclassName': '其他公告', 'code': 'ZcyAnnouncement8026', 'purchaseName': '批量成交信息公告'}
]


class AnhuiCcgpSpider(scrapy.Spider):
    name = 'anhui_ccgp'
    allowed_domains = ['www.ccgp-anhui.gov.cn']
    baseUrl = "http://www.ccgp-anhui.gov.cn/front/search/category"
    pageS = 100

    def __init__(self, goon=None, startTime=None, endTime=None, *args, **kwargs):
        super(AnhuiCcgpSpider, self).__init__(*args, **kwargs)
        self.goon = goon
        self.timeoutformat = "%Y-%m-%d"
        if goon == 'hub':
            if not startTime and not endTime:
                self.startT = get_timestr(str(datetime.date.today()), outformat=self.timeoutformat)
                self.endT = self.startT
            elif startTime and not endTime:
                self.startT = get_timestr(startTime, outformat=self.timeoutformat)
                self.endT = get_timestr(str(datetime.date.today()), outformat=self.timeoutformat)

            elif startTime and endTime:
                self.startT = get_timestr(startTime, outformat=self.timeoutformat)
                self.endT = get_timestr(endTime, outformat=self.timeoutformat)
            else:
                raise 'startTime or endTime INPUT ERROR'

        if goon != 'article' and goon != 'hub':
            raise 'pls input goon = hub  or  article'

    def start_requests(self):
        meta = {}

        # 抓取HUB页
        if self.goon == 'hub':
            for num, i in enumerate(codeList):
                # if num == 1:
                #     break
                meta['breakMark'] = 0
                meta['pageNum'] = 1

                meta['purchaseName'] = i['purchaseName']
                meta['subclassName'] = i['subclassName']
                meta['code'] = i['code']
                # if meta['code'] != 'ZcyAnnouncement10016':
                #     continue

                postdata = {"leaf": "0",
                            "categoryCode": meta['code'],
                            "pageSize": self.pageS,
                            "pageNo": meta['pageNum'],
                            "publishDateBegin": self.startT,
                            "publishDateEnd": self.endT
                            }
                yield scrapy.Request(url=self.baseUrl,
                                     method='POST',
                                         body=json.dumps(postdata),
                                         callback=self.parse_hub,
                                         meta=meta,
                                         dont_filter=True,
                                         headers=headers
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
                # meta['page_url'] = "http://www.ccgp-anhui.gov.cn/ZcyAnnouncement/ZcyAnnouncement2/ZcyAnnouncement3001/wRS5VHbtyFvsOUUxUXKxCA==.html"
                meta['hubinfo'] = i
                meta['handle_httpstatus_list'] = [301, 302]
                meta['dont_redirect'] = True

                yield scrapy.Request(url=meta['page_url'],
                                     callback=self.parse_article,
                                     meta=meta,
                                     dont_filter=True,
                                     headers=creatHeader(hub_HeadersWord)
                                     )

    def parse_hub(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)

        total = jsonT['hits']['total']
        pageInfoList = jsonT['hits']['hits']
        if not pageInfoList:
            print('not pageInfoList')
            return None
        mark=0

        for pageInfo in pageInfoList:

            hubItem = ShangqingHubItem()
            hubItem['site'] = self.allowed_domains[0]
            hubItem['subclass'] = meta['subclassName']
            hubItem['purchase_type'] = meta['purchaseName']
            page_url = urlpase.urljoin(base="http://www.ccgp-anhui.gov.cn/",url=pageInfo['_source']['url'])

            if bl.exists(page_url) or bh.exists(page_url):
                print('exists true')
                mark += 1
                continue
            hubItem['page_url'] = page_url


            try:
                hubItem['issue_time'] = timestampREtimestr(pageInfo['_source']['publishDate'])
                hubItem['title'] = pageInfo['_source']['title']
            except Exception as ff:
                print(ff)
                continue

            try:
                hubItem['ztb_project_tenderer'] = pageInfo['_source']['author']
            except:
                pass

            province_name_dict = tureLocation(localName='安徽省', title=pageInfo['_source']['districtName'] + hubItem['title'])
            hubItem['province_name'] = province_name_dict['province_name']
            if province_name_dict['city_name']:
                hubItem['city_name'] = province_name_dict['city_name']
                if len(province_name_dict['city_name']) <= 2:
                    hubItem['city_name'] = ''
            else:
                hubItem['city_name'] = ''

            # pprint.pprint(hubItem)
            yield hubItem


        if mark == len(pageInfoList):
            meta['breakMark'] += 1
        else:
            meta['breakMark'] = 0

        if meta['breakMark'] == 2:
            return None

        if meta['pageNum'] >= total:
            return None
        print('---------------------------------------',meta['pageNum'])
        meta['pageNum'] += 1

        postdata = {"leaf": "0",
                    "categoryCode": meta['code'],
                    "pageSize": self.pageS,
                    "pageNo": meta['pageNum'],
                    "publishDateBegin": self.startT,
                    "publishDateEnd": self.endT
                    }

        yield scrapy.Request(url=self.baseUrl,
                             method='POST',
                             body=json.dumps(postdata),
                             callback=self.parse_hub,
                             meta=meta,
                             dont_filter=True,
                             headers=headers
                             )


        pass



    def parse_article(self, response):
        meta = response.meta


        articleInfo = ShangqingArticleItem()
        articleInfo['hubid'] = meta['hubinfo'].id

        dict_HUBINFO = meta['hubinfo'].__dict__
        for i in dict_HUBINFO.keys():
            if i == 'id' or i == '_sa_instance_state':
                continue
            articleInfo[i] = dict_HUBINFO[i]


        soup = BeautifulSoup(response.text,'lxml')
        content_json = soup.find('input',attrs={"name":"articleDetail"}).get('value')
        content_dict = json.loads(content_json)

        content_soup = BeautifulSoup(content_dict['content'],'lxml')

        articleInfo['content'] = content_soup.prettify()

        attch_soupall = content_soup.find_all(href=re.compile("aliyuncs"))
        if attch_soupall:
            attchments = []
            for attch in attch_soupall:
                attchDict = {}
                try:
                    attchDict['download_url'] = attch.get('href')
                    attchDict['download_filename'] = attch.get_text()
                    if len(attchDict['download_url']) < 2 or len(attchDict['download_filename']) < 1:
                        continue
                except:
                    continue
                attchments.append(attchDict)

            if attchments:
                articleInfo['attchments'] = attchments

        # if content_dict['attachmentVO']:
        #     attchments = []
        #     for attch in content_dict['attachmentVO']['attachments']:
        #         attchDict = {}
        #         attchDict['download_url'] = urlpase.urljoin(base='https://anhui-gov-open-doc.oss-cn-hangzhou.aliyuncs.com/',url=attch['fileId'])
        #         attchDict['download_filename'] = attch['name']
        #         attchments.append(attchDict)
        #     articleInfo['attchments'] = attchments

        articleInfo['page_url'] = response.url

        # pprint.pprint(articleInfo)
        # print('------------------------------------')

        yield articleInfo
