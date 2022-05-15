# -*- coding: utf-8 -*-
import scrapy
import pprint
import json
import re
from u1webcrwal.u1parse import *
from u1webcrwal.items import U1WebcrwalItem
from urllib import parse
catJson = get_catJson()

class SinaSpider(scrapy.Spider):
    name = 'sina'
    dupcut = get_dbdupinfo(keysName=name)
    allowed_domains = ['sina.com']
    start_urls = ['http://interface.sina.cn/pc_api/public_news_data.d.json?callback=jQuery111107180783187032651_1576119364747&cids=241275%2C241279&pdps=PDPS000000066866&smartFlow=&editLevel=0%2C1%2C2%2C3&type=std_news%2Cstd_slide%2Cstd_video&mod=nt_category_tech_5g_latest&pageSize=100']

    def start_requests(self):
        meta = {}
        for i in self.start_urls:
            yield scrapy.Request(url=i,callback=self.parse,meta=meta,dont_filter=True)

    def parse(self, response):
        meta = response.meta
        cc = re.findall("\((.*)\)", response.text)[0]

        jsonT = json.loads(cc)['data']

        for num,i in enumerate(jsonT):
            meta['title'] = i['ltitle']
            meta['type'] = get_type(meta['title'], keysListall=catJson)
            if meta['type'] == 5:
                continue

            if i['ltitle'] in self.dupcut['title'] or i['url'] in self.dupcut['ArtUrl'] or i['pcurl'] in self.dupcut['ArtUrl']:
                continue

            if i['url']:
                meta['Posturl'] = i['url']
            elif i['pcurl']:
                meta['Posturl'] = i['pcurl']
            elif i['surl']:
                meta['Posturl'] = i['surl']
            else:
                continue

            if i['orgUrl']:
                meta['ArtUrl'] = i['orgUrl'][:499]
            else:
                meta['ArtUrl'] = meta['Posturl'][:499]

            timedict = timeall(ctime=i['ctime'])
            meta['publish'] = timedict['publish']
            meta['created'] = timedict['created']
            meta['updated'] = timedict['updated']
            meta['timeYmd'] = timedict['timeYmd']
            meta['weixinID'] = i['media']
            meta['summary'] = i['summary']

            if i['thumb']:
                meta['cover'] = i['thumb']
            elif isinstance(i['thumbs'], list) and len(i['thumbs']) > 0:
                meta['cover'] = i['thumbs'][0]
            else:
                meta['cover'] = ''
            if i['uuid']:
                meta['slug'] = getUrlCode() + '_sina_' + i['uuid']
            else:
                meta['slug'] = getUrlCode() + '_sina_Nuid'
            yield scrapy.Request(url=meta['Posturl'],callback=self.parseA,meta=meta,dont_filter=True)

    def parseA(self, response):
        meta = response.meta
        item = U1WebcrwalItem()
        brow = response.xpath("//div[@class = 'article' or @id = 'artibody']").extract_first()

        item['body'] = get_html(brow)

        if not meta['summary']:
            item['summary'] = precessSummary(item['body'])
        else:
            item['summary'] = meta['summary']

        item['title'] = meta['title']
        item['slug'] = meta['slug']
        item['publish'] = meta['publish']
        item['created'] = meta['created']
        item['updated'] = meta['updated']
        item['timeYmd'] = meta['timeYmd']
        item['weixinID'] = meta['weixinID']
        item['type'] = meta['type']
        item['ArtUrl'] = meta['ArtUrl']
        item['cover'] = meta['cover']
        item['media_id'] = self.name

        yield item