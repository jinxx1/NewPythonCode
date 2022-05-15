# -*- coding: utf-8 -*-
import scrapy
# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,datetime
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpHunanSpider(scrapy.Spider):
    name = 'ccgp_hunan'
    allowed_domains = ['www.ccgp-hunan.gov.cn']
    urlList = [{'catName': '湖南省_省级', 'url': 'http://www.ccgp-hunan.gov.cn/mvc/getNoticeList4Web.do', 'endYear': '2015'},
               {'catName': '湖南省_区县', 'url': 'http://www.ccgp-hunan.gov.cn/mvc/getNoticeListOfCityCounty.do', 'endYear': '2016'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            meta['endYear'] = i['endYear']
            try:
                startYear = i['startYear']
            except:
                startYear = int(str(datetime.datetime.now()).split(' ')[0].split('-')[0])
            for Year in range(startYear,int(meta['endYear']) - 1,-1):
                meta['startYear'] = str(Year)
                meta['startDate'] = meta['startYear'] + "-01-01"
                meta['endDate'] = meta['startYear']  + "-12-31"
                datapost = {
                    'startDate': meta['startDate'],
                    'endDate': meta['endDate'],
                    'page': str(meta['Num']),
                    'pageSize': '200'
                }
                yield scrapy.FormRequest(url=meta['url'],formdata=datapost,callback=self.parseList,meta=meta,dont_filter=True)


    def parseList(self, response):
        meta = response.meta
        if meta['endYear'] == '2015':
            jsonT = json.loads(response.text)['rows']
            ContentBaseUrl = 'http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp?noticeId={}'
            ContentRequestUrlBase = 'http://www.ccgp-hunan.gov.cn/mvc/viewNoticeContent.do?noticeId={}&area_id='
        else:
            jsonT = json.loads(response.text)
            ContentBaseUrl = 'http://www.ccgp-hunan.gov.cn/page/notice/notice.jsp?noticeId={}&area_id=1'
            ContentRequestUrlBase = 'http://www.ccgp-hunan.gov.cn/mvc/viewNoticeContent.do?noticeId={}&area_id=1'


        jsonT.append('0000')

        GotArtcl = 0
        notGotArtcl = 0

        for i in jsonT:
            urlListTemp = []
            # print('进入List循环体了')
            if notGotArtcl == 0 and GotArtcl == len(jsonT) - 1:
                # print('-------------------------------没有新文章退出')
                return None
            elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(jsonT) - 1:
                # print('--------------------翻页')
                meta['Num'] += 1
                datapost = {
                    'startDate': meta['startDate'],
                    'endDate': meta['endDate'],
                    'page': str(meta['Num']),
                    'pageSize': '200'
                }
                yield scrapy.FormRequest(url=meta['url'], formdata=datapost, callback=self.parseList, meta=meta,
                                         dont_filter=True)
            else:
                # print('--------------------最终进入文章')
                meta['catName1'] = meta['catName'] + '_' + i['AREA_NAME'] + '_' + i['NOTICE_NAME'] + '_' + i['PRCM_MODE_NAME']
                meta['issueTime'] = i['NEWWORK_DATE']
                meta['title'] = i['NOTICE_TITLE']
                meta['id'] = i['NOTICE_ID']
                meta['ContentUrl'] = ContentBaseUrl.format(str(meta['id']))
                urlListTemp.append(meta['ContentUrl'] + TEMPPATH)
                urllist = urlIsExist(urlListTemp)
                if len(urllist) < 1:
                    GotArtcl += 1
                    continue
                else:
                    notGotArtcl += 1
                    yield scrapy.Request(url=ContentRequestUrlBase.format(str(meta['id'])),
                                         callback=self.parseA, meta=meta,
                                         dont_filter=True)

    def parseA(self, response):
        meta=response.meta
        dict1 = {}
        try:
            html = response.xpath("//body//table | //body/div").extract()[0]
            dict1['content'] = html
            dict1['url'] = meta['ContentUrl']
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = meta['title']
            dict1['issueTime'] = timeReMark(meta['issueTime'])
            dict1['subclass'] = meta['catName1']
            requestsAPI = save_api(dict1)

            tempDict = meta['Breakpoint']
            tempDict['Num'] = meta['Num']
            tempDict['startYear'] = meta['startYear']
            writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

            print(dict1['title'])
            print(dict1['url'])
            print(dict1['issueTime'])
            print(dict1['subclass'])
            print(len(dict1['content']))
            print(requestsAPI.text)
            print('----------------------------------------------------------------------------------')

        except:
            if 'area_id=1' in response.url:
                reUrl = response.url
                Urlrequest = reUrl.replace('area_id=1','area_id=')
                yield scrapy.Request(url=Urlrequest,
                                     callback=self.parseA, meta=meta,
                                     dont_filter=True)
            else:
                return None