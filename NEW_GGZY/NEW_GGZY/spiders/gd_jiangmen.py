# -*- coding: utf-8 -*-
import scrapy,re,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class GdJiangmenSpider(scrapy.Spider):
    name = 'gd_jiangmen'
    allowed_domains = ['jiangmen.gov.cn']
    base_urls = [{'catName': '江门市_政府采购_采购公告', 'url': 'http://zyjy.jiangmen.gov.cn/cggg/index_{}.htm'}, {'catName': '江门市_政府采购_采购结果公告', 'url': 'http://zyjy.jiangmen.gov.cn/cjgg/index_{}.htm'}, {'catName': '江门市_建设工程_招标公告', 'url': 'http://zyjy.jiangmen.gov.cn/zbgg/index_{}.htm'}, {'catName': '江门市_建设工程_补充修改公告', 'url': 'http://zyjy.jiangmen.gov.cn/zbgzgg/index_{}.htm'}, {'catName': '江门市_建设工程_评标结果公示', 'url': 'http://zyjy.jiangmen.gov.cn/jggs/index_{}.htm'}, {'catName': '江门市_建设工程_中标公告', 'url': 'http://zyjy.jiangmen.gov.cn/zbgs/index_{}.htm'}, {'catName': '江门市_土地与矿权_网上挂牌公告', 'url': 'http://zyjy.jiangmen.gov.cn/gpxxgg/index_{}.htm'}, {'catName': '江门市_土地与矿权_其他公告', 'url': 'http://zyjy.jiangmen.gov.cn/qtgg/index_{}.htm'}, {'catName': '江门市_土地与矿权_报价/竞价信息预通告', 'url': 'http://zyjy.jiangmen.gov.cn/ygg/index_{}.htm'}, {'catName': '江门市_土地与矿权_结果公示', 'url': 'http://zyjy.jiangmen.gov.cn/gpjggs/index_{}.htm'}, {'catName': '江门市_产权交易_项目公告', 'url': 'http://zyjy.jiangmen.gov.cn/cqxmgg/index_{}.htm'}, {'catName': '江门市_产权交易_成交公告', 'url': 'http://zyjy.jiangmen.gov.cn/cqxmgs/index_{}.htm'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.base_urls)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].replace('index_{}.htm','index.htm'), callback=self.parse,meta=meta)

    def parse(self, response):
        meta = response.meta
        link=response.xpath("//div[@class='tab-item itemtw']//a/@href").extract()
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
        meta = response.meta
        dict1 = {}
        html = response.xpath("//div[@class='newsCon']").extract()
        titleT = response.xpath("//h1/text()").extract()
        timeT = response.xpath("//div[@class='msgbar']/text()").extract()
        try:
            regex = re.findall(r"\d{4}-\d{2}-\d{2}",timeT[0])[0]
        except:
            regex = '2000-01-01'
        if html and titleT and timeT:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = titleT[0]
            dict1['issueTime'] = timeReMark(regex)
            dict1['content'] = html[0]
            dict1['subclass'] = meta['catName']
            requestsAPI = save_api(dict1)


            tempDict = meta['Breakpoint']
            tempDict['Num'] = meta['Num']
            writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

            print(dict1['title'])
            print(dict1['url'])
            print(dict1['issueTime'])
            print(len(dict1['content']))
            print(dict1['subclass'])
            print(requestsAPI.text)

            print('------------------------------------')


            if meta['pageTune'] == 1:
                meta['Num'] += 1
                url = meta['url'].format(str(meta['Num']))
                yield scrapy.Request(url=url, callback=self.parse, meta=meta)
        else:
            return None

