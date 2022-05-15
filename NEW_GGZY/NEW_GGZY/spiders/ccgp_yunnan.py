# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST(112)



class CcgpYunnanSpider(scrapy.Spider):
    name = 'ccgp_yunnan'
    allowed_domains = ['www.ccgp-yunnan.gov.cn']
    urlDict = [{'catName': '云南省_', 'url': '1'}, {'catName': '云南省_', 'url': '2'}, {'catName': '云南省_', 'url': '3'}, {'catName': '云南省_', 'url': '4'}, {'catName': '云南省_', 'url': '5'}, {'catName': '云南省_', 'url': '6'}, {'catName': '云南省_', 'url': '7'}]
    base_url = 'http://www.ccgp-yunnan.gov.cn/bulletin.do?method=moreListQuery'

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlDict)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']

            datePost = {
                'current': str(meta['Num']),
                'rowCount': '200',
                'query_sign':meta['url']
            }
            yield scrapy.FormRequest(url=self.base_url,formdata=datePost,callback=self.parse,meta=meta,dont_filter=True)


    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)['rows']
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
                datePost = {
                    'current': str(meta['Num']),
                    'rowCount': '200',
                    'query_sign': meta['url']
                }
                yield scrapy.FormRequest(url=self.base_url, formdata=datePost, callback=self.parse, meta=meta,
                                         dont_filter=True)
            else:
                # print('--------------------最终进入文章')
                meta['catName1'] = meta['catName'] + i['codeName'] + '_' + i['bulletinclasschina']
                meta['issueTime'] = i['finishday']
                meta['title'] = i['bulletintitle']

                ContentBaseUrl = 'http://www.ccgp-yunnan.gov.cn/contract.do?method=showContractDetail&bulletin_id={}&bulletinclass={}'
                meta['ContentUrl'] = ContentBaseUrl.format(i['bulletin_id'],i['bulletinclass'])
                urlListTemp.append(meta['ContentUrl'] + TEMPPATH)
                urllist = urlIsExist(urlListTemp)
                if len(urllist) < 1:
                    GotArtcl += 1
                    continue
                else:
                    notGotArtcl += 1
                    yield scrapy.Request(url=meta['ContentUrl'].replace(TEMPPATH,''),
                                         callback=self.parseA, meta=meta,
                                         dont_filter=True)

    def parseA(self, response):
        meta = response.meta
        dict1 = {}
        try:
            html = response.xpath("//form[@id='institutionForm5']").extract()[0]
            dict1['content'] = html
        except:
            return None


        dict1['url'] = meta['ContentUrl']
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['title']
        dict1['issueTime'] = timeReMark(meta['issueTime'])
        dict1['subclass'] = meta['catName1']


        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print(len(dict1['content']))
        save_api(dict1)
        print('----------------------------------------------------------------------------------')