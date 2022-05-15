# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()




class CcgpXizangSpider(scrapy.Spider):
    name = 'ccgp_xizang'
    allowed_domains = ['www.ccgp-xizang.gov.cn']
    urlList = [{'catName': '西藏自治区_省级_结果', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=13'}, {'catName': '西藏自治区_省级_中标', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=9'}, {'catName': '西藏自治区_省级_合同', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=8'}, {'catName': '西藏自治区_省级_邀请', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=7'}, {'catName': '西藏自治区_省级_招标', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=2'}, {'catName': '西藏自治区_省级_单一', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=6'}, {'catName': '西藏自治区_省级_询价', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=3'}, {'catName': '西藏自治区_省级_成交', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=10'}, {'catName': '西藏自治区_省级_竞争性谈判', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=4'}, {'catName': '西藏自治区_省级_竞争性磋商', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=5'}, {'catName': '西藏自治区_省级_其他', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=124&noticetypeId=1,11,12'}, {'catName': '西藏自治区_市县_结果', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=13'}, {'catName': '西藏自治区_市县_中标', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=9'}, {'catName': '西藏自治区_市县_合同', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=8'}, {'catName': '西藏自治区_市县_邀请', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=7'}, {'catName': '西藏自治区_市县_招标', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=2'}, {'catName': '西藏自治区_市县_单一', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=6'}, {'catName': '西藏自治区_市县_询价', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=3'}, {'catName': '西藏自治区_市县_成交', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=10'}, {'catName': '西藏自治区_市县_竞争性谈判', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=4'}, {'catName': '西藏自治区_市县_竞争性磋商', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=5'}, {'catName': '西藏自治区_市县_其他', 'url': 'http://www.ccgp-xizang.gov.cn/shopHome/morePolicyNews.action?categoryId=125&noticetypeId=1,11,12'}]

    def start_requests(self):
        meta = {}
        meta['ListReView'] = 0
        meta['ContentReView'] = 0
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            datePost = {
                "currentPage": str(meta['Num'])
            }
            yield scrapy.FormRequest(url=meta['url'],formdata=datePost,callback=self.parse,meta=meta,dont_filter=True)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@id='news_div']/ul/li/div/a/@href").extract()


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
                    datePost = {
                        "currentPage": str(meta['Num'])
                    }
                    yield scrapy.FormRequest(url=meta['url'], formdata=datePost, callback=self.parse, meta=meta,
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
                            try:
                                meta['articleTitle'] = response.xpath("//a[@href = '{}']/text()".format(str(link[i]))).extract()[0]
                            except:

                                continue

                            try:
                                meta['articleTime'] = response.xpath("//a[@href = '{}']/../../span/text()".format(str(link[i]))).extract()[0]
                            except:

                                continue

                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,dont_filter=True)
        else:

            if meta['ListReView'] < 4:
                meta['ListReView'] += 1
                datePost = {
                    "currentPage": str(meta['Num'])
                }

                print("没有获取文章链接，休息5秒钟重新尝试。共三次，当前第{}次".format(str(meta['ListReView'])))
                time.sleep(5)
                yield scrapy.FormRequest(url=meta['url'], formdata=datePost, callback=self.parse, meta=meta,
                                         dont_filter=True)
            else:
                meta['ListReView'] = 0
                print('3次重新访问后，该页面没有list列表')
                meta['ListErrorWord'] = '3次重新访问后，该页面没有list列表'
                errorLOG(meta)
                return None



    def parseA(self, response):
        # print('进入文章了')

        meta = response.meta
        dict1 = {}

        try:
            html = response.xpath("//div[@class='neirong']").extract()[0]
            dict1['content'] = html
        except:
            if meta['ContentReView'] < 4:
                meta['ContentReView'] += 1
                print("没有获取正文，休息5秒钟重新尝试。共三次，当前第{}次".format(str(meta['ContentReView'])))
                time.sleep(5)
                yield scrapy.Request(url=response.url, callback=self.parseA, meta=meta, dont_filter=True)

            else:
                meta['ContentReView'] = 0
                print('3次重新访问后，该页面没有list列表')
                meta['ContentErrorWord'] = '3次重新访问后，没有获取正文'
                meta['ContentErrorUrl'] = response.url
                errorLOG(meta)
                return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle'].strip()
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['subclass'] = meta['catName']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print(len(dict1['content']))
        save_api(dict1)
        print('--------------------------------------------------------------------------------------------')




