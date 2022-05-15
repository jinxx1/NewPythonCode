# -*- coding: utf-8 -*-
import scrapy
from cicCrawl.mysql_processing import get_dupurl,get_type
from cicCrawl.scrapyParse import *
from cicCrawl.items import CiccrawlItem
from urllib import parse
from bs4 import BeautifulSoup


class ChinacicSpider(scrapy.Spider):
    name = 'chinacic'
    source = '中国通信学会'
    allowed_domains = ['china-cic.cn/']
    # base_info = [{'url': 'http://www.china-cic.cn/list/46/15/{}/', 'programa_dictionaries': '科普文章', 'subtopic_dictionaries': '0'}]
    base_info = [{'url': 'http://www.china-cic.cn/list/60/24/{}/', 'programa_dictionaries': '学会动态', 'subtopic_dictionaries': '学会动态'}, {'url': 'http://www.china-cic.cn/list/63/24/{}/', 'programa_dictionaries': '学会动态', 'subtopic_dictionaries': '地方动态'}, {'url': 'http://www.china-cic.cn/list/61/24/{}/', 'programa_dictionaries': '学会动态', 'subtopic_dictionaries': '委员会动态'}, {'url': 'http://www.china-cic.cn/list/65/13/{}/', 'programa_dictionaries': '学会动态', 'subtopic_dictionaries': '委员会动态'}, {'url': 'http://www.china-cic.cn/list/67/24/{}/', 'programa_dictionaries': '学会动态', 'subtopic_dictionaries': '通知公告'}, {'url': 'http://www.china-cic.cn/list/69/25/{}/', 'programa_dictionaries': '学会动态', 'subtopic_dictionaries': '通知公告'}, {'url': 'http://www.china-cic.cn/list/64/13/{}/', 'programa_dictionaries': '学会动态', 'subtopic_dictionaries': '学会动态'},
                 {'url': 'http://www.china-cic.cn/list/66/13/{}/', 'programa_dictionaries': '学会动态', 'subtopic_dictionaries': '学会动态'},
                 {'url': 'http://www.china-cic.cn/list/46/15/{}/', 'programa_dictionaries': '科普文章', 'subtopic_dictionaries': '0'}]
    start_urls = get_type(base_info)
    dupurl = get_dupurl(source)
    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['url'] = i['url']
            meta['programa_dictionaries'] = i['programa_dictionaries']
            meta['subtopic_dictionaries'] = i['subtopic_dictionaries']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])),
                                 meta=meta,
                                 callback=self.parse,
                                 dont_filter=True
                                 )

    def parse(self, response):
        meta = response.meta
        Link = response.xpath("//div[@class = 'newlist']//a/@href").extract()

        LinknoPDF = []
        for i in Link:
            if '.pdf' not in i:
                LinknoPDF.append(i)

        Turl = []
        for i in LinknoPDF:
            meta['actcleUrl'] = parse.urljoin(response.url, i)
            if meta['actcleUrl'] in self.dupurl:
                # print('去重成功去重成功去重成功去重成功去重成功去重成功去重成功去重成功去重成功')
                continue
            meta['title'] = response.xpath("//*[@href = '{}']/text()".format(i)).extract_first()
            if not meta['title']:
                continue
            meta['publishTime'] = get_timestr(response.xpath("//*[@href = '{}']/../div/text()".format(i)).extract_first(),"%Y-%m-%d %H:%M:%S")
            if not meta['publishTime']:
                continue


            yield scrapy.Request(url=meta['actcleUrl'],
                                 callback=self.parseA,
                                 meta=meta,
                                 dont_filter=True)
            Turl.append(meta['actcleUrl'])

        if len(Turl) != 10:
            print('结束------url为{}'.format(response.url))
            print(meta['Num'])
            print('*******************************************')
            return None
        # if meta['Num'] == 5:
        #     return None

        meta['Num'] += 1

        meta['url'] = meta['url'].strip().replace('%20','').replace(' ','')
        yield scrapy.Request(url=meta['url'].format(str(meta['Num'])),
                             meta=meta,
                             callback=self.parse,
                             dont_filter=True
                             )

    def parseA(self, response):
        item = CiccrawlItem()
        meta = response.meta

        Html = response.xpath("//div[@class = 'con']//*[not(contains(@class,'bdsharebuttonbox'))]|//div[@class = 'rich_media_content']").extract()

        # Html = response.xpath("//div[@class = 'con']/p|//div[@class = 'con']//table|//div[@class = 'con']/div[@align = 'center']").extract()
        # item['body'] = no_Html("".join(Html))
        item['body'] = no_script("".join(Html))
        if not item['body']:
            print(meta['title'])
            print(response.url)
            print('no HTML')
            return None

        item['url'] = response.url
        item['title'] = meta['title']
        item['publishTime'] = meta['publishTime']
        item['programa_dictionaries'] = meta['programa_dictionaries']
        if isinstance(meta['subtopic_dictionaries'],int):
            item['subtopic_dictionaries'] = meta['subtopic_dictionaries']
        else:
            item['subtopic_dictionaries'] = 0
        item['source'] = self.source
        item['summary'] = get_Summary(item['body'])




        soup = BeautifulSoup(item['body'], 'lxml')
        try:
            imgSrc = soup.img.get('src')
            item['cover'] = parse.urljoin(response.url, imgSrc)
        except:
            item['cover'] = ''
        yield item



