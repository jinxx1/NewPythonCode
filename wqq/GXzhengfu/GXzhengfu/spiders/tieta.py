import scrapy
import json
import logging
import faker
import copy
faker = faker.Faker()
import requests
seesion = requests.session()
site = "www.tower.com.cn"
subclass = {"资格预审公告":"1","招标公告":"2","必选公告":"3","单一来源公告":"13","结果公示":"4"}
page = [p for p in range(0,100,10)]
class TietaSpider(scrapy.Spider):
    name = 'tieta'
    allowed_domains = ['www.tower.com.cn']
    content_url = "http://www.tower.com.cn/default/main/index/cn.chinatowercom.obp.portal.portal_notice.queryByNoticeType.biz.ext"
    start_urls = ['http://www.tower.com.cn/default/main/index/cn.chinatowercom.obp.main.index.obphomepage.queryNoticeDetails.biz.ext']
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cookie': 'JSESSIONID=604DBA62F8143E9A97AA7499587199C5',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': faker.user_agent(),
        'X-Requested-With': 'XMLHttpRequest'
    }
    def start_requests(self):
        for k , resultsNoticeType in subclass.items():
            item = {}

            item["subclass"] = k
            item["site"] = site
            for p in page:
                data = {"noticeTitle": "", "effectTime": "2021-04-07 00:00:00", "failureTime": "", "noticeType": "null",
                        "purchaseNoticeType": "2", "resultsNoticeType": resultsNoticeType, "level": "", "provinceInput": "",
                        "cityInput": "", "pageIndex": 0, "pageSize": 10, "sortField": "", "sortOrder": "",
                        "page": {"begin": p, "length": 10}}
                yield scrapy.Request(
                    url = self.start_urls[0],
                    method="POST",
                    body = json.dumps(data),
                    headers=self.headers,
                    callback=self.parse,
                    meta={"item":item}
                )
    def parse(self, response):
        item = response.meta["item"]
        results = response.json()["obpNotice"]
        logging.error(results)
        for result in results:
            id = result["id"]
            item["page_url"] ="http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_notice=6&_id="+ id
            item["title"] = result["notice_title"]
            item["issue_time"] = result["effect_time"]
            data = {"id":id,"_notice":"6"}
            # 取文本
            yield scrapy.Request(
                method="POST",
                url=self.content_url,
                body=json.dumps(data),
                headers=self.headers,
                callback=self.parse_text,
                meta={"item":copy.deepcopy(item)}
            )
    def parse_text(self,response):
        item = response.meta["item"]
        item["content"] = response.json()["obpNotice"][0]["notice_content"]
        item["download_url"] = ""
        logging.debug(item)
        yield item