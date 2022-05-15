# -*- coding: utf-8 -*-
import scrapy,re,pprint,requests
import json,datetime
from getUrl.items import GeturlItem

b = datetime.datetime.now().strftime("%Y-%m-%d")
nowTime = datetime.datetime.strptime(b, "%Y-%m-%d")
# nowTime = '2019-08-27 00:00:00'
strnowTime = str(nowTime).split(' ')[0]


class CtSpider(scrapy.Spider):
    nn = 1

    name = 'ct'
    collName = 'monitorUrl'
    allowed_domains = ['caigou.chinatelecom.com.cn']
    start_urls = [{'catName': '中国电信_采购结果公告_集团', 'url': 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/resultannounc/listForAd.do?provinceJT=JT'},
                  {'catName': '中国电信_采购结果公告_省公司', 'url': 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/resultannounc/listForAd.do?provinceJT=NJT'},
                  {'catName': '中国电信_资格预审公告_省公司', 'url': 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/prequalfication/listForAd.do?provinceCodeNew=NJT'},
                  {'catName': '中国电信_资格预审公告_集团', 'url': 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/prequalfication/listForAd.do?provinceCodeNew=JT'},
                  {'catName': '中国电信_采购公告_省公司', 'url': 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=NJT'},
                  {'catName': '中国电信_采购公告_集团', 'url': 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/announcementjoin/list.do?provinceJT=JT'},
                  {'catName': '中国电信_澄清公告_省公司', 'url': 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/clearifynotice/listForAd.do?provinceJT=NJT'},
                  {'catName': '中国电信_澄清公告_集团', 'url': 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/clearifynotice/listForAd.do?provinceJT=JT'}]

    def start_requests(self):
        meta = {}

        meta['Num'] = 1
        PostDate = {
            'startDate': str(nowTime),
            'paging.start': '1',
            'paging.pageSize': '20000',
            'pageNum': '20000',
            'goPageNum': '1',
            'paging.start': '1',
            'paging.pageSize': '20000',
            'pageNum': '20000',
            'goPageNum': '1',
        }
        for i in self.start_urls:
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            if '澄清公告' in meta['catName']:
                PostDate = {
                    'paging.start': '1',
                    'paging.pageSize': '20000',
                    'pageNum': '20000',
                    'goPageNum': '1',
                    'paging.start': '1',
                    'paging.pageSize': '20000',
                    'pageNum': '20000',
                    'goPageNum': '1',
                }
            yield scrapy.FormRequest(url=meta['url'], callback=self.parse,
                                 dont_filter=True,
                                 formdata=PostDate,meta=meta
                                 )

    def parse(self, response):
        meta = response.meta
        item = GeturlItem()

        finD = {'issueTime': strnowTime, 'site': '中国电信'}
        dec = requests.post('http://localhost:1111/apiGetMongoInfo', data=json.dumps(finD)).text
        jsonT = json.loads(dec)['message']
        mongoLinkAll = [x['url'] for x in jsonT]

        icAll = response.xpath("//table[@class='table_data']//a/@onclick").extract()
        baseurl = 'https://caigou.chinatelecom.com.cn/MSS-PORTAL/clearifynotice/viewHome.do?id={}&encryCode={}'


        for i in icAll:
            regx = re.findall("\'(.*?)\'", i)
            item['url'] = baseurl.format(regx[0],regx[1])

            if item['url'] not in mongoLinkAll:

                item['collName'] = self.collName
                item['site'] = '中国电信'
                item['domain'] = self.allowed_domains[0]
                item['from_Page'] = meta['url']

                try:
                    item['title'] = response.xpath('//*[@onclick = "{}"]/text()'.format(i)).extract_first()
                except:
                    item['title'] = ''

                try:
                    item['subclass'] = meta['catName'] + response.xpath('//*[@onclick = "{}"]/../../td[1]/text()'.format(i)).extract_first()
                except:
                    item['subclass'] = meta['catName']


                if '资格预审' in meta['catName'] :
                    issueTime = response.xpath('//*[@onclick = "{}"]/../../td[9]/text()'.format(i)).extract_first()
                elif '采购公告' in meta['catName'] :
                    issueTime = response.xpath('//*[@onclick = "{}"]/../../td[6]/text()'.format(i)).extract_first()
                elif '澄清公告' in meta['catName'] :
                    issueTime = response.xpath('//*[@onclick = "{}"]/../../td[4]/text()'.format(i)).extract_first()
                elif '采购结果' in meta['catName'] :
                    issueTime = response.xpath('//*[@onclick = "{}"]/../../td[3]/text()'.format(i)).extract_first()
                else:
                    continue


                strTD3Time = str(issueTime).split(' ')[0]
                if strTD3Time == strnowTime:
                    item['issueTime'] = datetime.datetime.strptime(strTD3Time, "%Y-%m-%d")
                    # self.nn += 1
                    #
                    #
                    # pprint.pprint(item)
                    # print('--------------------------------------',self.nn)

                    yield item


