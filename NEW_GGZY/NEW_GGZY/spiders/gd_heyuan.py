# -*- coding: utf-8 -*-
import scrapy,re,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()


class GdHeyuanSpider(scrapy.Spider):
    name = 'gd_heyuan'
    allowed_domains = ['61.143.150.176']
    base_urls = 'http://61.143.150.176/{}/{}.html'
    lb_base = [
        {'catName':'河源市_建设工程','url':'jsgc'},
        {'catName': '河源市_政府采购', 'url': 'zfcg'},
        {'catName': '河源市_土矿交易', 'url': 'tdhkcjy'},
        {'catName': '河源市_产权交易', 'url': 'cqjy'}
    ]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.lb_base)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            url = self.base_urls.format(str(meta['url']),str(meta['Num']))
            yield scrapy.Request(url=url,callback=self.parse,meta=meta)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='ewb-com-block l']/a/@href").extract()
        if len(link) > 0:
            urlListTemp = []
            for i in link:
                urlTemp = parse.urljoin(response.url,i)
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
        html = response.xpath("//div[@class='xiangxiyekuang']").extract()
        title1 = response.xpath("//div[@class='xiangxiyebiaoti']//text()").extract()
        titleT = ''
        for i in title1:
            titleT = titleT + i.strip().replace('\n','').replace('\t','')
        time1 = response.xpath("//div[@class='xiangxidate']//text()").extract()
        timeT = ''
        for ii in time1:
            timeT = timeT + ii.strip().replace('\n','').replace('\t','')
        try:
            regex = re.findall(r"\d{2,4}-\d{1,2}-\d{1,2}",timeT)[0]
        except:
            regex = '2000-01-01'

        if html and titleT and timeT:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = titleT
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
            print(requestsAPI.text)

            print('------------------------------------')

            if meta['pageTune'] == 1:
                meta['Num'] += 1
                url = self.base_urls.format(str(meta['url']), str(meta['Num']))
                yield scrapy.Request(url=url, callback=self.parse, meta=meta)

        else:
            return None