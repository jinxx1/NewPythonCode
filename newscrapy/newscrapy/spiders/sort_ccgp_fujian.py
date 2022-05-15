# -*- coding: utf-8 -*-
import scrapy
import requests
import random
import time, pprint
from newscrapy.scrapyParse import *


# date_to_timestamp（）包括以下几种时间格式
# ['Ymd_HMS'] ['Y-m-d'] ['today']
TIME_DICT = date_to_timestamp()
HEA = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
    "Connection": "close",
    "Host": "ggzyfw.fujian.gov.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}
def dupcutUrl(jsonT):
    newjsonT = []
    orgLinkList = []
    for n in jsonT:
        n['indexurl'] = 'https://ggzyfw.fujian.gov.cn/Website/JYXX_{KIND}.aspx?ID={M_ID}&GGTYPE={GGTYPE}'.format(
            M_ID=str(int(n['M_ID'])),
            GGTYPE=str(int(n['GGTYPE'])),
            KIND=n['KIND']
        )
        newjsonT.append(n)
        orgLinkList.append(n['indexurl'])
    mysqlallurl = get_mysql_allurl(site='ggzyfw.fujian.gov.cn')

    no_insert_urlList = list(set(orgLinkList).difference(set(mysqlallurl)))
    llist = []
    for allinfo in newjsonT:
        if allinfo['indexurl'] in no_insert_urlList:
            llist.append(allinfo)
    return llist


class SortCcgpFujianSpider(scrapy.Spider):
    name = 'sort_ccgp_fujian'
    allowed_domains = ['ggzyfw.fujian.gov.cn']
    PostUrl = 'https://ggzyfw.fujian.gov.cn/Website/AjaxHandler/BuilderHandler.ashx'
    def __init__(self):
        print('开始无头浏览器')
        self.jar = get_cookies_by_headlessChrome(run=1)
        print('无头浏览器获得的jar为：',self.jar)

    def start_requests(self):
        for key in ['GCJS', 'ZFCG', 'GYCQ']:
            meta = {}
            meta['item'] = {}
            meta['item']['site'] = self.allowed_domains[0]
            meta['key'] = key
            meta['datapost'] = {
                "OPtype": "GetListNew",
                "pageNo": '1',
                "pageSize": '50',
                "proArea": "-1",
                "category": key,
                "announcementType": "-1",
                "ProType": "-1",
                "xmlx": "-1",
                "projectName": "",
                "TopTime": "1990-02-12 00:00:00",
                "EndTime": TIME_DICT['today']}
            yield scrapy.FormRequest(url=self.PostUrl,
                                     formdata=meta['datapost'],
                                     callback=self.parse_index,
                                     meta=meta,
                                     headers=HEA,
                                     cookies=self.jar,
                                     dont_filter=True)

    def parse_index(self, response):
        meta = response.meta
        if len(response.text) < 2:
            print('第一页，jar失效，即将获取新JAR')
            self.jar = get_cookies_by_headlessChrome(run=1)
            yield scrapy.FormRequest(url=self.PostUrl,
                                     formdata=meta['datapost'],
                                     callback=self.parse_index,
                                     meta=meta,
                                     headers=HEA,
                                     cookies=self.jar,
                                     dont_filter=True)

        else:
            jsoninfo = json.loads(response.text)['data']
            if not jsoninfo:
                print('index页没有找到json数据')
                return None
            jsoninfoall = dupcutUrl(jsoninfo)

            if not jsoninfoall:
                return None
            for num, info in enumerate(jsoninfoall):
                meta['jsonInfo'] = info
                meta['contentHeaders'] = HEA
                meta['contentHeaders']['Referer'] = meta['jsonInfo']['indexurl']
                meta['posturl'] = 'https://ggzyfw.fujian.gov.cn/Website/AjaxHandler/BuilderHandler.ashx?OPtype=GetGGInfoPC&ID={M_ID}&GGTYPE={GGTYPE}&url=AjaxHandler%2FBuilderHandler.ashx'.format(
                    M_ID=str(int(meta['jsonInfo']['M_ID'])),
                    GGTYPE=str(int(meta['jsonInfo']['GGTYPE'])))
                yield scrapy.Request(url=meta['posturl'],
                                     callback=self.parse,
                                     meta=meta,
                                     headers=meta['contentHeaders'],
                                     cookies=self.jar)


    def parse(self, response):
        meta = response.meta
        if len(response.text) < 2:
            print('第一页，jar失效，即将获取新JAR')
            self.jar = get_cookies_by_headlessChrome(run=1)
            yield scrapy.FormRequest(url=meta['posturl'],
                                     formdata=meta['datapost'],
                                     callback=self.parse,
                                     meta=meta,
                                     headers=meta['contentHeaders'],
                                     cookies=self.jar,
                                     dont_filter=True)
            return None

        jsonT = json.loads(response.text)

        KIND = '未知分类'
        if meta['jsonInfo']['KIND'] == 'GCJS':
            KIND = '工程建设'
        if meta['jsonInfo']['KIND'] == 'ZFCG':
            KIND = '政府采购'
        if meta['jsonInfo']['KIND'] == 'TDSYQ':
            KIND = '土地使用权'
        if meta['jsonInfo']['KIND'] == 'TDSYQ':
            KIND = '国有产权'
        TTitle = [meta['jsonInfo']['AREANAME'], KIND, meta['jsonInfo']['TITLE'], meta['jsonInfo']['NAME']]
        meta['item']['title'] = '_'.join([meta['jsonInfo']['TITLE'], meta['jsonInfo']['NAME']])
        meta['item']['issueTime'] = get_timestr(meta['jsonInfo']['TM'].replace('T', ' '))
        meta['item']['subclass'] = '_'.join(TTitle[:3])
        meta['item']['url'] = meta['jsonInfo']['indexurl']
        meta['item']['content'] = ''.join(jsonT['data'])
        meta['item']['content'] = len(meta['item']['content'])

        insertmysql = save_api(meta['item'])

        nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if insertmysql['msg'] != 'success':
            meta['item']['content'] = len(meta['item']['content'])
            meta['item']['msg'] = insertmysql['msg']
            meta['item']['errortime'] = nowTime
            print('error')
            print(meta['item'])
            print('error_end')
        else:
            print(nowTime)