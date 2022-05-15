# -*- coding: utf-8 -*-
import scrapy
import json
from newscrapy.scrapyParse import *
from newscrapy.items import NewscrapyItem
import pprint
from urllib import parse


class CcgpSpider(scrapy.Spider):
    name = 'ccgp'
    custom_settings = {
        "SCHEDULER": "scrapy.core.scheduler.Scheduler",
    }
    allowed_domains = ['www.ccgp.gov.cn']
    start_urls = [{'catName': '中国政府采购网_地方公告_成交公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/cjgg/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_单一来源公告和公示', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/dylygg/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_废标终止公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/fblbgg/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_公开招标', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/gkzb/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_更正公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/gzgg/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_竞争性磋商公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/jzxcs/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_竞争性谈判公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/jzxtpgg/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_其它公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/qtgg/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_询价公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/xjgg/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_邀请招标公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/yqzbgg/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_中标公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/zbgg/index_{}.htm'},
                  {'catName': '中国政府采购网_地方公告_资格预审公告', 'url': 'http://www.ccgp.gov.cn/cggg/dfgg/zgysgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_成交公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/cjgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_单一来源公告和公示', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/dylygg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_废标终止公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/fblbgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_公开招标', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/gkzb/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_更正公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/gzgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_竞争性磋商公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/jzxcs/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_竞争性谈判公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/jzxtpgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_其它公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/qtgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_询价公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/xjgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_邀请招标公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/yqzbgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_中标公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/zbgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央公告_资格预审公告', 'url': 'http://www.ccgp.gov.cn/cggg/zygg/zgysgg/index_{}.htm'},
                  {'catName': '中国政府采购网_中央单位单一来源政府采购审核前公示', 'url': 'http://www.ccgp.gov.cn/eadylynotice/index_{}.htm'},
                  {'catName': '中国政府采购网_中央批量集中采购招标公告', 'url': 'http://www.ccgp.gov.cn/zydwplcg/zy/zyzb/index_{}.htm'},
                  {'catName': '中国政府采购网_中央批量集中采购中标公告', 'url': 'http://www.ccgp.gov.cn/zydwplcg/zy/zyzhb/index_{}.htm'},
                  {'catName': '中国政府采购网_中直批量采购招标公告', 'url': 'http://www.ccgp.gov.cn/zydwplcg/zz/zzzb/index_{}.htm'},
                  {'catName': '中国政府采购网_中直批量采购中标公告', 'url': 'http://www.ccgp.gov.cn/zydwplcg/zz/zzzhb/index_{}.htm'}]

    mysql_allurl = get_mysql_allurl(allowed_domains[0])

    def start_requests(self):
        meta = {}
        meta['Num'] = 0
        for i in self.start_urls:
            meta['catName'] = i['catName']
            meta['indexUrl'] = i['url']
            indexUrl = meta['indexUrl'].replace('index_{}.htm', 'index.htm')

            if '单一来源政府' not in meta['catName']:
                yield scrapy.Request(url=indexUrl,
                                     callback=self.parse, meta=meta, dont_filter=True)
            else:
                yield scrapy.Request(url=indexUrl,
                                     callback=self.parse_1, meta=meta, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        linkList = response.xpath("//ul[@class='c_list_bid']/li/a/@href|//ul[@class='ulst']/li/a/@href").extract()
        if not linkList:
            return None
        num = 1
        for i in linkList:
            meta['url'] = parse.urljoin(response.url, i)
            if meta['url'] in self.mysql_allurl:
                num += 1
                if num == 10:
                    return None
                else:
                    continue
            meta['title'] = response.xpath("//*[@href = '{}']/@title".format(i)).extract_first()
            if '批量' in meta['catName']:
                timeT = response.xpath("//*[@href = '{}']/../span[2]/text()".format(i)).extract_first()
                location = response.xpath("//*[@href = '{}']/../span[3]/text()".format(i)).extract_first()
            else:
                timeT = response.xpath("//*[@href = '{}']/../em[2]/text()".format(i)).extract_first()
                location = response.xpath("//*[@href = '{}']/../em[3]/text()".format(i)).extract_first()
            meta['issueTime'] = get_timestr(timeT)
            meta['subclass'] = meta['catName'] + '_' + location
            # print('即将进入-----')
            # pprint.pprint(meta)
            # print('-----------------')
            yield scrapy.Request(url=meta['url'], callback=self.parseA, meta=meta)

        meta['Num'] += 1
        yield scrapy.Request(url=meta['indexUrl'].format(str(meta['Num'])),
                             callback=self.parse, meta=meta, dont_filter=True)

    def parse_1(self, response):
        meta = response.meta
        linkList = response.xpath("//ul[@id='pageContent']//a/@href").extract()
        # print(meta['catName'],len(linkList))
        if not linkList:
            # print('没有获取页面链接')
            # print(response.url)
            return None

        for i in linkList:
            meta['url'] = parse.urljoin(response.url, i)
            if meta['url'] in self.mysql_allurl:
                continue
            meta['title'] = response.xpath("//*[@href = '{}']/@title".format(i)).extract_first()
            timeT = response.xpath("//*[@href = '{}']/../span/text()".format(i)).extract_first()
            meta['issueTime'] = get_timestr(timeT)
            meta['subclass'] = meta['catName']
            # pprint.pprint(meta)
            # print('-----------------')
            # print('即将进入-----')
            yield scrapy.Request(url=meta['url'], callback=self.parseA, meta=meta)

    def parseA(self,response):
        # print('进入文章了',response.url)
        meta = response.meta
        dict1 = NewscrapyItem()
        dict1['content'] = response.xpath("//div[@class = 'vF_detail_content']").extract_first()
        if not dict1['content']:
            return None
        attachLink = response.xpath("//div[@class='vF_detail_content']/a[@class='bizDownload']/@href | //div[@class='vF_detail_main']/div[@class='table']//a[@class = 'bizDownload']/@href").extract()
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
        dict1['subclass'] = meta['subclass']

        if not meta['issueTime']:
            issueTime = get_timestr(response.xpath("//span[@id='pubTime']/text()").extract_first())
            if not issueTime:
                issueTime = "2000-01-01 00:00:00"
            dict1['issueTime'] = issueTime
        else:
            dict1['issueTime'] = meta['issueTime']

        # print('*******************')
        # pprint.pprint("抓取到的时间：{}".format(dict1['issueTime']))
        # print('*******************')


        yield dict1
