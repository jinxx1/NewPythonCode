# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpJiangsuSpider(scrapy.Spider):
    name = 'ccgp_jiangsu'
    allowed_domains = ['www.ccgp-jiangsu.gov.cn']
    urlList = [{'catName': '江苏省_资格预审公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/zgysgg/index_{}.html'}, {'catName': '江苏省_公告招标公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/gkzbgg/index_{}.html'}, {'catName': '江苏省_邀请招标公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/yqzbgg/index_{}.html'}, {'catName': '江苏省_竞争性谈判公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/jztbgg/index_{}.html'}, {'catName': '江苏省_竞争性磋商公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/jzqsgg/index_{}.html'}, {'catName': '江苏省_单一来源公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/dylygg/index_{}.html'}, {'catName': '江苏省_询价公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/xjgg/index_{}.html'}, {'catName': '江苏省_中标公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/zbgg/index_{}.html'}, {'catName': '江苏省_成交公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/cgcjgg/index_{}.html'}, {'catName': '江苏省_终止公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/zzgg/index_{}.html'}, {'catName': '江苏省_更正公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/cggzgg/index_{}.html'}, {'catName': '江苏省_其他公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/qtgg/index_{}.html'}, {'catName': '江苏省_合同公告', 'url': 'http://www.ccgp-jiangsu.gov.cn/ggxx/htgg_1/index_{}.html'}]


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
        titleT = response.xpath("//div[@class='list_list']/ul/li/a/text()").extract()
        link = response.xpath("//div[@class='list_list']/ul/li/a/@href").extract()
        timeT = response.xpath("//div[@class='list_list']/ul/li/text()").extract()
        titleT = remarkList(titleT)
        timeT = remarkList(timeT)

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
        metaCatName = meta['catName']
        dict1 = {}
        html = response.xpath("//div[@class='contain']/div[@class='content']/div[@class='detail']/div[@class='detail_con']").extract()
        try:
            catOther = response.xpath("//div[@class='local']/text()").extract()[0]
            meta['catName'] = catOther.strip().replace(' ','').replace('>','_').replace('当前位置：首页','江苏省').replace('&nbsp;','')
            if '当前位置' in meta['catName']:
                meta['catName'] = '江苏省'
                catOther = response.xpath("//a[@class = 'CurrChnlCls']/text()").extract()
                for i in catOther:
                    if '首页' not in i:
                        meta['catName'] = meta['catName'] + '_' + i
        except:
            meta['catName'] = metaCatName

        if '..' in meta['articleTitle']:
            try:
                meta['articleTitle'] = response.xpath("//div[@class='dtit']/h1/text()").extract()[0].strip()
            except:
                pass
        if html:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = meta['articleTitle']
            dict1['issueTime'] = timeReMark(meta['articleTime'])
            dict1['content'] = html[0]
            dict1['subclass'] = meta['catName'].replace(' ','')
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
            return None
