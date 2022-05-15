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

hub_HeadersWord = '''Accept: application/json, text/javascript, */*; q=0.01
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'''

headers = dict(line.split(": ", 1) for line in hub_HeadersWord.split("\n") if line != '')

def get_url():
    puurmet_dict = [
        {'purchaseName': "公开招标", 'purchaseCode': "1"},
        {'purchaseName': "邀请招标", 'purchaseCode': "2"},
        {'purchaseName': "竞争性谈判", 'purchaseCode': "3"},
        {'purchaseName': "询价", 'purchaseCode': "4"},
        {'purchaseName': "单一来源", 'purchaseCode': "5"},
        {'purchaseName': "竞争性磋商", 'purchaseCode': "6"},

    ]
    subclass_dict = [
        {"subclassName": "招标公告", "subclassCode": "cggg", "type": '1'},
        {"subclassName": "招标更正公告", "subclassCode": "cggg", "type": '2'},
        {"subclassName": "中标（成交）公告", "subclassCode": "cggg", "type": '3'},
        {"subclassName": "中标（成交）更正公告", "subclassCode": "cggg", "type": '4'},
        {"subclassName": "废标公告", "subclassCode": "cggg", "type": '5'},
        {"subclassName": "资格预审公告", "subclassCode": "cggg", "type": '6'},
        {"subclassName": "资格预审公告", "subclassCode": "cggg", "type": '7'},
    ]
    llist = []
    for pur in puurmet_dict:
        for sub in subclass_dict:
            ddict = {}
            ddict['purchaseName'] = pur['purchaseName']
            ddict['purchaseCode'] = pur['purchaseCode']
            ddict['subclassName'] = sub['subclassName']
            ddict['subclassCode'] = sub['subclassCode']
            ddict['type'] = sub['type']
            llist.append(ddict)
    return llist

class NeimengguCcgpSpider(scrapy.Spider):
    name = 'neimenggu_ccgp'
    allowed_domains = ['www.ccgp-neimenggu.gov.cn']
    baseUrl = "http://www.ccgp-neimenggu.gov.cn/zfcgwslave/web/index.php?r=pro%2Fanndata"

    def __init__(self, goon=None, startTime=None, endTime=None, *args, **kwargs):
        super(NeimengguCcgpSpider, self).__init__(*args, **kwargs)
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
            infoall = get_url()

            for num, i in enumerate(infoall):
                if num == 1:
                    break
                meta['breakMark'] = 0
                meta['pageNum'] = 1
                meta['purchaseName'] = i['purchaseName']
                meta['purchaseCode'] = i['purchaseCode']
                meta['subclassName'] = i['subclassName']
                meta['subclassCode'] = i['subclassCode']
                meta['type'] = i['type']
                postdata = {
                    'type_name': meta['type'],
                    'purmet': meta['purchaseCode'],
                    'annstartdate_S': str(self.startT),
                    'annstartdate_E': str(self.endT),
                    'byf_page': str(meta['pageNum']),
                    'fun': meta['subclassCode'],
                    'page_size': str(self.pageS),
                }
                meta['POSTDATA'] = postdata
                yield scrapy.FormRequest(url=self.baseUrl, formdata=postdata, callback=self.parse_hub, meta=meta,
                                         dont_filter=True, headers=headers
                                         )

        # 抓取ARTICLE页
        if self.goon == 'article':
            self.mysession = mysql_orm()
            urlList = self.mysession.get_ztbhubinfo(self.allowed_domains[0])
            # print('======================================',urlList)
            for num, i in enumerate(urlList):
                # if num >0:
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
        print('into parse_hub=================================')
        jsonT = json.loads(response.text)
        total = int(jsonT[1])
        if not jsonT or len(jsonT) == 0:
            return None

        mark = 0
        for pageInfo in jsonT[0]:
            print(meta['POSTDATA'])
            hubItem = ShangqingHubItem()
            hubItem['site'] = self.allowed_domains[0]
            hubItem['subclass'] = meta['subclassName']
            hubItem['purchase_type'] = meta['purchaseName']
            page_url_base = "http://www.ccgp-neimenggu.gov.cn/category/{subclass}g?tb_id={tb_id}&p_id={page_id}&type={type_id}"
            page_url = page_url_base.format(subclass=meta['subclassCode'],
                                            tb_id=pageInfo['ay_table_tag'],
                                            page_id=pageInfo['wp_mark_id'],
                                            type_id=2)
            if bl.exists(page_url) or bh.exists(page_url):
                mark += 1
                continue

            hubItem['page_url'] = page_url
            try:
                hubItem['issue_time'] = get_timestr(re.findall("\d{2,4}-\d{1,2}-\d{1,2}", pageInfo['SUBDATE'])[0])
                hubItem['title'] = pageInfo['TITLE']
            except:
                continue

            try:
                hubItem['business_type'] = pageInfo['PURNAME']
            except:
                pass

            province_name_dict = tureLocation(localName='内蒙古自治区', title=pageInfo['ADNAME'] + hubItem['title'])
            hubItem['province_name'] = province_name_dict['province_name']
            if province_name_dict['city_name']:
                hubItem['city_name'] = province_name_dict['city_name']
                if len(province_name_dict['city_name']) <= 2:
                    hubItem['city_name'] = ''
            else:
                hubItem['city_name'] = ''

            yield hubItem

        print(len(jsonT[0]))

        if mark == len(jsonT[0]):
            meta['breakMark'] += 1
        else:
            meta['breakMark'] = 0

        if meta['breakMark'] == 2:
            return None

        if meta['pageNum'] >= total:
            return None

        meta['pageNum'] += 1
        postdata = {
            'type_name': meta['type'],
            'purmet': meta['purchaseCode'],
            'annstartdate_S': str(self.startT),
            'annstartdate_E': str(self.endT),
            'byf_page': str(meta['pageNum']),
            'fun': meta['subclassCode'],
            'page_size': str(self.pageS),
        }
        meta['POSTDATA'] = postdata
        yield scrapy.FormRequest(url=self.baseUrl,
                                 formdata=postdata,
                                 callback=self.parse_hub,
                                 meta=meta,
                                 dont_filter=True,
                                 headers=headers
                                 )

    def parse_article(self, response):
        meta = response.meta
        articleInfo = ShangqingArticleItem()
        articleInfo['hubid'] = meta['hubinfo'].id
        if not meta['hubinfo'].id:
            return None
        dict_HUBINFO = meta['hubinfo'].__dict__
        for i in dict_HUBINFO.keys():
            if i == 'id' or i == '_sa_instance_state':
                continue
            articleInfo[i] = dict_HUBINFO[i]
        soup = BeautifulSoup(response.text, 'lxml')
        content = soup.find('div', attrs={"id": "content-box-1"})

        articleInfo['content'] = filter_content(content.prettify())

        attch_soupall = soup.find_all(href=re.compile("gpx-bid-file|gpx-bidconfirm"))
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

        yield articleInfo
