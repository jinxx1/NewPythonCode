# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class GdShantouSpider(scrapy.Spider):
    name = 'gd_shantou'
    allowed_domains = ['www.shantou.gov.cn']
    urlDict = [{'catName': '汕头市_政府采购', 'url': 'http://www.shantou.gov.cn/ggzyjy/zfcg/list_{}.shtml'}, {'catName': '汕头市_建设工程', 'url': 'http://www.shantou.gov.cn/ggzyjy/jsgc/list_{}.shtml'}, {'catName': '汕头市_土地矿产', 'url': 'http://www.shantou.gov.cn/ggzyjy/tdkc/list_{}.shtml'}, {'catName': '汕头市_产权交易', 'url': 'http://www.shantou.gov.cn/ggzyjy/cqjy/list_{}.shtml'}, {'catName': '汕头市_公车拍卖', 'url': 'http://www.shantou.gov.cn/ggzyjy/gcpm/list_{}.shtml'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.urlDict)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['key'] = i['catName']
            meta['ListUrl'] = i['url']
            yield scrapy.Request(url=meta['ListUrl'].replace('list_{}.shtml','list.shtml'), callback=self.parse,meta=meta)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='list-right_title fon_1']/a/@href").extract()
        if len(link) > 0:
            urlListTemp = []
            for i in link:
                urlTemp = parse.urljoin(response.url, i)
                urlListTemp.append(urlTemp + TEMPPATH)
            urllist = urlIsExist(urlListTemp)
            n = 0
            if len(urllist) > 0 and str(type(urllist)) == r"<class 'list'>":
                for url in urllist:
                    n += 1
                    if n == len(urllist):
                        meta['pageTune'] = 1
                    else:
                        meta['pageTune'] = 0
                    yield scrapy.Request(url=url.replace(TEMPPATH,''), callback=self.parseA,
                                         meta=meta)
            else:
                return None
        else:
            return None


    def parseA(self, response):
        dict1={}
        meta = response.meta
        try:
            titleT = response.xpath("//meta[@name = 'ArticleTitle']/@content").extract()[0]
            timeT = response.xpath("//meta[@name = 'PubDate']/@content").extract()[0]
            html = response.xpath("//div[@id='zoomcon']").extract()[0]
            catName = response.xpath("//meta[@name = 'ColumnName']/@content").extract()[0]
        except:
            return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = titleT
        dict1['issueTime'] = timeReMark(timeT)
        dict1['content'] = html
        dict1['subclass'] = response.meta['key'] + "_" + catName
        requestsAPI = save_api(dict1)

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))


        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(len(dict1['content']))
        print(requestsAPI.text)
        print('------------------------------------')

        if meta['pageTune'] ==1:
            meta['Num'] += 1
            url = meta['ListUrl'].format(str(meta['Num']))
            yield scrapy.Request(url=url, callback=self.parse, meta=meta)



