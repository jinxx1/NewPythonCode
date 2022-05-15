
import scrapy,re,json,requests
from NEW_GGZY.Exist import *
from urllib import parse
import chardet,pprint

from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()



class GdHuizhouSpider(scrapy.Spider):
    name = 'gd_huizhou'
    allowed_domains = ['huizhou.gov.cn']
    base_url = 'http://zyjy.huizhou.gov.cn/PublicServer/commonAnnouncementAction/getCommonAnnouncementList.do'
    urlList = [{'catName': '惠州市_政府采购_需求公示', 'lb': '14', 'businessType': '1'}, {'catName': '惠州市_政府采购_预备招标', 'lb': '15', 'businessType': '1'}, {'catName': '惠州市_政府采购_采购（资格预审）公告', 'lb': '10', 'businessType': '1'}, {'catName': '惠州市_政府采购_澄清变更公告', 'lb': '11', 'businessType': '1'}, {'catName': '惠州市_政府采购_中标公告', 'lb': '12', 'businessType': '1'}, {'catName': '惠州市_政府采购_失败公告', 'lb': '19', 'businessType': '1'}, {'catName': '惠州市_建设工程_招标（资格预审）公告', 'lb': '20', 'businessType': '2'}, {'catName': '惠州市_建设工程_邀标信息公开', 'lb': '21', 'businessType': '2'}, {'catName': '惠州市_建设工程_中标（资格预审结果）公示', 'lb': '22', 'businessType': '2'}, {'catName': '惠州市_建设工程_通知公告', 'lb': '23', 'businessType': '2'}, {'catName': '惠州市_土地与矿业权交易_交易信息', 'lb': '40', 'businessType': '4'}, {'catName': '惠州市_土地与矿业权交易_结果公示', 'lb': '43', 'businessType': '4'}, {'catName': '惠州市_土地与矿业权交易_其他公告', 'lb': '46', 'businessType': '4'}, {'catName': '惠州市_国有产权交易_挂牌（变更）公告', 'lb': '30', 'businessType': '3'}, {'catName': '惠州市_国有产权交易_招标（变更）公告', 'lb': '31', 'businessType': '3'}, {'catName': '惠州市_国有产权交易_挂牌结果公告', 'lb': '32', 'businessType': '3'}, {'catName': '惠州市_国有产权交易_招标结果公告', 'lb': '35', 'businessType': '3'}]
    # urlList = [{'catName': '惠州市_政府采购_需求公示', 'lb': '14', 'businessType': '1'}]

    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name,self.urlList)

        meta['Num'] = int(getTXTdict['Num'])
        meta['url'] = self.base_url

        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['lb'] = i['lb']
            meta['businessType'] = i['businessType']
            datePost = {'announcementType':str(meta['lb']),'page':str(meta['Num']),'businessType':meta['businessType'],'rows':'50'}
            yield scrapy.FormRequest(url=meta['url'],formdata=datePost, callback=self.parse,meta=meta)

    def parse(self, response):
        dict1 = {}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        meta = response.meta

        urlListTemp = []
        idListTemp = []
        jsonT = json.loads(response.text)['data']['list']
        for i in jsonT:
            ArticleUrl = 'http://zyjy.huizhou.gov.cn/PublicServer/public/commonAnnouncement/showDetail.html?businessType={}&sidebarIndex=1&id={}'
            url = ArticleUrl.format(meta['businessType'],i['id'])
            urlListTemp.append(url + TEMPPATH)
            idListTemp.append(i['id'])
        if len(urlListTemp)<1:
            return None
        urllist = urlIsExist(urlListTemp)

        postUrl = 'http://zyjy.huizhou.gov.cn/PublicServer/commonAnnouncementAction/selectPublishAnnouncementById.do'
        if len(urllist) > 0 and str(type(urllist)) == r"<class 'list'>":
            for url in urllist:
                try:
                    meta['artTempID'] = re.findall("&id=(.*)",url.replace(TEMPPATH,''))[0]
                except:
                    continue

                r = requests.post(url=postUrl,data={'id':meta['artTempID']},headers=headers)
                jsonT = json.loads(r.text)['data']['announcement']
                dict1['url'] = url.replace(TEMPPATH,'')
                dict1['site'] = self.allowed_domains[0]
                dict1['title'] = jsonT['title']
                dict1['issueTime'] = timeReMark(jsonT['publishTime'])
                dict1['content'] = jsonT['content']
                dict1['subclass'] = response.meta['catName']
                requestsAPI = save_api(dict1)
                print(dict1['title'])
                print(dict1['url'])
                print(dict1['issueTime'])
                print(dict1['subclass'])
                print(len(dict1['content']))
                print(requestsAPI.text)
                tempDict = meta['Breakpoint']
                tempDict['Num'] = meta['Num']
                writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

                print('--------------------------------------以上是第{}页------------------------------------------'.format(str(meta['Num'])))
                meta['Num'] += 1
                datePost = {'announcementType': str(meta['lb']), 'page': str(meta['Num']),
                            'businessType': meta['businessType'], 'rows': '50'}
                yield scrapy.FormRequest(url=meta['url'], formdata=datePost, callback=self.parse, meta=meta)
        else:
            return None