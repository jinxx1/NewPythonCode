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

class CcgpQinghaiSpider(scrapy.Spider):
    name = 'ccgp_qinghai'
    allowed_domains = ['www.ccgp-qinghai.gov.cn']
    base_url = 'http://www.ccgp-qinghai.gov.cn/front/search/category'


    urlList =[{'catName': '青海省_电子卖场公告', 'url': 'ZcyAnnouncement8'}, {'catName': '青海省_合同公告', 'url': 'ZcyAnnouncement5'}, {'catName': '青海省_资格预审公告', 'url': 'ZcyAnnouncement8888'}, {'catName': '青海省_废流标公告', 'url': 'ZcyAnnouncement9999'}, {'catName': '青海省_变更公告', 'url': 'ZcyAnnouncement3'}, {'catName': '青海省_中标公告', 'url': 'ZcyAnnouncement4'}, {'catName': '青海省_单一来源招标公告', 'url': 'ZcyAnnouncement1002'}, {'catName': '青海省_询价采购公告', 'url': 'ZcyAnnouncement3003'}, {'catName': '青海省_竞争性磋商公告', 'url': 'ZcyAnnouncement3011'}, {'catName': '青海省_竞争性谈判公告', 'url': 'ZcyAnnouncement3002'}, {'catName': '青海省_邀请招标公告', 'url': 'ZcyAnnouncement3009'}, {'catName': '青海省_公开招标', 'url': 'ZcyAnnouncement2'}, {'catName': '青海省_采购公示', 'url': 'ZcyAnnouncement1'}]


    # urlList = [{'catName': '青海省_电子卖场公告', 'url': '*6zcyannouncement86*'}]

    def start_requests(self):
        meta = {}
        meta['hearders'] = {'Content-Type':'application/json'}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = 0
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            datePost = {
	"pageNo": str(meta['Num']),
	"pageSize": '50',
	"categoryCode": meta['url'],
	"districtCode": ["639900"]
}
            yield scrapy.Request(url=self.base_url,method='POST',dont_filter=True,callback=self.parse,body=json.dumps(datePost),headers=meta['hearders'],meta=meta)

    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)['hits']['hits']
        jsonT.append('0000')

        GotArtcl = 0
        notGotArtcl = 0

        for xx in jsonT:
            try:
                i = xx['_source']
            except:
                return None

            urlListTemp = []
            # print('进入List循环体了')
            if notGotArtcl == 0 and GotArtcl == len(jsonT) - 1:
                # print('-------------------------------没有新文章退出')
                return None
            elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(jsonT) - 1:
                # print('--------------------翻页')
                meta['Num'] += 1
                datePost = {
                    "pageNo": str(meta['Num']),
                    "pageSize": '50',
                    "categoryCode": meta['url'],
                    "districtCode": ["639900"]
                }
                yield scrapy.Request(url=self.base_url, method='POST', dont_filter=True, callback=self.parse,
                                     body=json.dumps(datePost), headers=meta['hearders'], meta=meta)
            else:
                # print('--------------------最终进入文章')
                try:
                    localName = i['districtName']
                except:
                    localName = ''

                meta['catName1'] = meta['catName'] + '_' + i['pathName'].replace('|','_') + '_' + localName

                try:
                    meta['attachmentUrl'] = i['attachmentUrl']
                    fujianName = meta['attachmentUrl'].split('.')
                    meta['attachmentName'] = i['title'] + '.' + fujianName[len(fujianName)-1]
                except:
                    pass

                meta['issueTime'] = timestamp_datetime(i['publishDate'])

                meta['title'] = i['title']
                meta['ContentUrl'] = 'http://www.ccgp-qinghai.gov.cn' + i['url']
                urlListTemp.append(meta['ContentUrl'] + TEMPPATH)
                urllist = urlIsExist(urlListTemp)

                if len(urllist) < 1:
                    GotArtcl += 1
                    continue

                else:
                    notGotArtcl += 1
                    yield scrapy.Request(url=meta['ContentUrl'],
                                         callback=self.parseA, meta=meta,
                                         dont_filter=True)

    def parseA(self, response):

        meta = response.meta
        dict1 = GgzyItem()
        try:
            inputWord = response.xpath("//input[@name = 'articleDetail']/@value").extract()[0]
            html = re.findall("content\"\:\"(.*?)\"\,",inputWord)[0]
            dict1['content'] = html
        except:
            return None

        try:
            attachmentListJsonList = []
            dict1['attachmentListJson'] = []
            attachmentDict = {}
            attachmentDict['downloadUrl'] = meta['attachmentUrl']
            attachmentDict['name'] = meta['attachmentName']
            attachmentListJsonList.append(attachmentDict)
            dict1['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)
            print(dict1['attachmentListJson'])
        except:
            pass



        dict1['url'] = meta['ContentUrl']
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['title']
        dict1['issueTime'] = timeReMark(meta['issueTime'])
        dict1['subclass'] = meta['catName1']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))
        yield dict1

        # print(dict1['title'])
        # print(dict1['url'])
        # print(dict1['issueTime'])
        # print(dict1['subclass'])
        # print(len(dict1['content']))
        # save_api(dict1)
        # print('----------------------------------------------------------------------------------')





