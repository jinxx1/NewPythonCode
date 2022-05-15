# -*- coding: utf-8 -*-
import scrapy,re,json,pprint,time
from NEW_GGZY.Exist import *
from urllib import parse
from NEW_GGZY.Breakpoint import *
TEMPPATH = TMEPTEST()

HEA = {'Accept':'application/json, text/javascript, */*; q=0.01',
'Origin':'http://www.zjzfcg.gov.cn',
'Referer':'http://www.zjzfcg.gov.cn/purchaseNotice/index.html?categoryId=3001'}

class CcgpZhejiangSpider(scrapy.Spider):
    name = 'ccgp_zhejiang'
    allowed_domains = ['www.ccgp-zhejiang.gov.cn']
    urlList = [{'lbid': '3010', 'catName': '浙江省_采购合同公告'}, {'lbid': '5002', 'catName': '浙江省_其他采购合同公告'}, {'lbid': '3014', 'catName': '浙江省_采购文件需求公示'}, {'lbid': '3013', 'catName': '浙江省_允许采购进口产品公示'}, {'lbid': '3012', 'catName': '浙江省_单一来源公示'}, {'lbid': '1001', 'catName': '浙江省_其他意见征询公告'}, {'lbid': '3004', 'catName': '浙江省_中标（成交）结果公告'}, {'lbid': '3007', 'catName': '浙江省_废标公告'}, {'lbid': '3009', 'catName': '浙江省_邀请招标资格入围公告'}, {'lbid': '3015', 'catName': '浙江省_终止公告'}, {'lbid': '3017', 'catName': '浙江省_采购结果变更公告'}, {'lbid': '4004', 'catName': '浙江省_公开招标资格入围公告'}, {'lbid': '4007', 'catName': '浙江省_其他采购结果公告'}, {'lbid': '3016', 'catName': '浙江省_履约验收公告（服务类）'}, {'lbid': '6003', 'catName': '浙江省_其他履约验收公告'}, {'lbid': '3005', 'catName': '浙江省_更正公告'}, {'lbid': '3006', 'catName': '浙江省_澄清(修改)公告'}, {'lbid': '3018', 'catName': '浙江省_中止(暂停)公告'}, {'lbid': '3019', 'catName': '浙江省_其他更正公告'}, {'lbid': '10001', 'catName': '浙江省_公款竞争性存放意见征询'}, {'lbid': '10002', 'catName': '浙江省_公款竞争性存放招标公告'}, {'lbid': '10003', 'catName': '浙江省_公款竞争性存放更正公告'}, {'lbid': '10004', 'catName': '浙江省_公款竞争性存放结果公告'}, {'lbid': '10005', 'catName': '浙江省_公款竞争性存放合同公告'}, {'lbid': '10006', 'catName': '浙江省_其他非政府采购项目意见征询'}, {'lbid': '10007', 'catName': '浙江省_其他非政府采购项目招标公告'}, {'lbid': '10008', 'catName': '浙江省_其他非政府采购项目更正公告'}, {'lbid': '10009', 'catName': '浙江省_其他非政府采购项目结果公告'}, {'lbid': '10010', 'catName': '浙江省_其他非政府采购项目合同公告'}, {'lbid': '10012', 'catName': '浙江省_国库现金管理招标公告'}, {'lbid': '10013', 'catName': '浙江省_国库现金管理中标公告'}, {'lbid': '10014', 'catName': '浙江省_国库现金管理更正公告'}, {'lbid': '10011', 'catName': '浙江省_其他非政府采购公告'}, {'lbid': '4001', 'catName': '浙江省_协议定点项目招标公告'}, {'lbid': '4002', 'catName': '浙江省_协议定点项目中标公告'}, {'lbid': '4003', 'catName': '浙江省_协议定点项目更正公告'}, {'lbid': '1995', 'catName': '浙江省_电子卖场合同公告'}, {'lbid': '1996', 'catName': '浙江省_电子卖场终止公告'}, {'lbid': '8011', 'catName': '浙江省_在线询价公告'}, {'lbid': '8010', 'catName': '浙江省_反向竞价公告'}, {'lbid': '9003', 'catName': '浙江省_其他电子卖场采购公告'}, {'lbid': '8006', 'catName': '浙江省_协议定点项目采购结果更正公告'}, {'lbid': '1997', 'catName': '浙江省_电子卖场中止（暂停）公告'}, {'lbid': '8009', 'catName': '浙江省_在线询价结果公告'}, {'lbid': '9002', 'catName': '浙江省_定点服务结果公告'}, {'lbid': '8008', 'catName': '浙江省_反向竞价结果公告'}, {'lbid': '7003', 'catName': '浙江省_投诉处理信息公告'}, {'lbid': '7004', 'catName': '浙江省_行政处罚信息公告'}, {'lbid': '7005', 'catName': '浙江省_行政处理信息公告'}, {'lbid': '7006', 'catName': '浙江省_监督检查公告'}, {'lbid': '7007', 'catName': '浙江省_集中采购机构考核结果公告'}, {'lbid': '7008', 'catName': '浙江省_供应商、采购代理机构和评审专家的违法失信行为记录公告'}, {'lbid': '7009', 'catName': '浙江省_其他监管公告'}, {'lbid': '3001', 'catName': '浙江省_公开招标公告'}, {'lbid': '3002', 'catName': '浙江省_竞争性谈判公告'}, {'lbid': '3003', 'catName': '浙江省_询价公告'}, {'lbid': '3008', 'catName': '浙江省_邀请招标资格预审公告'}, {'lbid': '3011', 'catName': '浙江省_竞争性磋商公告'}, {'lbid': '2001', 'catName': '浙江省_公开招标资格预审公告'}, {'lbid': '2002', 'catName': '浙江省_其他采购项目公告'}]
    baseUrl = 'http://manager.zjzfcg.gov.cn/cms/api/cors/remote/results?pageSize=100&pageNo={PageNo}&sourceAnnouncementType={lbid}&url=notice'
    def start_requests(self):
        meta = {}
        getTXTdict = getTXT(self.name, self.urlList)
        meta['Num'] = 1
        for i in getTXTdict['urlDict']:
            meta['Breakpoint'] = i
            meta['catName'] = i['catName']
            meta['lbid'] = i['lbid']
            meta['url'] = self.baseUrl.format(lbid = meta['lbid'],PageNo = str(meta['Num']))
            yield scrapy.Request(url=meta['url'],callback=self.parse, meta=meta,dont_filter=True,headers=HEA)

    def parse(self, response):

        meta = response.meta
        try:
            jsonT = json.loads(response.text)['articles']
        except:
            return None

        jsonT.append('0000')

        GotArtcl = 0
        notGotArtcl = 0
        for i in jsonT:
            urlListTemp = []
            # print('进入List循环体了')
            if notGotArtcl == 0 and GotArtcl == len(jsonT) - 1:
                # print('-------------------------------没有新文章退出')
                return None
            elif notGotArtcl != 0 and notGotArtcl + GotArtcl == len(jsonT) - 1:
                # print('--------------------翻页')
                meta['Num'] += 1
                meta['url'] = self.baseUrl.format(lbid=meta['lbid'], PageNo=str(meta['Num']))
                yield scrapy.Request(url=meta['url'], callback=self.parse, meta=meta, dont_filter=True, headers=HEA)
            else:
                # print('--------------------最终进入文章')
                meta['catName1'] = meta['catName'] + '_' + i['districtName']
                meta['ContentUrl'] = i['url']
                meta['id'] = i['id']

                urlListTemp.append(meta['ContentUrl'] + TEMPPATH)
                urllist = urlIsExist(urlListTemp)
                if len(urllist) < 1:
                    GotArtcl += 1
                    continue
                else:
                    notGotArtcl += 1
                    ContentUrlBase = 'http://manager.zjzfcg.gov.cn/cms/api/cors/remote/results?noticeId={}&url=noticeDetail'
                    yield scrapy.Request(url=ContentUrlBase.format(str(meta['id'])),
                                         callback=self.parseA, meta=meta,
                                             dont_filter=True)

    def parseA(self, response):
        # print('进入文章了')
        try:
            jsonT = json.loads(response.text)
        except:
            return None
        meta = response.meta
        dict1 = {}
        dict1['url'] = meta['ContentUrl']
        dict1['site'] = self.allowed_domains[0]
        dict1['title'] = jsonT['noticeTitle']
        dict1['issueTime'] = timeReMark(jsonT['noticePubDate'])
        dict1['content'] = jsonT['noticeContent']
        dict1['subclass'] = meta['catName1']
        requestsAPI = save_api(dict1)

        tempDict = meta['Breakpoint']
        tempDict['Num'] = meta['Num']
        writeTXT(self.name, json.dumps(tempDict, ensure_ascii='utf-8'))

        print(dict1['title'])
        print(dict1['url'])
        print(dict1['issueTime'])
        print(dict1['subclass'])
        print(len(dict1['content']))
        print(requestsAPI.text)
        print('----------------------------------------------------------------------------------------------------')