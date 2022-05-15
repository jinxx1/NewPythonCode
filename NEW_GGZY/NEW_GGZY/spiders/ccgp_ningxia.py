# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
import time,datetime
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()





class CcgpNingxiaSpider(scrapy.Spider):
    name = 'ccgp_ningxia'
    allowed_domains = ['www.nxggzyjy.org']
    urlList = [{'catName': '宁夏_工程建设项目', 'url': 'http://www.nxggzyjy.org/ningxiaweb/002/002001/{}.html'}, {'catName': '宁夏_政府采购项目', 'url': 'http://www.nxggzyjy.org/ningxiaweb/002/002002/{}.html'}, {'catName': '宁夏_药品采购项目', 'url': 'http://www.nxggzyjy.org/ningxiaweb/002/002003/{}.html'}, {'catName': '宁夏_产权交易项目', 'url': 'http://www.nxggzyjy.org/ningxiaweb/002/002004/{}.html'}, {'catName': '宁夏_土地及矿业权交易项目', 'url': 'http://www.nxggzyjy.org/ningxiaweb/002/002005/{}.html'}]


    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,meta=meta)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//ul[@id = 'showList']//li/div/a/@href").extract()

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
                    # return None
                    meta['Num'] += 1
                    yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta)
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
                                meta['articleTitle'] = response.xpath("//a[@href = '{}']/text()".format(str(link[i]))).extract()[0]
                            except:
                                print('没找到标题****************')
                                return None
                            try:
                                meta['articleTime'] = response.xpath("//a[@href = '{}']/../../span[@class = 'ewb-date']/text()".format(str(link[i]))).extract()[0]
                            except:
                                print('没找到时间****************')
                                return None

                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,dont_filter=True)
        else:
            return None


    def parseA(self, response):
        # print('进入文章了')

        meta = response.meta
        dict1 = {}
        try:
            html = response.xpath("//div[@id = 'gonggaoid'] | //div[@id='mainContent']").extract()[0]
            dict1['content'] = html
        except:
            return None

        if meta['catName'] == '宁夏_政府采购项目' or meta['catName'] == '宁夏_工程建设项目':
            try:
                word = re.findall("\[(.*?)\]", meta['articleTitle'])[0]
                meta['catName1'] = meta['catName'] + '_' + word
            except:
                meta['catName1'] = meta['catName']+ '_无地区'
        else:
            meta['catName1'] = meta['catName']+ '_省级'

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle'].strip()
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
        print('--------------------------------------------------------------------------------------------')
