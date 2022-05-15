# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()




class CcgpHebeiSpider(scrapy.Spider):
    name = 'ccgp_hebei'
    allowed_domains = ['www.ccgp-hebei.gov.cn']
    urlList = [
        {'catName': '河北省_省级_招标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index_{}.html'},
        {'catName': '河北省_省级_中标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/zhbgg/index_{}.html'},
        {'catName': '河北省_省级_废标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/fbgg/index_{}.html'},
        {'catName': '河北省_省级_更正公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/gzgg/index_{}.html'},
        {'catName': '河北省_省级_单一来源', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/dyly/index_{}.html'},
        {'catName': '河北省_省级_合同公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/htgg/index_{}.html'},
        {'catName': '河北省_市县_招标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/zbgg/index_746_{}.html'},
        {'catName': '河北省_市县_更正公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/gzgg/index_749_{}.html'},
        {'catName': '河北省_市县_中标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/zhbgg/index_746_{}.html'},
        {'catName': '河北省_市县_合同公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/htgg/index_750_{}.html'},
        {'catName': '河北省_市县_废标公告', 'url': 'http://www.ccgp-hebei.gov.cn/province/cggg/fbgg/index_746_{}.html'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].replace('_{}',''),callback=self.parse,meta=meta,dont_filter=True)


    def parse(self, response):
        meta = response.meta
        meta['requestListNum'] = 0
        titleT = response.xpath("//table[@id='moredingannctable']//a[@class='a3']/text()").extract()
        link = response.xpath("//table[@id='moredingannctable']//a[@class='a3']/@href").extract()
        timeT = response.xpath("//td[@class='txt1']/span[@class='txt'][1]/text()").extract()
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
                    # print('-------------------------------没有新文章退出')
                    return None
                elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(link):
                    # print('--------------------翻页')
                    meta['Num'] += 1
                    yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta,
                                         dont_filter=True)
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
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,
                                                 dont_filter=True)
        else:

            return None


    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        meta['requestContentNum'] = 0
        dict1 = {}

        try:
            regTemp = re.findall("<!--主体 start-->(.*?)<!--主体 end-->", response.text, re.M | re.S)[0]
            hhtml = regTemp.replace('\n', '').replace(' ', '')
        except:
            return None

        if '...' in meta['articleTitle']:
            try:
                meta['articleTitle'] = response.xpath("//span[@class='txt2']/text()").extract()[0]
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
            return None