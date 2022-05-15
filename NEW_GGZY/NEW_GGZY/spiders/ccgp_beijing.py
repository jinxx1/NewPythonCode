# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpBeijingSpider(scrapy.Spider):
    name = 'ccgp_beijing'
    allowed_domains = ['www.ccgp-beijing.gov.cn']
    urlList = [{'catName': '北京市_市级信息公告_招标公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbgg/index_{}.html'}, {'catName': '北京市_市级信息公告_中标公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjzbjggg/index_{}.html'}, {'catName': '北京市_市级信息公告_合同公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjhtgg/index_{}.html'}, {'catName': '北京市_市级信息公告_更正公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjgzgg/index_{}.html'}, {'catName': '北京市_市级信息公告_废标公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjfbgg/index_{}.html'}, {'catName': '北京市_市级信息公告_单一公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjdygg/index_{}.html'}, {'catName': '北京市_市级信息公告_其他公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/sjzfcggg/sjqtgg/index_{}.html'}, {'catName': '北京市_区级信息公告_招标公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbgg/index_{}.html'}, {'catName': '北京市_区级信息公告_中标公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjzbjggg/index_{}.html'}, {'catName': '北京市_区级信息公告_合同公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjhtgg/index_{}.html'}, {'catName': '北京市_区级信息公告_更正公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjgzgg/index_{}.html'}, {'catName': '北京市_区级信息公告_废标公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjfbgg/index_{}.html'}, {'catName': '北京市_区级信息公告_单一公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjdygg/index_{}.html'}, {'catName': '北京市_区级信息公告_其他公告', 'url': 'http://www.ccgp-beijing.gov.cn/xxgg/qjzfcggg/qjqtgg/index_{}.html'}]
# 'http://www.ccgp-beijing.gov.cn/xxgg/index.html?city=shi&name=shiji'

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = 0
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].replace('index_{}.html','index.html'),callback=self.parse, meta=meta,dont_filter=True)



    def parse(self, response):
        meta = response.meta
        meta['requestListNum'] = 0
        titleT = response.xpath("//ul[@class='xinxi_ul']/li/a/text()").extract()
        link = response.xpath("//ul[@class='xinxi_ul']/li/a/@href").extract()
        timeT = response.xpath("//ul[@class='xinxi_ul']/li/span[@class='datetime']/text()").extract()
        titleT = remarkList(titleT)
        # print(len(link),len(titleT),len(timeT))
        if len(link) != len(titleT) or len(titleT) != len(timeT):
            return None

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
                    yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,meta=meta, dont_filter=True)
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
                            meta['articleTitle'] = titleT[i]
                            meta['articleTime'] = timeT[i]
                            if not meta['articleTitle']:
                                meta['articleTitle'] = '本文暂无标题'
                            if not meta['articleTime']:
                                meta['articleTime'] = '2000-01-01 00:00:00'
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,dont_filter=True)
        else:

            return None


    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        meta['requestContentNum'] = 0
        dict1 = {}
        html = response.xpath("/html/body/div/div[@align='left']").extract()
        if meta['articleTime'] == '2000-01-01 00:00:00':
            try:
                meta['articleTime'] = response.xpath("//span[@class='datetime']/text()").extract()[0]
            except:
                meta['articleTime'] = '2000-01-01'

        if '...' in meta['articleTitle']:
            try:
                meta['articleTitle'] = response.xpath("//div[@style = 'text-align: center;margin:28px 0 28px 0;']/span/text()").extract()[0]
            except:
                pass
        if html:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = meta['articleTitle']
            dict1['issueTime'] = timeReMark(meta['articleTime'])
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
            print('-----------------------------------------------------------------------------------------------------------------------')
        else:
            print('最终页未能获取到文章内容', response.url)
            return None
