# -*- coding: utf-8 -*-
import scrapy,re,json,pprint
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem
TEMPPATH = TMEPTEST()



class ZgcNanningZfcgSpider(scrapy.Spider):
    name = 'zgc_nanning_zfcg'
    allowed_domains = ['zfcg.nanning.gov.cn']
    urlList =[{'catName': '南宁市政府采购网_需求公示公告', 'url': 'http://zfcg.nanning.gov.cn/cxqgsgg/index_{}.htm'}, {'catName': '南宁市政府采购网_需求公示回复公告', 'url': 'http://zfcg.nanning.gov.cn/xqgshfgg/index_{}.htm'}, {'catName': '南宁市政府采购网_市本级_采购公告', 'url': 'http://zfcg.nanning.gov.cn//sjcggg/index_{}.htm'}, {'catName': '南宁市政府采购网_市本级_变更公告', 'url': 'http://zfcg.nanning.gov.cn//sjbggg/index_{}.htm'}, {'catName': '南宁市政府采购网_市本级_中标公告', 'url': 'http://zfcg.nanning.gov.cn//sjzbgs/index_{}.htm'}, {'catName': '南宁市政府采购网_区县级_中标公告', 'url': 'http://zfcg.nanning.gov.cn//xqzbgg/index_{}.htm'}, {'catName': '南宁市政府采购网_区县级_变更公告', 'url': 'http://zfcg.nanning.gov.cn//xqbggg/index_{}.htm'}, {'catName': '南宁市政府采购网_区县级_采购公告', 'url': 'http://zfcg.nanning.gov.cn//xqcggg/index_{}.htm'}, {'catName': '南宁市政府采购网_办公电器公告', 'url': 'http://zfcg.nanning.gov.cn/wsjj/index_{}.htm'}]


    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].replace('index_{}.htm','index.htm'),callback=self.parse, meta=meta,dont_filter=True)


    def parse(self, response):
        meta= response.meta
        link = response.xpath("//div[@class='f-left']/a/@href").extract()
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
                                meta['articleTitle'] = response.xpath("//*[@href='{}']/@title".format(str(link[i]))).extract()[0]
                            except:
                                return None

                            try:
                                meta['articleTime'] = response.xpath("//*[@href='{}']/../../div[@class = 'f-right']/text()".format(str(link[i]))).extract()[0]
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
            html = response.xpath("//div[@class='top10']").extract()[0]
            dict1['content'] = html.replace('\n','')
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
