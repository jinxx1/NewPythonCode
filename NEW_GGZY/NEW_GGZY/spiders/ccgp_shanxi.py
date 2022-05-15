# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()


class CcgpShanxiSpider(scrapy.Spider):
    name = 'ccgp_shanxi'
    allowed_domains = ['www.ccgp-shanxi.gov.cn']
    urlList = [{'catName': '山西省_招标公告', 'url': 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=100&page={}'}, {'catName': '山西省_结果公告', 'url': 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=104&page={}'}, {'catName': '山西省_变更公告', 'url': 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=105&page={}'}, {'catName': '山西省_单一来源公示', 'url': 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=116&page={}'}, {'catName': '山西省_招标预公告', 'url': 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=131&page={}'}, {'catName': '山西省_邀请招标', 'url': 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=132&page={}'},{'catName': '山西省_公告', 'url': 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=145&page={}'}, {'catName': '山西省_合同公示', 'url': 'http://www.ccgp-shanxi.gov.cn/view.php?app=&type=&nav=153&page={}'}]


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
        link = response.xpath("//table[@id='node_list']/tbody/tr/td/a/@href").extract()
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
                            try:
                                meta['articleTitle'] = response.xpath("//a[@href = '{}']/./@title".format(str(link[i]))).extract()[0]
                            except:
                                return None
                            try:
                                LocalAndTimeT = response.xpath("//a[@href = '{}']/../../td/text()".format(str(link[i]))).extract()

                            except:
                                return None

                            if len(LocalAndTimeT) < 2:
                                meta['catName1'] = meta['catName'] + '_未知地区'
                                meta['articleTime'] = LocalAndTimeT[0].replace('[','').replace(']','')
                            else:
                                meta['catName1'] = meta['catName'] + '_' + LocalAndTimeT[0]
                                meta['articleTime'] = LocalAndTimeT[1].replace('[', '').replace(']', '')

                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,dont_filter=True)
        else:

            return None


    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        dict1 = {}
        try:
            html = response.xpath("//div[@id='div_view']|//tr[@class='bk5']").extract()[0]
            dict1['content'] = html
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = meta['articleTitle']
            dict1['issueTime'] = timeReMark(meta['articleTime'])
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

            print(
                '-----------------------------------------------------------------------------------------------------------')
        except:
            return None

