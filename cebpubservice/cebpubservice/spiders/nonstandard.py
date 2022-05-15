import scrapy
import json
import pprint
from cebpubservice.scrapyParse import *
from cebpubservice.mysqlprecess import *
from scrapy.http.cookies import CookieJar
cookies_jar = CookieJar()

HEA = {
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9,zh-TW;q=0.8',
'Connection':'keep-alive',
'Content-Length':'228',
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Host':'www.cebpubservice.com',
'Origin':'http://www.cebpubservice.com',
'Referer':'http://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getSearch.do?tabledivIds=searchTabLi2',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',
}

import sqlalchemy

conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
                                                                                               'DBNAME'])
mysqlcon = sqlalchemy.create_engine(conStr)


class NonstandardSpider(scrapy.Spider):
    name = 'nonstandard'
    allowed_domains = ['www.cebpubservice.com/']
    pageCount = '15'
    start_urls = ['http://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getStringMethod.do']
    alltime1 = getallTime()

    def start_requests(self):
        meta = {}
        for num,i in enumerate(self.alltime1):
            # if num > 1:
            #     return None
            meta['mysqlid'] = i['id']
            meta['subclass'] = i['subclass']
            meta['starttime'] = i['starttime']
            meta['endtime'] = i['endtime']

            postdata = {
            'searchName': '',
            'searchArea': '',
            'searchIndustry': '',
            'centerPlat': '',
            'businessType': i['subclass'],
            'searchTimeStart': '',
            'searchTimeStop': '',
            'timeTypeParam': '',
            'bulletinIssnTime': '',
            'bulletinIssnTimeStart': i['starttime'],
            'bulletinIssnTimeStop': i['endtime'],
            'pageNo': str(1),
            'row': self.pageCount,
        }

            yield scrapy.FormRequest(url=self.start_urls[0],
                                 callback=self.parseA,
                                 meta = meta,
                                 formdata=postdata,
                                 dont_filter=True
                                 )

    def parseA(self, response):
        meta = response.meta
        try:
            jsonT = json.loads(response.text)['object']['page']
        except:
            print(response.text)

        if jsonT['totalCount'] > 0:
            exc = "update nonstandard_alltime set status_getpostinfo=1,totalCount={} where id={}".format(jsonT['totalCount'],meta['mysqlid'])
            mysqlcon.execute(exc)
        print('{},开始时间{},结束时间{}。录入完毕。一共有{}篇文章'.format(meta['subclass'],
                                             meta['starttime'],
                                             meta['endtime'],
                                            jsonT['totalCount']
        ))
        print('-------------------------------------------')


    def parse(self, response):
        meta = response.meta

        cookies_jar.extract_cookies(response,response.request)
        meta['cookiejar'] = cookies_jar

        jsonT = json.loads(response.text)['object']['returnlist']

        print('({subclass})页，第{pageNum}页，本共有{countart}篇文章：'.format(
            subclass = self.subclass,
            pageNum = meta['Num'],
            countart = len(jsonT)
        ))
        print(json.loads(response.text)['object']['page'])
        return None

        if len(jsonT) > 0:
            a = pandas_insermysql(jsonT,subclass=self.subclass)

            print(a)
            print(meta['Num'])
            print('-------------------------------')
            # return None
            meta['Num'] += 1
            postdata = {
                'searchName': '',
                'searchArea': '',
                'searchIndustry': '',
                'centerPlat': '',
                'businessType': self.subclass,
                'searchTimeStart': '',
                'searchTimeStop': '',
                'timeTypeParam': '',
                'bulletinIssnTime': '',
                'bulletinIssnTimeStart': '',
                'bulletinIssnTimeStop': '',
                'pageNo': str(meta['Num']),
                'row': self.pageCount,
            }
            yield scrapy.FormRequest(url=self.start_urls[0],
                                     callback=self.parse,
                                     meta=meta,
                                     formdata=postdata,
                                     dont_filter=True,
                                     # headers=HEA
                                     )
        else:
            print(response.text)
            return None