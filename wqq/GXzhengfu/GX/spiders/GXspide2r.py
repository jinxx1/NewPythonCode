import scrapy
import faker
import json
import time
import requests
from urllib import parse
from  lxml import etree
import copy
now_time = time.strftime('%Y-%m-%d')
session = requests.Session()
faker = faker.Faker()
data_dict = {"采购公告": 'ZcyAnnouncement3001', "结果公告": "ZcyAnnouncement2", "合同公告": "ZcyAnnouncement3",
                 "更正公告": "ZcyAnnouncement4", "招标文件预公示": "ZcyAnnouncement5", "单一来源": "ZcyAnnouncement6",
                 "电子卖场公告": 'ZcyAnnouncement7', "其他公告": "ZcyAnnouncement9"}
site = "www.ccgp-guangxi.gov.cn"
class GxspiderSpider(scrapy.Spider):
    name = 'GXspider2r'
    allowed_domains = ['http://www.ccgp-guangxi.gov.cn/']
    start_urls = ["http://www.ccgp-guangxi.gov.cn/front/search/category"]
    data = {"categoryCode": "", "pageSize": "15", "pageNo": 1, "publishDateBegin": "2021-04-9",
            "publishDateEnd": now_time}
    headers = {
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=76b20ffb16178632143157621e29ef55971a7d50fb8970813211c1e8e89587',
        'User-Agent': faker.user_agent(),
        'X-Requested-With': 'XMLHttpRequest'
    }
    def __init__(self, goon=None, *args, **kwargs):
        super(GxspiderSpider, self).__init__(*args, **kwargs)
        self.goon = goon
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            method="POST",
            headers=self.headers,
            body=json.dumps(self.data),
            callback=self.parse
        )
    def parse(self, response):
        item = {}
        item["from_data"] = self.data
        item["download_url"] = []
        results = response.json()['hits']['hits']
        if not results:
            return None
        p = 1
        for result in results:
            item['page_url'] = parse.urljoin(self.allowed_domains[0],result["_source"]['url'])
            item['title'] = result["_source"]['title']
            issue_time = int(result["_source"]['publishDate'] / 1000)
            item["issue_time"] = time.strftime("%Y-%m-%d", time.localtime(issue_time))
            text = session.get(item['page_url']).text.encode("ISO-8859-1").decode("utf-8")
            htmls = etree.HTML(text)
            contend = json.loads(htmls.xpath('//div[@class="guangxi-detail js-comp"]/input/@value')[0])["content"]
            item["content"] = contend
            if "附件信息：" in text:
                data = {"html": contend.encode("utf-8")}
                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                yield scrapy.Request(
                    method="POST",
                    url = "https://tool.oschina.net/action/format/html",
                    headers = headers,
                    body= data,
                    callback=self.parse_flie,
                    meta=item
                )
            yield item
            if item["from_data"]["pageNo"] > 20 and self.goon == "no":
                return None
            p += 1
            for k, v in data_dict.items():
                item["subclass"] = k
                item['site'] = site
                item["from_data"]["pageNo"] = p
                item["from_data"]["categoryCode"] = v
                print(item["from_data"])
                yield scrapy.Request(
                    url=self.start_urls[0],
                    method="POST",
                    headers=self.headers,
                    body=json.dumps(item["from_data"]),
                    callback=self.parse,
                    meta={"item": item}
                )
    def parse_flie(self,response):
        item = response.meta
        fujian = response.xpath('/html/body/ul/li')
        flie_dict = {}
        for url in fujian:
            download_url = url.xpath('./p/a/@href')[0]
            name = url.xpath('./p/a/text()')[0]
            flie_dict[name] = download_url
            item["download_url"] = [flie_dict]
            yield item






