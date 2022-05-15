# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,difflib
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem




class GdShenzhenSpider(scrapy.Spider):
    name = 'gd_shenzhen'
    allowed_domains = ['ggzy.sz.gov.cn']
    urlDict =[{'catName': '广东省_深圳市_建设工程_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/jsgc/jsgz_zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_建设工程_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/jsgc/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_建设工程_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/jsgc/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_市本级_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/sbj/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_福田区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/ftq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_南山区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/nsq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_罗湖区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/lhq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_盐田区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/ytq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_宝安区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/baq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_龙华区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/lhxq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_龙岗区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/lgq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_光明区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/gmq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_坪山区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/psq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_大鹏新区_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/dpxq/zbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_市本级_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/sbj/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_福田区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/ftq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_南山区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/nsq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_罗湖区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/lhq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_盐田区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/ytq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_宝安区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/baq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_龙华区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/lhxq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_龙岗区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/lgq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_光明区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/gmq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_坪山区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/psq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_大鹏新区_中标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/dpxq/zhbgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_市本级_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/sbj/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_福田区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/ftq/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_南山区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/nsq/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_罗湖区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/lhq/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_盐田区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/ytq/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_宝安区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/baq/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_龙华区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/lhxq/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_龙岗区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/lgq/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_光明区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/gmq/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_坪山区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/psq/gzgg/index_{}.htm'}, {'catName': '广东省_深圳市_政府采购_大鹏新区_更正公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/zfcg/dpxq/gzgg/index_{}.htm'}]
    # urlDict = [{'catName': '广东省_深圳市_建设工程_招标公告', 'url': 'http://ggzy.sz.gov.cn/cn/jyxx/jsgc/jsgz_zbgg/index_{}.htm'}]
    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.urlDict)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].replace('index_{}.htm','index.htm'), callback=self.parse,meta=meta)

    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='tag-list4']/ul/li/a/@href").extract()
        if not link:
            return None
        urlList_withDomain = [parse.urljoin(response.url,x) for x in link]
        urllist = urlIsExist(urlList_withDomain)
        if not urllist:
            return None
        for i in urllist:
            for n in link:
                # print(i.split('/')[-1])
                # print(n.split('/')[-1])
                if i.split('/')[-1] == n.split('/')[-1]:
                # if difflib.SequenceMatcher(None,i.split('/')[-1],n.split('/')[-1]).quick_ratio() > 0.5:
                #     print(difflib.SequenceMatcher(None,i.split('/')[-1],n.split('/')[-1]).quick_ratio())
                    meta['articleTitle'] = response.xpath("//*[contains(@href,'{}')]/@title".format(n)).extract_first()
                    meta['articleTime'] = response.xpath("//*[contains(@href,'{}')]/../span/text()".format(n)).extract_first()
                    if meta['articleTime'] or meta['articleTitle']:
                        yield scrapy.Request(url=i, callback=self.parseA, meta=meta,dont_filter=True)
                    else:
                        return None
        meta['Num'] += 1
        yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,meta=meta, dont_filter=True)

    def parseA(self, response):
        # print('进入最终页')
        dict1 = GgzyItem()
        meta = response.meta
        try:
            html = response.xpath("//div[@class='text']").extract()[0]
        except:
            return None
        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle']
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['content'] = html
        dict1['subclass'] = meta['catName']
        yield dict1