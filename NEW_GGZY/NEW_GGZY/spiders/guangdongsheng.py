# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class GuangdongshengSpider(scrapy.Spider):
    name = 'guangdongsheng'
    allowed_domains = ['www.gpcgd.com']
    base_url= 'http://www.gpcgd.com/gpcgd/portal/portal-news!list'
    url_mark = [{'catName': '广东省_中心通知公告', 'url': 30011}, {'catName': '广东省_政府采购', 'url': 40011}, {'catName': '广东省_批量集中采购', 'url': 9001}, {'catName': '广东省_竞价公告', 'url': 200064}, {'catName': '广东省_中标结果公示', 'url': 40012}, {'catName': '广东省_采购信息预告', 'url': 40013}, {'catName': '广东省_澄清更正公告', 'url': 40014}, {'catName': '广东省_资格预审公告', 'url': 40015}, {'catName': '广东省_中标候选人公示', 'url': 40016}]


    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.url_mark)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['lb'] = i['url']
            meta['catName'] = i['catName']
            yield scrapy.FormRequest(url=self.base_url,
                                         formdata={'portalNews.typeId': str(meta['lb']), 'pageNum':str(meta['Num'])},
                                         callback=self.parse,
                                         meta=meta)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//span[@class = 'span_tit']/a/@onclick").extract()
        titleT = response.xpath("//span[@class='span_tit']//a/text()").extract()
        timeT = response.xpath("//span[@class='span_time']//a/text()").extract()
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
                    formdata = {'portalNews.typeId': str(meta['lb']),'pageNum':str(meta['Num'])}
                    yield scrapy.FormRequest(url=self.base_url,formdata=formdata,callback=self.parse,meta=meta)
                else:
                    # print('urlTemp = parse.urljoin(response.url, link[i])--------------------最终进入文章')
                    artclNum = re.findall(r"detailNews\(\'(.*?)\'\)", link[i])[0]
                    TempUrl = 'http://www.gpcgd.com/gpcgd/portal/portal-news!detailNews?portalNews.id='
                    urlTemp = TempUrl + artclNum
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
        html = response.xpath("//div[@class ='detial']").extract()
        if meta['articleTime'] == '2000-01-01 00:00:00':
            timeT = response.xpath("//div[@class ='pub_note']//text()").extract()
            try:
                meta['articleTime'] = re.findall(r"\d{2,4}-\d{1,2}-\d{1,2}", timeT[0])[0].replace('/','-')
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
