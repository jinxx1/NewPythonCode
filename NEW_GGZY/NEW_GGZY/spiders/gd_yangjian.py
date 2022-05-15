# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class GdYangjianSpider(scrapy.Spider):
    name = 'gd_yangjian'
    allowed_domains = ['www.yjggzy.cn']
    base_urls = [{'catName': '阳江市_政府采购_采购交易公告', 'url': 'http://www.yjggzy.cn/Query/ArticleQuery2/465c897866824460b1783cfa20985510?page={}'}, {'catName': '阳江市_政府采购_采购结果公示', 'url': 'http://www.yjggzy.cn/Query/ArticleQuery2/43a0fbd899a34465945625ea39e34d9c?page={}'}, {'catName': '阳江市_政府采购_采购更正延期公告', 'url': 'http://www.yjggzy.cn/Query/ArticleQuery2/1512d4cad92c44858cd52b85debbd8ed?page={}'}, {'catName': '阳江市_建设工程交易_工程交易公告', 'url': 'http://www.yjggzy.cn/Query/JsgcBidAfficheQuery2/d4f193435ad04447a997719474139181?page={}'}, {'catName': '阳江市_建设工程交易_工程结果公示', 'url': 'http://www.yjggzy.cn/Query/JsgcWinBidAfficheQuery2/46eb01f656f4468cb65a434b77d73065?page={}'}, {'catName': '阳江市_建设工程交易_工程更正延期公告', 'url': 'http://www.yjggzy.cn/Query/ArticleQuery2/9cb01c8a51f54006ac15b302fe50cf0e?page={}'}, {'catName': '阳江市_土地与矿业权交易_土地交易公告', 'url': 'http://www.yjggzy.cn/Query/OnTradingQuery2/e5169aa9989d4ab7b27d2103e84031a7?page={}'}, {'catName': '阳江市_土地与矿业权交易_土地结果公示', 'url': 'http://www.yjggzy.cn/Query/OnResultsQuery2/4a7740eadb8442af9551896106dedf51?page={}'}, {'catName': '阳江市_土地与矿业权交易_土地更正延期公告', 'url': 'http://www.yjggzy.cn/Query/ArticleQuery2/dbaa51e20b934da9a3a61f22f3f719ab?page={}'}, {'catName': '阳江市_产权交易_产权交易公告', 'url': 'http://www.yjggzy.cn/Query/OnPropertyRightsQuery2/b733ae85155147bb9751974c80165d81?page={}'}, {'catName': '阳江市_产权交易_产权结果公示', 'url': 'http://www.yjggzy.cn/Query/OnCQResultsQuery2/b14fe81f79a5493a95e7ef973704aff7?page={}'}, {'catName': '阳江市_产权交易_产权更正延期公告', 'url': 'http://www.yjggzy.cn/Query/OnCorrectionDelayQuery2/592188160bdb424aac44ddd62292c07e?page={}'}, {'catName': '阳江市_其他交易_交易公告', 'url': 'http://www.yjggzy.cn/Query/ArticleQuery2/9dfecf1d2d904f9db0952ffe1b3ce6e3?page={}'}, {'catName': '阳江市_其他交易_结果公示', 'url': 'http://www.yjggzy.cn/Query/ArticleQuery2/d99678759b6c49d587f362c490fe816d?page={}'}, {'catName': '阳江市_其他交易_更正延期公告', 'url': 'http://www.yjggzy.cn/Query/ArticleQuery2/d2b657f3a0914d529a0efdf8e37912a8?page={}'}]


    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.base_urls)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url'].format(str(meta['Num']))
            yield scrapy.Request(url=meta['url'], callback=self.parse, meta=meta)

    def parse(self, response):
        meta = response.meta
        titleT = response.xpath("//div[@class = 'Rbox']/ul[@class='list']/li/a/@title").extract()
        link = response.xpath("//div[@class = 'Rbox']/ul[@class='list']/li/a/@href").extract()
        timeT = response.xpath("//div[@class = 'Rbox']/ul[@class='list']/li/span/text()").extract()

        if len(link) != len(titleT) or len(titleT) != len(timeT):
            return None
        GotArtcl = 0
        notGotArtcl = 0
        if len(link) > 0:

            for i in range(len(link)+1):
                urlListTemp = []
                # print('进入List循环体了')
                if notGotArtcl == 0 and GotArtcl == len(link):
                    # print('notGotArtcl == 0 and GotArtcl == len(link)-------------------------------没有新文章退出')
                    return None
                elif notGotArtcl !=0 and notGotArtcl + GotArtcl == len(link):
                    # print('notGotArtcl !=0 and notGotArtcl + GotArtcl == len(link)--------------------翻页')
                    meta['Num'] += 1
                    url = meta['url'].format(str(meta['Num']))
                    yield scrapy.Request(url=url, callback=self.parse, meta=meta)
                else:
                    # print('urlTemp = parse.urljoin(response.url, link[i])--------------------最终进入文章')
                    urlTemp = parse.urljoin(response.url, link[i])
                    urlListTemp.append(urlTemp + TEMPPATH)
                    urllist = urlIsExist(urlListTemp)
                    if len(urllist) < 1:
                        GotArtcl += 1
                        continue
                    else:
                        notGotArtcl +=1
                        for url in urllist:
                            meta['articleTitle'] = titleT[i]
                            meta['articleTime'] = timeT[i]
                            if not meta['articleTitle']:
                                meta['articleTitle'] = '本文暂无标题'
                            if not meta['articleTime']:
                                meta['articleTime'] = '2000-01-01 00:00:00'
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA,meta=meta)
        else:
            return None






    def parseA(self, response):
        # print('进入文章了')
        dict1 = {}
        meta = response.meta
        html = response.xpath("//div[@class='acticle'] | //div[@id='nr']").extract()

        if html:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = meta['articleTitle']
            dict1['issueTime'] = timeReMark(meta['articleTime'].replace('/','-'))
            dict1['content'] = html[0]
            dict1['subclass'] = meta['catName']
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
            print('-------------------------------------------------------------------------------------------------------------------------')
        else:
            return None