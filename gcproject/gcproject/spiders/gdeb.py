# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint
from urllib import parse
from bs4 import BeautifulSoup
from gcproject.items import GcprojectItem
from gcproject.parseScrpy import get_location
from gcproject.mysqlprecess import get_dupurl

# catid转化成 subclass
def catid_2_subclass(catid):
    dictList = [{'typeName': '不限分类', 'catid': '0'},
                {'typeName': '招标采购信息公告', 'catid': '74166'},
                {
                    'typeName': '预中标公告',
                    'catid': '74167'
                },
                {
                    'typeName': '结果公告',
                    'catid': '74168'
                },
                {
                    'typeName': '更正答疑公告',
                    'catid': '74169'
                },
                {
                    'typeName': '招标文件购买流程',
                    'catid': '74181'}]
    numList_int = [int(i['catid']) for i in dictList]
    numList_str = ','.join([i['catid'] for i in dictList])

    try:
        int(catid)
    except:
        print('catid输入错误，必须全部都是数字：',numList_str)
        return None


    if int(catid) not in numList_int:
        print('catid输入错误，必须是{}这些数字中的一项'.format(numList_str))
        return None


    for info in dictList:
        if int(catid) == int(info['catid']):
            return info['typeName'][0:20]



class GdebSpider(scrapy.Spider):
    name = 'gdeb'
    site = '广东采联采购招标平台'
    allowed_domains = ['www.chinapsp.cn']

    dupurl = get_dupurl(allowed_domains[0])
    start_urls = ['http://qy.chinapsp.cn:48882/api/services/app/AbpArticles/GetPaged?filter=a.ext2+%3D%3D+%2274166%22+and+a.isDispaly+%3D%3D+%22true%22&sorting=a.creationTime+desc&maxResultCount={maxResultCount}&skipCount={skipCount}']


    def start_requests(self):
        meta = {}
        meta['maxResultCount'] = 1000
        meta['skipCount'] = 0
        yield scrapy.Request(
            url=self.start_urls[0].format(maxResultCount=meta['maxResultCount'],skipCount=meta['skipCount']),
            callback=self.parse,
            meta=meta,
            dont_filter=True,
        )

    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)['result']['items']
        if len(jsonT) == 0:
            return None
        mark = 0
        artcleBaseUrl = 'http://www.chinapsp.cn/notice_content.html?itemid={}'
        for i in jsonT:
            meta['vertItem'] = {}
            meta['vertItem']['page_url'] = artcleBaseUrl.format(i['id'])
            if meta['vertItem']['page_url'] in self.dupurl:
                mark += 1
                continue
            meta['vertItem']['subclass'] = catid_2_subclass(i['ext2'])
            meta['vertItem']['purchase_type'] = i['projectType']
            meta['vertItem']['title'] = i['title']
            meta['vertItem']['site'] = self.allowed_domains[0]
            meta['vertItem']['issue_time'] = i['creationTime'].replace('T',' ')
            location = get_location(i['areas'],how=1)
            meta['vertItem']['province_name'] =location['Project_province']
            meta['vertItem']['city_name'] =location['Project_country']
            urlforGET = 'http://qy.chinapsp.cn:48882/api/services/app/AbpArticleData/GetArticleDataByAIdAsync?aId={}'
            yield scrapy.Request(url=urlforGET.format(i['id']),
                                 callback=self.parseA,
                                 meta = meta,
                                 dont_filter=True)


        # if mark == len(jsonT) and self.goon == 'no':
        #     return None

        # meta['skipCount'] += meta['maxResultCount']
        # yield scrapy.Request(
        #     url=self.start_urls[0].format(maxResultCount=meta['maxResultCount'],skipCount=meta['skipCount']),
        #     callback=self.parse,
        #     meta=meta,
        #     dont_filter=True,
        # )



    def parseA(self, response):
        meta = response.meta
        item = GcprojectItem()
        jsonT = json.loads(response.text)
        for k in meta['vertItem'].keys():
            item[k] = meta['vertItem'][k]
        item['content'] = jsonT['result']['content']

        yield item

        # item['content'] = len(item['content'])
        # pprint.pprint(item)
        # print('--------------------------------')





'''
    # ztbRawInfo 表名称（文章信息存储表）
    subclass = scrapy.Field()#子类型=
    site = scrapy.Field()#来源站点,域名=
    page_url = scrapy.Field()#链接地址=
    title = scrapy.Field()#标题=
    issue_time = scrapy.Field()#发布时间=
    creation_time = scrapy.Field()#抓取开始时间=
    end_time = scrapy.Field()#抓取结束时间=
    province_name = scrapy.Field()#省=
    city_name = scrapy.Field()#市=
    
    purchase_type = scrapy.Field()#采购方式=
    business_type = scrapy.Field()#业务大类
    minor_business_type = scrapy.Field()#业务细类
    money = scrapy.Field()#项目金额
# --------------------------------------------------------------------------
    # ztbRawInfoContent 表名称（内容存储表）
    content = scrapy.Field()#公告内容
# --------------------------------------------------------------------------
    # ztbInfoAttachment 表名称（附件存储表）
    download_url = scrapy.Field()#原始网站的附件下载地址
    file_name = scrapy.Field()#存储在本地的文件名
    name = scrapy.Field()#文件对应的名称,如文件名为123.xls,name为广州招标
'''