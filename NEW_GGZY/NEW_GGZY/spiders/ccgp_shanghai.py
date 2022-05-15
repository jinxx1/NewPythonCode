# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
import time,datetime
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()




class CcgpShanghaiSpider(scrapy.Spider):
    name = 'ccgp_shanghai'
    allowed_domains = ['www.zfcg.sh.gov.cn']

    urlList = [{'catName': '上海_采购公告_采购公告', 'url': 'cggg'}, {'catName': '上海_采购公告_澄清公告', 'url': 'cqgg'}, {'catName': '上海_采购公告_更正公告', 'url': 'gzgg'}, {'catName': '上海_单一来源公示', 'url': 'dylygs'}, {'catName': '上海_采购结果公告_成交公告', 'url': 'cjgg'}, {'catName': '上海_采购结果公告_失败公告', 'url': 'sbgg'}, {'catName': '上海_采购结果公告_中标公告', 'url': 'zbgg'}, {'catName': '上海_采购结果公告_更正更高', 'url': 'gzgg1'}, {'catName': '上海_反拍公告', 'url': 'fpgg'}, {'catName': '上海_团购公告_团购公告', 'url': 'tggg'}, {'catName': '上海_团购公告_团购成功公告', 'url': 'tgcggg'}, {'catName': '上海_团购公告_团购失败公告', 'url': 'tgsbgg'}]
    # urlList = [{'catName': '上海_采购公告_采购公告', 'url': 'cggg'}]
    base_url = 'http://www.zfcg.sh.gov.cn/news.do?method=purchasePracticeMore'

    def start_requests(self):
        meta = {}
        meta['bulletininfotable_crd'] = str(100)
        getTXTdict = getTXT(self.name,self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']

            datePost = {
                'bulletininfotable_crd': meta['bulletininfotable_crd'],
                'bulletininfotable_p': str(meta['Num']),
                'flag': meta['url'],
                'method': 'purchasePracticeMore',
            }
            yield scrapy.FormRequest(url=self.base_url,formdata=datePost,callback=self.parse,meta=meta,dont_filter=True)



    def parse(self, response):
        meta = response.meta
        link = response.xpath("//a/@value").extract()

        GotArtcl = 0
        notGotArtcl = 0
        if len(link) > 0:
            for i in range(len(link) + 1):
                urlListTemp = []
                # print('进入List循环体了')
                if notGotArtcl == 0 and GotArtcl == len(link):
                    # print('-------------------------------没有新文章退出')
                    return None
                elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(link):
                    # print('--------------------翻页')
                    meta['Num'] += 1
                    datePost = {
                        'bulletininfotable_crd': meta['bulletininfotable_crd'],
                        'bulletininfotable_p': str(meta['Num']),
                        'flag': meta['url'],
                        'method': 'purchasePracticeMore',
                    }
                    yield scrapy.FormRequest(url=self.base_url, formdata=datePost, callback=self.parse, meta=meta,
                                             dont_filter=True)
                else:
                    # print('--------------------最终进入文章')

                    urlTemp = 'http://www.zfcg.sh.gov.cn/emeb_bulletin.do?method=showbulletin&bulletin_id=' + link[i]
                    urlListTemp.append(urlTemp + TEMPPATH)
                    urllist = urlIsExist(urlListTemp)
                    # urllist = urlListTemp
                    if len(urllist) < 1:
                        GotArtcl += 1
                        continue
                    else:
                        notGotArtcl += 1
                        for url in urllist:
                            try:
                                meta['articleTitle'] = response.xpath("//a[@value = '{}']//text()".format(str(link[i]))).extract()[0]
                            except:

                                continue
                            try:
                                articleTime = response.xpath("//a[@value = '{}']/../../td[@width = '400']/text()".format(str(link[i]))).extract()[0]
                                meta['articleTime'] = re.findall("\d{4}-\d{2}-\d{2}",articleTime)[0]
                            except:

                                continue

                            meta['notGotArtcl'] = notGotArtcl
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,
                                                 dont_filter=True)
        else:

            return None


    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        dict1 = {}
        try:
            html = response.xpath("//body/table[1] | //div[@id='templateContext']").extract()[0]
            dict1['content'] = html
        except:

            return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle'].strip()
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['subclass'] = meta['catName']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print(len(dict1['content']))
        save_api(dict1)
        print(meta['Num'],meta['notGotArtcl'])
        print('--------------------------------------------------------------------------------------------')
