# -*- coding: utf-8 -*-
import scrapy,re,pprint,requests
import json,datetime
from getUrl.items import GeturlItem
b = datetime.datetime.now().strftime("%Y-%m-%d")
nowTime = datetime.datetime.strptime(b, "%Y-%m-%d")
strnowTime = str(nowTime).split(' ')[0]

class TowerSpider(scrapy.Spider):
    name = 'tower'
    allowed_domains = ['www.tower.com.cn']
    collName = 'monitorUrl'
    start_urls = 'http://www.tower.com.cn/default/main/index/cn.chinatowercom.obp.main.index.obphomepage.queryNoticeDetails.biz.ext'
    idbase = [{'catName': '中国铁塔_资格预审公告', 'resultsNoticeType': '1', 'purchaseNoticeType': '2'}, {'catName': '中国铁塔_比选公告', 'resultsNoticeType': '3', 'purchaseNoticeType': '2'}, {'catName': '中国铁塔_招标公告', 'resultsNoticeType': '2', 'purchaseNoticeType': '2'}, {'catName': '中国铁塔_谈判公告', 'resultsNoticeType': '14', 'purchaseNoticeType': '2'}, {'catName': '中国铁塔_单一来源公告', 'resultsNoticeType': '13', 'purchaseNoticeType': '2'}, {'catName': '中国铁塔_结果公示', 'resultsNoticeType': '4', 'purchaseNoticeType': '2'}, {'catName': '中国铁塔_物资拍卖', 'resultsNoticeType': '16', 'purchaseNoticeType': '2'}, {'catName': '中国铁塔_认证公告', 'resultsNoticeType': '1', 'purchaseNoticeType': '1'}, {'catName': '中国铁塔_报价公告', 'resultsNoticeType': '2', 'purchaseNoticeType': '1'}]

    def start_requests(self):
        meta = {}
        meta['Num'] = 0
        meta['firstHea'] = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        }

        for i in self.idbase:
            meta['resultsNoticeType'] = i['resultsNoticeType']
            meta['purchaseNoticeType'] = i['purchaseNoticeType']
            meta['catName'] = i['catName']
            postdate = {
                "noticeTitle": "",
                "effectTime": str(nowTime),
                "failureTime": "",
                "noticeType": "null",
                "purchaseNoticeType": str(meta['purchaseNoticeType']),
                "resultsNoticeType": meta['resultsNoticeType'],
                "pageIndex": str(meta['Num']),
                "pageSize": '100',
            }
            yield scrapy.FormRequest(url= self.start_urls,
                             callback=self.parse,
                             formdata=postdate,
                             dont_filter=True,
                             headers=meta['firstHea'],
                             meta=meta
                             )

    def parse(self, response):
        n = 0
        item = GeturlItem()
        finD = {'issueTime': strnowTime, 'site': '中国铁塔'}
        dec = requests.post('http://localhost:1111/apiGetMongoInfo', data=json.dumps(finD)).text
        jsonT = json.loads(dec)['message']
        try:
            mongoLinkAll = [x['artID'] for x in jsonT]
        except:
            mongoLinkAll = []
        meta = response.meta
        jsonT = json.loads(response.text)['obpNotice']
        baseUrl = 'http://www.tower.com.cn/default/main/index/noticedetail.jsp?_operation=notice&_notice=6&_id='
        if len(jsonT) == 0:
            return None
        for i in jsonT:
            item['artID'] = i['id']
            if item['artID'] in mongoLinkAll or i['effect_time'] != strnowTime:
                continue
            item['url']= baseUrl + i['id']
            item['artID'] = i['id']
            item['issueTime'] = datetime.datetime.strptime(i['effect_time'], "%Y-%m-%d")
            try:
                item['subclass'] = meta['catName'] + '_' + i['p_orgname']
            except:
                item['subclass'] = meta['catName']
            item['title'] = i['notice_title']
            item['collName'] = self.collName
            item['site'] = '中国铁塔'
            item['domain'] = self.allowed_domains[0]
            item['from_Page'] = 'PostKey(resultsNoticeType)={}'.format(str(meta['resultsNoticeType']))
            n += 1
            yield item


        if n != 0:
            meta['Num'] += 1
            postdate = {
                "noticeTitle": "",
                "effectTime": str(nowTime),
                "failureTime": "",
                "noticeType": "null",
                "purchaseNoticeType": str(meta['purchaseNoticeType']),
                "resultsNoticeType": meta['resultsNoticeType'],
                "pageIndex": str(meta['Num']),
                "pageSize": '100',
            }
            yield scrapy.FormRequest(url= self.start_urls,
                             callback=self.parse,
                             formdata=postdate,
                             dont_filter=True,
                             headers=meta['firstHea'],
                             meta=meta
                             )
        else:
            return None
