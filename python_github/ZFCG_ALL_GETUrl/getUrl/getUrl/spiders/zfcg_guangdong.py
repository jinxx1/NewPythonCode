# -*- coding: utf-8 -*-
import scrapy,time,datetime,re,pprint,json
# from fake_useragent import UserAgent
# ua = UserAgent()
from urllib import parse
from getUrl.items import GeturlItem
from getUrl.rexGetTime import timeReMark

from getUrl.DB_object import *


def list2str(localName):
    return ''.join(localName).replace('\n', '').replace('\t', '').replace('\r', '').strip().replace('[ ', '').replace('[', '').replace(']','').strip().replace(' · ', '_').replace('·', '_').strip()
def next_Month(metadict):
    meta = metadict
    try:
        wandaytouple = time.mktime(datetime.datetime.strptime(meta['wanday'], "%Y-%m-%d").timetuple())
    except:
        wandaytouple = time.mktime(
            datetime.datetime.strptime(meta['wanday'].strftime('%Y-%m-%d'), "%Y-%m-%d").timetuple())
    dateendday = datetime.datetime(1994, 1, 1)
    endtouple = time.mktime(dateendday.timetuple())

    if wandaytouple < endtouple:
        return None
    else:
        print('下一个月开始')
        onemonuthday = meta['zaoday']
        try:
            meta['wanday'] = datetime.datetime.strptime(onemonuthday, "%Y-%m-%d") - datetime.timedelta(days=1)
            meta['zaoday'] = datetime.datetime.strptime(onemonuthday, "%Y-%m-%d") - datetime.timedelta(days=30)
        except:
            meta['wanday'] = datetime.datetime.strptime(onemonuthday.strftime('%Y-%m-%d'),
                                                        "%Y-%m-%d") - datetime.timedelta(days=1)
            meta['zaoday'] = datetime.datetime.strptime(onemonuthday.strftime('%Y-%m-%d'),
                                                        "%Y-%m-%d") - datetime.timedelta(days=30)
        try:
            del meta['datapost']['pointPageIndexId']
        except:
            pass
        try:
            del meta['datapost']['pageIndex']
        except:
            pass

        meta['Num'] = 1
        try:
            del meta['datapost']['pageSize']
        except:
            pass
        meta['datapost']['channelCode'] = str(meta['channelCode'])
        try:
            meta['datapost']['operateDateFrom'] = str(meta['zaoday'].strftime('%Y-%m-%d'))  # 早
            meta['datapost']['operateDateTo'] = str(meta['wanday'].strftime('%Y-%m-%d'))  # 晚
        except:
            meta['datapost']['operateDateFrom'] = str(meta['zaoday'])  # 早
            meta['datapost']['operateDateTo'] = str(meta['wanday'])  # 晚
        meta['datapost']['isAdjust'] = ''
        print(str(meta['zaoday']), str(meta['wanday']))
        return meta
def next_page(metadict):
    meta = metadict
    NNum = meta['Num']
    meta['Num'] += 1
    print('-----翻页，当前第{}页-----{}'.format(NNum, meta['catName']))
    meta['datapost']['channelCode'] = str(meta['channelCode'])
    meta['datapost']['pageIndex'] = str(meta['Num'])
    try:
        meta['datapost']['operateDateFrom'] = str(meta['zaoday'].strftime('%Y-%m-%d'))  # 早
        meta['datapost']['operateDateTo'] = str(meta['wanday'].strftime('%Y-%m-%d'))  # 晚
    except:
        meta['datapost']['operateDateFrom'] = str(meta['zaoday'])  # 早
        meta['datapost']['operateDateTo'] = str(meta['wanday'])  # 晚
    meta['datapost']['pointPageIndexId'] = str(NNum)
    print(str(meta['zaoday']),str(meta['wanday']))
    return meta


class ZfcgGuangdongSpider(scrapy.Spider):
    name = 'zfcg_guangdong'
    collName = name + '_getUrl'
    allowed_domains = ['www.ccgp-guangdong.gov.cn']
    BRT = MongoDB_obj()
    BRT_urllist = BRT.breakpoint(collName,urllistP())

    datapost = {"channelCode": "",
                "pageIndex": "",
                "pageSize":"200",

                "issueOrgan": "",
                "performOrgName": "",
                "purchaserOrgName": "",
                "regionIds": "",
                "sitewebName": "",
                "stockIndexName": "",
                "stockNum": "",
                "stockTypes": "",
                "title": "",
                "isAdjust":"",

                "sitewebId":"-1",
                "operateDateFrom":"",#早
                "operateDateTo":"",#晚
                "pointPageIndexId":"1"
                }

    def start_requests(self):
        meta = {}
        meta['collName'] = self.collName
        meta['datapost'] = self.datapost


        for i in self.BRT_urllist:
            meta['catName'] = i['catName']
            meta['channelCode'] = i['channelCode']
            meta['url'] = i['requestUrl']
            meta['Num'] = i['Num']
            meta['zaoday'] = i['zaoday']
            meta['wanday'] = i['wanday']

            meta['datapost']['channelCode'] = str(meta['channelCode'])
            meta['datapost']['pageIndex'] = str(meta['Num'])
            meta['datapost']['operateDateFrom'] = str(meta['zaoday'])  # 早
            meta['datapost']['operateDateTo'] = str(meta['wanday'])  # 晚
            yield scrapy.FormRequest(url=meta['url'], formdata=meta['datapost'], callback=self.parse, meta=meta,
                                     dont_filter=True)

    def parse(self,response):
        item = GeturlItem()
        meta = response.meta
        try:
            meta['first'] += 1
        except:
            meta['first'] = 0

        del meta['datapost']

        meta['datapost'] = self.datapost

        link = response.xpath("//ul[@class='m_m_c_list']/li/a/@href").extract()

        if len(link) > 0:
            link2dewei = [{'pagelink': link[i], 'articllink': parse.urljoin(response.url, link[i])} for i in range(len(link))]
            quchongURL = self.BRT.url_deWeighting(self.collName, link2dewei)

            if len(quchongURL) == 0:
                nextPagemeta = next_page(meta)
                yield scrapy.FormRequest(url=meta['url'], formdata=nextPagemeta['datapost'], callback=self.parse,
                                         meta=nextPagemeta,
                                         dont_filter=True)
            else:
                print('有{}条数据可以录入'.format(len(quchongURL)))
                for i in quchongURL:
                    try:
                        item['title'] = response.xpath("//*[@href='{}']/@title".format(i['pagelink'])).extract()[0]
                        issueTime = response.xpath("//*[@href='{}']/../em/text()".format(i['pagelink'])).extract()[0]
                        item['issueTime'] = timeReMark(issueTime)
                    except:
                        continue

                    localName = response.xpath("//*[@href='{}']/../span//text()".format(i['pagelink'])).extract()
                    if localName:
                        strtitle = list2str(localName)
                        item['subclass'] = meta['catName'] + '_' + strtitle
                    else:
                        item['subclass'] = meta['catName']

                    item['ArticleUrl'] = i['articllink']
                    item['RequestUrl'] = meta['url']
                    item['Num'] = meta['Num']
                    item['channelCode'] = meta['channelCode']
                    item['collName'] = meta['collName']
                    
                    try:
                        item['zaoday'] = time.mktime(
                            datetime.datetime.strptime(str(meta['zaoday'].strftime('%Y-%m-%d')),"%Y-%m-%d").timetuple())
                        item['wanday'] = time.mktime(
                            datetime.datetime.strptime(str(meta['wanday'].strftime('%Y-%m-%d')),"%Y-%m-%d").timetuple())
                    except:
                        item['zaoday'] = time.mktime(datetime.datetime.strptime(meta['zaoday'], "%Y-%m-%d").timetuple())
                        item['wanday'] = time.mktime(datetime.datetime.strptime(meta['wanday'], "%Y-%m-%d").timetuple())

                    yield item

            if len(quchongURL) == 200 or len(quchongURL) == 15 or meta['first'] == 0:
                nextPagemeta = next_page(meta)
                yield scrapy.FormRequest(url=meta['url'], formdata=nextPagemeta['datapost'], callback=self.parse,
                                         meta=nextPagemeta,
                                         dont_filter=True)
            else:
                nextMonth = next_Month(meta)
                yield scrapy.FormRequest(url=meta['url'], formdata=nextMonth['datapost'], callback=self.parse,
                                         meta=nextMonth,
                                         dont_filter=True)
        else:
            metanext = next_Month(meta)
            yield scrapy.FormRequest(url=meta['url'], formdata=metanext['datapost'], callback=self.parse, meta=metanext,
                                     dont_filter=True)
