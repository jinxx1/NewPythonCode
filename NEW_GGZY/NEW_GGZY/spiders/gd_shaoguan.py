# -*- coding: utf-8 -*-
import scrapy,re,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class GdShaoguanSpider(scrapy.Spider):
    name = 'gd_shaoguan'
    allowed_domains = ['www.sgjyzx.com']
    base_url = 'http://www.sgjyzx.com/businessAnnounceAction!frontBusinessAnnounceIframeList.do?businessAnnounce.announcetype={}'
    urlList = [{'catName': '韶关市_建设工程交易_公告公示', 'url': '12'}, {'catName': '韶关市建设工程交易招标答疑', 'url': '13'}, {'catName': '韶关市建设工程交易中标候选人公示', 'url': '16'}, {'catName': '韶关市建设工程交易全过程评标结果公示', 'url': '15'}, {'catName': '韶关市建设工程交易全过程中标结果公示', 'url': '17'}, {'catName': '韶关市政府采购采购公告', 'url': '00'}, {'catName': '韶关市政府采购更正公告', 'url': '01'}, {'catName': '韶关市政府采购结果公示', 'url': '02'}, {'catName': '韶关市国土资源交易公告', 'url': '20'}, {'catName': '韶关市国土资源补遗答疑', 'url': '23'}, {'catName': '韶关市国土资源结果公示', 'url': '22'}, {'catName': '韶关市产权交易交易公告', 'url': '30'}, {'catName': '韶关市产权交易补遗答疑', 'url': '32'}, {'catName': '韶关市产权交易结果公示', 'url': '31'}, {'catName': '韶关市河沙权交易交易公告', 'url': '60'}, {'catName': '韶关市河沙权交易补遗答疑', 'url': '62'}, {'catName': '韶关市河沙权交易结果公示', 'url': '61'}, {'catName': '韶关市小额建设工程交易交易公告', 'url': '70'}, {'catName': '韶关市小额建设工程交易更正公告', 'url': '72'}, {'catName': '韶关市小额建设工程交易结果公示', 'url': '71'}]




    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['lb'] = i['url']
            meta['url'] = self.base_url.format(str(meta['lb']))
            datePost = {'pageSize':'50','page':str(meta['Num'])}
            yield scrapy.FormRequest(url=meta['url'],formdata=datePost, callback=self.parse,meta=meta)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//td[@class='tdRight']//a/@href").extract()
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
                    yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA,
                                         meta=meta)
            else:
                return None
        else:
            return None


    def parseA(self, response):
        meta = response.meta
        dict1 = {}
        html = response.xpath("//div[@class='xx-text']").extract()
        titletemp = response.xpath("//h2//text()").extract()
        titleT = ''
        for i in titletemp:
            titleT = titleT + i.strip().replace('\n','').replace('\t','')

        timetemp = response.xpath("//div[@class='publictime']//text()").extract()
        timeT = ''
        for ii in timetemp:
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
                url = self.base_url.format(str(meta['Num']))
                yield scrapy.Request(url=url, callback=self.parse, meta=meta)

        else:
            return None