# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST(112)



class BeijingSpider(scrapy.Spider):
    name = 'BEIJING'
    allowed_domains = ['ggzyfw.beijing.gov.cn']
    urlDict = [{'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxrjxxzbgg/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxrjxxzbhx/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxrjxxjyjg/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxswzcgpplxx/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxgqgpplxx/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxgqjyjg/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxswzcjyjg/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxzpgjggs/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxcggg/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxgzsx/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxzbjggg/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxggjtbyqs/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxzbhxrgs/index_{}.html'}, {'catName': '0', 'url': 'https://ggzyfw.beijing.gov.cn/jyxxzbgg/index_{}.html'}, {'catName': '北京市_交易信息_工程建设', 'url': 'https://ggzyfw.beijing.gov.cn/jylcgcjs/index_{}.html'}, {'catName': '北京市_交易信息_政府采购', 'url': 'https://ggzyfw.beijing.gov.cn/jylczfcg/index_{}.html'}, {'catName': '北京市_交易信息_土地使用权及矿业权', 'url': 'https://ggzyfw.beijing.gov.cn/jylctdsyq/index_{}.html'}, {'catName': '北京市_交易信息_国有产权_实物资产', 'url': 'https://ggzyfw.beijing.gov.cn/jylcswzc/index_{}.html'}, {'catName': '北京市_交易信息_国有产权_股权类', 'url': 'https://ggzyfw.beijing.gov.cn/jylcgq/index_{}.html'}, {'catName': '北京市_交易信息_软件和信息服务', 'url': 'https://ggzyfw.beijing.gov.cn/jylcrjxx/index_{}.html'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlDict)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].replace('index_{}.html', 'index.html'), callback=self.parse,
                                 meta=meta)

    def parse(self, response):
        meta = response.meta
        if meta['catName'] == '0':
            TempCatName = response.xpath("//div[@class='sitemap']").extract()
            htmLaLL = ''
            for i in TempCatName:
                htmLaLL = htmLaLL + i.strip().replace('\n','').replace('\t','')
            goodWord = re.findall(r"首页</a> (.*?)<script>",htmLaLL)
            meta['catName'] = '北京市_' + goodWord[0].replace(' ','').replace('&gt;','_')
        else:
            link = response.xpath("//div[@class='content-list']//a/@href").extract()
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
                        yield scrapy.Request(url=url.replace(TEMPPATH, ''),
                                             callback=self.parseA,
                                             meta=meta)
                else:
                    return None
            else:
                print('---------------------这个页面没有xpath到内容-------------------------')
                print(response.url)
                return None


    def parseA(self, response):
        meta = response.meta
        dict1 = {}
        html = response.xpath("//div[@class='newsCon']").extract()
        titleT = response.xpath("//div[@class='div-title']/text() | //div[@class='lc-title']/text()").extract()
        timeT = response.xpath("//div[@class='div-title2']/text() | //div[@class='lc-title-s']/text()").extract()
        try:
            regex = re.findall(r"\d{2,4}-\d{1,2}-\d{1,2}",timeT[0])[0]
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
            print(requestsAPI.text)

            print('------------------------------------')

            if meta['pageTune'] == 1:
                meta['Num'] += 1
                url = meta['url'].format(str(meta['Num']))
                yield scrapy.Request(url=url, callback=self.parse, meta=meta)

        else:
            print(".............................................................文章最终页没有得到内容")
            print(response.url)
            return None


