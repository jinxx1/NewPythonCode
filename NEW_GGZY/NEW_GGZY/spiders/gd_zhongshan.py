# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()


class GdZhongshanSpider(scrapy.Spider):
    name = 'gd_zhongshan'
    allowed_domains = ['www.zsjyzx.gov.cn']
    base_urls = [{'catName': '中山市_政府采购_采购需求公示', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=160', 'lb': '160 '}, {'catName': '中山市_政府采购_废标公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=138', 'lb': '138 '}, {'catName': '中山市_政府采购_中标公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=55', 'lb': '55 '}, {'catName': '中山市_政府采购_答疑、更正公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=54', 'lb': '54 '}, {'catName': '中山市_政府采购_采购公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=53', 'lb': '53 '}, {'catName': '中山市_建设工程_招投标信息公开', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=172', 'lb': '172 '}, {'catName': '中山市_建设工程_项目公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=107', 'lb': '107 '}, {'catName': '中山市_建设工程_中标信息', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=61', 'lb': '61 '}, {'catName': '中山市_建设工程_中标候选人公示', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=60', 'lb': '60 '}, {'catName': '中山市_建设工程_答疑、澄清', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=59', 'lb': '59 '}, {'catName': '中山市_建设工程_招标公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=58', 'lb': '58 '}, {'catName': '中山市_土地与矿业权_交易公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=64', 'lb': '64 '}, {'catName': '中山市_土地与矿业权_结果公布', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=65', 'lb': '65 '}, {'catName': '中山市_土地与矿业权_其他公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=66', 'lb': '66 '}, {'catName': '中山市_医疗设备_废标公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=152', 'lb': '152 '}, {'catName': '中山市_医疗设备_中标公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=105', 'lb': '105 '}, {'catName': '中山市_医疗设备_预中标公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=140', 'lb': '140 '}, {'catName': '中山市_医疗设备_更正、答疑', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=93', 'lb': '93 '}, {'catName': '中山市_医疗设备_招标公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=92', 'lb': '92 '}, {'catName': '中山市_综合交易_延期公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=135', 'lb': '135 '}, {'catName': '中山市_综合交易_其他公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=118', 'lb': '118 '}, {'catName': '中山市_综合交易_拍卖结果公示', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=117', 'lb': '117 '}, {'catName': '中山市_综合交易_拍卖公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=116', 'lb': '116 '}, {'catName': '中山市_综合交易_中标公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=115', 'lb': '115 '}, {'catName': '中山市_综合交易_结果公示', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=113', 'lb': '113 '}, {'catName': '中山市_综合交易_交易答疑澄清', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=112', 'lb': '112 '}, {'catName': '中山市_综合交易_交易公告', 'url': 'http://www.zsjyzx.gov.cn/Application/NewPage/PageSubItem.jsp?page={}&node=72', 'lb': '72'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.base_urls)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['key'] = i['catName']
            meta['url'] = i['url']
            meta['lb'] = i['lb']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,meta=meta)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='nav_list']/ul/li[@class='clear']/a/@href | //div[@class='nav_list_1']/ul/li[@class='clear']/a/@href").extract()
        if len(link) > 0:
            urlListTemp = []
            for i in link:
                urlTemp = parse.urljoin(response.url, i)
                if self.allowed_domains[0] not in urlTemp:
                    continue
                try:
                    rex = re.findall(r"articalID=(.*)",urlTemp)[0]
                except:
                    continue
                arUrl = 'http://www.zsjyzx.gov.cn/Application/NewPage/ggnr.jsp?articalID={}&nodeID={}'.format(rex,meta['lb'].strip())
                urlListTemp.append(arUrl + TEMPPATH)
            urllist = urlIsExist(urlListTemp)
            n = 0
            if len(urllist) > 0 and str(type(urllist)) == r"<class 'list'>":
                for url in urllist:
                    n +=1
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
        html = response.xpath("//div[@class = 'articalDiv']").extract()
        titleT = response.xpath("//div[@class = 'details_1']/h2/text()").extract()
        timeT = response.xpath("//div[@class = 'details_1']/h3/span/text()").extract()


        if html and titleT and timeT:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = titleT[0]
            dict1['issueTime'] = timeReMark(timeT[0])
            dict1['content'] = html[0]
            dict1['subclass'] = meta['key']
            requestsAPI = save_api(dict1)


            tempDict = meta['Breakpoint']
            tempDict['Num'] = meta['Num']
            writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))


            print(dict1['title'])
            print(dict1['url'])
            print(dict1['issueTime'])
            print(len(dict1['content']))
            print(requestsAPI.text)
            print('-----------------------------------------------------------------------------------------------------')
            if meta['pageTune'] == 1:
                meta['Num'] += 1
                url = meta['url'].format(str(meta['Num']))
                yield scrapy.Request(url=url, callback=self.parse, meta=meta)
        else:
            return None





    #


















    # urlListAll = [{'catName': '中山市_政府采购_采购需求公示', 'PageTotalNume': '12 ', 'lb': '160 '},
    #               {'catName': '中山市_政府采购_废标公告', 'PageTotalNume': '66 ', 'lb': '138 '},
    #               {'catName': '中山市_政府采购_中标公告', 'PageTotalNume': '2102 ', 'lb': '55 '},
    #               {'catName': '中山市_政府采购_答疑、更正公告', 'PageTotalNume': '247 ', 'lb': '54 '},
    #               {'catName': '中山市_政府采购_采购公告', 'PageTotalNume': '2471 ', 'lb': '53 '},
    #               {'catName': '中山市_建设工程_招投标信息公开', 'PageTotalNume': '251 ', 'lb': '172 '},
    #               {'catName': '中山市_建设工程_项目公告', 'PageTotalNume': '17 ', 'lb': '107 '},
    #               {'catName': '中山市_建设工程_中标信息', 'PageTotalNume': '240 ', 'lb': '61 '},
    #               {'catName': '中山市_建设工程_中标候选人公示', 'PageTotalNume': '242 ', 'lb': '60 '},
    #               {'catName': '中山市_建设工程_答疑、澄清', 'PageTotalNume': '189 ', 'lb': '59 '},
    #               {'catName': '中山市_建设工程_招标公告', 'PageTotalNume': '251 ', 'lb': '58 '},
    #               {'catName': '中山市_土地与矿业权_交易公告', 'PageTotalNume': '15 ', 'lb': '64 '},
    #               {'catName': '中山市_土地与矿业权_结果公布', 'PageTotalNume': '17 ', 'lb': '65 '},
    #               {'catName': '中山市_土地与矿业权_其他公告', 'PageTotalNume': '2 ', 'lb': '66 '},
    #               {'catName': '中山市_医疗设备_废标公告', 'PageTotalNume': '1 ', 'lb': '152 '},
    #               {'catName': '中山市_医疗设备_中标公告', 'PageTotalNume': '11 ', 'lb': '105 '},
    #               {'catName': '中山市_医疗设备_预中标公告', 'PageTotalNume': '8 ', 'lb': '140 '},
    #               {'catName': '中山市_医疗设备_更正、答疑', 'PageTotalNume': '1 ', 'lb': '93 '},
    #               {'catName': '中山市_医疗设备_招标公告', 'PageTotalNume': '11 ', 'lb': '92 '},
    #               {'catName': '中山市_综合交易_延期公告', 'PageTotalNume': '2 ', 'lb': '135 '},
    #               {'catName': '中山市_综合交易_其他公告', 'PageTotalNume': '7 ', 'lb': '118 '},
    #               {'catName': '中山市_综合交易_拍卖结果公示', 'PageTotalNume': '10 ', 'lb': '117 '},
    #               {'catName': '中山市_综合交易_拍卖公告', 'PageTotalNume': '13 ', 'lb': '116 '},
    #               {'catName': '中山市_综合交易_中标公告', 'PageTotalNume': '12 ', 'lb': '115 '},
    #               {'catName': '中山市_综合交易_结果公示', 'PageTotalNume': '17 ', 'lb': '113 '},
    #               {'catName': '中山市_综合交易_交易答疑澄清', 'PageTotalNume': '11 ', 'lb': '112 '},
    #               {'catName': '中山市_综合交易_交易公告', 'PageTotalNume': '19 ', 'lb': '72'}]