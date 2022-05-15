# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpJiangxiSpider(scrapy.Spider):
    name = 'ccgp_jiangxi'
    allowed_domains = ['www.ccgp-jiangxi.gov.cn']
    urlList = [{'catName': '江西省_采购公告_', 'url': 'http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/002006001/{}.html'}, {'catName': '江西省_变更公告_', 'url': 'http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/002006002/{}.html'}, {'catName': '江西省_答疑澄清_', 'url': 'http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/002006003/{}.html'}, {'catName': '江西省_结果公示_', 'url': 'http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/002006004/{}.html'}, {'catName': '江西省_单一来源公示_', 'url': 'http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/002006005/{}.html'}, {'catName': '江西省_合同公示_', 'url': 'http://www.ccgp-jiangxi.gov.cn/web/jyxx/002006/002006006/{}.html'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)




    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='ewb-infolist']/ul/li/a/@href").extract()
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
                    yield scrapy.Request(url=meta['url'].format(str(meta['Num'])),callback=self.parse,meta=meta,dont_filter=True)
                else:
                    # print('--------------------最终进入文章')
                    urlTemp = parse.urljoin(response.url, link[i])
                    urlListTemp.append(urlTemp)
                    urllist = urlIsExist(urlListTemp)
                    if len(urllist) < 1:
                        GotArtcl += 1
                        continue
                    else:
                        notGotArtcl += 1
                        for url in urllist:
                            try:
                                articleTitle = response.xpath("//a[@href = '{}']//text()".format(str(link[i]))).extract()
                                meta['articleTitle'] = ''.join(articleTitle).strip()
                            except:
                                return None
                            try:
                                meta['articleTime'] = response.xpath("//a[@href = '{}']/../span/text()".format(str(link[i]))).extract()[0]
                            except:
                                meta['articleTime'] = '0'
                            yield scrapy.Request(url=url, callback=self.parseA, meta=meta,dont_filter=True)
        else:

            return None


    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        dict1 = {}
        if meta['articleTime'] == '0':
            try:
                timeT = response.xpath("//p[@class='infotime']/text()").extract()[0]
                meta['articleTime'] = timeT.strip().replace('[','').replace(']','')
            except:
                meta['articleTime'] = '2001-01-01'

        try:
            html = response.xpath("//div[@class='article-info']/div[@class = 'con']").extract()[0]
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
        print('--------------------------------------------------------------------------------------------')
#
# if __name__ == '__main__':
#     print('121212')

