# -*- coding: utf-8 -*-
import scrapy,re,pprint,requests
import json,datetime
from getUrl.items import GeturlItem

b = datetime.datetime.now().strftime("%Y-%m-%d")
nowTime = datetime.datetime.strptime(b, "%Y-%m-%d")
strnowTime = str(nowTime).split(' ')[0]




class CmSpider(scrapy.Spider):
    name = 'cm'
    collName = 'monitorUrl'
    allowed_domains = ['b2b.10086.cn']
    start_urls = [{'catName': '中国移动_采购公告', 'url': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2','postUrl': 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=2'},{'catName': '中国移动_资格预审公告', 'url': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=3', 'postUrl': 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=3'}, {'catName': '中国移动_候选人公示', 'url': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=7', 'postUrl': 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=7'}, {'catName': '中国移动_中选结果公示', 'url': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=16', 'postUrl': 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=16'}, {'catName': '中国移动_单一来源采购信息公告', 'url': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=1', 'postUrl': 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=1'}, {'catName': '中国移动_供应商信息收集公告', 'url': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=8', 'postUrl': 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType=8'}]

    def start_requests(self):

        meta = {}
        meta['Num'] = 1
        meta['firstHea'] = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'b2b.10086.cn',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        for i in self.start_urls:
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            meta['postUrl'] = i['postUrl']
            yield scrapy.Request(url= meta['url'],
                             callback=self.parse,
                             dont_filter=True,
                             headers=meta['firstHea'],
                             meta=meta
                             )

    def parse(self, response):
        meta = response.meta
        regx = re.findall("type(.*?)function", response.text, re.M | re.S)
        a = ''.join(regx)
        b = a.replace('\t', '').replace('\r', '').replace(' ', '')
        regx1 = re.findall("\*/'(.*?)\'", b, re.M | re.S)
        meta['qt'] = ''.join(regx1)
        meta['postHea'] = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        PostDate = {
                       'page.currentPage': str(meta['Num']),
                       'page.perPageSize': '200',
                       'noticeBean.sourceCH': '',
                       'noticeBean.source': '',
                       'noticeBean.title': '',
                       'noticeBean.startDate': '',
                       'noticeBean.endDate': '',
                       '_qt': meta['qt'] }

        yield scrapy.FormRequest(url=meta['postUrl'],
                                 formdata=PostDate,
                                 callback=self.parseA,
                                 headers=meta['postHea'],
                                 dont_filter=True,
                                 meta=meta)

    def parseA(self, response):
        meta=response.meta
        item = GeturlItem()

        finD = {'issueTime': strnowTime, 'site': '中国移动'}
        dec = requests.post('http://localhost:1111/apiGetMongoInfo', data=json.dumps(finD)).text
        jsonT = json.loads(dec)['message']
        mongoLinkAll = [x['url'] for x in jsonT]

        baseUrl = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id='
        aa = response.xpath("//*[@onmousemove = 'cursorOver(this)']/@onclick").extract()

        n = 0
        for i in aa:
            getTime = response.xpath('//*[@onclick = "{}"]/td[4]/text()'.format(i)).extract_first()
            item['issueTime'] = datetime.datetime.strptime(getTime, "%Y-%m-%d")
            if item['issueTime'] == nowTime:

                regx = re.findall("(\d{6})",i)
                item['url'] = baseUrl + ''.join(regx)



                if item['url'] not in mongoLinkAll:
                    try:
                        cat1 = response.xpath('//*[@onclick = "{}"]/td[1]/text()'.format(i)).extract_first()
                    except:
                        cat1 = ''
                    try:
                        cat2 = response.xpath('//*[@onclick = "{}"]/td[2]/text()'.format(i)).extract_first()
                    except:
                        cat2 = ''
                    try:
                        title = response.xpath('//*[@onclick = "{}"]/td/a/@title'.format(i)).extract_first()
                        item['title'] = ''.join(title)
                    except:
                        item['title'] = ''
                    if not item['title']:
                        try:
                            item['title'] = response.xpath('//*[@onclick = "{}"]/td/a/text()'.format(i)).extract_first()
                        except:
                            item['title'] = ''
                    item['subclass'] = meta['catName'] + '_' + cat1 + '_' + cat2
                    item['collName'] = self.collName
                    item['site'] = '中国移动'
                    item['domain'] =self.allowed_domains[0]
                    item['from_Page'] = meta['url']
                    n += 1
                    yield item

        if n != 0:
            meta['Num'] += 1
            yield scrapy.Request(url= meta['url'],
                             callback=self.parse,
                             dont_filter=True,
                             headers=meta['firstHea'],
                             meta=meta
                             )
        else:
            return None

