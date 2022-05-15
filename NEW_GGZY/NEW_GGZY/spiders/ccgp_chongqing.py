# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpChongqingSpider(scrapy.Spider):
    name = 'ccgp_chongqing'
    allowed_domains = ['www.cqgp.gov.cn']
    urlList = [{'catName': '重庆市_采购公告','url': 'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi={}&ps=50&type=100,200,201,202,203,204,205,206,207,309,400,401,402,3091,4001'},
        {'catName': '重庆市_采购预公示','url': 'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi={}&ps=50&type=301,303'},
        {'catName': '重庆市_采购结果公告','url': 'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable?pi={}&ps=50&type=300,302,304,3041,305,306,307,308'}]
    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)
    def parse(self, response):
        meta = response.meta
        urlListTemp = []
        jsonT = json.loads(response.text)['notices']
        jsonT.append('0000')
        ContentBaseUrl = 'https://www.cqgp.gov.cn/notices/detail/{}'
        GotArtcl = 0
        notGotArtcl = 0
        for i in jsonT:
            urlListTemp =[]
            # print('进入List循环体了')
            if notGotArtcl == 0 and GotArtcl == len(jsonT) - 1:
                # print('-------------------------------没有新文章退出')
                return None
            elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(jsonT) - 1:
                # print('--------------------翻页')
                meta['Num'] += 1
                yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta,
                                     dont_filter=True)
            else:
                # print('--------------------最终进入文章')
                meta['catName1'] = meta['catName'] + '_' + i['districtName']
                meta['issueTime'] = i['issueTime']
                meta['title'] = i['title']
                meta['id'] = i['id']
                meta['ContentUrl'] = ContentBaseUrl.format(str(meta['id']))

                urlListTemp.append(meta['ContentUrl'] + TEMPPATH)
                urllist = urlIsExist(urlListTemp)
                if len(urllist) < 1:
                    GotArtcl += 1
                    continue
                else:
                    notGotArtcl += 1
                    ContentRequestUrlBase = 'https://www.cqgp.gov.cn/gwebsite/api/v1/notices/stable/{}'
                    yield scrapy.Request(url=ContentRequestUrlBase.format(str(meta['id'])),
                                         callback=self.parseA, meta=meta,
                                         dont_filter=True)
    def parseA(self, response):
        # print('进入文章了')
        try:
            jsonT = json.loads(response.text)['notice']
        except:
            return None
        meta = response.meta
        dict1 = {}
        dict1['url'] = meta['ContentUrl']
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['title']
        dict1['issueTime'] = timeReMark(meta['issueTime'])
        dict1['content'] = jsonT['html']
        dict1['subclass'] = meta['catName1']+ "_" + jsonT['projectPurchaseWayName']
        requestsAPI = save_api(dict1)

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print(len(dict1['content']))
        print(requestsAPI.text)
        print('----------------------------------------------------------------------------------------------------')


