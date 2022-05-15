# -*- coding: utf-8 -*-
import scrapy

HEA = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Host':'www.fjggfw.gov.cn',
            'Origin':'https://www.fjggfw.gov.cn',
            'Referer':'https://www.fjggfw.gov.cn/Website/JYXXNew.aspx',
            'Sec-Fetch-Mode':'cors',
            'Sec-Fetch-Site':'same-origin',
    'X-Requested-With': 'XMLHttpRequest',

       }
class GgzyFujianSpider(scrapy.Spider):
    name = 'ggzy_fujian'
    allowed_domains = ['fjggfw.gov.cn']
    start_urls = ['https://www.fjggfw.gov.cn/Website/AjaxHandler/BuilderHandler.ashx']


    def start_requests(self):

        for i in self.start_urls:
            meta = {}
            meta['url'] = i
            datePost = {
                'OPtype': 'GetListNew',
                'pageNo': '2',
                'pageSize': '10',
                'proArea': '-1',
                'category': 'GCJS',
                'announcementType': '-1',
                'ProType': '-1',
                'xmlx': '-1',
                'projectName': '',
                'TopTime': '2004-06-20 00:00:00',
                'EndTime': '2019-09-18 23:59:59',

            }

            yield scrapy.FormRequest(url=meta['url'],callback=self.parse,meta=meta,dont_filter=True,formdata=datePost,headers=HEA)


    def parse(self, response):
        print('into parse')
        print(response)
        print(response.body)
        print(response.text)
