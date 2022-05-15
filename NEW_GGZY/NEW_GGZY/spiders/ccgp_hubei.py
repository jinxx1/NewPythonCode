# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpHubeiSpider(scrapy.Spider):
    name = 'ccgp_hubei'
    allowed_domains = ['www.ccgp-hubei.gov.cn']
    urlList = urlList = [{
		'catName': '湖北省_招标(采购)公告_省级',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/pzbgg/index_{}.html'
	}, {
		'catName': '湖北省_中标（成交）结果公告_省级',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/pzhbgg/index_{}.html'
	}, {
		'catName': '湖北省_更正公告_省级',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/pgzgg/index_{}.html'
	}, {
		'catName': '湖北省_其他公告_省级',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/pqtgg/index_{}.html'
	}, {
		'catName': '湖北省_废标（终止）公告_省级',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/pfbgg/index_{}.html'
	}, {
		'catName': '湖北省_单一来源公示_省级',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/pdylygg/index_{}.html'
	}, {
		'catName': '湖北省_招标(采购)公告_市县',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/czbgg/index_{}.html'
	}, {
		'catName': '湖北省_中标（成交）结果公告_市县',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/czhbgg/index_{}.html'
	}, {
		'catName': '湖北省_更正公告_市县',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/cgzgg/index_{}.html'
	}, {
		'catName': '湖北省_废标（终止）公告_市县',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/cfbgg/index_{}.html'
	}, {
		'catName': '湖北省_单一来源公示_市县',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/cdylygg/index_{}.html'
	}, {
		'catName': '湖北省_其他公告_市县',
		'url': 'http://www.ccgp-hubei.gov.cn/notice/cggg/cqtgg/index_{}.html'
	}
]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])),callback=self.parse, meta=meta)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='news-list list-page']//li/a/@href").extract()
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

        try:
            html = response.xpath("//div[@class='art_con']").extract()[0]
            titleT = response.xpath("//h2[@class='title']/text()").extract()[0]
        except:
            return None
        try:
            timeT = response.xpath("//div[@class='art_info']/span[1]/text()").extract()[0]
            regex = re.findall(r"\d{2,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}", timeT)[0]
        except:
            regex = '2000-01-01 00:00:01'

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = titleT
        dict1['issueTime'] = timeReMark(regex)
        dict1['content'] = html
        dict1['subclass'] = meta['catName']
        requestsAPI = save_api(dict1)

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['subclass'])
        print(dict1['issueTime'])
        print(len(dict1['content']))
        print(requestsAPI.text)

        print('------------------------------------')

        if meta['pageTune'] == 1:
            meta['Num'] += 1
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta)
