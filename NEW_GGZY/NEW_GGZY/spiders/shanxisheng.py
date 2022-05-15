# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()


class ShanxishengSpider(scrapy.Spider):
    name = 'shanxisheng'
    allowed_domains = ['www.sxggzyjy.cn']
    urlList = [{'catName': '陕西省_交易公告_工程建设项目招标投标', 'url': 'http://www.sxggzyjy.cn/jydt/001001/001001001/{}.html'}, {'catName': '陕西省_交易公告_土地使用权和矿业权出让', 'url': 'http://www.sxggzyjy.cn/jydt/001001/001001002/{}.html'}, {'catName': '陕西省_交易公告_国有产权交易', 'url': 'http://www.sxggzyjy.cn/jydt/001001/001001003/{}.html'}, {'catName': '陕西省_交易公告_政府采购', 'url': 'http://www.sxggzyjy.cn/jydt/001001/001001004/{}.html'}, {'catName': '陕西省_交易公告_医用药品耗材及医疗机械采购', 'url': 'http://www.sxggzyjy.cn/jydt/001001/001001006/{}.html'}, {'catName': '陕西省_交易公告_煤炭产能指标交易', 'url': 'http://www.sxggzyjy.cn/jydt/001001/001001013/{}.html'}, {'catName': '陕西省_交易公告_其他', 'url': 'http://www.sxggzyjy.cn/jydt/001001/001001012/{}.html'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,meta=meta)



    def parse(self, response):
        meta = response.meta
        titleT = response.xpath("//a[@class='ewb-list-name ewb-otw']/text()").extract()
        link = response.xpath("//a[@class='ewb-list-name ewb-otw']/@href").extract()
        timeT = response.xpath("//a[@class='ewb-list-name ewb-otw']/../span/text()").extract()
        titleT = remarkList(titleT)

        if len(link) != len(titleT) or len(titleT) != len(timeT):
            return None

        GotArtcl = 0
        notGotArtcl = 0
        if len(link) > 0:

            for i in range(len(link) + 1):
                urlListTemp = []
                # print('进入List循环体了')
                if notGotArtcl == 0 and GotArtcl == len(link):
                    # print('notGotArtcl == 0 and GotArtcl == len(link)-------------------------------没有新文章退出')
                    return None
                elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(link):
                    # print('notGotArtcl !=0 and notGotArtcl + GotArtcl == len(link)--------------------翻页')
                    meta['Num'] += 1
                    url = meta['url'].format(str(meta['Num']))
                    yield scrapy.Request(url=url, callback=self.parse, meta=meta)
                else:
                    # print('urlTemp = parse.urljoin(response.url, link[i])--------------------最终进入文章')
                    urlTemp = parse.urljoin(response.url, link[i])
                    urlListTemp.append(urlTemp + TEMPPATH)
                    urllist = urlIsExist(urlListTemp)
                    if len(urllist) < 1:
                        GotArtcl += 1
                        continue
                    else:
                        notGotArtcl += 1
                        for url in urllist:
                            meta['articleTitle'] = titleT[i]
                            meta['articleTime'] = timeT[i].replace('[','').replace(']','')
                            if not meta['articleTitle']:
                                meta['articleTitle'] = '本文暂无标题'
                            if not meta['articleTime']:
                                meta['articleTime'] = '2000-01-01 00:00:00'
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta)
        else:

            return None

    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        dict1 = {}
        html = response.xpath("//div[@id='mainContent']").extract()
        if meta['articleTime'] == '2000-01-01 00:00:00':
            timeT = response.xpath("//div[@class='info-source']/text()").extract()
            timeT = remarkList(timeT)

            try:
                meta['articleTime'] = re.findall(r"\d{2,4}-\d{1,2}-\d{1,2}", timeT)[0].replace('/','-')
            except:
                meta['articleTime'] = '2000-01-01'
        if html:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = meta['articleTitle']
            dict1['issueTime'] = timeReMark(meta['articleTime'])
            dict1['content'] = html[0]
            dict1['subclass'] = meta['catName']
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
            print('----------------------------------------------------------------------------------------------')
        else:
            return None
