# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()


class CcgpGuangdongSpider(scrapy.Spider):
    name = 'ccgp_guangdong'
    allowed_domains = ['www.ccgp-guangdong.gov.cn']
    urlList = [{'catName': '广东省_审核前公示', 'channelCode': '-4', 'url': 'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do'}, {'catName': '广东省_资格预审公告', 'channelCode': '-6', 'url': 'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do'}, {'catName': '广东省_采购公告', 'channelCode': '00051', 'url': 'http://www.ccgp-guangdong.gov.cn/queryMoreCityCountyInfoList2.do'}, {'catName': '广东省_更正公告', 'channelCode': '0006', 'url': 'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do'}, {'catName': '广东省_结果公告', 'channelCode': '0008', 'url': 'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do'}, {'catName': '广东省_代理机构公示', 'channelCode': '0014', 'url': 'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do'}, {'catName': '广东省_电子反拍公告', 'channelCode': '0017', 'url': 'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do'}, {'catName': '广东省_批量集中采购', 'channelCode': '-3', 'url': 'http://www.ccgp-guangdong.gov.cn/queryMoreInfoList.do'}]

    def start_requests(self):
        meta = {}
        meta['ListReView'] = 0
        meta['ContentReView'] = 0
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])

        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['channelCode'] = i['channelCode']
            meta['url'] = i['url']
            datapost = {
            'channelCode':meta['channelCode'],
            'pointPageIndexId': '1',
            'pageIndex': str(meta['Num']),
            'pageSize': '200',
            'sitewebId': '-1'
        }
            yield scrapy.FormRequest(url=meta['url'], formdata=datapost, callback=self.parse, meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//ul[@class='m_m_c_list']/li/a/@href").extract()

        if len(link) > 0:
            urlListTemp = []
            for nonUrl in link:
                urlTemp = parse.urljoin(response.url, nonUrl)
                urlListTemp.append(urlTemp)
            # print('给链接API的链接数为：',len(urlListTemp))
            urllist = urlIsExist(urlListTemp)
            # print('API返回的链接数为：',len(urllist))
            if len(urllist)<1:
                return None
            else:
                DictUrlLIST = []
                for link_i in range(len(link)):
                    for urllist_i in range(len(urllist)):
                        if link[link_i] in urllist[urllist_i]:
                            dictUrl = {}
                            dictUrl['regexUrl'] = link[link_i]
                            dictUrl['requestUrl'] = urllist[urllist_i]
                            DictUrlLIST.append(dictUrl)

                for i in range(len(DictUrlLIST) + 1):
                    if i == len(DictUrlLIST):
                        meta['Num']+=1
                        datapost = {
                            'channelCode': meta['channelCode'],
                            'pointPageIndexId': '1',
                            'pageIndex': str(meta['Num']),
                            'pageSize': '200',
                            'sitewebId': '-1'
                        }
                        yield scrapy.FormRequest(url=meta['url'], formdata=datapost, callback=self.parse, meta=meta,
                                                 dont_filter=True)
                    else:
                        try:
                            meta['articleTitle'] = response.xpath("//*[@href = '{}']/./@title".format(DictUrlLIST[i]['regexUrl'])).extract()[0]
                        except:

                            continue
                        try:
                            meta['articleTime'] = response.xpath("//*[@href = '{}']/../em/text()".format(DictUrlLIST[i]['regexUrl'])).extract()[0]
                        except:

                            continue

                        catnamelist = response.xpath("//*[@href = '{}']/../span/a/text()".format(DictUrlLIST[i]['regexUrl'])).extract()
                        if catnamelist:
                            catname1 = '_'.join(catnamelist)
                            meta['catName1'] = meta['catName'] + '_' + catname1
                        else:
                            meta['catName1'] = meta['catName']

                        requestUrl =  DictUrlLIST[i]['requestUrl']

                        yield scrapy.Request(url=requestUrl, callback=self.parseA, meta=meta, dont_filter=True)

        else:
            if meta['ListReView'] < 4:
                meta['ListReView'] += 1
                datapost = {
                    'channelCode': meta['channelCode'],
                    'pointPageIndexId': '1',
                    'pageIndex': str(meta['Num']),
                    'pageSize': '200',
                    'sitewebId': '-1'
                }
                print("没有获取文章链接，休息5秒钟重新尝试。共三次，当前第{}次".format(str(meta['ListReView'])))
                time.sleep(5)
                yield scrapy.FormRequest(url=meta['url'], formdata=datapost, callback=self.parse, meta=meta,
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
        meta['requestContentNum'] = 0
        dict1 = {}
        html = response.xpath("//div[@class='zw_c_c_cont']").extract()
        if meta['articleTime'] == '2000-01-01 00:00:00':
            timeT = response.xpath("//div[@class='zw_c_c_qx']/p/span[3]/text()").extract()
            try:
                meta['articleTime'] = re.findall(r"\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}", timeT[0])[0].replace('/', '-')
            except:
                meta['articleTime'] = '2000-01-01'

        if html:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = meta['articleTitle']
            dict1['issueTime'] = timeReMark(meta['articleTime'])
            dict1['content'] = html[0]
            dict1['subclass'] = meta['catName1']

            print(dict1['title'])
            print(dict1['url'])
            print(dict1['issueTime'])
            print(dict1['subclass'])
            print(len(dict1['content']))
            # save_api(dict1)
            print('---------------------------------------------------------------------------------------------------------')
        else:
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


