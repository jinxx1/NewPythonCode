# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem
TEMPPATH = TMEPTEST()


def timestamp_datetime(timecl):
    intV = int(timecl)/1000
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(intV)
    dt = time.strftime(format,value)
    return dt


class CcgpXinjiangSpider(scrapy.Spider):
    name = 'ccgp_xinjiang'
    allowed_domains = ['www.ccgp-xinjiang.gov.cn']
    base_url = 'http://www.ccgp-xinjiang.gov.cn/front/search/category'

    urlList = [{'catName': '新疆_本级_采购公示', 'categoryCode': 'ZcyAnnouncement1'}, {'catName': '新疆_本级_采购项目公告', 'categoryCode': 'ZcyAnnouncement2'}, {'catName': '新疆_本级_采购结果公告', 'categoryCode': 'ZcyAnnouncement4'}, {'catName': '新疆_本级_采购合同公告', 'categoryCode': 'ZcyAnnouncement5'}, {'catName': '新疆_本级_澄清变更公告', 'categoryCode': 'ZcyAnnouncement3'}, {'catName': '新疆_本级_废标公告', 'categoryCode': 'ZcyAnnouncement10'}, {'catName': '新疆_本级_履约验收', 'categoryCode': 'ZcyAnnouncement6'}, {'catName': '新疆_本级_电子卖场公告', 'categoryCode': 'ZcyAnnouncement8'}, {'catName': '新疆_本级_非政府采购公告', 'categoryCode': 'ZcyAnnouncement9'}, {'catName': '新疆_地州_采购公示', 'categoryCode': 'ZcyAnnouncement1'}, {'catName': '新疆_地州_采购项目公告', 'categoryCode': 'ZcyAnnouncement2'}, {'catName': '新疆_地州_采购结果公告', 'categoryCode': 'ZcyAnnouncement4'}, {'catName': '新疆_地州_采购合同公告', 'categoryCode': 'ZcyAnnouncement5'}, {'catName': '新疆_地州_澄清变更公告', 'categoryCode': 'ZcyAnnouncement3'}, {'catName': '新疆_地州_废标公告', 'categoryCode': 'ZcyAnnouncement10'}, {'catName': '新疆_地州_履约验收', 'categoryCode': 'ZcyAnnouncement6'}, {'catName': '新疆_地州_电子卖场公告', 'categoryCode': 'ZcyAnnouncement8'}, {'catName': '新疆_地州_非政府采购公告', 'categoryCode': 'ZcyAnnouncement9'}]
    bj = ["659900"]
    dizhou = ["650", "652", "653", "654", "659099"]
    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = 1
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['categoryCode'] = i['categoryCode']
            if '本级' in meta['catName']:
                meta['districtCode'] = self.bj
            else:
                meta['districtCode'] = self.dizhou
            datePost = {
                "categoryCode": meta['categoryCode'],
                "districtCode": meta['districtCode'],
                "pageNo": str(meta['Num']),
                "pageSize": "50",
            }
            yield scrapy.Request(url=self.base_url, method='POST', dont_filter=True, callback=self.parse,
                                 body=json.dumps(datePost), headers={'Content-Type': 'application/json'}, meta=meta)

    def parse(self, response):

        meta = response.meta
        meta['Contentdict'] = {}
        jsonT = json.loads(response.text)['hits']['hits']
        urlListTemp = []
        dictList = []
        for xx in jsonT:
            i = xx['_source']
            ddict = {}
            try:
                ddict['catName'] = meta['catName'] + '_' + i['pathName'].replace('|', '_')
            except:
                ddict['catName'] = meta['catName']

            try:
                ddict['attachmentUrl'] = i['attachmentUrl']
                fujianName = ddict['attachmentUrl'].split('.')
                ddict['attachmentName'] = i['title'] + '.' + fujianName[len(fujianName) - 1]
            except:
                pass

            ddict['issueTime'] = timestamp_datetime(i['publishDate'])
            ddict['title'] = i['title']
            ddict['ContentUrl'] = 'http://www.ccgp-xinjiang.gov.cn' + i['url']
            urlListTemp.append(ddict['ContentUrl'] + TEMPPATH)
            dictList.append(ddict)


        urllist = urlIsExist(urlListTemp)

        if urllist:
            for linkurl in urllist:
                for dictlink in dictList:
                    if linkurl == dictlink['ContentUrl']:
                        meta['Contentdict'] = dictlink
                        yield scrapy.Request(url=meta['Contentdict']['ContentUrl'],
                                 callback=self.parseA, meta=meta,
                                 dont_filter=True)
        else:
            return None

        meta['Num'] += 1
        datePost = {
            "categoryCode": meta['categoryCode'],
            "districtCode": meta['districtCode'],
            "pageNo": str(meta['Num']),
            "pageSize": "50",
        }
        yield scrapy.Request(url=self.base_url, method='POST', dont_filter=True, callback=self.parse,
                             body=json.dumps(datePost), headers={'Content-Type': 'application/json'}, meta=meta)


    def parseA(self, response):

        meta = response.meta
        dict1 = GgzyItem()
        try:
            inputWord = response.xpath("//input[@name = 'articleDetail']/@value").extract()[0]
            html = re.findall("content\"\:\"(.*?)\"\,", inputWord)[0]
            dict1['content'] = html
        except:
            return None

        try:
            attachmentListJsonList = []
            dict1['attachmentListJson'] = []
            attachmentDict = {}
            attachmentDict['downloadUrl'] = meta['Contentdict']['attachmentUrl']
            attachmentDict['name'] = meta['Contentdict']['attachmentName']
            attachmentListJsonList.append(attachmentDict)
            dict1['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)
            print(dict1)
        except:
            pass

        dict1['url'] = meta['Contentdict']['ContentUrl']
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['Contentdict']['title']
        dict1['issueTime'] = timeReMark(meta['Contentdict']['issueTime'])
        dict1['subclass'] = meta['Contentdict']['catName']

        yield dict1






