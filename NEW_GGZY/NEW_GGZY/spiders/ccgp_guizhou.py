# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()





class CcgpGuizhouSpider(scrapy.Spider):
    name = 'ccgp_guizhou'
    allowed_domains = ['www.ccgp-guizhou.gov.cn']
    urlDict = [{'catName': '贵州省_省级_采购需求公示', 'url': '1153332561072666'}, {'catName': '贵州省_省级_采购公告', 'url': '1153418052184995'}, {'catName': '贵州省_省级_更正公告', 'url': '1153454200156791'}, {'catName': '贵州省_省级_废标公告', 'url': '1153488085289816'}, {'catName': '贵州省_省级_中标(成交)公告', 'url': '1153531755759540'}, {'catName': '贵州省_省级_单一来源公示', 'url': '1153567415242344'}, {'catName': '贵州省_省级_单一来源(成交)公告', 'url': '1153595823404526'}, {'catName': '贵州省_省级_资格预审', 'url': '1156071132711523'}, {'catName': '贵州省_市县_采购需求公示', 'url': '1153796890012888'}, {'catName': '贵州省_市县_采购公告', 'url': '1153797950913584'}, {'catName': '贵州省_市县_更正公告', 'url': '1153817836808214'}, {'catName': '贵州省_市县_废标公告', 'url': '1153845808113747'}, {'catName': '贵州省_市县_中标(成交)公告', 'url': '1153905922931045'}, {'catName': '贵州省_市县_单一来源公示', 'url': '1153924595764135'}, {'catName': '贵州省_市县_单一来源(成交)公告', 'url': '1153937977184763'}, {'catName': '贵州省_市县_资格预审', 'url': '1156071132710859'}]
    base_url = 'http://www.ccgp-guizhou.gov.cn/article-search.html'

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlDict)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']

            datePost = {
                "siteId": "1",
                "category.id": meta['url'],
                "areaName":"",
                "tenderRocurementPm":"",
                "keywords":"",
                "articlePageNo": str(meta['Num']),
                "articlePageSize": "15"
            }
            yield scrapy.FormRequest(url=self.base_url,
                                     formdata=datePost,callback=self.parse,
                                     meta=meta,dont_filter=True,
                                     headers={'Referer': 'http://www.ccgp-guizhou.gov.cn/article-search.html'})


    def parse(self, response):
        meta= response.meta
        link = response.xpath("//div[@class='xnrx']/ul/li/a/@href").extract()

        GotArtcl = 0
        notGotArtcl = 0
        if len(link) > 0:
            for i in range(len(link) + 1):
                urlListTemp = []
                # print('进入List循环体了')
                if notGotArtcl == 0 and GotArtcl == len(link):
                    # print('-------------------------------没有新文章退出')
                    return None
                elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(link):
                    # print('--------------------翻页')
                    meta['Num'] += 1

                    datePost = {
                        "siteId": "1",
                        "category.id": meta['url'],
                        "areaName": "",
                        "tenderRocurementPm": "",
                        "keywords": "",
                        "articlePageNo": str(meta['Num']),
                        "articlePageSize": "15"
                    }
                    yield scrapy.FormRequest(url=self.base_url,
                                             formdata=datePost, callback=self.parse,
                                             meta=meta, dont_filter=True,
                                             headers={
                                                 'Referer': 'http://www.ccgp-guizhou.gov.cn/article-search.html'})
                else:
                    # print('--------------------最终进入文章')
                    urlTemp = parse.urljoin(response.url, link[i])
                    urlListTemp.append(urlTemp + TEMPPATH)
                    urllist = urlIsExist(urlListTemp)
                    if len(urllist) < 1:
                        GotArtcl += 1
                        continue
                    else:
                        notGotArtcl += 1
                        for url in urllist:
                            try:
                                meta['articleTitle'] = response.xpath("//a[@href='{}']/text()".format(str(link[i]))).extract()[0]
                            except:

                                return None

                            try:
                                meta['articleTime'] = response.xpath("//a[@href='{}']/../span/text()".format(str(link[i]))).extract()[0]
                            except:

                                return None

                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,
                                                 dont_filter=True)
        else:

            return None

    def parseA(self, response):
        # print('进入文章了')

        meta = response.meta
        dict1 = {}

        try:
            html = response.xpath("//div[@id='content']").extract()[0]
            dict1['content'] = html
        except:
            return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle'].strip()
        dict1['issueTime'] = timeReMark(meta['articleTime'].replace('.','-'))
        dict1['subclass'] = meta['catName']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print(len(dict1['content']))
        save_api(dict1)
        print('--------------------------------------------------------------------------------------------')
