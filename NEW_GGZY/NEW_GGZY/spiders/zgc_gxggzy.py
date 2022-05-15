# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem
TEMPPATH = TMEPTEST()



class ZgcGxggzySpider(scrapy.Spider):
    name = 'zgc_gxggzy'
    allowed_domains = ['www.nnggzy.org.cn']

    urlList = [{'catName': '南宁公共资源交易中心_房建市政_招标公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001001/001001001', 'lb': '001001001'}, {'catName': '南宁公共资源交易中心_房建市政_澄清变更', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001001/001001002', 'lb': '001001002'}, {'catName': '南宁公共资源交易中心_房建市政_招标控制价', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001001/001001004', 'lb': '001001004'}, {'catName': '南宁公共资源交易中心_房建市政_评标结果公示', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001001/001001005', 'lb': '001001005'}, {'catName': '南宁公共资源交易中心_房建市政_中标公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001001/001001006', 'lb': '001001006'}, {'catName': '南宁公共资源交易中心_政府采购_采购公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001004/001004001', 'lb': '001004001'}, {'catName': '南宁公共资源交易中心_政府采购_变更公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001004/001004002', 'lb': '001004002'}, {'catName': '南宁公共资源交易中心_政府采购_招标控制价', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001004/001004005', 'lb': '001004005'}, {'catName': '南宁公共资源交易中心_政府采购_中标公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001004/001004004', 'lb': '001004004'}, {'catName': '南宁公共资源交易中心_政府采购_采购合同公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001004/001004007', 'lb': '001004007'}, {'catName': '南宁公共资源交易中心_政府采购_质疑投诉', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001004/001004006', 'lb': '001004006'}, {'catName': '南宁公共资源交易中心_政府分散采购_采购公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001012/001012001', 'lb': '001012001'}, {'catName': '南宁公共资源交易中心_政府分散采购_变更公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001012/001012002', 'lb': '001012002'}, {'catName': '南宁公共资源交易中心_政府分散采购_中标公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001012/001012003', 'lb': '001012003'}, {'catName': '南宁公共资源交易中心_政府分散采购_质疑投诉', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001012/001012004', 'lb': '001012004'}, {'catName': '南宁公共资源交易中心_国有产权交易_交易公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001007/001007001', 'lb': '001007001'}, {'catName': '南宁公共资源交易中心_国有产权交易_变更公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001007/001007003', 'lb': '001007003'}, {'catName': '南宁公共资源交易中心_国有产权交易_成交公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001007/001007002', 'lb': '001007002'}, {'catName': '南宁公共资源交易中心_土地使用权和矿业权出让_交易公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001008/001008001', 'lb': '001008001'}, {'catName': '南宁公共资源交易中心_土地使用权和矿业权出让_成交公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001008/001008002', 'lb': '001008002'}, {'catName': '南宁公共资源交易中心_土地使用权和矿业权出让_变更公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001008/001008003', 'lb': '001008003'}, {'catName': '南宁公共资源交易中心_综合交易_交易公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001009/001009001', 'lb': '001009001'}, {'catName': '南宁公共资源交易中心_综合交易_变更公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001009/001009003', 'lb': '001009003'}, {'catName': '南宁公共资源交易中心_综合交易_成交公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001009/001009002', 'lb': '001009002'}, {'catName': '南宁公共资源交易中心_综合交易_开评标结果', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001009/001009004', 'lb': '001009004'}, {'catName': '南宁公共资源交易中心_水利工程_招标公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001010/001010001', 'lb': '001010001'}, {'catName': '南宁公共资源交易中心_水利工程_变更澄清', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001010/001010002', 'lb': '001010002'}, {'catName': '南宁公共资源交易中心_水利工程_招标控制价', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001010/001010003', 'lb': '001010003'}, {'catName': '南宁公共资源交易中心_水利工程_开评标结果', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001010/001010004', 'lb': '001010004'}, {'catName': '南宁公共资源交易中心_水利工程_中标公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001010/001010005', 'lb': '001010005'}, {'catName': '南宁公共资源交易中心_交通工程_招标公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001011/001011001', 'lb': '001011001'}, {'catName': '南宁公共资源交易中心_交通工程_答疑澄清', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001011/001011002', 'lb': '001011002'}, {'catName': '南宁公共资源交易中心_交通工程_招标控制价', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001011/001011003', 'lb': '001011003'}, {'catName': '南宁公共资源交易中心_交通工程_开评标结果', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001011/001011004', 'lb': '001011004'}, {'catName': '南宁公共资源交易中心_交通工程_中标公告', 'url': 'https://www.nnggzy.org.cn/nnzbwmanger/jyxx/001011/001011005', 'lb': '001011005'}]


    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            meta['postUrl'] = 'https://www.nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=' + i['lb']

            yield scrapy.Request(url=meta['postUrl'],callback=self.parseFirst, meta=meta,dont_filter=True)


    def parseFirst(self, response):
        meta = response.meta

        try:
            meta['page__VIEWSTATEGENERATOR'] = response.xpath("//input[@name = '__VIEWSTATEGENERATOR']/@value").extract()[0]
            meta['page__CSRFTOKEN'] = response.xpath("//input[@name = '__CSRFTOKEN']/@value").extract()[0]
            meta['page__VIEWSTATE'] = response.xpath("//input[@name = '__VIEWSTATE']/@value").extract()[0]
        except:
            return None

        datePost = {
                    '__CSRFTOKEN':meta['page__CSRFTOKEN'],
                    '__VIEWSTATE':meta['page__VIEWSTATE'],
                    '__VIEWSTATEGENERATOR':meta['page__VIEWSTATEGENERATOR'],
                    '__EVENTTARGET':'MoreInfoList1$Pager',
                    '__EVENTARGUMENT':str(meta['Num']),
                    '__VIEWSTATEENCRYPTED':''
        }


        yield scrapy.FormRequest(url=meta['postUrl'],formdata=datePost,callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta= response.meta

        link = response.xpath("//td[@id='MoreInfoList1_tdcontent']//a/@href").extract()

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
                        '__CSRFTOKEN': meta['page__CSRFTOKEN'],
                        '__VIEWSTATE': meta['page__VIEWSTATE'],
                        '__VIEWSTATEGENERATOR': meta['page__VIEWSTATEGENERATOR'],
                        '__EVENTTARGET': 'MoreInfoList1$Pager',
                        '__EVENTARGUMENT': str(meta['Num']),
                        '__VIEWSTATEENCRYPTED': ''
                    }

                    yield scrapy.FormRequest(url=meta['postUrl'], formdata=datePost, callback=self.parse, meta=meta,
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
                                meta['articleTitle'] = response.xpath("//*[@href='{}']/@title".format(str(link[i]))).extract()[0]
                            except:

                                return None

                            try:
                                meta['articleTime'] = response.xpath("//*[@href='{}']/../../td[3]/text()".format(str(link[i]))).extract()[0]
                            except:

                                return None

                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,
                                                 dont_filter=True)
        else:

            return None


    def parseA(self, response):
        # print('进入文章了')

        meta = response.meta
        dict1 = GgzyItem()

        try:
            html = response.xpath("//td[@id='TDContent']").extract()[0]
            dict1['content'] = html.replace('\n','')
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

        yield dict1

