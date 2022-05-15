# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/13
# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/12
import os,json,datetime
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql
r = Redis('127.0.0.1',6379)

class MinhangSpider(scrapy.Spider):
    name = 'gc_mh'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        {'url':'https://zbtb.caac.gov.cn/sys-content/tableZbgg.html','page':20},  # 190
        {'url':'https://zbtb.caac.gov.cn/sys-content/tableZbgs.html','page':20},  # 129
        {'url':'https://zbtb.caac.gov.cn/sys-content/table.html','page':3},
        {'url':'https://zbtb.caac.gov.cn/sys-content/tableOtherAnnouncement.html','page':3}
    ]
    def start_requests(self):
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Referer': 'https://zbtb.caac.gov.cn/sys-content/index/zbggList.html',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'zbtb.caac.gov.cn',
            'Origin': 'https://zbtb.caac.gov.cn',
        }
        for dic in self.start_urls:
            if dic['url'] == 'https://zbtb.caac.gov.cn/sys-content/tableZbgg.html':
                for page in range(1,dic['page']):
                    data_zbgg = {"sEcho": page,
                            "iDisplayStart": (page - 1) * 15,
                            "iColumns": 10,
                            "sColumns": ",,,,,,,,,",
                            "iDisplayLength": 15,
                            "amDataProp": ["id", "", "announcementName", "announceTime", "annoPubContent", "projType",
                                           "reglQuth",
                                           "signEndTime", "fundsSource", "announceType"],
                            "abSortable": ["true", "false", "false", "false", "false", "false", "true", "true", "true", "true"],
                            "aiSortCol": [0],
                            "asSortDir": ["asc"],
                            "iSortingCols": 1,
                            "asSearch": ["projType", "announceTime", "projName", "reglQuth", "fundsSource", "announceType"],
                            "asSearchVal": ["", "", "", "", "", ""]}
                    yield scrapy.Request(url=dic['url'],
                                         method='POST',
                                         headers=headers,
                                         body=json.dumps(data_zbgg),
                                         callback=self.parse_zbgg,
                                         dont_filter=True)
            if dic['url'] == 'https://zbtb.caac.gov.cn/sys-content/tableZbgs.html':
                for page in range(1, dic['page']):
                    data_zbgs = {"sEcho":page,"iColumns":13,"sColumns":",,,,,,,,,,,,",
                         "iDisplayStart":(page - 1) * 15,
                         "iDisplayLength":15,
                         "amDataProp":["announceTime","","projName","projType","id","bidPublicityName","reglQuth",
                                       "firstCandidateName","secondCandidateName","thirdCandidateName","id",
                                       "projCode","oldBERId"],
                         "abSortable":['true','false','false','false','false','false','true','true','true','true','true','true','true'],
                         "aiSortCol":[0],"asSortDir":["desc"],"iSortingCols":1,
                         "asSearch":["projType","announceTime","bidPublicityName","reglQuth","projCode"],
                         "asSearchVal":["","","","",""]}
                    yield scrapy.Request(url=dic['url'],
                                         method='POST',
                                         headers=headers,
                                         body=json.dumps(data_zbgs),
                                         callback=self.parse_zbgs,
                                         dont_filter=True)
            if dic['url'] == 'https://zbtb.caac.gov.cn/sys-content/table.html':
                for page in range(1, dic['page']):
                    data_tzgg = {"sEcho":page,"iColumns":4,"sColumns":",,,",
                                 "iDisplayStart":(page - 1) * 15,"iDisplayLength":15,
                                 "amDataProp":["id","name","lastUpdateTime","contentDes"],
                                 "abSortable":['true','false','false','true'],"aiSortCol":[0],"asSortDir":["asc"],
                                 "iSortingCols":1,"asSearch":["groupCode"],"asSearchVal":["TZGG"]}
                    yield scrapy.Request(url=dic['url'],
                                         method='POST',
                                         headers=headers,
                                         body=json.dumps(data_tzgg),
                                         callback=self.parse_tzgg,
                                         dont_filter=True)
            if dic['url'] == 'https://zbtb.caac.gov.cn/sys-content/tableOtherAnnouncement.html':
                for page in range(1, dic['page']):
                    data_qtgg = {"sEcho":2,"iColumns":9,"sColumns":",,,,,,,,","iDisplayStart":0,
                                 "iDisplayLength":15,
                                 "amDataProp":["announceTime","","projName","projType","id","announcementName","reglQuth","id","quafExatMode"],
                                 "abSortable":["true","false","false","false","false","false","true","true","true"],"aiSortCol":[0],
                                 "asSortDir":["desc"],"iSortingCols":1,
                                 "asSearch":["projType","announceTime","announcementName","projName","reglQuth"],
                                 "asSearchVal":["","","","",""]}
                    yield scrapy.Request(url=dic['url'],
                                         method='POST',
                                         headers=headers,
                                         body=json.dumps(data_qtgg),
                                         callback=self.parse_qtgg,
                                         dont_filter=True)
    def parse_zbgs(self,response):
        for info in response.json()['aaData']:
            item = GcProjectItem()
            item['site'] = 'zbtb.caac.gov.cn'
            item['title'] = info['bidPublicityName']
            item['issue_time'] = info['announceTime']
            item['subclass'] = item['title'][-7::]
            item['page_url'] = 'https://zbtb.caac.gov.cn/sys-content/initPage.html?url=zbgsText&id=%s' % info[
                'DT_RowId']
            num = select_mysql("SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
    def parse_zbgg(self, response):
        for info in response.json()['aaData']:
            item = GcProjectItem()
            try:
                item['site'] = 'zbtb.caac.gov.cn'
                item['title'] = info['announcementName']
                item['issue_time'] = info['announceTime']
                item['subclass'] = item['title'][-4::]
                item['page_url'] = 'https://zbtb.caac.gov.cn/sys-content/initPage.html?url=zbgg_init&id=%s' % info[
                    'DT_RowId']
                num = select_mysql(
                    "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
                if num[0]['COUNT(*)'] == 1:
                    yield item
                else:
                    print('该条信息一爬取。。。',datetime.datetime.now())
            except Exception as e:
                print('error:  ',e)
    def parse_tzgg(self, response):
        for info in response.json()['aaData']:
            item = GcProjectItem()
            item['site'] = 'zbtb.caac.gov.cn'
            item['title'] = info['name']
            item['issue_time'] = info['lastUpdateTime']
            item['subclass'] = '通知公告'
            item['page_url'] = 'https://zbtb.caac.gov.cn/sys-content/index/tzggText.html?t=%s' % info['DT_RowId']
            num = select_mysql("SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())
    def parse_qtgg(self,response):
        for info in response.json()['aaData']:
            item = GcProjectItem()
            item['site'] = 'zbtb.caac.gov.cn'
            item['title'] = info['announcementName']
            item['issue_time'] = info['announceTime']
            item['subclass'] = '其它公告'
            item['page_url'] = 'https://zbtb.caac.gov.cn/sys-content/initPage.html?url=qtggText&id=%s' % info['DT_RowId']
            num = select_mysql("SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())

if __name__ == '__main__':
    os.system('scrapy crawl gc_mh')

