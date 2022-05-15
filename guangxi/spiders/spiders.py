import scrapy
import json
import faker
import requests
from lxml import etree
from  lxml import html
faker = faker.Faker()
session = requests.Session()
data_dict = {"采购公告":'ZcyAnnouncement3001',
             "结果公告":"ZcyAnnouncement2",
             "合同公告":"ZcyAnnouncement3",
             "更正公告":"ZcyAnnouncement4",
             "招标文件预公示":"ZcyAnnouncement5",
             "单一来源":"ZcyAnnouncement6",
             "电子卖场公告":'ZcyAnnouncement7',
             "其他公告":"ZcyAnnouncement9"}
page = 1000
class SpidersSpider(scrapy.Spider):
    name = 'spiders'
    allowed_domains = ['www.ccgp-guangxi.gov.cn']
    start_urls = ['http://www.ccgp-guangxi.gov.cn/front/search/category']
    data = {"categoryCode":"ZcyAnnouncement3001","pageSize":"15","pageNo":1,"publishDateBegin":"2018-01-01","publishDateEnd":"2020-12-31"}
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                method="POST",
                url = url,
                body=json.dumps(self.data),
                # headers=self.headers,
                cookies={'acw_tc':'76b20ffb16178632143157621e29ef55971a7d50fb8970813211c1e8e89587'},
                callback=self.parse_get
            )
    def parse_get(self,response):
        item = {}
        for v,k in data_dict.items():
            item["subclass"] = v
            for p in range(1,page):
                data = {"categoryCode": k, "pageSize": "15", "pageNo": p, "publishDateBegin": "2018-01-01",
                        "publishDateEnd": "2020-12-31"}
                yield scrapy.Request(
                    method="POST",
                    url=self.start_urls[0],
                    # headers=self.headers,
                    # cookies={'acw_tc':'76b20feb16178681413965325e25e9decac4ab8a6a60dab4c6546a8e0dc346'},
                    body=json.dumps(data),
                    meta={"item":item},
                    callback=self.parse
                )
    def parse(self, response):
        item = response.meta["item"]
        results = response.json()['hits']['hits']

        for get_url in results:
            end_url = "http://www.ccgp-guangxi.gov.cn/"+get_url["_source"]['url']
            item['site'] = self.allowed_domains[0]
            item['page_url'] =end_url
            item['title'] = get_url["_source"]['title']
            item["issue_time"] = get_url["_source"]['title']
            text = session.get(end_url).text
            print(text)
            htmls = etree.HTML(text)
            contend = html.tostring(htmls.xpath('//*[id="iframe"]')[0])
            item["cintend"] = contend
            # 返回执行文本获取
            yield item
