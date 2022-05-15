import scrapy
import pprint
import json
import re
from u1webcrwal.u1parse import *
from u1webcrwal.items import U1WebcrwalItem
from urllib import parse
from bs4 import BeautifulSoup
catJson = get_catJson()




class NbdSpider(scrapy.Spider):
    name = 'nbd'
    allowed_domains = ['www.nbd.cn']
    dupcut = get_dbdupinfo(keysName=name)
    start_urls = ['http://www.nbd.com.cn/columns/3/page/{}.html']

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        meta['weixinID'] = '每日经济网'
        for i in self.start_urls:
            meta['startUrl'] = i
            yield scrapy.Request(url=meta['startUrl'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)


    def parse(self, response):
        nowtime = nowTime()
        meta = response.meta
        urlall = response.xpath("//li[@class='u-news-title']/a/@href").extract()
        link = [x for x in urlall if nowtime in x]
        if not link:
            return None

        ddictList = []
        for num,i in enumerate(link):
            ddict = {}
            ddict['title'] = response.xpath("//*[@href = '{}']/text()".format(i)).extract_first()
            if not ddict['title'] or ddict['title'] in self.dupcut['title']:
                continue
            ddict['url'] = parse.urljoin(response.url, i)
            if not ddict['url'] or ddict['url'] in self.dupcut['ArtUrl']:
                continue
            publishtime = response.xpath("//*[@href = '{}']/../span//text()".format(i)).extract_first().strip()
            ddict['time'] = nowtime + ' ' + publishtime
            # pprint.pprint(ddict)
            # printline()
            ddictList.append(ddict)

        if len(ddictList) == 0:
            return None
        else:
            for i in ddictList:
                meta['title'] = i['title']
                meta['type'] = get_type(meta['title'], keysListall=catJson, input_id=4, next=True)
                if meta['type'] == 5:
                    continue

                timedict = date_to_timestamp(date=nowtime)
                meta['publish'] = i['time']
                meta['created'] = timedict['created']
                meta['updated'] = timedict['updated']
                meta['timeYmd'] = timedict['timeYmd']
                # pprint.pprint(meta)
                # printline()
                yield scrapy.Request(url=i['url'],callback=self.parseA,meta=meta,dont_filter=True)

        meta['Num'] += 1
        yield scrapy.Request(url=meta['startUrl'].format(str(meta['Num'])), callback=self.parse, meta=meta,
                             dont_filter=True)



    def parseA(self, response):
        meta = response.meta
        item = U1WebcrwalItem()
        brow = response.xpath("//div[@class='g-articl-text']").extract_first()
        item['body'] = get_html(brow)

        summary = response.xpath("//meta[@name = 'Description']/@content").extract_first()
        item['summary'] = precessSummary(summary)

        item['title'] = meta['title']
        item['type'] = meta['type']
        item['ArtUrl'] = response.url
        item['slug'] = getUrlCode() + '_{}'.format(self.name)
        item['media_id'] = self.name


        ttime = response.xpath("//span[@class='time']/text()").extract()
        if ttime:
            try:
                publish = date_to_timestamp(''.join(ttime),format_string='%Y-%m-%d %H:%M:%S')
                item['publish'] = publish['publish']
                item['created'] = publish['created']
                item['updated'] = publish['updated']
                item['timeYmd'] = publish['timeYmd']
            except:
                item['publish'] = meta['publish']
                item['created'] = meta['created']
                item['updated'] = meta['updated']
                item['timeYmd'] = meta['timeYmd']
        else:
            item['publish'] = meta['publish']
            item['created'] = meta['created']
            item['updated'] = meta['updated']
            item['timeYmd'] = meta['timeYmd']

        try:
            laiyuan = response.xpath("//span[@class='source']/text()").extract()
            if laiyuan:
                item['weixinID'] = ''.join(laiyuan)
            else:
                item['weixinID'] = meta['weixinID']
        except:
            item['weixinID'] = meta['weixinID']

        soup = BeautifulSoup(item['body'], 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
        except:
            item['cover'] = ''
        # pprint.pprint(item)
        # printline()
        yield item
