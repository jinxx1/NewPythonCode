import scrapy
import json
import time
import faker
import requests
import copy
seesion = requests.session()
site = 'txzbqy.miit.gov.cn'
'''
# page_url 无法定义
'''
faker = faker.Faker()
page = [p for p in range(1,5)]
now_time = time.strftime('%Y-%m-%d')
ZB_subclass_dict = {'招标公告':"22","资格预审公告":"21","招标终止公告":"23"}
IN_subclass_dict = {"中标候选人公示":"11","中标结果":"12"}
# 中标业绩公告
url = 'https://txzbqy.miit.gov.cn/zbtb/gateway/gatewayExpert/getBidInformationList'
headers = {
        'Accept': 'application/json, text/plain, */*',
        'Cookie': 'jsessionid=rBQhuRroYHFKhH6A4sptGkn3qFdUUdEbChcA',
        'Content-Type': 'application/json;charset=UTF-8',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
}
class GxspiderSpider(scrapy.Spider):
    name = 'gongxin'
    allowed_domains = ['txzbqy.miit.gov.cn']
    start_urls = ['https://txzbqy.miit.gov.cn/zbtb/gateway/gatewayPublicity/bidBulletinList']

    def start_requests(self):
        #招标公告
        for k,v in ZB_subclass_dict.items():
            for p in page:
                item = {}
                item["subclass"] = k
                item['site'] = site
                data1 = {"resource":"","page":p,"limit":15,"totalSize":"","bulletinTitle":"","issueDate":"","status":"11",\
    "bulletinType":v,"unitRestrict":[],"supervisorName":[],"nationFlag":"null","bidType":"null","bidSubtype":[],\
    "fileBuyBeginTime":"","fileBuyEndTime":"","occupationBeginDate":"2021-04-09","occupationEndDate":now_time,\
    "issueDates":["2021-04-09",now_time],"gatewayFlag":0}
                yield scrapy.Request(
                    url=self.start_urls[0],
                    method="POST",
                    headers=headers,
                    body=json.dumps(data1),
                    callback=self.parse,
                    meta={"item": item}
                )

    def parse(self, response):
        #招标公告
        item = response.meta["item"]
        results = response.json()["page"]["list"]
        for result in results:
            item["page_url"] = ""
            item["title"] = result["bulletinTitle"]
            item["issue_time"] = time.strftime("%Y--%m--%d",time.localtime(int(result["issueDate"])/1000))
            item["content"] = result["bulletinComment"]
            #附件下载
            if result["fileId"]:
                file = result["fileId"]
                data = [file]
                #获取附件密钥
                url = "https://txzbqy.miit.gov.cn/zbtb/zwzt/file/getFileByKeys"
                response = seesion.post(url=url, headers=headers, data=json.dumps(data)).json()
                keynum = response["files"][0]["keyNum"]
                #获取附件地址
                url = "https://txzbqy.miit.gov.cn/zbtb/zwzt/file/getAccessToken"
                data = {"userId": "-1", "md5Paths": keynum}
                responses = seesion.post(url=url, headers=headers, data=json.dumps(data)).json()
                flie_url = "https://file.miit.gov.cn/file/download?&t=" + responses["accessToken"][0]
                item["download_url"] = flie_url
            yield item
            # 中标公告
            for i, t in IN_subclass_dict.items():
                for a in page:
                    item["subclass"] = i
                    item['site'] = site
                    data1 = {"totalSize":"","page":a,"limit":15,"publicityTitle":"","publishTime":["2021-04-09",now_time],\
                            "occupationBeginDate":"2021-04-09","occupationEndDate":now_time,"publicityType":t,"bidderName":"",\
                            "datetime":"","supervisorName":[],"unitRestrict":[],"nationFlag":"null","bidType":"null",\
                             "bidSubtype":[],"gatewaySize":0
                             }
                    yield scrapy.Request(
                        url=self.start_urls[0],
                        method="POST",
                        headers=headers,
                        body=json.dumps(data1),
                        callback=self.parse_IN,
                        meta={"item": copy.deepcopy(item)}
                    )
    def parse_IN(self, response):
        item = response.meta["item"]
        results = response.json()["page"]["list"]
        for result in results:
            item["page_url"] = ""
            item["title"] = result["publicityTitle"]
            item["issue_time"] = result["publishTime"]
            item["content"] = result["publicityComment"]
            yield item
            # 中标业绩信息
            for g in page:
                item = {}
                item["subclass"] = "中标业绩信息"
                item['site'] = site
                data3 = {"totalSize":18,"page":g,"limit":15,"bidProjectName":"","supervisorName":[],"occupationBeginDate":"2021-04-04",\
                    "occupationEndDate":now_time,"nationFlag":"null","bidType":"null","bidSubtype":[],"acceptanceBidder":"","unitRestrict":[],\
                    "bidAcceptanceNotificaiton":["2021-04-04",now_time],"flag":2,"isPublic":"0"}
                yield scrapy.Request(
                    url=url,
                    method="POST",
                    headers=headers,
                    body=json.dumps(data3),
                    callback=self.parse_YEJI,
                    meta={"item": item}
                )
    def parse_YEJI(self,response):
        print(response.json())