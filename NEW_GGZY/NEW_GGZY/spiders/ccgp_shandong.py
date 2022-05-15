# -*- coding: utf-8 -*-
import scrapy
# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,datetime
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpShandongSpider(scrapy.Spider):
    name = 'ccgp_shandong'
    allowed_domains = ['www.ccgp-shandong.gov.cn']
    base_url = 'http://www.ccgp-shandong.gov.cn/sdgp2017/site/channelall.jsp'
    urlList = [
        {'catName': '山东省_省采购公告', 'url': '0301'},
        {'catName': '山东省_省中标公告', 'url': '0302'},
        {'catName': '山东省_市县采购公告', 'url': '0303'},
        {'catName': '山东省_市县中标公告', 'url': '0304'},
        {'catName': '山东省_信息更正', 'url': '0305'},
        {'catName': '山东省_废标公告', 'url': '0306'},
        {'catName': '山东省_资格预审公告', 'url': '0307'}]


    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            datapost = {
                'colcode': meta['url'],
                'curpage': str(meta['Num'])
            }
            yield scrapy.FormRequest(url=self.base_url,formdata=datapost,callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        titleT = response.xpath("//td[@background = 'images/main/table_bk_04.jpg']//td[@class='Font9']/a[@class='five']/@title").extract()
        link = response.xpath("//td[@background = 'images/main/table_bk_04.jpg']//td[@class='Font9']/a[@class='five']/@href").extract()

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
                    datapost = {
                        'colcode': meta['url'],
                        'curpage': str(meta['Num'])
                    }
                    yield scrapy.FormRequest(url=self.base_url, formdata=datapost, callback=self.parse, meta=meta,
                                             dont_filter=True)
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
                            try:
                                timeWord = response.xpath("//td[@class='Font9']/a[@class='five' and @title='{}']/..".format(meta['articleTitle'])).extract()[0]
                                timeT = re.findall("\d{4}-\d{1,2}-\d{1,2}", timeWord)[0]
                                meta['articleTime'] = timeT
                            except:
                                return None
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,
                                                 dont_filter=True)

        else:
            return None

    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        dict1 = {}
        html = response.xpath("//td[@background = 'images/erji/er_bk_04.jpg']/../td[@bgcolor = '#FFFFFF']").extract()

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
            print('----------------------------------------------------------------------------------------------------------')
        else:
            return None
