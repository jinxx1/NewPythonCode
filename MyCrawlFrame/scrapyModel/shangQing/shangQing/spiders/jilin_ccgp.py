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
import execjs

sys_code = platform.system()
if sys_code == 'Windows':
    sys.path.append(r"D:\PythonCode\mypythonpath")
from mkdir import mkdir
from redisBloomHash import bl, bh
from getmysqlInfo import jsonInfo
from crawltools import *
from reqSession import *
from uxue_orm import *
from crawl_js import get_jsCode

hub_HeadersWord = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Content-Length: 346
Content-Type: application/x-www-form-urlencoded
Cookie: _gscu_1208125908=46986802m1416n11; _gscbrs_1208125908=1; _gscs_1208125908=t4819467100k8ud20|pv:1
Host: www.ccgp-jilin.gov.cn
Origin: http://www.ccgp-jilin.gov.cn
Referer: http://www.ccgp-jilin.gov.cn/ext/search/morePolicyNews.action
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'''

headers = dict(line.split(": ", 1) for line in hub_HeadersWord.split("\n") if line != '')


class JilinCcgpSpider(scrapy.Spider):
    name = 'jilin_ccgp'
    allowed_domains = ['www.ccgp-jilin.gov.cn']
    urlList = [{'subclassName': '省级采购公告', 'purchaseName': '资格预审', 'noticetypeId': '1', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '公开招标', 'noticetypeId': '2', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '邀请招标', 'noticetypeId': '7', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '竞争性谈判', 'noticetypeId': '4', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '竞争性磋商', 'noticetypeId': '5', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '单一来源', 'noticetypeId': '6', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '询价公告', 'noticetypeId': '3', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '中标公告', 'noticetypeId': '9', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '成交公告', 'noticetypeId': '10', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '废标、更正、其他公告', 'noticetypeId': '11', 'categoryId': '124'},
               {'subclassName': '省级采购公告', 'purchaseName': '合同、验收公告', 'noticetypeId': '13', 'categoryId': '124'},
               {'subclassName': '市县级采购公告', 'purchaseName': '资格预审', 'noticetypeId': '1', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '公开招标', 'noticetypeId': '2', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '邀请招标', 'noticetypeId': '7', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '竞争性谈判', 'noticetypeId': '4', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '竞争性磋商', 'noticetypeId': '5', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '单一来源', 'noticetypeId': '6', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '询价公告', 'noticetypeId': '3', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '中标公告', 'noticetypeId': '9', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '成交公告', 'noticetypeId': '10', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '废标、更正、其他公告', 'noticetypeId': '11', 'categoryId': '125'},
               {'subclassName': '市县级采购公告', 'purchaseName': '合同、验收公告', 'noticetypeId': '13', 'categoryId': '125'}]
    # ss = get_ss()
    baseUrl = "http://www.ccgp-jilin.gov.cn/ext/search/morePolicyNews.action"

    pageS = 100

    def __init__(self, goon=None, startTime=None, endTime=None, *args, **kwargs):
        super(JilinCcgpSpider, self).__init__(*args, **kwargs)
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
        url = "http://www.ccgp-jilin.gov.cn/ext/search/keyPair.action"
        yield scrapy.Request(url=url,callback=self.get_ss_and_start,
                             dont_filter=True,meta=meta,headers=creatHeader(hub_HeadersWord))

    def get_ss_and_start(self, response):
        meta = response.meta
        jm = json.loads(response.text)
        exponent = jm['map']["exponent"]
        modulus = jm['map']["modulus"]
        keyId = jm['keyId']
        context = execjs.compile(get_jsCode('jilin_ccgp'))

        meta['ss'] = context.call("dd", exponent, modulus, keyId)


        # 抓取HUB页
        if self.goon == 'hub':
            for num, i in enumerate(self.urlList):
                # if num == 1:
                #     break
                meta['breakMark'] = 0
                meta['pageNum'] = 1

                meta['purchaseName'] = i['purchaseName']
                meta['subclassName'] = i['subclassName']
                meta['noticetypeId'] = i['noticetypeId']
                meta['categoryId'] = i['categoryId']


                postdata = {"currentPage": str(meta['pageNum']),
                            "noticetypeId": str(meta['noticetypeId']),
                            "categoryId": str(meta['categoryId']),
                            "ss": meta['ss']
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
            # print(urlList)
            for num, i in enumerate(urlList):

                if bl.exists(i.page_url):
                    self.mysession.update_ztbHubInfo(update_dict={"craw_status": 1}, hubInfo_id=i.id)
                    continue
                meta['page_url'] = i.page_url
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
        soup = BeautifulSoup(response.text, 'lxml')
        # soup.prettify()
        links = soup.find('div', id='list_right').find_all('li')
        # links = soup.find_all('a', href=re.compile("gotoHelpFrontList"))
        pageInfoList =[x for x in links]
        if not len(pageInfoList):
            return None

        mark = 0
        for pageInfo in links:


            hubItem = ShangqingHubItem()
            hubItem['site'] = self.allowed_domains[0]
            hubItem['subclass'] = meta['subclassName']
            hubItem['purchase_type'] = meta['purchaseName']
            a = pageInfo.find('a')

            page_url = urlpase.urljoin(base="http://www.ccgp-jilin.gov.cn/", url=a.get('href'))

            if bl.exists(page_url) or bh.exists(page_url):
                mark += 1
                continue
            hubItem['page_url'] = page_url

            try:

                hubItem['issue_time'] = get_timestr(pageInfo.find('span').get_text())
                hubItem['title'] = a.get_text()
            except Exception as ff:
                print(ff)
                continue

            city = pageInfo.find('em').get_text()


            province_name_dict = tureLocation(localName='吉林',title=city + hubItem['title'])
            hubItem['province_name'] = province_name_dict['province_name']
            if province_name_dict['city_name']:
                hubItem['city_name'] = province_name_dict['city_name']
                if len(province_name_dict['city_name']) <= 2:
                    hubItem['city_name'] = ''
            else:
                hubItem['city_name'] = ''
            yield hubItem

        print('本页有多少篇文章：', len(pageInfoList))
        print('本页已录入{}文章：。未录入{}文章'.format(mark,len(pageInfoList)-mark))
        print('subclass：{}  pusrchase：{}  pageNum：{}'.format(meta['subclassName'], meta['purchaseName'],meta['pageNum']))
        print('*******'*2,)

        if mark == len(pageInfoList):
            meta['breakMark'] += 1
        else:
            meta['breakMark'] = 0

        if meta['breakMark'] == 3:
            return None

        total_page = soup.find('p',attrs={'class':"yeshu"}).get_text()
        total = int(re.findall("共有(.*?)页",total_page)[0].strip())

        if meta['pageNum'] >= total:
            return None
        print('---------------------------------------', meta['pageNum'])
        meta['pageNum'] += 1

        postdata = {"currentPage": str(meta['pageNum']),
                    "noticetypeId": str(meta['noticetypeId']),
                    "categoryId": str(meta['categoryId']),
                    "ss": meta['ss']
                    }
        if meta['pageNum'] > 2:
            return None

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

        dict_HUBINFO = meta['hubinfo'].__dict__
        for i in dict_HUBINFO.keys():
            if i == 'id' or i == '_sa_instance_state':
                continue
            articleInfo[i] = dict_HUBINFO[i]

        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find('div', attrs={"id": "xiangqingneiron"})


        articleInfo['content'] = content.prettify()

        attch_soupall = content.find_all(href=re.compile("aliyuncs|filedownload|TPBidder"))
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


        articleInfo['page_url'] = response.url

        # pprint.pprint(articleInfo)
        # print('------------------------------------')

        yield articleInfo
