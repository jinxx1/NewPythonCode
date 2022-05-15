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
    path = os.path.join(os.getcwd(), 'spiders/shannxi_ccpy_urlList.json')
    with open(path, 'rb') as ff:
        jsonT = json.load(ff)
        ff.close()
    return jsonT

class ShannxiSpider(scrapy.Spider):
    name = 'shannxi_ccgp'
    allowed_domains = ['www.ccgp-shaanxi.gov.cn']
    cname = '陕西省政府采购网'
    urlList = get_urlList()
    mysqlSession = mysql_orm()
    baseUrl = "http://www.ccgp-shaanxi.gov.cn/freecms/rest/v1/notice/selectInfoMoreChannel.do?&siteId=a7a15d60-de5b-42f2-b35a-7e3efc34e54f&channel=1eb454a2-7ff7-4a3b-b12c-12acc2685bd1&currPage={pageNum}&pageSize={pageS}&noticeType={noticeType}&regionCode=&purchaseManner={purchaseManner}&title=&openTenderCode=&purchaseNature=&operationStartTime={startTime}&operationEndTime={endTime}&selectTimeName=noticeTime&cityOrArea="

    def __init__(self, goon=None, startTime=None, endTime=None, *args, **kwargs):
        super(ShannxiSpider, self).__init__(*args, **kwargs)
        self.pageS = 100
        self.goon = goon
        self.timeoutformat = "%Y-%m-%d %H:%M:%S"
        if goon == 'hub':
            if not startTime and not endTime:
                a = datetime.datetime.now() + datetime.timedelta(days=-1)
                self.startT = a.strftime("%Y-%m-%d %H:%M:%S")
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
                if i['count'] <= 100:
                    continue
                meta['purchase_type'] = i['purchaseName']
                meta['subclass'] = i['catName']
                meta['purchase_type_code'] = i['purchaseCode']
                meta['subclass_code'] = i['catNameCode']

                apiurl = self.baseUrl.format(pageNum=meta['pageNum'], pageS=self.pageS, startTime=self.startT,
                                             endTime=self.endT, noticeType=meta['subclass_code'],
                                             purchaseManner=meta['purchase_type_code'])
                yield scrapy.Request(url=apiurl,callback=self.parse_hub,
                                     meta=meta,dont_filter=True,
                                     headers=creatHeader(hub_HeadersWord))

        if self.goon == 'article':

            self.mysession = mysql_orm()
            urlList = self.mysession.get_ztbhubinfo(self.allowed_domains[0])
            for num, i in enumerate(urlList):
                if bl.exists(i.page_url):
                    self.mysession.update_ztbHubInfo(update_dict={"craw_status": 1}, hubInfo_id=i.id)
                    continue
                meta['page_url'] = i.page_url
                meta['hubinfo'] = i
                yield scrapy.Request(url=meta['page_url'],callback=self.parse_article,meta=meta,dont_filter=True,
                                     headers=creatHeader(hub_HeadersWord))

    def parse_hub(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)

        if jsonT['total'] == 0:
            return None
        allpage = get_pagecount(articlecount=jsonT['total'], pageS=self.pageS)

        mark = 0
        for num, pageInfo in enumerate(jsonT['data']):
            try:
                page_url = urlpase.urljoin(base="http://www.ccgp-shaanxi.gov.cn/", url=pageInfo['pageurl'])
            except:
                continue

            if bl.exists(page_url) or bh.exists(page_url):
                mark += 1
                continue

            info_dict = ShangqingHubItem()
            info_dict['site'] = self.allowed_domains[0]
            info_dict['purchase_type'] = meta['purchase_type']
            info_dict['subclass'] = meta['subclass']

            info_dict['page_url'] = page_url
            try:
                # 标题
                info_dict['title'] = pageInfo['title']
            except:
                continue
            try:
                # 发布时间
                info_dict['issue_time'] = pageInfo['addtimeStr']
            except:
                continue

            keys_mate = [
                # 业务类型，其他专业技术服务,信息化工程监理服务，工程类等等
                {'infokey': 'business_type', 'pagekey': 'catalogueNameList'},
                # 合同总额
                {'infokey': 'project_amount', 'pagekey': 'budget'},
                # 代理方
                {'infokey': 'ztb_project_agent', 'pagekey': 'agency'}
            ]

            for kk in keys_mate:
                infokey = kk['infokey']
                pagekey = kk['pagekey']
                try:
                    if not pageInfo[pagekey]:
                        continue
                    info_dict[infokey] = pageInfo[pagekey]
                except:
                    continue

            try:
                # 处理省市信息
                regionName = pageInfo['regionName']
            except:
                regionName = ''
            province_name_dict = tureLocation(localName='陕西省', title=regionName + info_dict['title'])
            info_dict['province_name'] = province_name_dict['province_name']
            if province_name_dict['city_name']:
                info_dict['city_name'] = province_name_dict['city_name']
                if len(province_name_dict['city_name']) <= 2:
                    info_dict['city_name'] = ''
            else:
                info_dict['city_name'] = ''

            yield info_dict

        if mark == len(jsonT['data']):
            meta['breakMark'] += 1
        else:
            meta['breakMark'] = 0

        if meta['breakMark'] == 5:
            return None

        if meta['pageNum'] >= allpage:
            return None

        meta['pageNum'] += 1
        apiurl = self.baseUrl.format(pageNum=meta['pageNum'], pageS=self.pageS, startTime=self.startT,
                                     endTime=self.endT, noticeType=meta['subclass_code'],
                                     purchaseManner=meta['purchase_type_code'])
        yield scrapy.Request(url=apiurl,callback=self.parse_hub,meta=meta,dont_filter=True,
                             headers=creatHeader(hub_HeadersWord))

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
        content = soup.find('div',attrs={"id":"content"})
        articleInfo['content'] = content.prettify()
        attch_soupall = soup.find_all(href=re.compile("gpx-bid-file|uploader"))
        if attch_soupall:
            attchments = []
            for attch in attch_soupall:
                attchDict = {}
                if 'javascript' in attch.get('href'):
                    try:
                        attchDict['download_url'] = re.findall("encodeURI\(\'(.*?)&fileName", self.allowed_domains[0])[0]
                    except:
                        continue
                else:
                    attchDict['download_url'] = attch.get('href')
                attchDict['download_filename'] = attch.get_text()
                attchments.append(attchDict)

            if attchments:
                articleInfo['attchments'] = attchments

        yield articleInfo
