# -*- coding: utf-8 -*-
import scrapy,re,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class GdYunfuSpider(scrapy.Spider):
    name = 'gd_yunfu'
    allowed_domains = ['ggzy.yunfu.gov.cn']
    urlList = [{'catName': '云浮市_建设工程_招标公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/jsgc/002001/?Paging={}'}, {'catName': '云浮市_建设工程_补充公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/jsgc/002002/?Paging={}'}, {'catName': '云浮市_建设工程_中标公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/jsgc/002003/?Paging={}'}, {'catName': '云浮市_建设工程_中标结果公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/jsgc/002005/?Paging={}'}, {'catName': '云浮市_建设工程_其他通知', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/jsgc/002004/?Paging={}'}, {'catName': '云浮市_政府采购_采购公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003001/?Paging={}'}, {'catName': '云浮市_政府采购_澄清变更公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003002/?Paging={}'}, {'catName': '云浮市_政府采购_中标信息', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003003/?Paging={}'}, {'catName': '云浮市_政府采购_其他通知', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003004/?Paging={}'}, {'catName': '云浮市_政府采购_结果公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003005/?Paging={}'}, {'catName': '云浮市_政府采购_单一来源公示', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003006/?Paging={}'}, {'catName': '云浮市_政府采购_采购异常', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/zfcg/003007/?Paging={}'}, {'catName': '云浮市_土地矿业权_交易公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/tdjy/004001/?Paging={}'}, {'catName': '云浮市_土地矿业权_撤销补充公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/tdjy/004005/?Paging={}'}, {'catName': '云浮市_土地矿业权_其他通知', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/tdjy/004004/?Paging={}'}, {'catName': '云浮市_土地矿业权_历史记录', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/tdjy/004002/?Paging={}'}, {'catName': '云浮市_产权交易_交易公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/cqjy/005001/?Paging={}'}, {'catName': '云浮市_产权交易_结果公示', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/cqjy/005002/?Paging={}'}, {'catName': '云浮市_产权交易_其他公告', 'url': 'http://ggzy.yunfu.gov.cn/yfggzy/cqjy/005003/?Paging={}'}]



    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url'].format(str(meta['Num']))
            yield scrapy.Request(url=meta['url'], callback=self.parse, meta=meta)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//li[@class='common-item clearfix']//a/@href").extract()
        titleT = response.xpath("//li[@class='common-item clearfix']//a/text()").extract()
        timeT = response.xpath("//li[@class='common-item clearfix']//span/text()").extract()
        if len(link) != len(titleT) or len(titleT) != len(timeT):
            return None

        GotArtcl = 0
        notGotArtcl = 0
        if len(link) > 0:

            for i in range(len(link)+1):
                urlListTemp = []
                # print('进入List循环体了')
                if notGotArtcl == 0 and GotArtcl == len(link):
                    # print('notGotArtcl == 0 and GotArtcl == len(link)-------------------------------没有新文章退出')
                    return None
                elif notGotArtcl !=0 and notGotArtcl + GotArtcl == len(link):
                    # print('notGotArtcl !=0 and notGotArtcl + GotArtcl == len(link)--------------------翻页')
                    meta['Num'] += 1
                    url = meta['url'].format(str(meta['Num']))
                    yield scrapy.Request(url=url, callback=self.parse, meta=meta)
                else:
                    # print('urlTemp = parse.urljoin(response.url, link[i])--------------------最终进入文章')
                    urlTemp = parse.urljoin(response.url, link[i])
                    urlListTemp.append(urlTemp + TEMPPATH)
                    urllist = urlIsExist(urlListTemp)
                    if len(urllist) < 1:
                        GotArtcl += 1
                        continue
                    else:
                        notGotArtcl +=1
                        for url in urllist:
                            meta['articleTitle'] = titleT[i]
                            meta['articleTime'] = timeT[i]
                            if not meta['articleTitle']:
                                meta['articleTitle'] = '本文暂无标题'
                            if not meta['articleTime']:
                                meta['articleTime'] = '2000-01-01 00:00:00'
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA,meta=meta)
        else:
            return None

    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        dict1 = {}
        html = response.xpath("//div[@data-id = 'tab-a'] | //div[@id='mainContent']").extract()

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
            print('-------------------------------------------------------------------------------------------------------------------------')
        else:
            return None