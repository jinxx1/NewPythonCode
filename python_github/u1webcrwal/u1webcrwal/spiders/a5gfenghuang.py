import scrapy
import pprint
import json
import re
from u1webcrwal.u1parse import *
from u1webcrwal.items import U1WebcrwalItem
from urllib import parse
from bs4 import BeautifulSoup
catJson = get_catJson()

class A5gfenghuangSpider(scrapy.Spider):
    name = '5gfenghuang'
    allowed_domains = ['5g.ifeng.com/']
    dupcut = get_dbdupinfo(keysName=name)


    start_urls = ['https://5g.ifeng.com/']

    def start_requests(self):
        meta = {}
        meta['weixinID'] = '凤凰网5G'
        for i in self.start_urls:
            yield scrapy.Request(url=i,callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//h2/a/@href").extract()
        link2 = response.xpath("//div/h3[1]/a/@href").extract()
        if not link and not link2:
            return None
        ddictList = []
        for num,i in enumerate(link):
            ddict = {}
            ddict['title'] = response.xpath("//a[@href = '{}']/@title".format(i)).extract_first().strip()
            if not ddict['title'] or ddict['title'] in self.dupcut['title']:
                continue
            ddict['url'] = parse.urljoin(response.url, i)
            if not ddict['url'] or ddict['url'] in self.dupcut['ArtUrl']:
                continue
            publishtime = response.xpath("//a[@href = '{}']/../../div/time/text()".format(i)).extract_first()
            publishtime1 = ' '.join(publishtime) + ":00"
            ddict['time'] = publishtime1.replace(' ','').replace('天','天 ')
            if not ddict['time'] or '今天' not in ddict['time']:
                continue
            ddict['time'] = ddict['time'].replace('今天',nowTime())
            ddict['type'] = get_type(ddict['title'], keysListall=catJson)
            if ddict['type'] == 5:
                continue
            ddictList.append(ddict)

        if len(ddictList) == 0:
            return None
        else:
            for i in ddictList:
                meta['title'] = i['title']
                meta['type'] = i['type']
                timedict = date_to_timestamp(date=nowTime())
                meta['publish'] = i['time']
                meta['created'] = timedict['created']
                meta['updated'] = timedict['updated']
                meta['timeYmd'] = timedict['timeYmd']
                meta['summary'] = ''
                yield scrapy.Request(url=i['url'],callback=self.parseA,meta=meta,dont_filter=True)

        link2List = []
        for num,i in enumerate(link2):
            ddict = {}
            ddict['title'] = response.xpath("//a[@href = '{}']/@title".format(i)).extract_first().strip()
            if not ddict['title'] or ddict['title'] in self.dupcut['title']:
                continue
            ddict['url'] = parse.urljoin(response.url, i)
            if not ddict['url'] or ddict['url'] in self.dupcut['ArtUrl']:
                continue
            ddict['type'] = get_type(ddict['title'], keysListall=catJson)
            if ddict['type'] == 5:
                continue
            link2List.append(ddict)

        if len(link2List) == 0:
            return None
        else:
            for i in link2List:
                meta['title'] = i['title']
                meta['type'] = i['type']
                meta['publish'] = ''
                meta['created'] = ''
                meta['updated'] = ''
                meta['timeYmd'] = ''
                meta['summary'] = ''
                yield scrapy.Request(url=i['url'],callback=self.parseA,meta=meta,dont_filter=True)

    def parseA(self, response):
        meta = response.meta
        item = U1WebcrwalItem()
        brow = response.xpath("//div[@class='text-3zQ3cZD4']").extract_first()
        if not brow:
            return None
        item['body'] = get_html(brow)
        if not meta['summary']:
            item['summary'] = precessSummary(item['body'])
        else:
            item['summary'] = meta['summary']
        item['title'] = meta['title']

        item['type'] = meta['type']
        item['ArtUrl'] = response.url
        item['slug'] = getUrlCode() + '_{}'.format(self.name)
        item['media_id'] = self.name
        item['cover'] = response.xpath("//meta[@property = 'og:image']/@content").extract_first()

        ttime = response.xpath("//meta[@name = 'og:time ']/@content").extract_first()
        if ttime:
            timedict = date_to_timestamp(date=ttime, format_string="%Y-%m-%d %H:%M:%S")
            item['publish'] = ttime
            item['created'] = timedict['created']
            item['updated'] = timedict['updated']
            item['timeYmd'] = timedict['timeYmd']
        else:
            item['publish'] = meta['created']
            item['created'] = meta['created']
            item['updated'] = meta['updated']
            item['timeYmd'] = meta['timeYmd']

        laiyuan = response.xpath("//span[@class='source-2pXi2vGI']/a/text()").extract_first()
        if laiyuan:
            item['weixinID'] = laiyuan
        else:
            item['weixinID'] = meta['weixinID']

        # pprint.pprint(item)
        # printline()
        yield item
