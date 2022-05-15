# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()


class GdShanweiSpider(scrapy.Spider):
    name = 'gd_shanwei'
    allowed_domains = ['swggzy.shanwei.gov.cn']
    base_url = 'http://swggzy.shanwei.gov.cn/noticesList/getNotices'
    lb_base = [{'catName': '汕尾市_建设工程_招标公告', 'url': '4793892710e942bdb8edb883822dbab4'}, {'catName': '汕尾市_建设工程_澄清公告', 'url': 'c0d135163be342c2b76a4957dc4b1999'}, {'catName': '汕尾市_建设工程_中标公示', 'url': '089ddf2ff80c4e259ac5b208e9154469'}, {'catName': '汕尾市_政府采购_采购公告', 'url': 'd3174a1009b141bcb4a99666527f53ed'}, {'catName': '汕尾市_政府采购_更正公告', 'url': '4a6dafa78918407eb17400c5ef72dcfe'}, {'catName': '汕尾市_政府采购_中标公告', 'url': '02f4929cf37641a5b1dfbd746af46e7b'}, {'catName': '汕尾市_土地矿业_交易公告', 'url': '4ba294626a8946a2b827904d48c5536e'}, {'catName': '汕尾市_土地矿业_结果公示', 'url': '43a4dc9369784c96a5035e06cd8972a4'}, {'catName': '汕尾市_产权交易_交易公告', 'url': '6c2a731f67ca4e92acf71bf1d88e187e'}, {'catName': '汕尾市_产权交易_结果公告', 'url': '362120bd761e4a4f9bef6136011475b0'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.lb_base)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            dataPost = {
            'area': 'all',
            'columnId': meta['url'],
            'pageIndex': str(meta['Num']),
            'pageSize': '50'}
            yield scrapy.FormRequest(url=self.base_url,formdata=dataPost,meta=meta,callback=self.parse)

    def parse(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)['attributes']['notices']
        urlListTemp = []
        if len(jsonT)<1:
            return None
        for i in jsonT:
            urlTemp = parse.urljoin(response.url,i['href'])
            urlListTemp.append(urlTemp + TEMPPATH)
        urllist = urlIsExist(urlListTemp)
        n = 0
        if len(urllist) > 0 and str(type(urllist)) == r"<class 'list'>":
            for url in urllist:
                n += 1
                if n == len(urllist):
                    meta['pageTune'] = 1
                else:
                    meta['pageTune'] = 0
                yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA,
                                     meta=meta)
        else:
            return None


    def parseA(self, response):
        meta = response.meta
        dict1 = {}
        html = response.xpath("//div[@class='contentbox2']").extract()
        titleT = response.xpath("//div[@class='contentbox2']/div[@class='contenttitle2 clearfix']/h3//text()").extract()
        timeT = response.xpath("//div[@class='fbtime']/span[1]/text()").extract()
        try:
            regex = re.findall(r"\d{2,4}-\d{1,2}-\d{1,2}", timeT[0])[0]
        except:
            regex = '2000-01-01'

        if html and titleT and timeT:
            dict1['url'] = response.url
            dict1['site'] = self.allowed_domains[0]
            dict1['title'] = titleT[0].strip()
            dict1['issueTime'] = timeReMark(regex)
            dict1['content'] = html[0]
            dict1['subclass'] = meta['catName']
            requestsAPI = save_api(dict1)


            tempDict = meta['Breakpoint']
            tempDict['Num'] = meta['Num']
            writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))


            print(dict1['title'])
            print(dict1['url'])
            print(dict1['issueTime'])
            print(len(dict1['content']))
            print(dict1['subclass'])
            print(requestsAPI.text)

            print('--------------------------------------------------------------------------------')

            if meta['pageTune'] == 1:
                meta['Num'] += 1
                dataPost = {
                    'area': 'all',
                    'columnId': meta['url'],
                    'pageIndex': str(meta['Num']),
                    'pageSize': '50'}
                yield scrapy.FormRequest(url=self.base_url, formdata=dataPost, meta=meta)

        else:
            return None