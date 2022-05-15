# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpSichuanSpider(scrapy.Spider):
    name = 'ccgp_sichuan'
    allowed_domains = ['www.ccgp-sichuan.gov.cn']
    urlList = [{'catName': '四川省_', 'url': 'http://www.ccgp-sichuan.gov.cn/CmsNewsController.do?method=search&years=&chnlNames=\u6240\u6709&chnlCodes=&title=&tenderno=&agentname=&buyername=&startTime=&endTime=&distin_like=510000&city=&town=&cityText=\u8BF7\u9009\u62E9&townText=\u8BF7\u9009\u62E9&searchKey=&distin=&type=&beginDate=&endDate=&str1=&str2=&pageSize=10&curPage={}&searchResultForm=search_result_anhui.ftl'}]


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
        link = response.xpath("//div[@class = 'info']/ul/li/a/@href").extract()

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
                    yield scrapy.Request(url=meta['url'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)
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
                                meta['articleTitle'] = response.xpath("//a[@href = '{}']/div/text()".format(str(link[i]))).extract()[0]
                            except:
                                print('没找到标题****************')
                                return None

                            meta['link']=link[i]
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,dont_filter=True)
        else:
            return None


    def parseA(self, response):
        # print('进入文章了')

        meta = response.meta
        dict1 = {}

        try:
            timeTemp = response.xpath("//p[@class='time']/text()").extract()[0]
            meta['articleTime'] = re.findall(r"\d{2,4}-\d{1,2}-\d{1,2}",timeTemp)[0]
        except:
            meta['articleTime'] = '2001-01-01'

        try:
            html = response.xpath("//div[@id='myPrintArea'] | //div[@class = 'cont-info']").extract()[0]
            dict1['content'] = html

        except:
            return None

        try:
            catAll = response.xpath("//div[@class='siteBox']/a/@title").extract()
            lbword = ''
            for i in range(len(catAll) - 1):
                lbword = lbword + '_' + catAll[i]
            meta['catName1'] = meta['catName'] + lbword


        except:
            return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle'].strip()
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['subclass'] = meta['catName1'].replace('__首页','')

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
