# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem
TEMPPATH = TMEPTEST()


def tianjinContentUrl(xpathUrl):
    url = 'http://www.ccgp-tianjin.gov.cn/portal/documentView.do?method=view&id={id}&ver={ver}'
    try:
        regexid = re.findall("id=(.*)&",xpathUrl)[0]
        regexver = re.findall(r"&ver=(.*)",xpathUrl)[0]
        return url.format(id=regexid,ver=regexver)
    except:
        return None

class CcgpTianjinSpider(scrapy.Spider):
    name = 'ccgp_tianjin'
    allowed_domains = ['www.ccgp-tianjin.gov.cn']
    base_url = 'http://www.ccgp-tianjin.gov.cn/portal/topicView.do'
    urlList =[{'catName': '天津市_采购需求征求意见_市级', 'url': '1662'}, {'catName': '天津市_采购需求征求意见_区级', 'url': '1994'}, {'catName': '天津市_采购公告_市级', 'url': '1665'}, {'catName': '天津市_采购公告_区级', 'url': '1664'}, {'catName': '天津市_更正公告_市级', 'url': '1663'}, {'catName': '天津市_更正公告_区级', 'url': '1666'}, {'catName': '天津市_采购结果公告_市级', 'url': '2014'}, {'catName': '天津市_采购结果公告_区级', 'url': '2013'}, {'catName': '天津市_合同及验收公告_市级', 'url': '2015'}, {'catName': '天津市_合同及验收公告_区级', 'url': '2016'}, {'catName': '天津市_单一来源公示_市级', 'url': '2033'}, {'catName': '天津市_单一来源公示_区级', 'url': '2034'}]


    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            datapost = {
                'page': str(meta['Num']),
                'id': meta['url'],
        }
            yield scrapy.FormRequest(url=self.base_url, formdata=datapost, callback=self.parse, meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//ul[@class='dataList']/li/a/@href").extract()
        if not link:
            return None

        urlList_withDomain = [tianjinContentUrl(x) for x in link]
        urllist = urlIsExist(urlList_withDomain)
        if not urllist:
            return None

        for i in urllist:
            try:
                i_id = re.findall("id=(.*)&", i)[0]
            except:
                continue
            for n in link:
                try:
                    n_id = re.findall("id=(.*)&", n)[0]
                except:
                    continue

                if i_id == n_id:
                    titleT = response.xpath("//a[@href='{}']/@title".format(n)).extract()
                    timeT = response.xpath("//a[@href='{}']/../span/text()".format(n)).extract()
                    try:
                        meta['articleTitle'] = titleT[0]
                        meta['articleTime'] = timeT[0]
                        meta['sUrl'] = i
                        yield scrapy.Request(url=i, callback=self.parseA, meta=meta,
                                             dont_filter=True)
                    except:
                        continue

        meta['Num'] += 1
        datapost = {
                'page': str(meta['Num']),
                'id': meta['url'],
        }
        yield scrapy.FormRequest(url=self.base_url, formdata=datapost, callback=self.parse, meta=meta,dont_filter=True)


    def parseA(self, response):
        # print('进入文章了')
        dict1 = GgzyItem()
        meta = response.meta
        try:
            html = response.xpath("//td[@bgcolor = '#ffffff']").extract()[0]
        except:
            return None

        dict1['url'] = response.url
        print('筛选出来的连接：',meta['sUrl'])
        print('即将入库的连接：',response.url)
        if meta['sUrl'] == response.url:
            print('筛选出来和即将入库的连接相同')
        else:
            print('不相同')
        print('********************-------------------********************')
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle']
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['content'] = html
        dict1['subclass'] = meta['catName']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))


        yield dict1
