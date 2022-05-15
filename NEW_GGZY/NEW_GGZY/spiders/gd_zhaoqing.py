# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()


class GdZhaoqingSpider(scrapy.Spider):
    name = 'gd_zhaoqing'
    allowed_domains = ['ggzy.zhaoqing.gov.cn']
    base_urls = [{'catName': '肇庆市_建设工程', 'url': 'http://ggzy.zhaoqing.gov.cn/zqfront/showinfo/moreinfolist.aspx?categorynum=003001&Paging={}'}, {'catName': '肇庆市_政府采购', 'url': 'http://ggzy.zhaoqing.gov.cn/zqfront/showinfo/moreinfolist.aspx?categorynum=003002&Paging={}'}, {'catName': '肇庆市_土地矿业权交易', 'url': 'http://ggzy.zhaoqing.gov.cn/zqfront/showinfo/moreinfolist.aspx?categorynum=003003&Paging={}'}, {'catName': '肇庆市_产权交易', 'url': 'http://ggzy.zhaoqing.gov.cn/zqfront/showinfo/moreinfolist.aspx?categorynum=003004&Paging={}'}, {'catName': '肇庆市_林权交易', 'url': 'http://ggzy.zhaoqing.gov.cn/zqfront/showinfo/moreinfolist.aspx?categorynum=003005&Paging={}'}, {'catName': '肇庆市_一般招标', 'url': 'http://ggzy.zhaoqing.gov.cn/zqfront/showinfo/moreinfolist.aspx?categorynum=003006&Paging={}'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.base_urls)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['key'] = i['catName']
            meta['url'] = i['url'].format(str(meta['Num']))
            yield scrapy.Request(url=meta['url'], callback=self.parse,meta=meta)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='column-info-list']/ul/li[@class='clearfix']/a/@href").extract()
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
        html = response.xpath("//div[@id='mainContent']").extract()
        titleT = response.xpath("//div[@class='menu-info']/h1/text()").extract()
        ooo = response.xpath("//div[@class='info-sources']//text()").extract()
        timeT = ''
        for i in ooo:
            timeT = timeT + i
        try:
            regex = re.findall(r"\d{2,4}-\d{1,2}-\d{1,2}",timeT)[0]
        except:
            regex = '2000-01-01'

        if html and titleT and timeT:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = titleT[0]
            dict1['issueTime'] = timeReMark(regex)
            dict1['content'] = html[0]
            dict1['subclass'] = response.meta['key']
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
            print('------------------------------------')
            if meta['pageTune'] == 1:
                meta['Num'] += 1
                url = meta['url'].format(str(meta['Num']))
                yield scrapy.Request(url=url, callback=self.parse, meta=meta)
        else:
            return None











