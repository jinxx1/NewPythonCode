# -*- coding: utf-8 -*-
import scrapy

import sys, re, os, json, pprint, chardet, cchardet, time, datetime, lxml, requests
import lxml.html
from lxml.html import HtmlComment
from lxml import etree
from lxml import html as htmlstr

from requests.adapters import HTTPAdapter
from urllib import parse as urlpase
from bs4 import BeautifulSoup
from shangQing.items import ShangqingItem, ShangqingHubItem, ShangqingArticleItem

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


def get_urlList():
    word = '''需求公开	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&colcode=2501&curpage={pageNum}&grade=province&region=&firstpage=1
意向公开	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&colcode=2500&curpage={pageNum}&grade=province&region=&firstpage=1
采购公告	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&pdate={startTime}&kindof=&unitname=&projectname=&projectcode=&colcode=0301&curpage={pageNum}&grade=province&region=&firstpage=1
单一来源公示	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&colcode=2102&curpage={pageNum}&grade=province&region=&firstpage=1
信息更正	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&pdate={startTime}&kindof=&areacode=&unitname=&projectname=&projectcode=&colcode=0305&curpage={pageNum}&grade=province&region=&firstpage=1
结果公告	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&pdate={startTime}&kindof=&unitname=&projectname=&projectcode=&colcode=0302&curpage={pageNum}&grade=province&region=&firstpage=1
废标公告	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&pdate={startTime}&kindof=&areacode=&unitname=&projectname=&projectcode=&colcode=0306&curpage={pageNum}&grade=province&region=&firstpage=1
合同公开	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&colcode=2502&curpage={pageNum}&grade=province&region=&firstpage=1
验收公开	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&colcode=2503&curpage={pageNum}&grade=province&region=&firstpage=1
市县需求(意向)公开	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&areacode=&colcode=2504&curpage={pageNum}&grade=city&region=&firstpage=1
市县采购公告	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&pdate={startTime}&kindof=&areacode=&unitname=&projectname=&projectcode=&colcode=0303&curpage={pageNum}&grade=city&region=&firstpage=1
投标保证金	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&areacode=&colcode=2508&curpage={pageNum}&grade=city&region=&firstpage=1
市县单一来源公示	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&areacode=&colcode=2106&curpage={pageNum}&grade=city&region=&firstpage=1
信息更正	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&pdate={startTime}&kindof=&areacode=&unitname=&projectname=&projectcode=&colcode=0305&curpage={pageNum}&grade=city&region=&firstpage=1
市县结果公告	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&pdate={startTime}&kindof=&areacode=&unitname=&projectname=&projectcode=&colcode=0304&curpage={pageNum}&grade=city&region=&firstpage=1
废标公告	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&pdate={startTime}&kindof=&areacode=&unitname=&projectname=&projectcode=&colcode=0306&curpage={pageNum}&grade=city&region=&firstpage=1
市县合同公开	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&areacode=&colcode=2505&curpage={pageNum}&grade=city&region=&firstpage=1
市县验收公开	http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&areacode=&colcode=2506&curpage={pageNum}&grade=city&region=&firstpage=1'''.split(
        '\n')

    llist = []
    for i in word:
        i_cut = i.split('\t')

        ddict = {}
        ddict['catName'] = i_cut[0]
        ddict['baseUrl'] = i_cut[1]

        llist.append(ddict)
    return llist


hub_HeadersWord = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Content-Length: 93
Content-Type: application/x-www-form-urlencoded
Cookie: JSESSIONID=5C4AF14CE90B4667B96DD2D01140855D; insert_cookie=83172026
Host: www.ccgp-shandong.gov.cn
Origin: http://www.ccgp-shandong.gov.cn
Referer: http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'''


class ShandongCcgpSpider(scrapy.Spider):
    name = 'shandong_ccgp'
    allowed_domains = ['www.ccgp-shandong.gov.cn']
    cname = '山东省政府采购网'
    urlList = get_urlList()

    # baseUrl = "http://www.ccgp-shandong.gov.cn/sdgp2017/site/listnew.jsp?subject=&unitname=&pdate={startTime}&colcode={colcode}&curpage={pageNum}&grade={location}&region=&firstpage=1"

    def __init__(self, goon=None, startTime=None, endTime=None, *args, **kwargs):
        super(ShandongCcgpSpider, self).__init__(*args, **kwargs)
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

        if goon == 'article':
            self.mysession = mysql_orm()

    def start_requests(self):
        meta = {}

        meta['breakMark'] = 0
        meta['pageNum'] = 1
        if self.goon == 'hub':
            for num, i in enumerate(self.urlList):
                # if num == 1:
                #     break
                meta['purchase_type'] = i['catName']
                meta['baseUrl'] = i['baseUrl']
                yield scrapy.Request(url=meta['baseUrl'].format(startTime=self.startT, pageNum=meta['pageNum']),
                                     callback=self.parse_hub,
                                     meta=meta,
                                     dont_filter=True,
                                     headers=creatHeader(hub_HeadersWord)
                                     )

        if self.goon == 'article':
            urlList = self.mysession.get_ztbhubinfo(self.allowed_domains[0])
            # print('======================================',len(urlList))
            for i in urlList:
                if bl.exists(i.page_url):
                    self.mysession.update_ztbHubInfo(update_dict={"craw_status": 1}, hubInfo_id=i.id)
                    continue
                meta['hubinfo'] = i
                meta['handle_httpstatus_list'] = [301, 302]
                meta['dont_redirect'] = True

                yield scrapy.Request(url=i.page_url,
                                     callback=self.parse_article,
                                     meta=meta,
                                     dont_filter=True,
                                     headers=creatHeader(hub_HeadersWord)
                                     )

    def parse_hub(self, response):
        meta = response.meta

        soup = BeautifulSoup(response.text, 'lxml')

        links = soup.find('ul', attrs={"class": "news_list2"}).find_all('li')
        if len(links) == 0:
            print('本页无文章', meta['purchase_type'])
            print(response.url)
            return None
        mark = 0
        for num, i in enumerate(links):
            hubItem = ShangqingHubItem()
            a = i.find('span', attrs={"class": "title"}).find('a')

            hubItem['page_url'] = urlpase.urljoin(base='http://www.ccgp-shandong.gov.cn/', url=a.get('href'))
            if bl.exists(hubItem['page_url']) or bh.exists(hubItem['page_url']):
                mark += 1
                continue
            hubItem['site'] = self.allowed_domains[0]
            hubItem['subclass'] = meta['purchase_type']
            hubItem['purchase_type'] = meta['purchase_type']
            hubItem['title'] = a.get('title')

            hubItem['issue_time'] = get_timestr(i.find('span', attrs={"class": "hits"}).get_text())

            province_name_dict = tureLocation(localName='山东省', title=a.get_text())
            hubItem['province_name'] = province_name_dict['province_name']
            if province_name_dict['city_name']:
                hubItem['city_name'] = province_name_dict['city_name']
                if len(province_name_dict['city_name']) <= 2:
                    hubItem['city_name'] = ''
            else:
                hubItem['city_name'] = ''

            yield hubItem

        print('-------------------------------------------------------', meta['pageNum'], mark)

        pageTotal = int(soup.find('span', attrs={"id": "totalnum"}).get_text())

        if mark == len(links):
            meta['breakMark'] += 1
        else:
            meta['breakMark'] = 0

        if meta['breakMark'] == 2:
            return None

        if meta['pageNum'] >= pageTotal:
            return None

        meta['pageNum'] += 1
        yield scrapy.Request(url=meta['baseUrl'].format(startTime=self.startT, pageNum=meta['pageNum']),
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
        content = soup.find('div', attrs={"id": "textarea"})
        articleInfo['content'] = content.prettify()
        attch_soupall = soup.find_all(href=re.compile("upload|readcontractnew|Bibreportnew"))
        if attch_soupall:
            articleInfo['attchments'] = []
            for attch in attch_soupall:
                attchDict = {}
                attchDict['download_url'] = urlpase.urljoin('http://www.ccgp-shandong.gov.cn/sdgp2017/',
                                                            attch.get('href'))
                attchDict['download_filename'] = attch.get_text()
                articleInfo['attchments'].append(attchDict)
        yield articleInfo
        # item['hubid']
        #
        # articleInfo['content'] = len(articleInfo['content'] )
        # pprint.pprint(articleInfo)
        # print('--------------------------------------------------------------------')
