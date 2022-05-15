# # -*- coding: utf-8 -*-
import scrapy,pprint,re
from urllib import parse
from NEW_GGZY.Breakpoint import *
from NEW_GGZY.items import GgzyItem


class EcpSgccSpider(scrapy.Spider):
    name = 'ecp_sgcc'
    allowed_domains = ['ecp.sgcc.com.cn']
    start_url = 'http://ecp.sgcc.com.cn/html/topic/all/topic00/list_{}.html'


    def start_requests(self):
        meta={}
        meta['Num'] = 1
        yield scrapy.Request(url=self.start_url.format(str(meta['Num'])),callback=self.parse,dont_filter=True,meta=meta)


    def parse(self, response):
        meta = response.meta
        link = response.xpath("//div[@class = 'titleList']//a/@onclick").extract()

        if not link:
            return None

        print(meta['Num'])
        print(len(link))
        print('--------------------------------')

        urlList_withDomain = []
        for i in link:
            codeWord = re.findall("\'(.*?)\'",i)
            baseArtUrl = 'http://ecp.sgcc.com.cn/html/news/{}/{}.html'.format(codeWord[0],codeWord[1])
            urlList_withDomain.append(baseArtUrl)

        del link
        # urllist = urlList_withDomain
        urllist = urlIsExist(urlList_withDomain)

        if not urllist:
            return None

        for artUrl in urllist:
            yield scrapy.Request(url=artUrl, callback=self.parseA, dont_filter=True,meta=meta)

        del urllist
        meta['Num'] += 1
        yield scrapy.Request(url=self.start_url.format(str(meta['Num'])), callback=self.parse, dont_filter=True,meta=meta)


    def parseA(self,response):
        meta = response.meta
        dict1 = GgzyItem()

        dict1['content'] = response.xpath("//div[@class='article']/div[@class='bot_list']").extract_first()
        if not dict1['content']:
            return None



        title = response.xpath("//div[@class='articleTitle font04']/text()").extract_first()
        if not title:
            return None
        dict1['title'] = title.strip()


        issTime = response.xpath("//div[@class='article']/div[@class='articleTitle_details']/text()").extract_first()
        if not issTime:
            return None
        dict1['issueTime'] = timeReMark(issTime.strip())


        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]

        subclass = response.xpath("//div[@class = 'positionRight']//text()").extract()
        subclass = ''.join(subclass)

        dict1['subclass'] = subclass.replace('当前位置：','').replace('首页','国家电网有限公司').replace('>','_').replace(' ','')


        attachLink = response.xpath("//div[@class='article']/p[@class='bot_list']/a/@href").extract()
        if attachLink:
            attachmentListJsonList = []
            for i in attachLink:
                att_dict = {}
                att_dict['downloadUrl'] = parse.urljoin(response.url, i)
                attname = response.xpath("//*[@href = '{}']//text()".format(i)).extract()
                att_dict['name'] = ''.join(attname)
                attachmentListJsonList.append(att_dict)
            dict1['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)
            del attachmentListJsonList
        del attachLink




        yield dict1
