# -*- coding: utf-8 -*-
import scrapy,json,pprint,re
from NEW_GGZY.Exist import *
from NEW_GGZY.Breakpoint import *
from urllib import parse
TEMPPATH = TMEPTEST()



def findYMD(timeList):
    timeWord = ''
    for i in timeList:
        timeWord = timeWord + i
    try:
        yearw= re.findall(r"(\d{2,4})年",timeWord)[0]
        mouthw = re.findall(r"(\d{1,2})月",timeWord)[0]
        dayw = re.findall(r"(\d{1,2})日",timeWord)[0]
    except:
        try:
            issueTime = re.findall(r"\d{2,4}-\d{1,2}-\d{1,2}", timeWord)[0]
            i = issueTime.split('-')
            yearw = i[0]
            mouthw = i[1]
            dayw = i[2]
        except:
            return None
    if len(mouthw)<2:
        mouthw = '0' + mouthw
    if len(dayw)<2:
        dayw = '0' + dayw
    if len(yearw) < 4:
        yearw = '20' + yearw
    timeT = yearw + '-' + mouthw + '-' + dayw
    return timeT

class GdDongguanSpider(scrapy.Spider):
    name = 'gd_dongguan'
    allowed_domains = ['ggzy.dg.gov.cn']
    start_urls = ['http://ggzy.dg.gov.cn/']
    urlDict = [{'catName': '东莞市_建设工程_招标公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=1&tenderkind=All&projecttendersite=SS&orderFiled=fcInfostartdate&orderValue=desc', 'toal': '2225'}, {'catName': '东莞市_建设工程_补充通知', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=4&tenderkind=All&projecttendersite=SS', 'toal': '540'}, {'catName': '东莞市_建设工程_中标公示', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=7&tenderkind=All&projecttendersite=SS&orderFiled=fcInfostartdate&orderValue=desc', 'toal': '779'}, {'catName': '东莞市_建设工程_延期公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/findListByPage?fcInfotype=4&fcInfopubsource=1&tenderkind=All&projecttendersite=SS', 'toal': '6'}, {'catName': '东莞市_政府采购_采购公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/findListByPage?fcInfotype=1&openbidbelong=All', 'toal': '43'}, {'catName': '东莞市_政府采购_更正公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/findListByPage?fcInfotype=4&openbidbelong=All', 'toal': '9'}, {'catName': '东莞市_政府采购_结果公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/findListByPage?fcInfotype=7&openbidbelong=All', 'toal': '43'}, {'catName': '东莞市_国有产权_交易公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TenderPublishInfo/CQTPublishInfo/findListByPage?fcInfotype=1&openbidbelong=100', 'toal': '11'}, {'catName': '东莞市_国有产权_结果公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TenderPublishInfo/CQTPublishInfo/findListByPage?fcInfotype=undefined&openbidbelong=100', 'toal': '4'}, {'catName': '东莞市_排污权交易_交易公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/PWQPublishInfo/findListByPage?fcInfotype=1', 'toal': '2'}, {'catName': '东莞市_排污权交易_交易方式公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/PWQPublishInfo/findListByPage?fcInfotype=5', 'toal': '2'}, {'catName': '东莞市_排污权交易_结果公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/PWQPublishInfo/findListByPage?fcInfotype=7', 'toal': '2'}, {'catName': '东莞市_其他_其他公告', 'url': 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TenderPublishInfo/OtherPublishInfo/findListByPage', 'toal': '27'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.urlDict)
        meta['Num'] = int(getTXTdict['Num'])
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['key'] = i['catName']
            meta['url'] = i['url']
            yield scrapy.FormRequest(url=meta['url'],
                                     formdata={'currentPage':str(meta['Num'])},
                                     callback=self.parse,
                                     meta=meta)
    def parse(self, response):
        meta = response.meta
        ContentUrlList =[]
        try:
            jsonT = json.loads(response.text)['ls']
        except:
            meta['error'] = '没有发现json数据'
            meta['errorUrl'] = response.url
            errorLOG(meta)
            return None

        for i in jsonT:
            publishinfoid = ''
            NormalID = ''
            fgKeyid = ''
            dict = meta
            try:
                publishinfoid = i['publishinfoid']
            except:
                try:
                    NormalID = i['id']
                    if not NormalID:
                        fgKeyid = i['fgKeyid']
                except:
                    fgKeyid = i['fgKeyid']
            if publishinfoid:
                ContentTempUrl = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TradeInfo/GovProcurement/govdetail?publishinfoid={}&fcInfotype=1'
                ContentUrl = ContentTempUrl.format(publishinfoid)
                ContentUrlList.append(ContentUrl + TEMPPATH)
            elif NormalID:
                if '排污权' in dict['key']:
                    ContentTempUrl = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/PWQPublishInfo/detail?id={}'
                    ContentUrl = ContentTempUrl.format(NormalID)
                    ContentUrlList.append(ContentUrl + TEMPPATH)
                elif '其他公告' in dict['key']:
                    ContentTempUrl = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TenderPublishInfo/OtherPublishInfo/detail?id={}'
                    ContentUrl = ContentTempUrl.format(NormalID)
                    ContentUrlList.append(ContentUrl + TEMPPATH)
                else:
                    ContentTempUrl = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/jsdetail?publishId={}&fcInfotype=1'
                    ContentUrl = ContentTempUrl.format(NormalID)
                    ContentUrlList.append(ContentUrl + TEMPPATH)
            elif fgKeyid:
                if '其他公告' in dict['key']:
                    ContentTempUrl = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TenderPublishInfo/OtherPublishInfo/detail?id={}'
                    ContentUrl = ContentTempUrl.format(fgKeyid)
                    ContentUrlList.append(ContentUrl + TEMPPATH)
                else:
                    ContentTempUrl = 'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/TenderPublishInfo/CQTPublishInfo/detail?id={}&fcInfotype=1'
                    ContentUrl = ContentTempUrl.format(fgKeyid)
                    ContentUrlList.append(ContentUrl + TEMPPATH)
            else:
                meta['error'] = '列表页中，没有有效链接'
                meta['errorUrl'] = response.url
                errorLOG(meta)
                return None


        n=0
        urllist = urlIsExist(ContentUrlList)
        if len(urllist) > 0 and str(type(urllist)) == r"<class 'list'>":
            for url in urllist:
                n +=1
                if n == len(urllist):
                    meta['pageTune'] = 1
                else:
                    meta['pageTune'] = 0
                meta['ListPageNow'] = '本页第{}条，共{}条'.format(n,len(urllist))
                yield scrapy.Request(url=url.replace(TEMPPATH,''), callback=self.parseA, meta=meta)
        else:
            return None


    def parseA(self,response):
        meta = response.meta
        dict1 = {}
        try:
            html = response.xpath("//div[@class='content']").extract()[0]
            titleT = response.xpath("//h1/text() | //div[@class='header']/h2/text()").extract()[0]
        except:
            meta['error'] = '没有正文或标题'
            meta['errorUrl'] = response.url
            errorLOG(meta)
            return None

        timeT = response.xpath("//div[@class='detail']/div[@class='date']/text() | //div[@class='header']//text()").extract()
        PDFName = response.xpath("//table[@class='table02']//a/text()").extract()
        PDFDownLoadUrl = response.xpath("//table[@class='table02']//a/@href").extract()
        attachmentListJsonList = []
        dict1['attachmentListJson'] = []

        if len(PDFName) > 0:
            issueTime = response.xpath("//table[@class='table02']/tbody/tr[1]/td[2]/text()").extract()[0]
            if not issueTime:
                issueTime = findYMD(timeT)
            for i in range(len(PDFName)):
                attachmentDict = {}
                attachmentDict['downloadUrl'] = parse.urljoin(response.url, PDFDownLoadUrl[i])
                attachmentDict['name'] = PDFName[i]
                attachmentListJsonList.append(attachmentDict)
        elif len(timeT) > 0:
            issueTime = findYMD(timeT)
        else:
            issueTime = "2000-01-01 00:00:00"

        tempTime = timeReMark(issueTime)
        if tempTime == "2000-01-01 00:00:00":
            findTimeWord = titleT + html
            issueTime = findYMD(findTimeWord)

        dict1['url'] = response.url
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = titleT.replace('\r','').replace('\n','')
        dict1['issueTime'] = timeReMark(issueTime)
        if dict1['issueTime'] == "2000-01-01 00:00:00":
            meta['error'] = '时间错误'
            meta['errorUrl'] = response.url
            errorLOG(meta)

        dict1['content'] = html
        dict1['subclass'] = response.meta['key']
        dict1['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)

        requestsAPI = save_api(dict1)

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print('正文一共有字节：',len(dict1['content']))
        print(dict1['attachmentListJson'])
        print(requestsAPI.text)

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name,json.dumps(tempDict,ensure_ascii='utf-8'))
        print('------------------------------------')

        if meta['pageTune'] == 1:
            meta['Num'] += 1
            yield scrapy.FormRequest(url=meta['url'],formdata={'currentPage':str(meta['Num'])},callback=self.parse,meta=meta)