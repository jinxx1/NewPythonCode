import json, os,datetime
import scrapy
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql

r = Redis('127.0.0.1', 6379)


class ShezhenyangguangSpider(scrapy.Spider):
    name = 'gc_szyg'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://cgpt.sotcbb.com/trade/getSearchResultList']

    def start_requests(self):
        url = 'https://cgpt.sotcbb.com/trade/getSearchResultList'
        headers = {
            ':authority': 'cgpt.sotcbb.com',
            ':method': 'POST',
            ':path': '/trade/getSearchResultList',
            ':scheme': 'https',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://cgpt.sotcbb.com',
            'referer': 'https://cgpt.sotcbb.com/list',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'x-requested-with': 'XMLHttpRequest'
        }
        data = {
            'project_type': '',
            'pageNo': '0',
            'cate_id': '全部',
            'dateState': '',
            'moneyStr': '',
            'gonggaoStr': '',
            'gongshiStr': '',
            'company_name': '',
            'project_name': '',
        }
        for i in range(1, 100):# 11550
            pageNo = str(i * 10)
            data['pageNo'] = pageNo
            yield FormRequest(
                url=url,
                method='POST',
                headers=headers,
                formdata=data,
                callback=self.parse_list,
                dont_filter=True
            )

    def parse_list(self, response):
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://cgpt.sotcbb.com'
        }
        data = {'gongao_type': 'cjgg', 'noticeId': ''}
        for dic in response.json():
            item = GcProjectItem()
            if dic['gongao_type'] == '采购公告':
                data['gongao_type'] = 'cggg'
                data['noticeId'] = dic['info_guid']
            elif dic['gongao_type'] == '变更公告':
                data['gongao_type'] = 'bggg'
                data['noticeId'] = dic['id']
            elif dic['gongao_type'] == '废标公告':
                data['gongao_type'] = 'fbgg'
                data['noticeId'] = dic['id']
            elif dic['gongao_type'] == '结果公示':
                data['gongao_type'] = 'cjgg'
                data['noticeId'] = dic['info_guid']
            elif dic['gongao_type'] == '单一来源采购公告':
                data['gongao_type'] = 'dyly'
                data['noticeId'] = dic['info_guid']
            elif dic['gongao_type'] == '招投标服务网公告':
                data = {'batch_no': dic['buyer_name']}
                continue
            if dic['cate_id'] == 'A':
                item['business_type'] = '工程'
            elif dic['cate_id'] == 'B':
                item['business_type'] = '货物'
            elif dic['cate_id'] == 'C':
                item['business_type'] = '服务'
            else:
                item['business_type'] = ''
            item['title'] = dic['title']
            item['subclass'] = dic['gongao_type']
            item['issue_time'] = dic['publicity_start_date']
            item['site'] = 'cgpt.sotcbb.com'
            item['page_url'] = 'https://cgpt.sotcbb.com/detail?%s&%s.html' % (data['gongao_type'], data['noticeId'])
            num = select_mysql(
                "SELECT COUNT(*) FROM `ztbRawInfo` WHERE page_url = '%s'" % item['page_url'])
            if num[0]['COUNT(*)'] == 1:
                yield item
            else:
                print('该条信息一爬取。。。',datetime.datetime.now())

if __name__ == '__main__':
    os.system('scrapy crawl gc_szyg')

