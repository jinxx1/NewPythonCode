# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()


class GdMeizhouSpider(scrapy.Spider):
    name = 'gd_meizhou'
    allowed_domains = ['mzggzy.meizhou.gov.cn']
    base_urls = [{'catName': '梅州市_政府采购_采购公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/zfcg/003001/Default.aspx?Paging={}'}, {'catName': '梅州市_政府采购_更正公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/zfcg/003002/Default.aspx?Paging={}'}, {'catName': '梅州市_政府采购_中标公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/zfcg/003003/Default.aspx?Paging={}'}, {'catName': '梅州市_建设工程_招标公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/jsgc/004001/?Paging={}'}, {'catName': '梅州市_建设工程_通知公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/jsgc/004002/?Paging={}'}, {'catName': '梅州市_建设工程_资审公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/jsgc/004003/?Paging={}'}, {'catName': '梅州市_建设工程_中标公示', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/jsgc/004004/?Paging={}'}, {'catName': '梅州市_建设工程_中标结果公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/jsgc/004005/?Paging={}'}, {'catName': '梅州市_土地和矿权_土地和矿业权招拍挂公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/tdky/005003/005003001/Default.aspx?Paging={}'}, {'catName': '梅州市_土地和矿权_土地和矿业权招拍挂结果公示', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/tdky/005003/005003002/?Paging={}'}, {'catName': '梅州市_产权交易_产权交易公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/cqjy/006001/?Paging={}'}, {'catName': '梅州市_产权交易_产权交易资料', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/cqjy/006002/?Paging={}'}, {'catName': '梅州市_产权交易_产权交易结果公告', 'url': 'https://mzggzy.meizhou.gov.cn/TPFront/cqjy/006003/?Paging={}'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.base_urls)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,meta=meta)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//li[@class='ewb-data-item']//a/@href").extract()
        titleT = response.xpath("//li[@class='ewb-data-item']//a/text()").extract()
        timeT = response.xpath("//li[@class='ewb-data-item']/span/text()").extract()
        titleT = remarkList(titleT)
        link = remarkList(link)

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
                            meta['articleTime'] = timeT[i]
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
        html = response.xpath("//td[@id='TDContent']").extract()
        if meta['articleTime'] == '2000-01-01 00:00:00':
            timeT = response.xpath("//td[@bgcolor = '#ececec' and @align = 'center']/text()").extract()
            try:
                meta['articleTime'] = re.findall(r"\d{4}\/\d{1,2}\/\d{1,2}", timeT[0])[0].replace('/','-')
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
            print(
                '-------------------------------------------------------------------------------------------------------------------------')
        else:

            return None











