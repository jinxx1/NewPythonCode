# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class GdQingyuanSpider(scrapy.Spider):
    name = 'gd_qingyuan'
    allowed_domains = ['www.qyggzy.cn']
    urlList = [{'catName': '清远市_政府采购_采购公告_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010304/01030401'}, {'catName': '清远市_政府采购_采购公告_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010304/01030402'}, {'catName': '清远市_政府采购_采购公告_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010304/01030403'}, {'catName': '清远市_政府采购_采购公告_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010304/01030404'}, {'catName': '清远市_政府采购_采购公告_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010304/01030405'}, {'catName': '清远市_政府采购_采购公告_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010304/01030406'}, {'catName': '清远市_政府采购_采购公告_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010304/01030407'}, {'catName': '清远市_政府采购_澄清公告_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010305/01030501'}, {'catName': '清远市_政府采购_澄清公告_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010305/01030503'}, {'catName': '清远市_政府采购_澄清公告_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010305/01030504'}, {'catName': '清远市_政府采购_澄清公告_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010305/01030506'}, {'catName': '清远市_政府采购_澄清公告_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010305/01030507'}, {'catName': '清远市_政府采购_中标公告_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010306/01030601'}, {'catName': '清远市_政府采购_中标公告_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010306/01030602'}, {'catName': '清远市_政府采购_中标公告_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010306/01030603'}, {'catName': '清远市_政府采购_中标公告_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010306/01030604'}, {'catName': '清远市_政府采购_中标公告_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010306/01030605'}, {'catName': '清远市_政府采购_中标公告_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010306/01030606'}, {'catName': '清远市_政府采购_中标公告_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010306/01030607'}, {'catName': '清远市_国土资源_土地招拍挂_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010401/01040101'}, {'catName': '清远市_国土资源_土地招拍挂_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010401/01040102'}, {'catName': '清远市_国土资源_土地招拍挂_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010401/01040103'}, {'catName': '清远市_国土资源_土地招拍挂_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010401/01040104'}, {'catName': '清远市_国土资源_土地招拍挂_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010401/01040105'}, {'catName': '清远市_国土资源_土地招拍挂_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010401/01040106'}, {'catName': '清远市_国土资源_土地招拍挂_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010401/01040107'}, {'catName': '清远市_国土资源_土地成交结果_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010402/01040201'}, {'catName': '清远市_国土资源_土地成交结果_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010402/01040202'}, {'catName': '清远市_国土资源_土地成交结果_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010402/01040203'}, {'catName': '清远市_国土资源_土地成交结果_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010402/01040204'}, {'catName': '清远市_国土资源_土地成交结果_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010402/01040205'}, {'catName': '清远市_国土资源_土地成交结果_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010402/01040206'}, {'catName': '清远市_国土资源_土地成交结果_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010402/01040207'}, {'catName': '清远市_国土资源_矿业权招拍挂_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010403/01040301'}, {'catName': '清远市_国土资源_矿业权招拍挂_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010403/01040302'}, {'catName': '清远市_国土资源_矿业权招拍挂_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010403/01040303'}, {'catName': '清远市_国土资源_矿业权招拍挂_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010403/01040304'}, {'catName': '清远市_国土资源_矿业权招拍挂_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010403/01040305'}, {'catName': '清远市_国土资源_矿业权招拍挂_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010403/01040306'}, {'catName': '清远市_国土资源_矿业权招拍挂_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010403/01040307'}, {'catName': '清远市_国土资源_矿业权成交结果_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010404/01040401'}, {'catName': '清远市_国土资源_矿业权成交结果_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010404/01040402'}, {'catName': '清远市_国土资源_矿业权成交结果_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010404/01040403'}, {'catName': '清远市_国土资源_矿业权成交结果_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010404/01040404'}, {'catName': '清远市_国土资源_矿业权成交结果_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010404/01040405'}, {'catName': '清远市_国土资源_矿业权成交结果_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010404/01040406'}, {'catName': '清远市_国土资源_矿业权成交结果_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010404/01040407'}, {'catName': '清远市_国土资源_指标交易_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010405/01040501'}, {'catName': '清远市_国土资源_指标交易结果_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010406/01040601'}, {'catName': '清远市_建设工程_招标公告_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010201/01020101'}, {'catName': '清远市_建设工程_招标公告_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010201/01020102'}, {'catName': '清远市_建设工程_招标公告_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010201/01020103'}, {'catName': '清远市_建设工程_招标公告_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010201/01020104'}, {'catName': '清远市_建设工程_招标公告_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010201/01020105'}, {'catName': '清远市_建设工程_招标公告_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010201/01020106'}, {'catName': '清远市_建设工程_招标公告_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010201/01020107'}, {'catName': '清远市_建设工程_澄清公告_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010205/01020501'}, {'catName': '清远市_建设工程_澄清公告_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010205/01020502'}, {'catName': '清远市_建设工程_澄清公告_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010205/01020503'}, {'catName': '清远市_建设工程_澄清公告_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010205/01020504'}, {'catName': '清远市_建设工程_澄清公告_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010205/01020505'}, {'catName': '清远市_建设工程_澄清公告_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010205/01020506'}, {'catName': '清远市_建设工程_澄清公告_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010205/01020507'}, {'catName': '清远市_建设工程_中标候选公示_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010202/01020201'}, {'catName': '清远市_建设工程_中标候选公示_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010202/01020202'}, {'catName': '清远市_建设工程_中标候选公示_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010202/01020203'}, {'catName': '清远市_建设工程_中标候选公示_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010202/01020204'}, {'catName': '清远市_建设工程_中标候选公示_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010202/01020205'}, {'catName': '清远市_建设工程_中标候选公示_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010202/01020206'}, {'catName': '清远市_建设工程_中标候选公示_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010202/01020207'}, {'catName': '清远市_建设工程_中标结果公示_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010210/01021001'}, {'catName': '清远市_建设工程_中标结果公示_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010210/01021002'}, {'catName': '清远市_建设工程_中标结果公示_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010210/01021003'}, {'catName': '清远市_建设工程_中标结果公示_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010210/01021004'}, {'catName': '清远市_建设工程_中标结果公示_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010210/01021006'}, {'catName': '清远市_建设工程_中标结果公示_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010210/01021007'}, {'catName': '清远市_建设工程_资料下载_市直', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010203/01020301'}, {'catName': '清远市_建设工程_资料下载_连州市', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010203/01020302'}, {'catName': '清远市_建设工程_资料下载_连南县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010203/01020303'}, {'catName': '清远市_建设工程_资料下载_英德县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010203/01020304'}, {'catName': '清远市_建设工程_资料下载_阳山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010203/01020305'}, {'catName': '清远市_建设工程_资料下载_连山县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010203/01020306'}, {'catName': '清远市_建设工程_资料下载_佛冈县', 'url': 'https://www.qyggzy.cn/webIndex/newsLeftBoard/010203/01020307'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'], callback=self.parse,meta=meta)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='context_div']//td/a/@href").extract()
        try:
            meta['TokenCode'] = response.xpath("//input[@name = 'TokenCode']/@value").extract()[0]
        except:
            meta['TokenCode'] = ''
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
                    meta['n'] = n
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
        titleT = response.xpath("//td[@class='toptd1']/span/strong//text()").extract()
        timeT = response.xpath("//td[@class='toptd_bai']//text()").extract()

        try:
            regex = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}",timeT[0])[0]
        except:
            regex = '2000-01-01'
        html = response.xpath("//div[@id='context_div']").extract()

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = titleT[0]
        dict1['issueTime'] = timeReMark(regex)
        dict1['content'] = html[0]
        dict1['subclass'] = response.meta['catName']
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
        print('--------------------------------------以上是第{}页，第{}条------------------------------------------'.format(str(meta['Num']),str(meta['n'])))

        if meta['pageTune'] ==1:
            meta['Num'] +=1
            datePost = {'pageNO': str(meta['Num']), 'TokenCode': meta['TokenCode']}
            yield scrapy.FormRequest(url=meta['url'], formdata=datePost, callback=self.parse, meta=meta)



