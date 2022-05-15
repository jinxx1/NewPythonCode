# -*- coding: utf-8 -*-
import scrapy,re,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()


class GdJieyangSpider(scrapy.Spider):
    name = 'gd_jieyang'
    allowed_domains = ['www.jysggzy.com']
    base_urls = [{'catName': '揭阳市_建设工程_招标公告', 'url': 'http://www.jysggzy.com/TPFront/jsgc/004001/?pageing={}'}, {'catName': '揭阳市_建设工程_资质审核公告', 'url': 'http://www.jysggzy.com/TPFront/jsgc/004002/?pageing={}'}, {'catName': '揭阳市_建设工程_中标候选人', 'url': 'http://www.jysggzy.com/TPFront/jsgc/004003/?pageing={}'}, {'catName': '揭阳市_建设工程_中标公示', 'url': 'http://www.jysggzy.com/TPFront/jsgc/004004/?pageing={}'}, {'catName': '揭阳市_建设工程_异常公告', 'url': 'http://www.jysggzy.com/TPFront/jsgc/004005/?pageing={}'}, {'catName': '揭阳市_政府采购_采购公告', 'url': 'http://www.jysggzy.com/TPFront/zfcg/003001/?pageing={}'}, {'catName': '揭阳市_政府采购_更正公告', 'url': 'http://www.jysggzy.com/TPFront/zfcg/003002/?pageing={}'}, {'catName': '揭阳市_政府采购_中标公示', 'url': 'http://www.jysggzy.com/TPFront/zfcg/003003/?pageing={}'}, {'catName': '揭阳市_政府采购_预审公告', 'url': 'http://www.jysggzy.com/TPFront/zfcg/003004/?pageing={}'}, {'catName': '揭阳市_政府采购_合同公示', 'url': 'http://www.jysggzy.com/TPFront/zfcg/003005/?pageing={}'}, {'catName': '揭阳市_土地与矿业_出让公告', 'url': 'http://www.jysggzy.com/TPFront/tdky/005005/?pageing={}'}, {'catName': '揭阳市_土地与矿业_成交公示', 'url': 'http://www.jysggzy.com/TPFront/tdky/005006/?pageing={}'}, {'catName': '揭阳市_土地与矿业_补充公告', 'url': 'http://www.jysggzy.com/TPFront/tdky/005007/?pageing={}'}, {'catName': '揭阳市_产权交易_信息公告', 'url': 'http://www.jysggzy.com/TPFront/cqjy/006001/?pageing={}'}, {'catName': '揭阳市_产权交易_交易结果公告', 'url': 'http://www.jysggzy.com/TPFront/cqjy/006002/?pageing={}'}, {'catName': '揭阳市_产权交易_补充公告', 'url': 'http://www.jysggzy.com/TPFront/cqjy/006003/?pageing={}'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.base_urls)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,meta=meta)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//li[@class='ewb-data-item']//a/@href").extract()
        titleT = response.xpath("//li[@class='ewb-data-item']//a/text()").extract()
        timeT = response.xpath("//li[@class='ewb-data-item']//span/text()").extract()
        link = remarkList(link)
        titleT = remarkList(titleT)

        if len(link) != len(titleT) or len(titleT) != len(timeT):

            return None

        GotArtcl = 0
        notGotArtcl = 0
        if len(link) > 0:

            for i in range(len(link) + 1):
                urlListTemp = []
                # print('进入List循环体了')
                if notGotArtcl == 0 and GotArtcl == len(link):
                    # print('----------------------------------------------------------------------------没有新文章退出')
                    return None
                elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(link):
                    # print('--------------------------------------------------------------------------------------翻页')
                    meta['Num'] += 1
                    url = meta['url'].format(str(meta['Num']))
                    yield scrapy.Request(url=url, callback=self.parse, meta=meta)
                else:
                    # print('------------------------------------------------------------------------------最终进入文章')
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
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta)
        else:

            return None

    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        dict1 = {}
        html = response.xpath("//td[@id='TDContent']").extract()
        if meta['articleTime'] == '2000-01-01 00:00:00':
            timeT = response.xpath("//td[@bgcolor = '#ececec' and @align = 'center']/text()").extract()

            try:
                meta['articleTime'] = re.findall(r"\d{4}\/\d{1,2}\/\d{1,2}", timeT[0])[0].replace('/','-')
            except:
                meta['articleTime'] = '2000-01-01'

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
            print(
                '-------------------------------------------------------------------------------------------------------------------------')
        else:

            return None

