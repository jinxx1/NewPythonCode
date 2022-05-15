# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class ZhejiangshengSpider(scrapy.Spider):
    name = 'zhejiangsheng'
    allowed_domains = ['new.zmctc.com']
    urlList = [{'catName': '浙江省_评标专家公示_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004009/004009001/?Paging={}'}, {'catName': '浙江省_评标专家公示_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004009/004009002/?Paging={}'}, {'catName': '浙江省_评标专家公示_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004009/004009003/?Paging={}'}, {'catName': '浙江省_开标实况_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004008/004008001/?Paging={}'}, {'catName': '浙江省_开标实况_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004008/004008002/?Paging={}'}, {'catName': '浙江省_中标候选人公示_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004006/004006001/?Paging={}'}, {'catName': '浙江省_中标候选人公示_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004006/004006002/?Paging={}'}, {'catName': '浙江省_中标候选人公示_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004006/004006003/?Paging={}'}, {'catName': '浙江省_资格预审公示_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004005/004005001/?Paging={}'}, {'catName': '浙江省_资格预审公示_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004005/004005002/?Paging={}'}, {'catName': '浙江省_资格预审公示_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004005/004005003/?Paging={}'}, {'catName': '浙江省_开标结果_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004004/004004001/?Paging={}'}, {'catName': '浙江省_开标结果_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004004/004004002/?Paging={}'}, {'catName': '浙江省_开标结果_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004004/004004003/?Paging={}'}, {'catName': '浙江省_项目登记_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004003/004003001/?Paging={}'}, {'catName': '浙江省_项目登记_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004003/004003002/?Paging={}'}, {'catName': '浙江省_项目登记_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004003/004003003/?Paging={}'}, {'catName': '浙江省_补充文件_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004002/004002001/?Paging={}'}, {'catName': '浙江省_补充文件_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004002/004002002/?Paging={}'}, {'catName': '浙江省_补充文件_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004002/004002003/?Paging={}'}, {'catName': '浙江省_招标公告_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004001/004001001/?Paging={}'}, {'catName': '浙江省_招标公告_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004001/004001002/?Paging={}'}, {'catName': '浙江省_招标公告_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004001/004001003/?Paging={}'}, {'catName': '浙江省_招标公告_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004001/004001004/?Paging={}'}, {'catName': '浙江省_补充文件_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004002/004002004/?Paging={}'}, {'catName': '浙江省_项目登记_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004003/004003004/?Paging={}'}, {'catName': '浙江省_开标结果_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004004/004004004/?Paging={}'}, {'catName': '浙江省_资格预审公示_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004005/004005004/?Paging={}'}, {'catName': '浙江省_中标候选人公示_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004006/004006004/?Paging={}'}, {'catName': '浙江省_开标实况_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004008/004008003/?Paging={}'}, {'catName': '浙江省_开标实况_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004008/004008004/?Paging={}'}, {'catName': '浙江省_评标专家公示_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004009/004009004/?Paging={}'}, {'catName': '浙江省_中标结果公告_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004010/004010001/?Paging={}'}, {'catName': '浙江省_中标结果公告_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004010/004010002/?Paging={}'}, {'catName': '浙江省_中标结果公告_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004010/004010003/?Paging={}'}, {'catName': '浙江省_中标结果公告_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004010/004010004/?Paging={}'}, {'catName': '浙江省_招标文件公示_工程', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004011/004011001/?Paging={}'}, {'catName': '浙江省_招标文件公示_货物', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004011/004011002/?Paging={}'}, {'catName': '浙江省_招标文件公示_服务', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004011/004011003/?Paging={}'}, {'catName': '浙江省_招标文件公示_其他', 'url': 'http://new.zmctc.com/zjgcjy/jyxx/004011/004011004/?Paging={}'}]


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
        link = response.xpath("//a[@class='WebList_sub']/@href").extract()
        titleT = response.xpath("//a[@class='WebList_sub']/@title").extract()
        timeT = response.xpath("//a[@class='WebList_sub']/../../td[@width = '80']/text()").extract()
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
        html = response.xpath("//td[@id='TDContent']").extract()
        if meta['articleTime'] == '2000-01-01 00:00:00':
            timeT = response.xpath("//td[@id='tdTitle']/font[@color='#888888']/text()").extract()
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
            print('----------------------------------------------------------------------------------------------')
        else:
            print('最终页未能获取到文章内容',response.url)

            return None


