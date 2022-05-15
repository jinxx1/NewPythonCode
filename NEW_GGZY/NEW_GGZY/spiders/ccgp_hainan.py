# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class CcgpHainanSpider(scrapy.Spider):
    name = 'ccgp_hainan'
    allowed_domains = ['www.ccgp-hainan.gov.cn']
    urlList = [{'catName': '海南省_',
                'url': 'http://www.ccgp-hainan.gov.cn/cgw/cgw_list_cgxx.jsp?currentPage={}'}]

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

        link = response.xpath("//ul[@class='nei03_04_08_01']/li/em/a/@href").extract()

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
                    yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse,meta=meta, dont_filter=True)
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
                                meta['articleTitle'] = response.xpath("//*[@href = '{}']/text()".format(link[i])).extract()[0]
                            except:

                                continue
                            try:
                                meta['articleTime'] = response.xpath("//li//*[@href = '{}']/../../i/text()".format(link[i])).extract()[0]
                            except:

                                continue
                            try:
                                meta['localName'] = response.xpath("//li//*[@href = '{}']/../../span/b/a/text()".format(link[i])).extract()[0]
                            except:

                                continue
                            try:
                                meta['lbName'] = response.xpath("//li//*[@href = '{}']/../../span/tt/a/text()".format(link[i])).extract()[0]
                            except:

                                continue

                            meta['catName1'] = meta['catName'] + meta['localName'] + '_' + meta['lbName']
                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,dont_filter=True)
        else:

            return None

    def parseA(self, response):
        # print('进入文章了')
        meta = response.meta
        meta['requestContentNum'] = 0
        dict1 = {}
        try:
            html = response.xpath("//div[@class = 'content01']").extract()[0]

        except:
            if meta['requestContentNum'] < 4:
                meta['requestContentNum'] +=1
                print("没有获取正文，休息5秒钟重新尝试，现在重试第{}次,共重试3次".format(meta['requestContentNum']))

                time.sleep(5)
                yield scrapy.Request(url=response.url, callback=self.parseA, meta=meta,dont_filter=True)
            else:

                return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle']
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['content'] = html
        dict1['subclass'] = meta['catName1'].replace(' ','')

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        yield dict1