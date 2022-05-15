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


true = True
false = False

HEA = {'Content-Type': 'application/json'}

zbgg ={"sColumns": ",,,,,,,,,,,,",
	"amDataProp": ["announceTime", "", "projName", "projType", "id", "bidPublicityName", "reglQuth", "firstCandidateName", "secondCandidateName", "thirdCandidateName", "id", "projCode", "oldBERId"],
	"abSortable": [true, false, false, false, false, false, true, true, true, true, true, true, true],
	"aiSortCol": [0],
	"asSortDir": ["desc"],
	"iSortingCols": 1,
	"asSearch": ["projType", "announceTime", "bidPublicityName", "reglQuth", "projCode"],
	"asSearchVal": ["", "", "", "", ""]}


class CaacSpider(scrapy.Spider):
    name = 'caac'
    siteName = '中国民用航天局'
    allowed_domains = ['zbtb.caac.gov.cn']
    dateInfo = {
"中标公示":{
"iColumns": 13,
"sColumns": ",,,,,,,,,,,,",
"amDataProp": ["announceTime", "", "projName", "projType", "id", "bidPublicityName", "reglQuth",
               "firstCandidateName", "secondCandidateName", "thirdCandidateName", "id", "projCode", "oldBERId"],
"abSortable": [true, false, false, false, false, false, true, true, true, true, true, true, true],
"aiSortCol": [0],
"asSortDir": ["desc"],
"iSortingCols": 1,
"asSearch": ["projType", "announceTime", "bidPublicityName", "reglQuth", "projCode"],
"asSearchVal": ["", "", "", "", ""],
"url": "https://zbtb.caac.gov.cn/sys-content/tableZbgs.html"},

"其他公告":{
    "iColumns": 9,
    "sColumns": ",,,,,,,,",
    "amDataProp": ["announceTime", "", "projName", "projType", "id", "announcementName", "reglQuth", "id", "quafExatMode"],
    "abSortable": [true, false, false, false, false, false, true, true, true],
    "aiSortCol": [0],
    "asSortDir": ["desc"],
    "iSortingCols": 1,
    "asSearch": ["projType", "announceTime", "announcementName", "projName", "reglQuth"],
    "asSearchVal": ["", "", "", "", ""],
    "url": "https://zbtb.caac.gov.cn/sys-content/tableOtherAnnouncement.html"},

"招标公告":{
    "iColumns": 10,
    "sColumns": ",,,,,,,,,",
    "amDataProp": ["id", "", "announcementName", "announceTime", "annoPubContent", "projType", "reglQuth", "signEndTime", "fundsSource", "announceType"],
    "abSortable": [true, false, false, false, false, false, true, true, true, true],
    "aiSortCol": [0],
    "asSortDir": ["asc"],
    "iSortingCols": 1,
    "asSearch": ["projType", "announceTime", "projName", "reglQuth", "fundsSource", "announceType"],
    "asSearchVal": ["", "", "", "", "", ""],
    "url": "https://zbtb.caac.gov.cn/sys-content/tableZbgg.html"}
    }
    dupurl = get_dupurl(allowed_domains[0])

    def __init__(self, goon=None, *args, **kwargs):
        super(CaacSpider, self).__init__(*args, **kwargs)
        self.goon = goon
        

    def start_requests(self):
        meta = {}

        print('-------------------',self.goon)

        for i in self.dateInfo.keys():
            meta['vertItem'] = {}
            meta['vertItem']['site'] = self.allowed_domains[0]
            meta['dataForm'] = self.dateInfo[i]
            meta['postUrl'] = meta['dataForm']['url']
            del meta['dataForm']['url']
            meta['dataForm']['iDisplayStart'] = 0
            meta['dataForm']['iDisplayLength'] = 100
            meta['dataForm']["sEcho"] = 0
            meta['vertItem']['subclass'] = i
            yield scrapy.Request(
                method='POST',
                url=meta['postUrl'],
                callback=self.parse,
                meta=meta,
                dont_filter=True,
                body=json.dumps(meta['dataForm']),
                headers=HEA
            )

    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)['aaData']
        pprint.pprint(jsonT)
        print('---------------------------',meta['vertItem']['subclass'],meta['dataForm']['iDisplayStart'])

        # meta['dataForm']['iDisplayStart'] += meta['dataForm']['iDisplayLength']
        # yield scrapy.Request(
        #     method='POST',
        #     url=self.start_urls[0],
        #     callback=self.parse,
        #     meta=meta,
        #     dont_filter=True,
        #     body=json.dumps(meta['dataForm']),
        #     headers=HEA
        # )


