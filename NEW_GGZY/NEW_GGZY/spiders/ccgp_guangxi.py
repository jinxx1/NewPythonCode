# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpGuangxiSpider(scrapy.Spider):
    name = 'ccgp_guangxi'
    allowed_domains = ['www.ccgp-guangxi.gov.cn']
    urlList = [{'catName': '广西省_区本级_中标公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_zbgg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_区本级_采购公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_cggg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_区本级_更正公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_gzgg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_区本级_成交公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_cjgg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_区本级_其他公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_qtgg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_区本级_单一来源公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_dylygg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_区本级_招标文件预公示', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_zbwjygg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_市县级_其他公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_qtgg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_市县级_单一来源公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_dylygg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_市县级_成交公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_cjgg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_市县级_更正公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_gzgg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_市县级_中标公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_zbgg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_市县级_采购公告', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_cggg/param_bulletin/20/page_{}.html'}, {'catName': '广西省_市县级_招标文件预公示', 'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_zbwjygs/param_bulletin/20/page_{}.html'}]



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
        link = response.xpath("//div[@class='rowContainer']//a[@onclick = 'updatenoticemore(id)']/@href").extract()


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
                            try:
                                meta['articleTitle'] = response.xpath("//a[@href = '{}']/@title".format(str(link[i]))).extract()[0]
                            except:

                                continue

                            try:
                                meta['articleTime'] = response.xpath("//a[@href = '{}']/../span[@class = 'date']/text()".format(str(link[i]))).extract()[0]
                            except:

                                continue

                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,dont_filter=True)
        else:

            return None






    def parseA(self, response):
        # print('进入文章了')

        meta = response.meta
        dict1 = {}

        try:
            html = response.xpath("//div[@class='frameReport']").extract()[0]
            dict1['content'] = html
        except:
            return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle'].strip()
        dict1['issueTime'] = timeReMark(meta['articleTime'])
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
