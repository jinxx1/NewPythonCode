# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()




class CcgpDalianSpider(scrapy.Spider):
    name = 'ccgp_dalian'
    allowed_domains = ['www.ccgp-dalian.gov.cn']
    baseUrl = 'http://www.ccgp-dalian.gov.cn/dlweb/showinfo/bxmoreinfo.aspx?CategoryNum={}'
    urlList = [{'catName': '大连市_市直_采购公告及文件公示', 'url': '003001001'}, {'catName': '大连市_市直_中标及废标公告', 'url': '003002001'}, {'catName': '大连市_市直_单一来源公示', 'url': '003004001'}, {'catName': '大连市_市直_采购合同公告', 'url': '003005001'}, {'catName': '大连市_县区_采购公告及文件公示', 'url': '003001002'}, {'catName': '大连市_县区_中标及废标公告', 'url': '003002002'}, {'catName': '大连市_县区_单一来源公示', 'url': '003004002'}, {'catName': '大连市_县区_采购合同公告', 'url': '003005002'}]

    # urlList = [{'catName': '大连市_市直_采购公告及文件公示','url': '003001001'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = self.baseUrl.format(i['url'])
            yield scrapy.Request(url=meta['url'],callback=self.netxPage,meta=meta,dont_filter=True)

    def netxPage(self, response):
        meta = response.meta
        try:
            EVENTVALIDATION = response.xpath("//input[@id = '__EVENTVALIDATION']/@value").extract()[0]
            VIEWSTATE = response.xpath("//input[@id = '__VIEWSTATE']/@value").extract()[0]
            VIEWSTATEGENERATOR = response.xpath("//input[@id = '__VIEWSTATEGENERATOR']/@value").extract()[0]
        except:
            return None
        dataPost = {
            '__VIEWSTATE':VIEWSTATE,
            '__VIEWSTATEGENERATOR':VIEWSTATEGENERATOR,
            '__EVENTTARGET':'MoreInfoList$Pager',
            '__EVENTARGUMENT': str(meta['Num']),
            '__VIEWSTATEENCRYPTED':'',
            '__EVENTVALIDATION':EVENTVALIDATION,
            'MoreInfoList$Titletxt':''
        }
        yield scrapy.FormRequest(url=meta['url'],callback=self.parse,formdata=dataPost,meta=meta,dont_filter=True)


    def parse(self, response):
        meta = response.meta
        titleT = response.xpath("//td[@class='border']//a/@title").extract()
        link = response.xpath("//td[@class='border']//a/@href").extract()
        timeTemp = response.xpath("//td[@class='border' and @style='width:80px;']/text()").extract()
        timeT = remarkList(timeTemp)
        if len(link) != len(titleT) or len(titleT) != len(timeT):
            return None
        GotArtcl = 0
        notGotArtcl = 0
        if len(link) > 0:

            for i in range(len(link) + 1):
                urlListTemp = []
                # print('进入List循环体了')
                if notGotArtcl == 0 and GotArtcl == len(link):
                    # print('-------------------------------没有新文章退出')
                    return None
                elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(link):
                    # print('--------------------翻页')
                    meta['Num'] += 1
                    yield scrapy.Request(url=meta['url'], callback=self.netxPage, meta=meta,dont_filter=True)
                else:
                    # print('--------------------最终进入文章')
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
                            meta['articleTime'] = timeT[i]
                            if not meta['articleTime']:
                                meta['articleTime'] = '2000-01-01 00:00:00'
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta)
        else:

            return None


    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta

        dict1 = {}
        html = response.xpath("//table[@id='tblInfo']").extract()

        if '..' in meta['articleTitle']:
            try:
                meta['articleTitle'] = response.xpath("//td[@id='tdTitle']/font/b/text()").extract()[0].strip()
            except:
                pass
        if html:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = meta['articleTitle']
            dict1['issueTime'] = timeReMark(meta['articleTime'])
            dict1['content'] = html[0]
            dict1['subclass'] = meta['catName'].replace(' ','')
            requestsAPI = save_api(dict1)

            tempDict = meta['Breakpoint']
            tempDict['Num'] = meta['Num']
            writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

            print(dict1['title'])
            print(dict1['url'])
            print(dict1['issueTime'])
            print(dict1['subclass'])
            print(len(dict1['content']))
            print('列表页，第{}页'.format(meta['Num']))
            print(requestsAPI.text)
            print('-----------------------------------------------------------------------------------------------------------------------')
        else:
            print('最终页未能获取到文章内容', response.url)
            return None
