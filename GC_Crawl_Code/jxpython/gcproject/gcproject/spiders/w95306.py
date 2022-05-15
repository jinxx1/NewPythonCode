# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint,datetime
from urllib import parse
from bs4 import BeautifulSoup
from gcproject.items import GcprojectItem
from gcproject.parseScrpy import get_location,get_timestr
from gcproject.mysqlprecess import get_dupurl


class W95306Spider(scrapy.Spider):
    name = 'w95306'
    allowed_domains = ['wzcgzs.95306.cn']
    start_urls = [
{'minor_business_type': '运营物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=20&unitType=&noticeType=01&dealType=&materialType=01&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '无'},
{'minor_business_type': '建设物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=20&unitType=&noticeType=01&dealType=&materialType=02&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '无'},
{'minor_business_type': '运营物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&unitType=&noticeType=01&dealType=&materialType=01&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '项目公告'},
{'minor_business_type': '运营物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&unitType=&noticeType=02&dealType=&materialType=01&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '变更公告'},
{'minor_business_type': '运营物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&unitType=&noticeType=03&dealType=&materialType=01&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '答疑补疑'},
{'minor_business_type': '运营物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&unitType=&noticeType=04&dealType=&materialType=01&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '结果公告'},
{'minor_business_type': '建设物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&unitType=&noticeType=01&dealType=&materialType=02&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '项目公告'},
{'minor_business_type': '建设物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&unitType=&noticeType=02&dealType=&materialType=02&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '变更公告'},
{'minor_business_type': '建设物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&unitType=&noticeType=03&dealType=&materialType=02&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '答疑补疑'},
{'minor_business_type': '建设物资', 'baseUrl': 'http://wzcgzs.95306.cn/notice/indexlist.do?dealGroup=10&unitType=&noticeType=04&dealType=&materialType=02&extend=1&curPage={}&notTitle=&inforCode=&time0=&time1=', 'subclass': '结果公告'}
    ]
    dupurl = get_dupurl(allowed_domains[0])

    def __init__(self, goon=None, *args, **kwargs):
        super(W95306Spider, self).__init__(*args, **kwargs)
        self.goon = goon

    def start_requests(self):
        meta = {}
        meta['vertItem'] = {}
        meta['vertItem']['site'] = self.allowed_domains[0]
        meta['Num'] = 1
        for i in self.start_urls:
            meta['vertItem']['minor_business_type'] = i['minor_business_type']
            meta['baseUrl'] = i['baseUrl']
            meta['vertItem']['subclass'] = i['subclass']
            yield scrapy.Request(
                    url=meta['baseUrl'].format(str(meta['Num'])),
                    callback=self.parse,
                    meta=meta,
                    dont_filter=True
                )

    def parse(self, response):
        meta = response.meta
        links = response.xpath("//table[@class='listInfoTable']//a/@href").extract()
        if not links:
            return None

        mark = 0
        for i in links:
            url = parse.urljoin(response.url, i)
            if url in self.dupurl:
                mark += 1
                continue
            issue_time = response.xpath("//*[@href='{}']/../../td[6]/text()".format(i)).extract_first()
            if not issue_time:
                issue_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            meta['vertItem']['issue_time'] = get_timestr(issue_time, "%Y-%m-%d %H:%M:%S")

            meta['vertItem']['province_name'] = response.xpath("//*[@href='{}']/../../td[5]/text()".format(i)).extract_first()
            dsb_LinYongZhang = ''
            dsb_LinYongZhang = response.xpath("//*[@href='{}']/../../td[4]/text()".format(i)).extract_first()

            if meta['vertItem']['subclass'] == '无':
                meta['vertItem']['subclass'] = dsb_LinYongZhang
            else:
                meta['vertItem']['purchase_type'] = dsb_LinYongZhang
            yield scrapy.Request(url=url,
                                 callback=self.parseA,
                                 meta=meta,
                                 dont_filter=True
                                 )


        if mark == len(links) and self.goon == 'no':
            return None
        else:
            try:
                PageNumAll = int(re.findall("共(\d{1,5})页", response.text)[0])
            except:
                return None
            if meta['Num'] == PageNumAll:
                return None

            meta['Num'] += 1
            yield scrapy.Request(url=meta['baseUrl'].format(str(meta['Num'])),
                             callback=self.parse,
                             meta=meta,
                             dont_filter=True
                             )

    def parseA(self, response):
        meta = response.meta
        item = GcprojectItem()
        for k in meta['vertItem'].keys():
            item[k] = meta['vertItem'][k]
        item['content'] = response.xpath("//div[@class = 'noticeBox']").extract_first()
        if not item['content']:
            return None
        item['title'] = response.xpath("//p[@class = 'title']/text()").extract_first()
        if not item['title']:
            return None
        item['page_url'] = response.url
        yield item

        # item['content'] = len(item['content'])
        # pprint.pprint(item)
        # print('-------------------------------------------------------------')


