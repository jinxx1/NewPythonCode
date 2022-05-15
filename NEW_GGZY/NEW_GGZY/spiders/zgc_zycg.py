# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem
TEMPPATH = TMEPTEST()


class ZgcZycgSpider(scrapy.Spider):
    name = 'zgc_zycg'
    allowed_domains = ['www.zycg.gov.cn']
    urlList = [{'catName': '中央政府采购网_征求意见公告', 'url': 'http://www.zycg.gov.cn/article/llist?catalog=zqyjgg&page={}'}, {'catName': '中央政府采购网_招标公告', 'url': 'http://www.zycg.gov.cn/article/llist?catalog=StockAffiche&page={}'}, {'catName': '中央政府采购网_中标（成交）公告', 'url': 'http://www.zycg.gov.cn/article/llist?catalog=ZhongBiao&page={}'}, {'catName': '中央政府采购网_近期开标项目', 'url': 'http://www.zycg.gov.cn/home/jqkbxm?catalog=StockAffiche&page={}'}, {'catName': '中央政府采购网_变更公告', 'url': 'http://www.zycg.gov.cn/article/llist?catalog=bggg&page={}'}, {'catName': '中央政府采购网_废标公告', 'url': 'http://www.zycg.gov.cn/article/llist?catalog=fbgg&page={}'}, {'catName': '中央政府采购网_需求公告', 'url': 'http://www.zycg.gov.cn/article/wsjjxq_list?page={}'}, {'catName': '中央政府采购网_成交公告', 'url': 'http://www.zycg.gov.cn/article/wsjjcj_list?page={}'}, {'catName': '中央政府采购网_废标公告', 'url': 'http://www.zycg.gov.cn/article/llist?catalog=wsjjfbgg&page={}'}]
    # urlList = [{'catName': '中央政府采购网_征求意见公告', 'url': 'http://www.zycg.gov.cn/article/llist?catalog=zqyjgg&page={}'}]
    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])),callback=self.parse, meta=meta,dont_filter=True)

    def parse(self, response):
        meta= response.meta
        link = response.xpath("//td[@class='news']/a/@href | //ul[@class='lby-list']/li/a/@href").extract()
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
                    yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,
                                         meta=meta, dont_filter=True)
                else:
                    # print('--------------------最终进入文章')
                    urlTemp = parse.urljoin(response.url, link[i])
                    urlListTemp.append(urlTemp + TEMPPATH)
                    urllist = urlIsExist(urlListTemp)
                    if len(urllist) < 1:
                        GotArtcl += 1
                        continue
                    else:
                        notGotArtcl += 1
                        for url in urllist:
                            try:
                                articleTitle = response.xpath("//*[@href='{}']/@title".format(str(link[i]))).extract()
                                meta['articleTitle'] = remarkList(articleTitle)[0]
                            except:

                                return None

                            try:
                                articleTime= response.xpath("//*[@href='{}']/../span/text()".format(str(link[i]))).extract()
                                articleTime1 = remarkList(articleTime)[0]
                                meta['articleTime'] =articleTime1.replace('[','').replace(']','')

                            except:

                                return None

                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,
                                                 dont_filter=True)
        else:

            return None


    def parseA(self, response):
        # print('进入文章了')

        meta = response.meta
        dict1 = GgzyItem()
        try:
            findHtml = re.findall("\<script id\=\"container\" name\=\"content\" type\=\"text/plain\"\>(.*?)\</script\>",response.text,re.S)
            dict1['content'] = findHtml[0].replace('\n','')
        except:
            try:
                dict1['content'] = response.xpath("//table[@class='detail_gg']").extract()[0]
            except:
                return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle'].strip()
        dict1['issueTime'] = timeReMark(meta['articleTime'].replace('.','-'))
        dict1['subclass'] = meta['catName']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        yield dict1
