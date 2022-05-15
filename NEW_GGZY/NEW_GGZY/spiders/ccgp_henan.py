# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,difflib
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem
TEMPPATH = TMEPTEST()


class CcgpHenanSpider(scrapy.Spider):
    name = 'ccgp_henan'
    allowed_domains = ['www.hngp.gov.cn']
    urlList = [{'catName': '河南省_采购公告_全部_省直', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&pageSize=20&bz=1&pageSize=20&pageNo={}'}, {'catName': '河南省_结果公告_全部_省直', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&pageSize=20&bz=1&pageSize=20&pageNo={}'}, {'catName': '河南省_变更公告_全部_省直', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0103&pageSize=20&bz=1&pageSize=20&pageNo={}'}, {'catName': '河南省_其他公告_单一来源_省直', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1301&pageSize=20&bz=1&pageSize=20&pageNo={}'}, {'catName': '河南省_其他公告_进口产品_省直', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1302&pageSize=20&bz=1&pageSize=20&pageNo={}'}, {'catName': '河南省_其他公告_技术指标_省直', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1303&pageSize=20&bz=1&pageSize=20&pageNo={}'}, {'catName': '河南省_其他公告_征询意见_省直', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1304&pageSize=20&bz=1&pageSize=20&pageNo={}'}, {'catName': '河南省_合同验收公告_合同公告_省直', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1401&pageSize=20&bz=1&pageSize=20&pageNo={}'}, {'catName': '河南省_合同验收公告_验收结果公告_省直', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1402&pageSize=20&bz=1&pageSize=20&pageNo={}'}, {'catName': '河南省_采购公告_全部_市县', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0101&pageSize=20&bz=2&pageSize=20&pageNo={}'}, {'catName': '河南省_结果公告_全部_市县', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0102&pageSize=20&bz=2&pageSize=20&pageNo={}'}, {'catName': '河南省_变更公告_全部_市县', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=0103&pageSize=20&bz=2&pageSize=20&pageNo={}'}, {'catName': '河南省_其他公告_单一来源_市县', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1301&pageSize=20&bz=2&pageSize=20&pageNo={}'}, {'catName': '河南省_其他公告_进口产品_市县', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1302&pageSize=20&bz=2&pageSize=20&pageNo={}'}, {'catName': '河南省_其他公告_技术指标_市县', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1303&pageSize=20&bz=2&pageSize=20&pageNo={}'}, {'catName': '河南省_其他公告_征询意见_市县', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1304&pageSize=20&bz=2&pageSize=20&pageNo={}'}, {'catName': '河南省_合同验收公告_合同公告_市县', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1401&pageSize=20&bz=2&pageSize=20&pageNo={}'}, {'catName': '河南省_合同验收公告_验收结果公告_市县', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1402&pageSize=20&bz=2&pageSize=20&pageNo={}'}, {'catName': '河南省_网上竞价_信息公告_全省', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1201&pageSize=20&pageSize=20&pageNo={}'}, {'catName': '河南省_网上竞价_结果公告_全省', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1202&pageSize=20&pageSize=20&pageNo={}'}, {'catName': '河南省_协议定点_协议供货_全省', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1009&pageSize=20&pageSize=20&pageNo={}'}, {'catName': '河南省_协议定点_定点服务_全省', 'url': 'http://www.hngp.gov.cn/henan/ggcx?appCode=H60&channelCode=1010&pageSize=20&pageSize=20&pageNo={}'}]

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
        link = response.xpath("//div[@class='List2']/ul/li/a/@href").extract()
        if not link:
            return None

        urlList_withDomain = [parse.urljoin(response.url,x) for x in link]
        urllist = urlIsExist(urlList_withDomain)
        if not urllist:
            return None

        for i in urllist:
            for n in link:
                if difflib.SequenceMatcher(None,i,n).quick_ratio() > 0.5:
                    titleT = response.xpath("//*[@href = '{}']/text()".format(n)).extract()
                    timeT = response.xpath("//*[@href = '{}']/../span/text()".format(n)).extract()
                    try:
                        meta['articleTitle'] = titleT[0]
                        meta['articleTime'] = timeT[0]
                        meta['sUrl'] = i
                        yield scrapy.Request(url=i, callback=self.parseTempContent, meta=meta,
                                             dont_filter=True)
                    except:
                        continue

        meta['Num'] += 1
        yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,meta=meta, dont_filter=True)



    def parseTempContent(self,response):
        # print('进入附件页')


        meta = response.meta
        meta['ContentUrl'] = response.url
        jqS = response.text

        try:
            TrueContentUrl = re.findall("/webfile(.*?)\.htm", jqS)[0]
        except:
            print('TrueContentUrl   return')
            return None

        url = 'http://www.hngp.gov.cn/webfile/'+TrueContentUrl+'.htm'

        downloadUrl = response.xpath("//div[@class='List1 Top5']//a/@href").extract()

        meta['attachmentListJsonList'] = []

        if len(downloadUrl)>0:

            for i in range(len(downloadUrl)):
                attachmentDict = {}
                attachmentDict['downloadUrl'] = parse.urljoin(response.url, downloadUrl[i])
                try:
                    attachmentDict['name'] = response.xpath("//a[@href='{}']//text()".format(downloadUrl[i])).extract()[0]
                except:
                    attachmentDict['name'] = '本文附件{}'.format(i)

                meta['attachmentListJsonList'].append(attachmentDict)
        else:
            pass


        yield scrapy.Request(url=url, callback=self.parseA, meta=meta, dont_filter=True)

    def parseA(self, response):
        # print('进入最终页')

        dict1 = GgzyItem()
        meta = response.meta

        try:
            html = response.xpath("//body").extract()[0]
        except:
            return None

        dict1['url'] = meta['ContentUrl']

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
        dict1['subclass'] = meta['catName'].replace(' ','')
        if len(meta['attachmentListJsonList'])>0:
            dict1['attachmentListJson'] = json.dumps(meta['attachmentListJsonList'], ensure_ascii=False)

        yield dict1