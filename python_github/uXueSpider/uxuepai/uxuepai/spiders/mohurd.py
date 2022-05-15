#! /usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
import re
import time

from uxuepai.items import UxuepaiItem

ToDayTime = time.strftime("%Y%m%d", time.localtime())
# ToDayTime = 20181030
TimeStart = 20181001
TimeEnd = 20181031
class MohurdSpider(scrapy.Spider):
    name = 'mohurd'
    allowed_domains = ['mohurd.gov.cn']
    start_urls = ['http://jzsc.mohurd.gov.cn/asite/jsbpp/jsp/news_list.jsp']



    def parse(self, response):
        classModle = ['jsbpp_news_tzgg',
                      'jsbpp_news_hydt',
                      'jsbpp_news_pqgs',
                      'jsbpp_news_phgg',
                      'jsbpp_news_cftb',
                      'jsbpp_news_dftb',
                      'jsbpp_news_yxtz'
                      ]
        for n in classModle:
            postdata = {
                'data-callback': 'lastRefreshMoreLink',
                'data-contentid': 'news_tab2',
                'class': 'formsubmit',
                'data-url': 'news_list.jsp',
                'item_code': n,
                '$pg': '1',
            }
            yield scrapy.FormRequest.from_response(
                response = response,
                callback = self.parseA,
                formdata=postdata,
            )


    def parseA(self,response):
        Link = response.xpath("//div[@class = 'news_group_title']/a[@class = 'formsubmit']/@data-exturl").extract()
        Title = response.xpath("//div[@class = 'news_group_title']/a[@class = 'formsubmit']/text()").extract()
        Time = response.xpath("//div[@class = 'news_group_date']/text()").extract()
        for i in range(len(Time)):
            Time1 = Time[i].replace('\r','').replace('\n','').replace('\t','').split(" ")
            num = re.sub(r'\.*$', "", Time1[0]).split('\xa0')[0].split('-')
            TimeT = "".join(num)
            if TimeT == ToDayTime:
                TitleT = Title[i].replace('\r', '').replace('\n', '').replace('\t', '')
                LinkT = Link[i]
                yield scrapy.Request(url=LinkT,callback=self.parseB,meta={'Title':TitleT,'time1':TimeT})

    def parseB(self,response):
        item = UxuepaiItem()
        word1 = response.xpath("//p//text()").extract()
        wo = ''
        for i1 in range(len(word1)):
            ss = word1[i1].replace(u'\3000', u'').strip()
            if len(ss) > 0:
                s = '<p>' + str(ss) + '</p>'
                wo = wo + s
        # item['Pageid'] = random.randrange(10000001, 99999999, 1)
        item['NameTOTALItem'] = '住建部'
        item['TitleItem'] = response.meta['Title']
        item['LinkItem'] = response.url
        item['TimeItem'] = int(response.meta['time1'])
        item['WordItem'] = wo
        item['WebNameWord'] = 'mohurd'
        yield item