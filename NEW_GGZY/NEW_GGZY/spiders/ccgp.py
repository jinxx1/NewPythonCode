# -*- coding: utf-8 -*-
wword = '''中国政府采购网_中央公告	http://www.ccgp.gov.cn/cggg/zygg/index_{}.htm
中国政府采购网_地方公告	http://www.ccgp.gov.cn/cggg/dfgg/index_{}.htm
中国政府采购网_中央批量集中采购招标公告	http://www.ccgp.gov.cn/zydwplcg/zy/zyzb/index_{}.htm
中国政府采购网_中央批量集中采购中标公告	http://www.ccgp.gov.cn/zydwplcg/zy/zyzhb/index_{}.htm
中国政府采购网_中直批量采购招标公告	http://www.ccgp.gov.cn/zydwplcg/zz/zzzb/index_{}.htm
中国政府采购网_中直批量采购中标公告	http://www.ccgp.gov.cn/zydwplcg/zz/zzzhb/index_{}.htm
中国政府采购网_中央单位单一来源政府采购审核前公示	http://www.ccgp.gov.cn/eadylynotice/'''.split('\n')

def cSech(id):
    aa = '其他公告'
    catSerach=[{"id": "974","chn":"公开招标"},{"id": "975","chn":"询价公告"},{"id": "978","chn":"竞争性谈判"},{"id": "977","chn":"单一来源"},{"id": "979","chn":"资格预审"},{"id": "976","chn":"邀请公告"},{"id": "982","chn":"中标公告"},{"id": "981","chn":"更正公告"},{"id": "990","chn":"其他公告"},{"id": "984","chn":"其他公告"},{"id": "985","chn":"其他公告"},{"id": "2653","chn":"竞争性磋商"},{"id": "2655","chn":"成交公告"},{"id": "2656","chn":"终止公告"},{"id": "998","chn":"公开招标"},{"id": "997","chn":"询价公告"},{"id": "1000","chn":"竞争性谈判"},{"id": "999","chn":"单一来源"},{"id": "1001","chn":"资格预审"},{"id": "996","chn":"邀请公告"},{"id": "1004","chn":"中标公告"},{"id": "1003","chn":"更正公告"},{"id": "1012","chn":"其他公告"},{"id": "1006","chn":"其他公告"},{"id": "1007","chn":"其他公告"},{"id": "2654","chn":"竞争性磋商"},{"id": "2657","chn":"成交公告"},{"id": "2658","chn":"终止公告"}]
    if id:
        for nn in catSerach:
            if id == nn["id"]:
                aa = nn["chn"]
                break
    else:
        aa = ''
    return aa

import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem
TEMPPATH = TMEPTEST()


class CcgpSpider(scrapy.Spider):
    name = 'ccgp'
    allowed_domains = ['www.ccgp.gov.cn']
    urlList = [{'catName': x.split('\t')[0], 'url': x.split('\t')[1]} for x in wword if x]


    def start_requests(self):
        meta = {}
        meta['Num'] = 0
        getTXTdict = getTXT(self.name, self.urlList)
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            if meta['Num'] == 0:
                meta['indexUrl'] = i['url'].replace('index_{}.htm','index.htm')
            else:
                meta['indexUrl'] = i['url'].format(str(meta['Num']))

            if '单一来源' not in meta['catName']:
                yield scrapy.Request(url=meta['indexUrl'].replace('index_{}.htm','index.htm'),
                                     callback=self.parse, meta=meta,dont_filter=True)
            else:

                yield scrapy.Request(url=meta['indexUrl'].replace('index_{}.htm','index.htm'),
                                     callback=self.parse_1, meta=meta,dont_filter=True)


    def parse(self, response):
        meta = response.meta
        linkList = response.xpath("//ul[@class='c_list_bid']/li/a/@href|//ul[@class='ulst']/li/a/@href").extract()
        if not linkList:
            return None
        link = duplicateUrl(linkList,response.url)

        del linkList
        if not link:
            return None
        for i in link:
            meta['title'] = response.xpath("//*[@href = '{}']/@title".format(i)).extract_first()
            if '批量' in meta['catName']:
                catName = response.xpath("//*[@href = '{}']/../span[1]/text()".format(i)).extract_first()
                timeT = response.xpath("//*[@href = '{}']/../span[2]/text()".format(i)).extract_first()
                location = response.xpath("//*[@href = '{}']/../span[3]/text()".format(i)).extract_first()
            else:
                catName = response.xpath("//*[@href = '{}']/../em[1]/text()".format(i)).extract_first()
                timeT = response.xpath("//*[@href = '{}']/../em[2]/text()".format(i)).extract_first()
                location = response.xpath("//*[@href = '{}']/../em[3]/text()".format(i)).extract_first()
            meta['issueTime'] = timeReMark(timeT)
            meta['subclass'] = meta['catName'] + '_' + cSech(catName) + '_' + location
            meta['url'] = parse.urljoin(response.url, i)
            yield scrapy.Request(url=meta['url'],callback=self.parseA,meta=meta,dont_filter=True)

        del link

        meta['Num'] += 1
        yield scrapy.Request(url=meta['indexUrl'].format(str(meta['Num'])),
                             callback=self.parse, meta=meta, dont_filter=True)


    def parse_1(self, response):
        meta = response.meta
        linkList1 = response.xpath("//ul[@id='pageContent']//a/@href").extract()
        if not linkList1:
            return None

        linkList = [linkList1[x] for x in range(500)]
        del linkList1

        link = duplicateUrl(linkList,response.url)

        if not link:
            return None

        for i in link:
            meta['title'] = response.xpath("//*[@href = '{}']/@title".format(i)).extract_first()
            timeT = response.xpath("//*[@href = '{}']/../span/text()".format(i)).extract_first()
            meta['issueTime'] = timeReMark(timeT)
            meta['subclass'] = meta['catName']
            meta['url'] = parse.urljoin(response.url, i)
            yield scrapy.Request(url=meta['url'],callback=self.parseA,meta=meta,dont_filter=True)
        del link


    def parseA(self,response):
        # print('进入文章了')
        meta = response.meta
        dict1 = GgzyItem()
        dict1['content'] = response.xpath("//div[@class = 'vF_detail_content']").extract_first()
        if not dict1['content']:
            return None
        attachLink = response.xpath("//div[@class='vF_detail_content']/a[@class='bizDownload']/@href").extract()
        if attachLink:
            attachmentListJsonList = []
            for i in attachLink:
                att_dict = {}
                att_dict['downloadUrl'] = parse.urljoin(response.url, i)
                attname = response.xpath("//*[@href = '{}']/text()".format(i)).extract()
                att_dict['name'] = ''.join(attname)
                attachmentListJsonList.append(att_dict)
            dict1['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)
            del attachmentListJsonList
        del attachLink

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['title'].strip()
        dict1['issueTime'] = meta['issueTime']
        dict1['subclass'] = meta['subclass']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))
        yield dict1
