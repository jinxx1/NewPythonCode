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
from shangQing.cutContent import filter_content

sys_code = platform.system()
if sys_code == 'Windows':
    sys.path.append(r"D:\PythonCode\mypythonpath")
from mkdir import mkdir
from redisBloomHash import bl, bh
from getmysqlInfo import jsonInfo
from crawltools import *
from reqSession import *
from uxue_orm import *

hub_HeadersWord = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Content-Length: 92
Content-Type: application/x-www-form-urlencoded
Cookie: HttpOnly; JSESSIONID=sLm3v9Yfn0LJ2BTShL2csy5MCPYcwW5bSn8HHJX7pcpFsJLczKKT!344495240; insert_cookie=20057268; HttpOnly
Host: www.ccgp-tianjin.gov.cn
Origin: http://www.ccgp-tianjin.gov.cn
Referer: http://www.ccgp-tianjin.gov.cn/portal/topicView.do?method=view&view=intention&ver=2&id=2021&st=1&stmp=1648204153037
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'''

headers = dict(line.split(": ", 1) for line in hub_HeadersWord.split("\n") if line != '')


class TianjinCcgpSpider(scrapy.Spider):
    name = 'tianjin_ccgp'
    allowed_domains = ['www.ccgp-tianjin.gov.cn']
    baseUrl = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'
    urlList = [
        {'subclassName': '采购需求征求意见_市级', 'purchaseName': '采购需求征求意见', 'code_id': '1662'},
        {'subclassName': '采购需求征求意见_区级', 'purchaseName': '采购需求征求意见', 'code_id': '1994'},
        {'subclassName': '采购公告_市级', 'purchaseName': '采购公告', 'code_id': '1665'},
        {'subclassName': '采购公告_区级', 'purchaseName': '采购公告', 'code_id': '1664'},
        {'subclassName': '更正公告_市级', 'purchaseName': '更正公告', 'code_id': '1663'},
        {'subclassName': '更正公告_区级', 'purchaseName': '更正公告', 'code_id': '1666'},
        {'subclassName': '采购结果公告_市级', 'purchaseName': '采购结果公告', 'code_id': '2014'},
        {'subclassName': '采购结果公告_区级', 'purchaseName': '采购结果公告', 'code_id': '2013'},
        {'subclassName': '合同及验收公告_市级', 'purchaseName': '合同及验收公告', 'code_id': '2015'},
        {'subclassName': '合同及验收公告_区级', 'purchaseName': '合同及验收公告', 'code_id': '2016'},
        {'subclassName': '采购意向公开_市级', 'purchaseName': '采购意向公开', 'code_id': '2021'},
        {'subclassName': '采购意向公开_区级', 'purchaseName': '采购意向公开', 'code_id': '2022'},
        {'subclassName': '单一来源公示_市级', 'purchaseName': '单一来源公示', 'code_id': '2033'},
        {'subclassName': '单一来源公示_区级', 'purchaseName': '单一来源公示', 'code_id': '2034'}
    ]

    def __init__(self, goon=None, startTime=None, endTime=None, *args, **kwargs):
        super(TianjinCcgpSpider, self).__init__(*args, **kwargs)
        self.pageS = 100
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
            for num, i in enumerate(self.urlList):
                # if num == 1:
                #     break
                meta['breakMark'] = 0
                meta['pageNum'] = 1
                meta['purchaseName'] = i['purchaseName']
                meta['subclassName'] = i['subclassName']
                meta['code_id'] = i['code_id']

                postdata = {
                    'method': "find",
                    'ldateQGE': str(self.startT),
                    'ldateQLE': str(self.endT),
                    'id': meta['code_id'],
                    'view': 'Infor',
                    'page': str(meta['code_id'])

                }

                yield scrapy.FormRequest(url=self.baseUrl,
                                         formdata=postdata,
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
                # if num > 0:
                #     continue
                if bl.exists(i.page_url):
                    self.mysession.update_ztbHubInfo(update_dict={"craw_status": 1}, hubInfo_id=i.id)
                    continue
                meta['page_url'] = i.page_url.replace('cggg?', 'cgggg?')
                meta['hubinfo'] = i
                # meta['handle_httpstatus_list'] = [301, 302]
                # meta['dont_redirect'] = True


                yield scrapy.Request(url=meta['page_url'],
                                     callback=self.parse_article,
                                     meta=meta,
                                     dont_filter=True,
                                     headers=creatHeader(hub_HeadersWord)
                                     )

    def parse_hub(self, response):
        meta = response.meta

        soup = BeautifulSoup(response.text, 'lxml')
        if '未查到相关数据' in soup.prettify():
            return None
        links = soup.find('ul', class_='dataList').find_all('li')
        pageInfoList = [x for x in links]
        if not len(pageInfoList):
            return None

        mark = 0
        for pageInfo in links:
            hubItem = ShangqingHubItem()
            hubItem['site'] = self.allowed_domains[0]
            hubItem['subclass'] = meta['subclassName']
            hubItem['purchase_type'] = meta['purchaseName']
            a = pageInfo.find('a')
            page_url = urlpase.urljoin(base="http://www.ccgp-tianjin.gov.cn/", url=a.get('href'))

            if bl.exists(page_url) or bh.exists(page_url):
                # print('exists true')
                mark += 1
                continue
            hubItem['page_url'] = page_url

            try:

                hubItem['issue_time'] = get_timestr(pageInfo.find('span', attrs={'class': "time"}).get_text())
                hubItem['title'] = a.get('title')
            except Exception as ff:
                print(ff)
                continue

            province_name_dict = tureLocation(localName='天津', title=hubItem['title'])
            hubItem['province_name'] = province_name_dict['province_name']
            if province_name_dict['city_name']:
                hubItem['city_name'] = province_name_dict['city_name']
                if len(province_name_dict['city_name']) <= 2:
                    hubItem['city_name'] = ''
            else:
                hubItem['city_name'] = ''

            # pprint.pprint(hubItem)
            yield hubItem
            # print('--------------------------------')

        if mark == len(pageInfoList):
            meta['breakMark'] += 1
        else:
            meta['breakMark'] = 0

        if meta['breakMark'] == 3:
            return None

        total = soup.find('span', attrs={'class': "countPage"}).find('b').get_text()
        if meta['pageNum'] >= int(total):
            return None

        print('subclass：{}  pusrchase：{}  本类别共：{}页。pageNum：{}'.format(meta['subclassName'], meta['purchaseName'], total,
                                                                      meta['pageNum']))
        print('本页有{}篇文章。mark：{}。未录入{}文章'.format(len(pageInfoList), mark, len(pageInfoList) - mark))
        print('*********************************************' * 2, )

        meta['pageNum'] += 1

        postdata = {
            'method': "find",
            'ldateQGE': str(self.startT),
            'ldateQLE': str(self.endT),
            'id': meta['code_id'],
            'view': 'Infor',
            'page': str(meta['code_id'])

        }

        yield scrapy.FormRequest(url=self.baseUrl,
                                 formdata=postdata,
                                 callback=self.parse_hub,
                                 meta=meta,
                                 dont_filter=True,
                                 headers=creatHeader(hub_HeadersWord)
                                 )

    def parse_article(self, response):
        meta = response.meta

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
        # print(soup.prettify())
        content = soup.find('div', attrs={"class": "pageInner"}).find('table')

        articleInfo['content'] = filter_content(content.prettify())


        attch_soupall = soup.find_all(href=re.compile("downEnId"))
        if attch_soupall:
            attchments = []
            for attch in attch_soupall:
                attchDict = {}
                try:
                    attchDict['download_url'] = urlpase.urljoin(base='http://www.ccgp-tianjin.gov.cn/',url=attch.get('href'))
                    attchDict['download_filename'] = attch.get_text()
                    if len(attchDict['download_url']) < 2 or len(attchDict['download_filename']) < 1:
                        continue
                except:
                    continue
                attchments.append(attchDict)

            if attchments:
                articleInfo['attchments'] = attchments
        articleInfo['page_url'] = response.url

        # print(articleInfo)
        # print('------------------------------------------')

        yield articleInfo
