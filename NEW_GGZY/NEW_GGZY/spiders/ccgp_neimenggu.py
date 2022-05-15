# -*- coding: utf-8 -*-
import scrapy,json,pprint
from NEW_GGZY.Exist import *
from NEW_GGZY.items import GgzyItem


class CcgpNeimengguSpider(scrapy.Spider):
    name = 'ccgp_neimenggu'
    allowed_domains = ['www.ccgp-neimenggu.gov.cn']
    base_url = 'http://www.ccgp-neimenggu.gov.cn/category/cggg?type_name=1'
    PostUrl = 'http://www.ccgp-neimenggu.gov.cn/zfcgwslave/web/index.php?r=zfcgw%2Fanndata'

    def start_requests(self):
        meta = {}
        meta['PostDate'] = {'type_name': '1',
                    'purorgform': '11',
                    'purmet': '',
                    'byf_page': '',
                    'fun': 'cggg',
                    '_csrf': '', }
        yield scrapy.Request(url=self.base_url,dont_filter=True,callback=self.parse,meta=meta)

    def parse(self, response):
        meta = response.meta
        meta['PostDate']['_csrf'] = response.xpath("//*[@id = '_csrf']/@value").extract_first()
        # urlList = [{'catName': '内蒙古_招标公告', 'url': '1'}, {'catName': '内蒙古_招标更正公告', 'url': '2'}, {'catName': '内蒙古_中标(成交)公告', 'url': '3'}, {'catName': '内蒙古_中标(成交)更正公告', 'url': '4'}, {'catName': '内蒙古_废标公告', 'url': '5'}, {'catName': '内蒙古_资格预审公告', 'url': '6'}, {'catName': '内蒙古_资格预审更正公告', 'url': '7'}, {'catName': '内蒙古_合同公告', 'url': '8'}]
        urlList = [{'catName': '内蒙古_招标公告', 'url': '1'}]
        meta['Num'] = 1

        for i in urlList:
            meta['catName'] = i['catName']
            meta['PostDate']['purmet'] = i['url']
            meta['PostDate']['byf_page'] = str(meta['Num'])
            # pprint.pprint(meta)
            yield scrapy.FormRequest(url=self.PostUrl,formdata=meta['PostDate'],callback=self.parseA,meta=meta,dont_filter=True)

    def parseA(self, response):
        meta = response.meta
        jsonT = json.loads(response.text)[0]
        articleUrl = 'http://www.nmgp.gov.cn/ay_post/post.php?tb_id={}&p_id={}'



        linkTemp = []
        TruelinkListDict = []

        for jsoninfo in jsonT:

            jsonDict = {}
            jsonDict['catName'] = meta['catName'] + '_' + jsoninfo['ADNAME']
            jsonDict['subclass'] = jsoninfo['SUBDATE']
            jsonDict['title'] = jsoninfo['TITLE_ALL']
            tb_id = jsoninfo['ay_table_tag']
            mark_id = jsoninfo['wp_mark_id']

            jsonDict['url'] = articleUrl.format(tb_id,mark_id)

            TruelinkListDict.append(jsonDict)
            linkTemp.append(jsonDict['url'])


        urllist = urlIsExist(linkTemp)

        # pprint.pprint(TruelinkListDict)

        if len(urllist) <1:
            return None

        for tempurl in urllist:
            for jsonDict in TruelinkListDict:
                if tempurl == jsonDict['url']:
                    # print('即将到parseB的连接：',jsonDict['url'])
                    yield scrapy.Request(url=jsonDict['url'], callback=self.parseB, dont_filter=True, meta=jsonDict)



        meta['Num'] += 1
        meta['PostDate']['byf_page'] = str(meta['Num'])
        print('翻页---------------------')
        yield scrapy.FormRequest(url=self.PostUrl, formdata=meta['PostDate'], callback=self.parseA, meta=meta,
                                 dont_filter=True)

    def parseB(self,response):
        meta = response.meta
        dict1 = GgzyItem()

        dict1['content'] = response.xpath("//div[@id = 'content-box-1']").extract_first()
        if not dict1['content']:
            return None


        DownLoadUrl = response.xpath("//div[@id='content-box-1']/div [not(@linhai)]/span/a/@href").extract()

        if len(DownLoadUrl)>1:
            attachmentListJson = []

            for i in DownLoadUrl:

                attachmentDict = {}
                attachmentDict['name'] = response.xpath("//*[@href = '{}']/text()".format(i)).extract_first()
                attachmentDict['downloadUrl'] = i
                attachmentListJson.append(attachmentDict)

            dict1['attachmentListJson'] = json.dumps(attachmentListJson)


        dict1['url'] = meta['url']
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['title']
        dict1['issueTime'] = meta['subclass']
        dict1['subclass'] = meta['catName']

        yield dict1
