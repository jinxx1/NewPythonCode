# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import pprint
from masterpic.items import MasterpicItem
from masterpic.pipelines import Mongo_getUrl_Pipline

MONGO_DB = Mongo_getUrl_Pipline()

class GetpicurlSpider(scrapy.Spider):
    name = 'getpicurl'
    allowed_domains = ['gallerix.asia']
    base_url = 'https://gallerix.asia/storeroom/letter/{}/'
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_RUS']

    def start_requests(self):
        meta = {}

        for i in self.letters:
            meta['letterNameListPageUrl'] = self.base_url.format(i)
            meta['letter'] = i
            yield scrapy.Request(url=meta['letterNameListPageUrl'],callback=self.parse,dont_filter=True,meta=meta)


    def parse(self, response):
        meta = response.meta
        links = response.xpath("//div[@class = 'panel']/div/div[@class='row']/div/div/p/a/@href").extract()

        for link in links:
            meta['MasterName'] = response.xpath("//*[@href = '{}']/text()".format(link)).extract_first()
            meta['MasterNameUrl'] = parse.urljoin(response.url,link)

            yield scrapy.Request(url=meta['MasterNameUrl'],callback=self.parseA,dont_filter=True,meta=meta)

    def parseA(self,response):
        meta = response.meta
        links = response.xpath("//div[@class='pic']/a/@href").extract()
        for link in links:
            meta['PicUrl'] = parse.urljoin(response.url,link)

            iconImg = response.xpath("//*[@href = '{}']/div/img/@src".format(link)).extract_first()
            meta['iconImg'] = parse.urljoin(response.url,iconImg)

            yield scrapy.Request(url=meta['PicUrl'],callback=self.parseB,dont_filter=True,meta=meta)

    def parseB(self,response):
        meta = response.meta
        meta['PicTitle'] = response.xpath("//h1/text()").extract_first()
        PicFullUrl = response.xpath("//p[@class = 'xpic']/a/@href").extract_first()
        PicFullUrlTemp = parse.urljoin(response.url,PicFullUrl)
        meta['referer'] = PicFullUrlTemp
        meta['PicFullTitle'] = response.xpath("//meta[@itemprop = 'name']/@content").extract_first()
        meta['description'] = response.xpath("//meta[@name = 'description']/@content").extract_first()
        meta['collName'] = self.name
        yield scrapy.Request(url=PicFullUrlTemp,callback=self.parseC,dont_filter=True,meta=meta)


    def parseC(self,response):
        meta = response.meta
        aa = response.xpath("//a/@href").extract_first()
        meta['PicFullUrl'] = parse.urljoin(response.url,aa)

        del meta['download_timeout']
        del meta['download_slot']
        del meta['depth']
        del meta['download_latency']

        item = MasterpicItem()
        item = meta
        yield item





