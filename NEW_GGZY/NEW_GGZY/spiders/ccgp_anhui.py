# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time,requests
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
from scrapy.settings import default_settings
TEMPPATH = TMEPTEST()



class CcgpAnhuiSpider(scrapy.Spider):
    name = 'ccgp_anhui'
    allowed_domains = ['www.ccgp-anhui.gov.cn']
    base_url = 'http://www.ccgp-anhui.gov.cn/cmsNewsController/getCgggNewsList.do?pageNum={}&numPerPage=20&title=&buyer_name=&agent_name=&proj_code=&bid_type=01&type=&dist_code=&pubDateStart=&pubDateEnd=&pProviceCode=&areacode_city=&areacode_dist=&channelCode='
    urlList = [{'catName': '安徽省',
                'url': 'sxqcg_cggg'},
               {'catName': '安徽省',
                'url': 'sjcg_cggg'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['url'] = self.base_url + i['url']
            yield scrapy.Request(url=meta['url'].format(str(meta['Num'])),
                                 callback=self.parse,
                                 meta=meta,
                                 dont_filter=True)



    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class='zc_contract_top']//a[@title]/@href").extract()


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
                    yield scrapy.Request(url=meta['url'].format(str(meta['Num'])), callback=self.parse, meta=meta,
                                         dont_filter=True)
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
                                meta['articleTitle'] = response.xpath("//*[@href = '{}']/@title".format(link[i])).extract()[0]
                            except:
                                continue
                            try:
                                meta['articleTime'] = response.xpath("//a[@href= '{}']/../../td/a[@href = 'javascript:void(0);']/text()".format(link[i])).extract()[0].replace('[','').replace(']','')
                            except:

                                continue
                            try:
                                catInfoTemp = response.xpath("//*[@href = '{}']".format(link[i])).extract()[0]
                                catInfo = re.findall("【(.*?)】", catInfoTemp.replace('\n','').replace('\t','').replace('\r',''), re.S)

                                ww = ''
                                for xx in catInfo:
                                    ww = ww + '_' + xx
                                meta['catName1'] = meta['catName'] + ww.strip()
                            except:

                                continue

                            yield scrapy.Request(url=url.replace(TEMPPATH, ''), callback=self.parseA, meta=meta,dont_filter=True)
        else:
            return None




    def parseA(self, response):
        meta=response.meta
        dict1 = {}
        try:
            html = response.xpath("//div[@class='column noBox con_shadow']").extract()[0]
            dict1['content'] = html
        except:
            return None

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['articleTitle']
        dict1['issueTime'] = timeReMark(meta['articleTime'])
        dict1['subclass'] = meta['catName1']

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print(len(dict1['content']))
        save_api(dict1)
        print('----------------------------------------------------------------------------------')