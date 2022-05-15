import scrapy
import pprint
import json
import re
from u1webcrwal.u1parse import *
from u1webcrwal.items import U1WebcrwalItem
from urllib import parse
from bs4 import BeautifulSoup
catJson = get_catJson()

class IthomeSpider(scrapy.Spider):
    name = 'ithome'
    allowed_domains = ['www.ithome.com']
    dupcut = get_dbdupinfo(keysName=name)
    start_urls = ['https://www.ithome.com/list/list_{}.html']

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        meta['weixinID'] = 'IT之家'
        for i in self.start_urls:
            meta['startUrl'] = i
            yield scrapy.Request(url=meta['startUrl'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='post_list']/ul[@class='ulcl']/li/a/@href").extract()

        if not link:
            return None
        ddictList = []
        for num,i in enumerate(link):
            ddict = {}
            ddict['title'] = response.xpath("//*[@href = '{}']/text()".format(i)).extract_first().strip()
            if not ddict['title'] or ddict['title'] in self.dupcut['title']:
                continue
            ddict['url'] = parse.urljoin(response.url, i)
            if not ddict['url'] or ddict['url'] in self.dupcut['ArtUrl']:
                continue
            publishtime = response.xpath("//*[@href = '{}']/../span//text()".format(i)).extract()
            ddict['time'] = ' '.join(publishtime)
            if not ddict['time'] or '今日' not in ddict['time']:
                continue
            ddict['time'] = ddict['time'].replace('今日',nowTime())
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
                meta['publish'] = timedict['publish']
                meta['created'] = timedict['created']
                meta['updated'] = timedict['updated']
                meta['timeYmd'] = timedict['timeYmd']
                yield scrapy.Request(url=i['url'],callback=self.parseA,meta=meta,dont_filter=True)

        meta['Num'] += 1
        yield scrapy.Request(url=meta['startUrl'].format(str(meta['Num'])), callback=self.parse, meta=meta,
                             dont_filter=True)

    def parseA(self, response):
        xpathcode = "//span[@id='pubtime_baidu']/text()"
        meta = response.meta
        item = U1WebcrwalItem()
        brow = response.xpath("//div[@id='paragraph']").extract_first()
        item['body'] = get_html(brow).replace('src','noimg')
        item['body'] = item['body'].replace('data-original', 'src')

        summary = response.xpath("//meta[@name = 'description']/@content").extract_first()
        item['summary'] = precessSummary(summary)

        ttime = response.xpath(xpathcode).extract_first()

        if ttime:
            try:
                publish = date_to_timestamp(ttime,format_string='%Y/%m/%d %H:%M:%S')
                item['publish'] = publish['publish']
                item['created'] = publish['created']
                item['updated'] = publish['updated']
                item['timeYmd'] = publish['timeYmd']
            except:
                item['publish'] = meta['created']
                item['created'] = meta['created']
                item['updated'] = meta['updated']
                item['timeYmd'] = meta['timeYmd']
        else:
            item['publish'] = meta['created']
            item['created'] = meta['created']
            item['updated'] = meta['updated']
            item['timeYmd'] = meta['timeYmd']

        try:
            laiyuan = response.xpath("//span[@id='source_baidu']/a/text()").extract_first().split('：')[1]
            if laiyuan:
                item['weixinID'] = laiyuan
            else:
                item['weixinID'] = meta['weixinID']
        except:
            item['weixinID'] = meta['weixinID']


        item['title'] = meta['title']
        item['type'] = meta['type']
        item['ArtUrl'] = response.url
        item['slug'] = getUrlCode() + '_{}'.format(self.name)
        item['media_id'] = self.name




        soup = BeautifulSoup(item['body'], 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
        except:
            item['cover'] = ''
        # pprint.pprint(item)
        # printline()
        yield item
