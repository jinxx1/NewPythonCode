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
Content-Length: 162
Content-Type: application/json
Host: www.ccgp-guizhou.gov.cn
Origin: http://www.ccgp-guizhou.gov.cn
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36
X-Requested-With: XMLHttpRequest'''

headers = dict(line.split(": ", 1) for line in hub_HeadersWord.split("\n") if line != '')

location = ["529900", "520100", "520200", "520300", "520400", "520500", "520600", "520800", "520900", "522300",
            "522600", "522700"]

urlList_all = [
    {'subclassName': '采购公告_招标公告', 'subclassCode': 'ZcyAnnouncement3001', 'purchaseName': '公开招标',
     'purchaseCode': '1'},
    {'subclassName': '采购意向_采购意向公开', 'subclassCode': 'ZcyAnnouncement10016', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购意向_采购意向公开', 'subclassCode': 'ZcyAnnouncement10016', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购意向_采购意向公开', 'subclassCode': 'ZcyAnnouncement10016', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购意向_采购意向公开', 'subclassCode': 'ZcyAnnouncement10016', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购意向_采购意向公开', 'subclassCode': 'ZcyAnnouncement10016', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购意向_采购意向公开', 'subclassCode': 'ZcyAnnouncement10016', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购意向_采购意向公开', 'subclassCode': 'ZcyAnnouncement10016', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购意向_采购意向公开', 'subclassCode': 'ZcyAnnouncement10016', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '采购需求公示_采购文件需求公示', 'subclassCode': 'ZcyAnnouncement3014', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购需求公示_采购文件需求公示', 'subclassCode': 'ZcyAnnouncement3014', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购需求公示_采购文件需求公示', 'subclassCode': 'ZcyAnnouncement3014', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购需求公示_采购文件需求公示', 'subclassCode': 'ZcyAnnouncement3014', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购需求公示_采购文件需求公示', 'subclassCode': 'ZcyAnnouncement3014', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购需求公示_采购文件需求公示', 'subclassCode': 'ZcyAnnouncement3014', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购需求公示_采购文件需求公示', 'subclassCode': 'ZcyAnnouncement3014', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购需求公示_采购文件需求公示', 'subclassCode': 'ZcyAnnouncement3014', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '采购需求公示_单一来源公示', 'subclassCode': 'ZcyAnnouncement3012', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购需求公示_单一来源公示', 'subclassCode': 'ZcyAnnouncement3012', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购需求公示_单一来源公示', 'subclassCode': 'ZcyAnnouncement3012', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购需求公示_单一来源公示', 'subclassCode': 'ZcyAnnouncement3012', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购需求公示_单一来源公示', 'subclassCode': 'ZcyAnnouncement3012', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购需求公示_单一来源公示', 'subclassCode': 'ZcyAnnouncement3012', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购需求公示_单一来源公示', 'subclassCode': 'ZcyAnnouncement3012', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购需求公示_单一来源公示', 'subclassCode': 'ZcyAnnouncement3012', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '采购公告_资格预审公告', 'subclassCode': 'ZcyAnnouncement33', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购公告_资格预审公告', 'subclassCode': 'ZcyAnnouncement33', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购公告_资格预审公告', 'subclassCode': 'ZcyAnnouncement33', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购公告_资格预审公告', 'subclassCode': 'ZcyAnnouncement33', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购公告_资格预审公告', 'subclassCode': 'ZcyAnnouncement33', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购公告_资格预审公告', 'subclassCode': 'ZcyAnnouncement33', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购公告_资格预审公告', 'subclassCode': 'ZcyAnnouncement33', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购公告_资格预审公告', 'subclassCode': 'ZcyAnnouncement33', 'purchaseName': '其它',
            'purchaseCode': '9'},

           {'subclassName': '采购公告_招标公告', 'subclassCode': 'ZcyAnnouncement3001', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购公告_招标公告', 'subclassCode': 'ZcyAnnouncement3001', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购公告_招标公告', 'subclassCode': 'ZcyAnnouncement3001', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购公告_招标公告', 'subclassCode': 'ZcyAnnouncement3001', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购公告_招标公告', 'subclassCode': 'ZcyAnnouncement3001', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购公告_招标公告', 'subclassCode': 'ZcyAnnouncement3001', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购公告_招标公告', 'subclassCode': 'ZcyAnnouncement3001', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '采购公告_非招标公告', 'subclassCode': 'ZcyAnnouncement333', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购公告_非招标公告', 'subclassCode': 'ZcyAnnouncement333', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购公告_非招标公告', 'subclassCode': 'ZcyAnnouncement333', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购公告_非招标公告', 'subclassCode': 'ZcyAnnouncement333', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购公告_非招标公告', 'subclassCode': 'ZcyAnnouncement333', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购公告_非招标公告', 'subclassCode': 'ZcyAnnouncement333', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购公告_非招标公告', 'subclassCode': 'ZcyAnnouncement333', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购公告_非招标公告', 'subclassCode': 'ZcyAnnouncement333', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '更正公告_更正公告', 'subclassCode': 'ZcyAnnouncement3005', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '更正公告_更正公告', 'subclassCode': 'ZcyAnnouncement3005', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '更正公告_更正公告', 'subclassCode': 'ZcyAnnouncement3005', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '更正公告_更正公告', 'subclassCode': 'ZcyAnnouncement3005', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '更正公告_更正公告', 'subclassCode': 'ZcyAnnouncement3005', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '更正公告_更正公告', 'subclassCode': 'ZcyAnnouncement3005', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '更正公告_更正公告', 'subclassCode': 'ZcyAnnouncement3005', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '更正公告_更正公告', 'subclassCode': 'ZcyAnnouncement3005', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '采购结果公告_中标(成交)结果公告', 'subclassCode': 'ZcyAnnouncement3004', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购结果公告_中标(成交)结果公告', 'subclassCode': 'ZcyAnnouncement3004', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购结果公告_中标(成交)结果公告', 'subclassCode': 'ZcyAnnouncement3004', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购结果公告_中标(成交)结果公告', 'subclassCode': 'ZcyAnnouncement3004', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购结果公告_中标(成交)结果公告', 'subclassCode': 'ZcyAnnouncement3004', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购结果公告_中标(成交)结果公告', 'subclassCode': 'ZcyAnnouncement3004', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购结果公告_中标(成交)结果公告', 'subclassCode': 'ZcyAnnouncement3004', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购结果公告_中标(成交)结果公告', 'subclassCode': 'ZcyAnnouncement3004', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '采购结果公告_终止公告', 'subclassCode': 'ZcyAnnouncement3015', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购结果公告_终止公告', 'subclassCode': 'ZcyAnnouncement3015', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购结果公告_终止公告', 'subclassCode': 'ZcyAnnouncement3015', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购结果公告_终止公告', 'subclassCode': 'ZcyAnnouncement3015', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购结果公告_终止公告', 'subclassCode': 'ZcyAnnouncement3015', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购结果公告_终止公告', 'subclassCode': 'ZcyAnnouncement3015', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购结果公告_终止公告', 'subclassCode': 'ZcyAnnouncement3015', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购结果公告_终止公告', 'subclassCode': 'ZcyAnnouncement3015', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '采购结果公告_采购结果变更公告', 'subclassCode': 'ZcyAnnouncement3017', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购结果公告_采购结果变更公告', 'subclassCode': 'ZcyAnnouncement3017', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购结果公告_采购结果变更公告', 'subclassCode': 'ZcyAnnouncement3017', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购结果公告_采购结果变更公告', 'subclassCode': 'ZcyAnnouncement3017', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购结果公告_采购结果变更公告', 'subclassCode': 'ZcyAnnouncement3017', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购结果公告_采购结果变更公告', 'subclassCode': 'ZcyAnnouncement3017', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购结果公告_采购结果变更公告', 'subclassCode': 'ZcyAnnouncement3017', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购结果公告_采购结果变更公告', 'subclassCode': 'ZcyAnnouncement3017', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '采购结果公告_废标公告', 'subclassCode': 'ZcyAnnouncement3007', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购结果公告_废标公告', 'subclassCode': 'ZcyAnnouncement3007', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购结果公告_废标公告', 'subclassCode': 'ZcyAnnouncement3007', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购结果公告_废标公告', 'subclassCode': 'ZcyAnnouncement3007', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购结果公告_废标公告', 'subclassCode': 'ZcyAnnouncement3007', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购结果公告_废标公告', 'subclassCode': 'ZcyAnnouncement3007', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购结果公告_废标公告', 'subclassCode': 'ZcyAnnouncement3007', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购结果公告_废标公告', 'subclassCode': 'ZcyAnnouncement3007', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '采购合同公告_采购合同公告', 'subclassCode': 'ZcyAnnouncement3010', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '采购合同公告_采购合同公告', 'subclassCode': 'ZcyAnnouncement3010', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '采购合同公告_采购合同公告', 'subclassCode': 'ZcyAnnouncement3010', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '采购合同公告_采购合同公告', 'subclassCode': 'ZcyAnnouncement3010', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '采购合同公告_采购合同公告', 'subclassCode': 'ZcyAnnouncement3010', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '采购合同公告_采购合同公告', 'subclassCode': 'ZcyAnnouncement3010', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '采购合同公告_采购合同公告', 'subclassCode': 'ZcyAnnouncement3010', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '采购合同公告_采购合同公告', 'subclassCode': 'ZcyAnnouncement3010', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '履约验收公告_公共服务项目验收结果公告', 'subclassCode': 'ZcyAnnouncement3016', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '履约验收公告_公共服务项目验收结果公告', 'subclassCode': 'ZcyAnnouncement3016', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '履约验收公告_公共服务项目验收结果公告', 'subclassCode': 'ZcyAnnouncement3016', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '履约验收公告_公共服务项目验收结果公告', 'subclassCode': 'ZcyAnnouncement3016', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '履约验收公告_公共服务项目验收结果公告', 'subclassCode': 'ZcyAnnouncement3016', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '履约验收公告_公共服务项目验收结果公告', 'subclassCode': 'ZcyAnnouncement3016', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '履约验收公告_公共服务项目验收结果公告', 'subclassCode': 'ZcyAnnouncement3016', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '履约验收公告_公共服务项目验收结果公告', 'subclassCode': 'ZcyAnnouncement3016', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': '履约验收公告_其他履约验收公告', 'subclassCode': 'ZcyAnnouncement6003', 'purchaseName': '公开招标',
            'purchaseCode': '1'},
           {'subclassName': '履约验收公告_其他履约验收公告', 'subclassCode': 'ZcyAnnouncement6003', 'purchaseName': '邀请招标',
            'purchaseCode': '2'},
           {'subclassName': '履约验收公告_其他履约验收公告', 'subclassCode': 'ZcyAnnouncement6003', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': '履约验收公告_其他履约验收公告', 'subclassCode': 'ZcyAnnouncement6003', 'purchaseName': '询价采购',
            'purchaseCode': '4'},
           {'subclassName': '履约验收公告_其他履约验收公告', 'subclassCode': 'ZcyAnnouncement6003', 'purchaseName': '单一来源',
            'purchaseCode': '5'},
           {'subclassName': '履约验收公告_其他履约验收公告', 'subclassCode': 'ZcyAnnouncement6003', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': '履约验收公告_其他履约验收公告', 'subclassCode': 'ZcyAnnouncement6003', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': '履约验收公告_其他履约验收公告', 'subclassCode': 'ZcyAnnouncement6003', 'purchaseName': '其它',
            'purchaseCode': '9'},
           {'subclassName': 'PPP项目公示', 'subclassCode': 'ZcyAnnouncement9', 'purchaseName': '公开招标', 'purchaseCode': '1'},
           {'subclassName': 'PPP项目公示', 'subclassCode': 'ZcyAnnouncement9', 'purchaseName': '邀请招标', 'purchaseCode': '2'},
           {'subclassName': 'PPP项目公示', 'subclassCode': 'ZcyAnnouncement9', 'purchaseName': '竞争性谈判',
            'purchaseCode': '3'},
           {'subclassName': 'PPP项目公示', 'subclassCode': 'ZcyAnnouncement9', 'purchaseName': '询价采购', 'purchaseCode': '4'},
           {'subclassName': 'PPP项目公示', 'subclassCode': 'ZcyAnnouncement9', 'purchaseName': '单一来源', 'purchaseCode': '5'},
           {'subclassName': 'PPP项目公示', 'subclassCode': 'ZcyAnnouncement9', 'purchaseName': '竞争性磋商',
            'purchaseCode': '6'},
           {'subclassName': 'PPP项目公示', 'subclassCode': 'ZcyAnnouncement9', 'purchaseName': '电子卖场',
            'purchaseCode': '70'},
           {'subclassName': 'PPP项目公示', 'subclassCode': 'ZcyAnnouncement9', 'purchaseName': '其它', 'purchaseCode': '9'}
]


class GuizhouCcgpSpider(scrapy.Spider):
    name = 'guizhou_ccgp'
    allowed_domains = ['www.ccgp-guizhou.gov.cn']
    baseUrl = "http://www.ccgp-guizhou.gov.cn/front/search/category"
    pageS = 15

    urlList = urlList_all

    # urlList = [
    #     {'subclassName': '采购公告_招标公告', 'subclassCode': 'ZcyAnnouncement3001', 'purchaseName': '公开招标',
    #      'purchaseCode': '1'}
    # ]

    def __init__(self, goon=None, startTime=None, endTime=None, *args, **kwargs):
        super(GuizhouCcgpSpider, self).__init__(*args, **kwargs)
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
                print('into   hub')
                # if num == 1:
                #     break
                meta['breakMark'] = 0
                meta['pageNum'] = 1

                meta['purchaseName'] = i['purchaseName']
                meta['subclassName'] = i['subclassName']
                meta['subclassCode'] = i['subclassCode']
                meta['purchaseCode'] = i['purchaseCode']

                postdata = {"districtCode": location,
                            "categoryCode": meta['subclassCode'],
                            "pageSize": str(self.pageS),
                            "pageNo": str(meta['pageNum']),
                            "publishDateBegin": self.startT,
                            "publishDateEnd": self.endT,
                            "procurementMethodCode": meta['purchaseCode']}
                # print(postdata)
                yield scrapy.Request(url=self.baseUrl,
                                     method='POST',
                                     body=json.dumps(postdata),
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
        # pprint.pprint(jsonT)

        try:
            pageInfoList =jsonT['hits']['hits']
            total = jsonT['hits']['total']
            if not pageInfoList:
                return None
        except:
            return None

        mark = 0
        for pageInfo in pageInfoList:
            # print(pageInfo)
            # print('---------------------------------')

            hubItem = ShangqingHubItem()
            hubItem['site'] = self.allowed_domains[0]
            hubItem['subclass'] = meta['subclassName']
            hubItem['purchase_type'] = meta['purchaseName']

            try:
                hubItem['issue_time'] = timestampREtimestr(pageInfo['_source']['publishDate'])
                hubItem['title'] = pageInfo['_source']['title']
                page_url = urlpase.urljoin(base="http://www.ccgp-guizhou.gov.cn/", url=pageInfo['_source']['url'])
            except Exception as ff:
                print(ff)
                continue


            if bl.exists(page_url) or bh.exists(page_url):
                print('exists true')
                mark += 1
                continue
            hubItem['page_url'] = page_url


            try:
                hubItem['ztb_ztbInfo_bidDate'] = timestampREtimestr(pageInfo['_source']['bidOpeningTime'])
            except:
                pass

            try:
                city = pageInfo['_source']['districtName']
            except Exception as fff:
                city = ''

            province_name_dict = tureLocation(localName='贵州省',title=city + hubItem['title'])
            hubItem['province_name'] = province_name_dict['province_name']
            if province_name_dict['city_name']:
                hubItem['city_name'] = province_name_dict['city_name']
                if len(province_name_dict['city_name']) <= 2:
                    hubItem['city_name'] = ''
            else:
                hubItem['city_name'] = ''



            getDict = [
                {"itemkey":"subclass","pagekey":"pathName"},
                {"itemkey": "purchase_type", "pagekey": "procurementMethod"},
                {"itemkey": "business_type", "pagekey": "gpCatalogType"},
            ]

            for nn in getDict:
                pageKey = nn['pagekey']
                itemKey = nn["itemkey"]
                try:
                    if pageInfo['_source'][pageKey]:
                        hubItem[itemKey] = pageInfo['_source'][pageKey]
                except:
                    continue


            # pprint.pprint(hubItem)
            yield hubItem
            # print('--------------------------------')

        print('本页有多少篇文章：', len(pageInfoList))
        print('本页已录入{}文章：。未录入{}文章'.format(mark,len(pageInfoList)-mark))
        print('subclass：{}  pusrchase：{}  pageNum：{}'.format(meta['subclassName'], meta['purchaseName'],meta['pageNum']))
        print('*******************************************'*2,)

        if mark == len(pageInfoList):
            meta['breakMark'] += 1
        else:
            meta['breakMark'] = 0

        if meta['breakMark'] == 3:
            return None

        if total % self.pageS == 0:
            allPage = total // self.pageS
        else:
            allPage = total // self.pageS + 1

        if meta['pageNum'] >= allPage:
            return None
        print('---------------------------------------', meta['pageNum'])
        meta['pageNum'] += 1

        postdata = {"districtCode": location,
                    "categoryCode": meta['subclassCode'],
                    "pageSize": str(self.pageS),
                    "pageNo": str(meta['pageNum']),
                    "publishDateBegin": self.startT,
                    "publishDateEnd": self.endT,
                    "procurementMethodCode": meta['purchaseCode']}
        # print(postdata)
        yield scrapy.Request(url=self.baseUrl,
                             method='POST',
                             body=json.dumps(postdata),
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


        soup = BeautifulSoup(response.text,'lxml')
        content_json = soup.find('input',attrs={"name":"articleDetail"}).get('value')
        content_dict = json.loads(content_json)

        # pprint.pprint(content_dict)

        content_soup = BeautifulSoup(content_dict['content'],'lxml')

        articleInfo['content'] = content_soup.prettify()

        attch_soupall = content_soup.find_all(href=re.compile("gzdata"))
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