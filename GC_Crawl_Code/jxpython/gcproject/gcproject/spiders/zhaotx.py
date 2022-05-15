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

def attmenSTR(downLoad):
    from urllib.parse import unquote
    import requests
    ddict = {}
    ddict['download_url'] = downLoad
    brow = requests.get(url=downLoad)
    ddict['name'] = unquote(brow.headers['Content-Disposition'],'utf-8')
    return ddict

class ZhaotxSpider(scrapy.Spider):

    name = 'zhaotx'
    allowed_domains = ['www.zhaotx.cn']
    start_urls = ['https://www.zhaotx.cn/searchlist.htm?type=&fbpt=&page={}']
    dupurl = get_dupurl(allowed_domains[0])

    def __init__(self, goon=None, *args, **kwargs):
        super(ZhaotxSpider, self).__init__(*args, **kwargs)
        self.goon = goon
    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        yield scrapy.Request(
            url=self.start_urls[0].format(str(meta['Num'])),
            callback=self.parse,
            meta=meta,
            dont_filter=True)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='ztbxx']/div[@class='ztb_list']/ul/li/a/@href").extract()
        if not link:
            return None

        mark = 0
        for i in link:
            meta['vertItem'] = {}
            url = parse.urljoin(response.url,i)
            if url in self.dupurl:
                mark += 1
                continue
            meta['vertItem']['page_url'] = url
            meta['vertItem']['site'] = self.allowed_domains[0]
            subclass_xpath = "//*[@href = '{}']/p[@class = 'ztblb_dq'][1]/text()".format(i)
            meta['vertItem']['subclass'] = response.xpath(subclass_xpath).extract_first()
            location_xpath = "//*[@href = '{}']/p[@class = 'ztblb_dq'][2]/text()".format(i)
            loction = response.xpath(location_xpath).extract_first()
            location = get_location(loction, how=1)
            meta['vertItem']['province_name'] = location['Project_province']
            meta['vertItem']['city_name'] = location['Project_country']
            purchase_type_xpath = "//*[@href = '{}']/p[@class = 'ztblb_lx']/text()".format(i)
            meta['vertItem']['purchase_type'] = response.xpath(purchase_type_xpath).extract_first()
            TimeT = "//*[@href = '{}']/p[@class = 'ztblb_fb']/text()".format(i)
            meta['vertItem']['issue_time'] = response.xpath(TimeT).extract_first()
            meta['vertItem']['issue_time'] = get_timestr(meta['vertItem']['issue_time'],"%Y-%m-%d %H:%M:%S")
            if not meta['vertItem']['issue_time']:
                continue
            title_xpath = "//*[@href = '{}']/p[@class = 'ztblb_xm']/text()".format(i)
            meta['vertItem']['title'] = response.xpath(title_xpath).extract_first()

            yield scrapy.Request(
                url=url,
                callback=self.parseA,
                meta=meta,
                dont_filter=True)
            # break
            # pprint.pprint(meta['vertItem'])
            # print('------------------------------------------------',meta['Num'])

        if len(link) < 20:
            return None
        if mark == len(link) and self.goon !='no':
            return None
        meta['Num'] += 1
        yield scrapy.Request(
            url=self.start_urls[0].format(str(meta['Num'])),
            callback=self.parse,
            meta=meta,
            dont_filter=True)
        # a


    def parseA(self, response):
        meta = response.meta
        item = GcprojectItem()

        for k in meta['vertItem'].keys():
            item[k] = meta['vertItem'][k]
        content = response.xpath("//div[@class='ztbxq_bk']").extract()
        item['content'] = ''.join(content)
        soup = BeautifulSoup(item['content'], 'lxml')
        hrefall = soup.find_all(href=re.compile("upload/download"))
        item['attchment']=[]
        for nn in hrefall:
            ddict = {}
            ddict['download_url'] = nn.get('href')
            ddict['name'] = response.xpath("//*[@href = '{}']/text()".format(nn.get('href'))).extract_first()
            item['attchment'].append(ddict)

        if not item['attchment']:
            del item['attchment']
        yield item

        # item['content'] = len(item['content'])
        # pprint.pprint(item)
        # print('---------------------------')




