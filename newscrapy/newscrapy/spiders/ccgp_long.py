# -*- coding: utf-8 -*-
import scrapy
import json, re
from newscrapy.scrapyParse import *
from newscrapy.items import NewscrapyItem
import pprint
from urllib import parse
import pandas as pd


def yid_json():
    import time
    nnn = 0
    while nnn < 20:
        rootPath = os.getcwd().replace('\\', '/')
        jsonpath = rootPath + "/ccgp_artall"
        jsonpathList = file_name_walk(jsonpath)
        for path in jsonpathList:
            df = pd.read_json(path_or_buf=path, orient='index')
            df['path'] = path
            yield df
        time.sleep(3600 * 10)
        nnn += 1

def resaveJsonfile(meta):
    try:
        df = pd.read_json(path_or_buf=meta['jsonpath'], orient='index')
        df.loc[meta['id'], 'mark'] = 1
        df.to_json(path_or_buf=meta['jsonpath'], orient='index')
    except Exception as ff:
        print('json文件写入失败---', ff)
        print(meta['path'], meta['id'])


class CcgpLongSpider1(scrapy.Spider):
    name = 'ccgp_long1'
    allowed_domains = ['www.ccgp.gov.cn']

    def start_requests(self):
        for num, i in enumerate(yid_json()):
            for n in range(len(i)):
                if i.loc[n].mark != 0:
                    continue
                meta = {}
                meta['issueTime'] = i.loc[n].issueTime
                meta['subclass'] = i.loc[n].subclass
                meta['title'] = i.loc[n].title
                meta['url'] = i.loc[n].url
                meta['jsonpath'] = i.loc[n].path
                meta['id'] = n
                yield scrapy.Request(url=meta['url'],
                                     callback=self.parse,
                                     meta=meta, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        dict1 = {}
        dict1['content'] = response.xpath("//div[@class = 'vF_detail_content']").extract_first()
        if not dict1['content']:
            contentList = response.xpath("//div[@class='vT_detail_content w760c']").extract()
            dict1['content'] = ''.join(contentList)
        if not dict1['content']:
            return None
        attachLink = response.xpath(
            "//div[@class='vF_detail_content']/a[@class='bizDownload']/@href | //div[@class='vF_detail_main']/div[@class='table']//a[@class = 'bizDownload']/@href").extract()
        if attachLink:
            attachmentListJsonList = []
            for i in attachLink:
                att_dict = {}
                att_dict['downloadUrl'] = parse.urljoin(response.url, i)
                attname = response.xpath("//*[@href = '{}']/text()".format(i)).extract()
                att_dict['name'] = ''.join(attname)
                attachmentListJsonList.append(att_dict)
            dict1['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)
            del attachmentListJsonList
        del attachLink
        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = meta['title'].strip()
        dict1['subclass'] = meta['subclass'][0:254]
        if not meta['issueTime']:
            issueTime = get_timestr(response.xpath("//span[@id='pubTime']/text()").extract_first())
            if not issueTime:
                issueTime = "2000-01-01 00:00:00"
            dict1['issueTime'] = issueTime
        else:
            dict1['issueTime'] = meta['issueTime']
        dict1['content'] = len(dict1['content'])
        insertmysql = save_api(dict1)
        resaveJsonfile(meta)

        # pprint.pprint(dict1)
        # print(insertmysql)
        # print('----------------------')


class CcgpLongSpider(scrapy.Spider):
    name = 'ccgp_long'
    allowed_domains = ['www.ccgp.gov.cn']
    custom_settings = {
        "SCHEDULER": "scrapy.core.scheduler.Scheduler",
    }
    urlBase = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index={pageindex}&bidSort=&buyerName=&projectId=&pinMu=&bidType=&dbselect=bidx&kw=&start_time={date}&end_time={date}&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName='
    DF = pd.read_json(path_or_buf='ccgp_date.json', orient='index')
    mysql_allurl = get_mysql_allurl(allowed_domains[0])

    def start_requests(self):
        meta = {}
        for i in range(len(self.DF)):
            if self.DF.loc[i].mark != 0:
                continue
            for n in ['2018', '2019', '2020']:
                if n in self.DF.loc[i].date:
                    meta['allPageNum'] = self.DF.loc[i].allPageNum
                    meta['date'] = self.DF.loc[i].date
                    for n in range(1, meta['allPageNum'] + 1):
                        geturl = self.urlBase.format(pageindex=n, date=meta['date'])
                        yield scrapy.Request(url=geturl,
                                             callback=self.parse,
                                             meta=meta, dont_filter=True)

    def parse(self, response):
        meta = response.meta
        links = response.xpath("//ul[@class='vT-srch-result-list-bid']/li/a/@href").extract()

        for num, link in enumerate(links):
            if link in self.mysql_allurl:
                continue

            TitleList = response.xpath("//*[@href = '{}']/text()".format(link)).extract()
            if TitleList:
                Title = ''.join(TitleList).strip()
            else:
                Title = '无标题'

            subclassList = []

            location = response.xpath("//*[@href = '{}']/../span/a/text()".format(link)).extract_first()
            if location:
                subclassList.append(location)

            sub1 = response.xpath("//*[@href = '{}']/../span/strong[1]/text()".format(link)).extract()
            if sub1:
                sub1 = ''.join(sub1).replace('\n', '').strip()
                subclassList.append(sub1)

            sub2 = response.xpath("//*[@href = '{}']/../span/strong[2]/text()".format(link)).extract()
            if sub2:
                sub2 = ''.join(sub2).replace('\n', '').strip()
                subclassList.append(sub2)

            subclassList = [x for x in subclassList if x]
            if subclassList:
                subclass = '_'.join(subclassList)
            else:
                subclass = '无任何分类'

            ttime = response.xpath("//*[@href = '{}']/../span/text()".format(link)).extract()
            s1 = re.findall("\d{4}.\d{2}.\d{2}.*\d{2}.\d{2}.\d{2}", ''.join(ttime))
            Time = get_timestr(''.join(s1))
            if not Time:
                Time = ''

            meta['dict1'] = {}
            meta['dict1']['url'] = link
            meta['dict1']['title'] = Title.strip()
            meta['dict1']['subclass'] = subclass
            meta['dict1']['issueTime'] = Time
            # meta['dict1']['allPageNum'] = meta['allPageNum']
            # meta['dict1']['date'] = meta['date']
            # meta['dict1']['pageNum'] = meta['Num']
            # meta['dict1']['mark'] = 0
            # meta['dict1']['artNum'] = num
            yield scrapy.Request(url=meta['dict1']['url'],
                                 callback=self.parseContent,
                                 dont_filter=True,
                                 meta=meta,
                                 )

            # llist.append(dict1)
        # filepath = 'ccgp_artall/' + meta['date'].replace(":",'') + "_" + str(meta['Num']) + '.json'
        # df = pd.DataFrame(llist)
        # df.to_json(filepath,orient='index')

    def parseContent(self, response):
        meta = response.meta
        dict1 = NewscrapyItem()

        dict1['content'] = response.xpath("//div[@class = 'vF_detail_content']").extract_first()
        if not dict1['content']:
            contentList = response.xpath("//div[@class='vT_detail_content w760c']").extract()
            dict1['content'] = ''.join(contentList)
            if not dict1['content']:
                return None

        dict1['title'] = meta['dict1']['title'].strip()
        if dict1['title'] == '无标题':
            dict1['title'] = response.xpath("//title/text()").extract_first()
            if not dict1['title']:
                dict1['title'] = response.xpath("//h2/text()").extract_first()
            if not dict1['title']:
                return None

        dict1['issueTime'] = meta['dict1']['issueTime']
        if not dict1['issueTime']:
            issueTime = get_timestr(response.xpath("//span[@id='pubTime']/text()").extract_first())
            if not issueTime:
                return None

        attachLink = response.xpath(
            "//div[@class='vF_detail_content']/a[@class='bizDownload']/@href | //div[@class='vF_detail_main']/div[@class='table']//a[@class = 'bizDownload']/@href").extract()
        if attachLink:
            attachmentListJsonList = []
            for i in attachLink:
                att_dict = {}
                att_dict['downloadUrl'] = parse.urljoin(response.url, i)
                attname = response.xpath("//*[@href = '{}']/text()".format(i)).extract()
                att_dict['name'] = ''.join(attname)
                attachmentListJsonList.append(att_dict)
            dict1['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)

        dict1['url'] = meta['dict1']['url']
        dict1['site'] = self.allowed_domains[0]
        dict1['subclass'] = meta['dict1']['subclass'][0:254]
        yield dict1

        # print('标题：', dict1['title'])
        # print('链接：', dict1['url'])
        # print('时间：', dict1['issueTime'])
        # print('类别：', dict1['subclass'])
        # print('内容字数：', len(dict1['content']))
        # if dict1['attachmentListJson']:
        #     print('附件：', len(dict1['attachmentListJson']))
        # else:
        #     print('附件：0')
        #
        # print('-------------------------------------')

