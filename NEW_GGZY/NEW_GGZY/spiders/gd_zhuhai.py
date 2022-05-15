# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class GdZhuhaiSpider(scrapy.Spider):
    name = 'gd_zhuhai'
    allowed_domains = ['ggzy.zhuhai.gov.cn']
    base_urls = [{'catName': '珠海_政府采购', 'url': 'http://ggzy.zhuhai.gov.cn/exchangeinfo/govbuy/index_{}.jhtml'}, {'catName': '珠海_建设工程', 'url': 'http://ggzy.zhuhai.gov.cn/exchangeinfo/jsgc/index_{}.jhtml'}, {'catName': '珠海_土地房产矿业权', 'url': 'http://ggzy.zhuhai.gov.cn/exchangeinfo/landexchange/index_{}.jhtml'}, {'catName': '珠海_国有资产产权交易', 'url': 'http://ggzy.zhuhai.gov.cn/exchangeinfo/propertyexchange/index_{}.jhtml'}, {'catName': '珠海_其他公共资源交易_排污权', 'url': 'http://ggzy.zhuhai.gov.cn/exchangeinfo/qtggzyjy/pawq/index_{}.jhtml'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.base_urls)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].replace('_{}',''), callback=self.parse,meta=meta)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class = 'rl-box-right']//a/@href").extract()
        if len(link) > 0:
            urlListTemp = []
            for i in link:
                urlTemp = parse.urljoin(response.url, i)
                if self.allowed_domains[0] not in urlTemp:
                    continue
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
        meta = response.meta
        dict1 = {}
        html = response.xpath("//div[@class = 'newsCon']").extract()
        titleT = response.xpath("//meta[@name = 'ArticleTitle']/@content").extract()
        timeT = response.xpath("//meta[@name = 'PubDate']/@content").extract()
        cat = response.xpath("//div[@class='break']/ul/li[3]//text()").extract()
        wordCat = ''
        for i in cat:
            wordCat = wordCat + i.replace('\n','').replace('\t','').strip()
        catName = '珠海市_' + wordCat.replace('>','_').replace('_正文','')

        if html and titleT and timeT:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = titleT[0]
            dict1['issueTime'] = timeReMark(timeT[0])
            dict1['content'] = html[0]
            dict1['subclass'] = catName
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
            if meta['pageTune'] == 1:
                meta['Num'] += 1
                url = meta['url'].format(str(meta['Num']))
                yield scrapy.Request(url=url, callback=self.parse, meta=meta)
        else:
            return None








