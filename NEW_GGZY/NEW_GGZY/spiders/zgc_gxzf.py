# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem
TEMPPATH = TMEPTEST()




class ZgcGxzfSpider(scrapy.Spider):
    name = 'zgc_gxzf'
    allowed_domains = ['gxggzy.gxzf.gov.cn']
    urlList = [{'catName': '广西壮族自治区_铁路工程_招标公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001010/001010001', 'lb': '1010001'}, {'catName': '广西壮族自治区_铁路工程_澄清公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001010/001010002', 'lb': '1010002'}, {'catName': '广西壮族自治区_铁路工程_上限价', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001010/001010003', 'lb': '1010003'}, {'catName': '广西壮族自治区_铁路工程_结果公示', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001010/001010004', 'lb': '1010004'}, {'catName': '广西壮族自治区_铁路工程_中标公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001010/001010005', 'lb': '1010005'}, {'catName': '广西壮族自治区_房建市政_招标公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001001/001001001', 'lb': '1001001'}, {'catName': '广西壮族自治区_房建市政_澄清公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001001/001001002', 'lb': '1001002'}, {'catName': '广西壮族自治区_房建市政_上限价', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001001/001001004', 'lb': '1001004'}, {'catName': '广西壮族自治区_房建市政_结果公示', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001001/001001005', 'lb': '1001005'}, {'catName': '广西壮族自治区_房建市政_中标公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001001/001001006', 'lb': '1001006'}, {'catName': '广西壮族自治区_政府采购_采购公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001004/001004001', 'lb': '1004001'}, {'catName': '广西壮族自治区_政府采购_澄清变更', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001004/001004002', 'lb': '1004002'}, {'catName': '广西壮族自治区_政府采购_结果公示', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001004/001004004', 'lb': '1004004'}, {'catName': '广西壮族自治区_产权交易_交易公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001007/001007001', 'lb': '1007001'}, {'catName': '广西壮族自治区_产权交易_成交公示', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001007/001007002', 'lb': '1007002'}, {'catName': '广西壮族自治区_土地矿权_交易公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001008/001008001', 'lb': '1008001'}, {'catName': '广西壮族自治区_药械采购_交易公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001009/001009001', 'lb': '1009001'}, {'catName': '广西壮族自治区_药械采购_成交公示', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001009/001009002', 'lb': '1009002'}, {'catName': '广西壮族自治区_药械采购_澄清变更', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001009/001009003', 'lb': '1009003'}, {'catName': '广西壮族自治区_水利工程_交易公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001011/001011001', 'lb': '1011001'}, {'catName': '广西壮族自治区_水利工程_成交公示', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001011/001011002', 'lb': '1011002'}, {'catName': '广西壮族自治区_水利工程_澄清变更', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001011/001011003', 'lb': '1011003'}, {'catName': '广西壮族自治区_水利工程_中标公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001011/001011005', 'lb': '1011005'}, {'catName': '广西壮族自治区_交通工程_招标公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001012/001012001', 'lb': '1012001'}, {'catName': '广西壮族自治区_交通工程_澄清变更', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001012/001012002', 'lb': '1012002'}, {'catName': '广西壮族自治区_交通工程_上限价', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001012/001012003', 'lb': '1012003'}, {'catName': '广西壮族自治区_交通工程_中标公示', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001012/001012004', 'lb': '1012004'}, {'catName': '广西壮族自治区_交通工程_中标公告', 'url': 'http://gxggzy.gxzf.gov.cn/gxzbw/jyxx/001012/001012005', 'lb': '1012005'}]
    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url'] + '/MoreInfo.aspx?CategoryNum=' + i['lb']
            yield scrapy.Request(url=meta['url'],callback=self.parseFirst, meta=meta,dont_filter=True)

    def parseFirst(self, response):
        meta = response.meta
        try:
            meta['page__VIEWSTATEGENERATOR'] = response.xpath("//input[@name = '__VIEWSTATEGENERATOR']/@value").extract()[0]
            meta['page__CSRFTOKEN'] = response.xpath("//input[@name = '__CSRFTOKEN']/@value").extract()[0]
            meta['page__VIEWSTATE'] = response.xpath("//input[@name = '__VIEWSTATE']/@value").extract()[0]
        except:
            return None

        datePost = {
                    '__CSRFTOKEN':str(meta['page__CSRFTOKEN']),
                    '__VIEWSTATE':str(meta['page__VIEWSTATE']),
                    '__VIEWSTATEGENERATOR':str(meta['page__VIEWSTATEGENERATOR']),
                    '__EVENTTARGET':'MoreInfoList1$Pager',
                    '__EVENTARGUMENT':str(meta['Num']),
                    '__VIEWSTATEENCRYPTED':''
        }
        yield scrapy.FormRequest(url=meta['url'],formdata=datePost,callback=self.parse,meta=meta,dont_filter=True)

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
                        '__CSRFTOKEN': str(meta['page__CSRFTOKEN']),
                        '__VIEWSTATE': str(meta['page__VIEWSTATE']),
                        '__VIEWSTATEGENERATOR': str(meta['page__VIEWSTATEGENERATOR']),
                        '__EVENTTARGET': 'MoreInfoList1$Pager',
                        '__EVENTARGUMENT': str(meta['Num']),
                        '__VIEWSTATEENCRYPTED': ''
                    }
                    yield scrapy.FormRequest(url=meta['url'], formdata=datePost, callback=self.parseA, meta=meta,
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


