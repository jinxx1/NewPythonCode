# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpShaanxiSpider(scrapy.Spider):
    name = 'ccgp_shaanxi'
    allowed_domains = ['www.ccgp-shaanxi.gov.cn']
    urlList = [{'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_陕西省本级', 'regionguid': '610001'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_西安市', 'regionguid': '6101'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_铜川市', 'regionguid': '6102'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_宝鸡市', 'regionguid': '6103'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_咸阳市', 'regionguid': '6104'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_渭南市', 'regionguid': '6105'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_延安市', 'regionguid': '6106'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_汉中市', 'regionguid': '6107'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_榆林市', 'regionguid': '6108'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_安康市', 'regionguid': '6109'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_商洛市', 'regionguid': '6110'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_杨凌示范区', 'regionguid': '6111'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=3', 'catName': '陕西省_采购公告_西咸新区', 'regionguid': '6169'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_陕西省本级', 'regionguid': '610001'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_西安市', 'regionguid': '6101'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_铜川市', 'regionguid': '6102'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_宝鸡市', 'regionguid': '6103'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_咸阳市', 'regionguid': '6104'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_渭南市', 'regionguid': '6105'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_延安市', 'regionguid': '6106'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_汉中市', 'regionguid': '6107'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_榆林市', 'regionguid': '6108'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_安康市', 'regionguid': '6109'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_商洛市', 'regionguid': '6110'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_杨凌示范区', 'regionguid': '6111'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=5', 'catName': '陕西省_结果公告_西咸新区', 'regionguid': '6169'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_陕西省本级', 'regionguid': '610001'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_西安市', 'regionguid': '6101'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_铜川市', 'regionguid': '6102'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_宝鸡市', 'regionguid': '6103'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_咸阳市', 'regionguid': '6104'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_渭南市', 'regionguid': '6105'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_延安市', 'regionguid': '6106'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_汉中市', 'regionguid': '6107'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_榆林市', 'regionguid': '6108'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_安康市', 'regionguid': '6109'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_商洛市', 'regionguid': '6110'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_杨凌示范区', 'regionguid': '6111'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=4', 'catName': '陕西省_更正公告_西咸新区', 'regionguid': '6169'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_陕西省本级', 'regionguid': '610001'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_西安市', 'regionguid': '6101'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_铜川市', 'regionguid': '6102'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_宝鸡市', 'regionguid': '6103'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_咸阳市', 'regionguid': '6104'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_渭南市', 'regionguid': '6105'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_延安市', 'regionguid': '6106'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_汉中市', 'regionguid': '6107'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_榆林市', 'regionguid': '6108'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_安康市', 'regionguid': '6109'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_商洛市', 'regionguid': '6110'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_杨凌示范区', 'regionguid': '6111'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=6', 'catName': '陕西省_终止公告_西咸新区', 'regionguid': '6169'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_陕西省本级', 'regionguid': '610001'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_西安市', 'regionguid': '6101'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_铜川市', 'regionguid': '6102'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_宝鸡市', 'regionguid': '6103'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_咸阳市', 'regionguid': '6104'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_渭南市', 'regionguid': '6105'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_延安市', 'regionguid': '6106'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_汉中市', 'regionguid': '6107'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_榆林市', 'regionguid': '6108'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_安康市', 'regionguid': '6109'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_商洛市', 'regionguid': '6110'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_杨凌示范区', 'regionguid': '6111'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=99', 'catName': '陕西省_其他_西咸新区', 'regionguid': '6169'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_陕西省本级', 'regionguid': '610001'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_西安市', 'regionguid': '6101'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_铜川市', 'regionguid': '6102'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_宝鸡市', 'regionguid': '6103'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_咸阳市', 'regionguid': '6104'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_渭南市', 'regionguid': '6105'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_延安市', 'regionguid': '6106'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_汉中市', 'regionguid': '6107'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_榆林市', 'regionguid': '6108'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_安康市', 'regionguid': '6109'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_商洛市', 'regionguid': '6110'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_杨凌示范区', 'regionguid': '6111'}, {'url': 'http://www.ccgp-shaanxi.gov.cn/notice/noticeaframe.do?noticetype=1', 'catName': '陕西省_单一来源及进口产品公示_西咸新区', 'regionguid': '6169'}]


    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            meta['regionguid'] = i['regionguid']
            datePost = {
                "page.pageNum": str(meta['Num']),
                "parameters['regionguid']": str(meta['regionguid'])
            }
            yield scrapy.FormRequest(url=meta['url'],formdata=datePost,callback=self.parse,meta=meta,dont_filter=True)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//table[@class='table table-no tab-striped tab-hover']/tbody/tr/td/a/@href").extract()

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
                        "page.pageNum": str(meta['Num']),
                        "parameters['regionguid']": str(meta['regionguid'])
                    }
                    yield scrapy.FormRequest(url=meta['url'], formdata=datePost, callback=self.parse,meta=meta, dont_filter=True)

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
                                meta['articleTitle'] = response.xpath("//a[@href = '{}']/../../td/@title".format(str(link[i]))).extract()[0]
                            except:

                                return None
                            try:
                                LocalAndTimeT = response.xpath("//a[@href = '{}']/../../td[4]/text()".format(str(link[i]))).extract()[0]

                            except:
                                LocalAndTimeT = '0'

                            meta['articleTime'] = LocalAndTimeT
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,
                                                 dont_filter=True)
        else:

            return None


    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        dict1 = {}
        if meta['articleTime'] == '0':
            try:
                timeT = response.xpath("//div[@class='content_about']/span/em[@class='red']").extract()[0]
                meta['articleTime'] = timeT
            except:
                meta['articleTime'] = '2001-01-01'

        try:
            html = response.xpath("//div[@class = 'annBox'] | //div[@class='inner-Box'] | //div[@class='content-inner']").extract()[0]
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
