import scrapy
import faker
import json
import time
import requests
from urllib import parse
from  lxml import etree
session = requests.Session()
faker = faker.Faker()
data_dict = {"采购公告": 'ZcyAnnouncement3001', "结果公告": "ZcyAnnouncement2", "合同公告": "ZcyAnnouncement3",
                 "更正公告": "ZcyAnnouncement4", "招标文件预公示": "ZcyAnnouncement5", "单一来源": "ZcyAnnouncement6",
                 "电子卖场公告": 'ZcyAnnouncement7', "其他公告": "ZcyAnnouncement9"}
site = "www.ccgp-guangxi.gov.cn"
headers = {
        'Content-Type': 'application/json',
        'Cookie': 'acw_tc=76b20ffb16178632143157621e29ef55971a7d50fb8970813211c1e8e89587',
        'User-Agent': faker.user_agent(),
        'X-Requested-With': 'XMLHttpRequest'
}
class GxspiderSpider(scrapy.Spider):
    name = 'GXspider'
    allowed_domains = ['http://www.ccgp-guangxi.gov.cn/']
    start_urls = ["http://www.ccgp-guangxi.gov.cn/front/search/category"]
    def start_requests(self):
        item = {}
        now_time = time.strftime('%Y-%m-%d')
        for k ,v in data_dict.items():
            for p in range(1,661):
                item["subclass"] = k
                item['site'] = site
                data = {"categoryCode": v, "pageSize": "15", "pageNo": p, "publishDateBegin": "2018-01-01",
                        "publishDateEnd": now_time}
                yield scrapy.Request(
                    url=self.start_urls[0],
                    method="POST",
                    headers=headers,
                    body=json.dumps(data),
                    callback=self.parse,
                    meta={"item": item}
                )
    def parse(self, response):
        item = response.meta["item"]
        item["download_url"] = []
        results = response.json()['hits']['hits']
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
                url = "https://tool.oschina.net/action/format/html"
                data = {
                    "html": contend.encode("utf-8")
                }
                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                responses = requests.post(url=url, headers=headers, data=data).json()
                htmlst = etree.HTML(responses["fhtml"])
                fujian = htmlst.xpath('/html/body/ul/li')
                flie_dict = {}
                for url in fujian:
                    download_url = url.xpath('./p/a/@href')[0]
                    name = url.xpath('./p/a/text()')[0]
                    flie_dict[name] = download_url
                    item["download_url"] = [flie_dict]
                yield item
            else:
                yield item



