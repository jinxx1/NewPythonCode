import scrapy
from urllib import parse
import pprint
import re
from electric.scrapyParse import *
from bs4 import BeautifulSoup
from electric.items import ElectricItem


class CrpszSpider(scrapy.Spider):
    name = 'crpsz'
    allowed_domains = ['www.crpsz.com']
    start_urls = [
        {'catName': '招标专区_招标（预审）公告', 'baseUrl': 'http://www.crpsz.com/zbxx/006001/006001001/{}.html', 'startPage': 'secondpagejy', 'allPage': 947},
        {'catName': '招标专区_变更公告', 'baseUrl': 'http://www.crpsz.com/zbxx/006001/006001002/{}.html', 'startPage': 'secondpagejy', 'allPage': 157},
        {'catName': '招标专区_中标候选人公示', 'baseUrl': 'http://www.crpsz.com/zbxx/006001/006001003/{}.html', 'startPage': 'secondpagejyNoStatuw', 'allPage': 660},
        {'catName': '招标专区_中标公告', 'baseUrl': 'http://www.crpsz.com/zbxx/006001/006001004/{}.html', 'startPage': 'secondpagejyNoStatuw', 'allPage': 653},
        {'catName': '招标专区_终止公告', 'baseUrl': 'http://www.crpsz.com/zbxx/006001/006001005/{}.html', 'startPage': 'secondpagejyNoStatuw', 'allPage': 47},
        {'catName': '非招标专区_采购公告', 'baseUrl': 'http://www.crpsz.com/zbxx/006002/006002001/{}.html', 'startPage': 'secondpagejy', 'allPage': 274},
        {'catName': '非招标专区_变更公告', 'baseUrl': 'http://www.crpsz.com/zbxx/006002/006002002/{}.html', 'startPage': 'secondpagejy', 'allPage': 66},
        {'catName': '非招标专区_结果公告', 'baseUrl': 'http://www.crpsz.com/zbxx/006002/006002003/{}.html',
         'startPage': 'secondpagejyNoStatuw', 'allPage': 36}
    ]

    def __init__(self, goon=None, *args, **kwargs):
        super(CrpszSpider, self).__init__(*args, **kwargs)
        self.goon = goon

    def start_requests(self):
        meta = {}
        meta['Num'] = 1
        for i in self.start_urls:
            meta['catName'] = i['catName']
            meta['baseUrl'] = i['baseUrl']
            meta['allPage'] = i['allPage']
            yield scrapy.Request(url=meta['baseUrl'].format(i['startPage']),
                                 callback=self.parse,
                                 meta=meta,
                                 dont_filter=True
                                 )

    def parse(self, response):
        meta = response.meta
        link = response.xpath(
            "//table[@id='staticContent']/tbody[@id='infocontent']/tr/td[@class='ewb-td2']/a/@href").extract()
        if not link:
            return None

        notdupUrl = [parse.urljoin(response.url, i) for i in link]
        llistUrl = urlIsExist(notdupUrl)
        for i in llistUrl:
            yield scrapy.Request(url=i,
                                 callback=self.parseA,
                                 dont_filter=True,
                                 meta=meta
                                 )

        if meta['Num'] == meta['allPage']:
            return None
        if not llistUrl and self.goon == 'no':
            return None

        meta['Num'] += 1
        yield scrapy.Request(url=meta['baseUrl'].format(str(meta['Num'])),
                             callback=self.parse,
                             meta=meta,
                             dont_filter=True
                             )



    def parseA(self, response):
        meta = response.meta
        item = ElectricItem()
        title = response.xpath("//td[@class = 'title']/text()|//a[@class='ewb-con-tt']/text()").extract()
        item['title'] = ''.join(title)
        if not item['title']:
            return None
        Time = ''.join(response.xpath("//div[@class = 'ewb-con-info']//text()").extract())
        # print('Time',Time)
        Timel = re.findall("\d{4}-\d{2}-\d{2} \d{2}:\d{2}",Time,re.M|re.S)
        # print('Timel', Timel)
        item['issueTime'] = get_timestr(Timel[0],'%Y-%m-%d %H:%M:%S')
        # print('item[issueTime]', item['issueTime'])
        if not item['issueTime']:
            return None
        content = response.xpath("//div[@id = 'lw_ft']/table|//div[@id= 'lw_ft']").extract()

        item['content'] = ''.join(content)
        item['url'] = response.url
        item['site'] = self.allowed_domains[0]
        item['subclass'] = meta['catName']
        yield item


        # item['content'] = len(item['content'])
        # pprint.pprint(item)
        # print('------------------------------------')