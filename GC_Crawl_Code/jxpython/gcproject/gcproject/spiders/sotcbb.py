# -*- coding: utf-8 -*-
import scrapy
import json
import re
import pprint,datetime
from urllib import parse
from bs4 import BeautifulSoup
from gcproject.items import GcprojectItem
from gcproject.parseScrpy import get_location,get_timestr
from gcproject.mysqlprecess import get_dupurl
import pandas as pd

header_raw = '''accept: application/json, text/javascript, */*; q=0.01
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,zh-TW;q=0.8
content-type: application/x-www-form-urlencoded; charset=UTF-8
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')

def infoDF():
    wordd = '''采购公告	https://cgpt.sotcbb.com/trade/noticeDetail	cggg	info_guid	NO
变更公告	https://cgpt.sotcbb.com/trade/noticeDetail	bggg	id	NO
废标公告	https://cgpt.sotcbb.com/trade/noticeDetail	fbgg	id	NO
结果公示	https://cgpt.sotcbb.com/trade/noticeDetail	cjgg	info_guid	NO
单一来源采购公告	https://cgpt.sotcbb.com/trade/noticeDetail	dyly	info_guid	NO
招投标服务网公告	https://cgpt.sotcbb.com/indexNotice/gzjgDdetails	NO	NO	buyer_name'''.split('\n')
    llist = []
    for i in wordd:
        list_t = tuple(i.split('\t'))
        llist.append(list_t)
    df = pd.DataFrame(llist, columns=['zhname', 'artileurl', 'gongao_type', 'noticeId', 'batch_no'])
    return df

class SotcbbSpider(scrapy.Spider):
    name = 'sotcbb'
    allowed_domains = ['cgpt.sotcbb.com']
    start_urls = 'https://cgpt.sotcbb.com/trade/getSearchResultList'
    infoDF = infoDF()
    ddict = {'A':'工程','B':'货物','C':'服务'}
    postInfo = {'project_type': '',
                    'cate_id':'',
                    'dateState':'',
                    'moneyStr':'',
                    'gonggaoStr':'',
                    'gongshiStr':'',
                    'company_name':'',
    }

    dupurl = get_dupurl(allowed_domains[0])
    def __init__(self, goon=None, *args, **kwargs):
        super(SotcbbSpider, self).__init__(*args, **kwargs)
        self.goon = goon

    def start_requests(self):
        meta={}
        meta['Num'] = 0
        meta['postInfo'] = self.postInfo
        meta['postInfo']['pageNo'] = str(meta['Num'])
        yield scrapy.FormRequest(url=self.start_urls,
                                 formdata=meta['postInfo'],
                             callback=self.parse,
                             meta=meta,
                             dont_filter=True)
    def parse(self, response):
        meta = response.meta
        if meta['Num'] > 11800:
            return None
        jsonT = json.loads(response.text)
        mark = 0
        for i in jsonT:
            meta['vertItem'] = {}
            df = self.infoDF[self.infoDF['zhname'] == i['gongao_type']]
            if i['gongao_type'] != '招投标服务网公告':
                articleUrlBase = 'https://cgpt.sotcbb.com/detail1?{}&{}.html'
                noticeId = df['noticeId'].values[0]
                meta['url'] = articleUrlBase.format(df['gongao_type'].values[0],i[noticeId])
                postUrl = df['artileurl'].values[0]
                postInfo = {'gongao_type': str(df['gongao_type'].values[0]),
                            'noticeId':str(i[noticeId])}
            else:
                articleUrlBase = 'https://cgpt.sotcbb.com/gzjgdetails?ztbfww-{}'
                meta['url'] = articleUrlBase.format(i[df['batch_no'].values[0]])
                postUrl = df['artileurl'].values[0]
                postInfo = {'batch_no':str(i[df['batch_no'].values[0]])}

            if meta['url'] in self.dupurl:
                mark += 1
                continue
            meta['vertItem']['subclass'] = i['gongao_type']
            meta['vertItem']['title'] = i['title']
            if i['cate_id'] in self.ddict.keys():
                meta['vertItem']['business_type'] = self.ddict[i['cate_id']]
            yield scrapy.FormRequest(url=postUrl,
                                     formdata=postInfo,
                                     callback=self.parseA,
                                     meta=meta,
                                     dont_filter=True)

        if mark == 10 and self.goon == 'no':
            return None
        meta['Num'] += 10
        meta['postInfo']['pageNo'] = str(meta['Num'])
        yield scrapy.FormRequest(url=self.start_urls,
                                 formdata=meta['postInfo'],
                             callback=self.parse,
                             meta=meta,
                             dont_filter=True)

    def parseA(self,response):
        meta = response.meta
        item = GcprojectItem()
        for k in meta['vertItem'].keys():
            item[k] = meta['vertItem'][k]

        item['page_url'] = meta['url']
        item['site'] = self.allowed_domains[0]
        item['issue_time'] = ''
        item['content'] = ''
        jsonT = json.loads(response.text)
        YN_list = isinstance(jsonT,list)
        if YN_list:
            item['content'] = "<p>请参看附件</p>"
            item['attchment'] = []
            for i in jsonT:
                if 'publish_time' not in i.keys():
                    continue
                if not i['name'] or not i['url']:
                    continue
                item['issue_time'] = get_timestr(i['publish_time'], "%Y-%m-%d %H:%M:%S")
                ddict={}
                ddict['name'] = i['name']
                ddict['download_url'] = i['url']
                item['attchment'].append(ddict)
        else:
            item['content'] = jsonT['content']
            item['issue_time'] = get_timestr(jsonT['create_time'],"%Y-%m-%d %H:%M:%S")

        if not item['content'] or not item['issue_time']:
            return None

        yield item

        # item['content'] = len(item['content'])
        # pprint.pprint(item)
        # print('-----------------------------------------')