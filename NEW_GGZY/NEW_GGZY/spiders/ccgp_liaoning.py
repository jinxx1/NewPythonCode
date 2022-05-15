# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem




class CcgpLiaoningSpider(scrapy.Spider):
    name = 'ccgp_liaoning'
    allowed_domains = ['www.ccgp-liaoning.gov.cn']
    urlList = [{'catName': '辽宁省_采购公告', 'lbcode': '1001'},
               {'catName': '辽宁省_单一来源公示', 'lbcode': '1008'},
               {'catName': '辽宁省_结果公告', 'lbcode': '1002'},
               {'catName': '辽宁省_采购文件公示', 'lbcode': '1007'},
               {'catName': '辽宁省_更正公告', 'lbcode': '1003'}
               ]

    base_url = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoList&t_k=null'



    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['lbcode'] = i['lbcode']
            datePost = {
            'current': str(meta['Num']),
            'rowCount': '100',
            'infoTypeCode':str(meta['lbcode'])
}
            yield scrapy.FormRequest(url=self.base_url,formdata=datePost,callback=self.parse,meta=meta,dont_filter=True)


    def parse(self, response):

        meta = response.meta
        try:
            jsonT = json.loads(response.text)['rows']
        except:
            return None

        listUrl = []
        listDict = []
        for jsoninfo in jsonT:
            contentDict = {}
            contentDict['catNameList'] = meta['catName'].split('_')

            try:
                contentDict['articleTime'] = jsoninfo['releaseDate']
                contentDict['title'] = jsoninfo['title']
                article_id = jsoninfo['id']
                contentDict['ContentUrl'] = 'http://www.ccgp-liaoning.gov.cn/portalindex.do?method=getPubInfoViewOpen&infoId=' + article_id
                listUrl.append(contentDict['ContentUrl'])
            except:
                continue

            try:
                districtName = jsoninfo['districtName']
            except:
                districtName = '未知地区'

            try:
                infoTypeName = jsoninfo['infoTypeName']
            except:
                infoTypeName = ''

            if contentDict['catNameList'][1] != infoTypeName:
                contentDict['catName'] = contentDict['catNameList'][0] + '_' + districtName + '_' + contentDict['catNameList'][1] + '_' + infoTypeName
            else:
                contentDict['catName'] = contentDict['catNameList'][0] + '_' + districtName + '_' + contentDict['catNameList'][1]

            listDict.append(contentDict)


        urllist = urlIsExist(listUrl)


        if not urllist:
            return None
        else:
            for contentUrl in listUrl:
                for dictinfo in listDict:
                    if contentUrl == dictinfo['ContentUrl']:
                        dictinfo['Num'] = meta['Num']
                        dictinfo['lbcode'] = meta['lbcode']
                        dictinfo['Breakpoint'] = meta['Breakpoint']
                        yield scrapy.Request(url = contentUrl,callback=self.parseA,dont_filter=True,meta=dictinfo)


        meta['Num'] +=1
        datePost = {
            'current': str(meta['Num']),
            'rowCount': '100',
            'infoTypeCode': str(meta['lbcode'])
        }
        yield scrapy.FormRequest(url=self.base_url, formdata=datePost, callback=self.parse, meta=meta, dont_filter=True)


    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        dict1 = GgzyItem()
        try:
            html = response.xpath("//*[@id = 'template']").extract()[0]
            dict1['content'] = html.replace('&lt;','<').replace('&gt;','>').replace('&#034;','\"').replace('display:none','')
        except:
            return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['title'].strip()
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['subclass'] = meta['catName']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        yield dict1
