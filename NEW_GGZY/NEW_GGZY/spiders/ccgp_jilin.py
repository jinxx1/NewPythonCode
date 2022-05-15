# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()




class CcgpJilinSpider(scrapy.Spider):
    name = 'ccgp_jilin'
    allowed_domains = ['www.ccgp-jilin.gov.cn']
    base_url = 'http://www.ccgp-jilin.gov.cn/shopHome/morePolicyNews.action'
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'www.ccgp-jilin.gov.cn',
'Origin':'http://www.ccgp-jilin.gov.cn',
'Referer':'http://www.ccgp-jilin.gov.cn/shopHome/morePolicyNews.action',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}

    urlList = [{'catName': '吉林省_省级_资格预审', 'local': '124', 'lb': '1'}, {'catName': '吉林省_省级_公开招标', 'local': '124', 'lb': '2'}, {'catName': '吉林省_省级_邀请招标', 'local': '124', 'lb': '7'}, {'catName': '吉林省_省级_竞争性谈判', 'local': '124', 'lb': '4'}, {'catName': '吉林省_省级_竞争性磋商', 'local': '124', 'lb': '5'}, {'catName': '吉林省_省级_单一来源', 'local': '124', 'lb': '6'}, {'catName': '吉林省_省级_询价公告', 'local': '124', 'lb': '3'}, {'catName': '吉林省_省级_中标公告', 'local': '124', 'lb': '9'}, {'catName': '吉林省_省级_成交公告', 'local': '124', 'lb': '10'}, {'catName': '吉林省_省级_废标、更正、其他公告', 'local': '124', 'lb': '11,12,8'}, {'catName': '吉林省_省级_合同、验收公告', 'local': '124', 'lb': '13,14'}, {'catName': '吉林省_市县级_资格预审', 'local': '125', 'lb': '1'}, {'catName': '吉林省_市县级_公开招标', 'local': '125', 'lb': '2'}, {'catName': '吉林省_市县级_邀请招标', 'local': '125', 'lb': '7'}, {'catName': '吉林省_市县级_竞争性谈判', 'local': '125', 'lb': '4'}, {'catName': '吉林省_市县级_竞争性磋商', 'local': '125', 'lb': '5'}, {'catName': '吉林省_市县级_单一来源', 'local': '125', 'lb': '6'}, {'catName': '吉林省_市县级_询价公告', 'local': '125', 'lb': '3'}, {'catName': '吉林省_市县级_中标公告', 'local': '125', 'lb': '9'}, {'catName': '吉林省_市县级_成交公告', 'local': '125', 'lb': '10'}, {'catName': '吉林省_市县级_废标、更正、其他公告', 'local': '125', 'lb': '11,12,8'}, {'catName': '吉林省_市县级_合同、验收公告', 'local': '125', 'lb': '13,14'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['local'] = i['local']
            meta['lb'] = i['lb']
            datePost = {
                'currentPage': str(meta['Num']),
                'noticetypeId': meta['lb'],
                'categoryId': meta['local'],
            }
            yield scrapy.FormRequest(url=self.base_url,formdata=datePost,callback=self.parse,meta=meta,dont_filter=True,headers=self.headers)
    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@id='list_right']/ul/li/a/@href").extract()
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
                        'currentPage': str(meta['Num']),
                        'noticetypeId': meta['lb'],
                        'categoryId': meta['local'],
                    }
                    yield scrapy.FormRequest(url=self.base_url, formdata=datePost, callback=self.parse, meta=meta,
                                             dont_filter=True,headers=self.headers)
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
                                TempCat = response.xpath("//a[@href = '{}']/../em/text()".format(str(link[i]))).extract()[0]
                                meta['catName1'] = meta['catName'].replace('市县级',TempCat)
                            except:
                                meta['catName1'] = meta['catName']
                            try:
                                meta['articleTime'] = response.xpath("//a[@href = '{}']/../span/text()".format(str(link[i]))).extract()[0]
                            except:
                                continue
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,dont_filter=True,headers=self.headers)
        else:

            return None



    def parseA(self, response):
        # print('进入文章了')

        meta = response.meta
        dict1 = {}

        try:
            html = response.xpath("//div[@id='xiangqingneiron']").extract()[0]
            dict1['content'] = html
        except:
            return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle'].strip()
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['subclass'] = meta['catName1']

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
