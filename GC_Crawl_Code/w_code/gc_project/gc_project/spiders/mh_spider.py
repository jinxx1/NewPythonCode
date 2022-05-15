# -*- coding: utf-8 -*-
# author = wph
# date = 2020/11/23
import os,json,datetime,pymysql
import scrapy
from time import sleep
from scrapy import FormRequest
from gc_project.items import GcProjectItem
from redis import Redis
from scrapy.selector import Selector
from gc_project.db_helper import select_mysql,insert_mysql
from gc_project.db_helper import MysqlPool
r = Redis('127.0.0.1',6379)

m = MysqlPool()

class ZhaotianxiaSpider(scrapy.Spider):
    name = 'mh'
    # allowed_domains = ['www.xxx.com']
    start_urls = [
        {'url': 'https://zbtb.caac.gov.cn/sys-content/tableZbgg.html', 'page': 1},  # 190
        {'url': 'https://zbtb.caac.gov.cn/sys-content/tableZbgs.html', 'page': 1},  # 129
        {'url': 'https://zbtb.caac.gov.cn/sys-content/table.html', 'page': 1},
        {'url': 'https://zbtb.caac.gov.cn/sys-content/tableOtherAnnouncement.html', 'page': 1}
    ]

    def start_requests(self):
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Referer': 'https://zbtb.caac.gov.cn/sys-content/index/zbggList.html',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'zbtb.caac.gov.cn',
            'Origin': 'https://zbtb.caac.gov.cn',
        }
        for dic in self.start_urls:
            if dic['url'] == 'https://zbtb.caac.gov.cn/sys-content/tableZbgg.html':
                for page in range(1, dic['page']):
                    data_zbgg = {"sEcho": page,
                                 "iDisplayStart": (page - 1) * 15,
                                 "iColumns": 10,
                                 "sColumns": ",,,,,,,,,",
                                 "iDisplayLength": 15,
                                 "amDataProp": ["id", "", "announcementName", "announceTime", "annoPubContent",
                                                "projType",
                                                "reglQuth",
                                                "signEndTime", "fundsSource", "announceType"],
                                 "abSortable": ["true", "false", "false", "false", "false", "false", "true", "true",
                                                "true", "true"],
                                 "aiSortCol": [0],
                                 "asSortDir": ["asc"],
                                 "iSortingCols": 1,
                                 "asSearch": ["projType", "announceTime", "projName", "reglQuth", "fundsSource",
                                              "announceType"],
                                 "asSearchVal": ["", "", "", "", "", ""]}
                    # sleep(30)
                    yield scrapy.Request(url=dic['url'],
                                         method='POST',
                                         headers=headers,
                                         body=json.dumps(data_zbgg),
                                         callback=self.parse_zbgg,
                                         dont_filter=True)
            if dic['url'] == 'https://zbtb.caac.gov.cn/sys-content/tableZbgs.html':
                for page in range(1, dic['page']):
                    data_zbgs = {"sEcho":page,"iColumns":13,"sColumns":",,,,,,,,,,,,",
                         "iDisplayStart":(page - 1) * 15,
                         "iDisplayLength":15,
                         "amDataProp":["announceTime","","projName","projType","id","bidPublicityName","reglQuth",
                                       "firstCandidateName","secondCandidateName","thirdCandidateName","id",
                                       "projCode","oldBERId"],
                         "abSortable":['true','false','false','false','false','false','true','true','true','true','true','true','true'],
                         "aiSortCol":[0],"asSortDir":["desc"],"iSortingCols":1,
                         "asSearch":["projType","announceTime","bidPublicityName","reglQuth","projCode"],
                         "asSearchVal":["","","","",""]}
                    # sleep(30)
                    yield scrapy.Request(url=dic['url'],
                                         method='POST',
                                         headers=headers,
                                         body=json.dumps(data_zbgs),
                                         callback=self.parse_zbgs,
                                         dont_filter=True)
            if dic['url'] == 'https://zbtb.caac.gov.cn/sys-content/table.html':
                for page in range(1, dic['page']):
                    data_tzgg = {"sEcho":page,"iColumns":4,"sColumns":",,,",
                                 "iDisplayStart":(page - 1) * 15,"iDisplayLength":15,
                                 "amDataProp":["id","name","lastUpdateTime","contentDes"],
                                 "abSortable":['true','false','false','true'],"aiSortCol":[0],"asSortDir":["asc"],
                                 "iSortingCols":1,"asSearch":["groupCode"],"asSearchVal":["TZGG"]}
                    # sleep(30)
                    yield scrapy.Request(url=dic['url'],
                                         method='POST',
                                         headers=headers,
                                         body=json.dumps(data_tzgg),
                                         callback=self.parse_tzgg,
                                         dont_filter=True)
            if dic['url'] == 'https://zbtb.caac.gov.cn/sys-content/tableOtherAnnouncement.html':
                for page in range(1, dic['page']):
                    data_qtgg = {"sEcho":2,"iColumns":9,"sColumns":",,,,,,,,","iDisplayStart":0,
                                 "iDisplayLength":15,
                                 "amDataProp":["announceTime","","projName","projType","id","announcementName","reglQuth","id","quafExatMode"],
                                 "abSortable":["true","false","false","false","false","false","true","true","true"],"aiSortCol":[0],
                                 "asSortDir":["desc"],"iSortingCols":1,
                                 "asSearch":["projType","announceTime","announcementName","projName","reglQuth"],
                                 "asSearchVal":["","","","",""]}
                    # sleep(30)
                    yield scrapy.Request(url=dic['url'],
                                         method='POST',
                                         headers=headers,
                                         body=json.dumps(data_qtgg),
                                         callback=self.parse_qtgg,
                                         dont_filter=True)

    def parse_zbgs(self,response):
        for info in response.json()['aaData']:
            dic_obj = {}
            try:
                dic_obj['site'] = 'zbtb.caac.gov.cn'
                dic_obj['title'] = info['bidPublicityName']
                dic_obj['issue_time'] = info['announceTime']
                dic_obj['subclass'] = dic_obj['title'][-7::]
                dic_obj['page_url'] = 'https://zbtb.caac.gov.cn/sys-content/initPage.html?url=zbgsText&id=%s'%info['DT_RowId']
                link = 'https://zbtb.caac.gov.cn/sys-content/getBidEvaResById.html?id=%s' % info['DT_RowId']
                # sleep(30)
                yield scrapy.Request(url=link,callback=self.parse_zbgsdetail,dont_filter=True,meta={'dic_obj':dic_obj})
            except Exception as e:
                print('error :',e)
    def parse_zbgg(self, response):
        for info in response.json()['aaData']:
            dic_obj = {}
            try:
                dic_obj['site'] = 'zbtb.caac.gov.cn'
                dic_obj['title'] = info['announcementName']
                dic_obj['issue_time'] = info['announceTime']
                dic_obj['subclass'] = dic_obj['title'][-4::]
                dic_obj['page_url'] = 'https://zbtb.caac.gov.cn/sys-content/initPage.html?url=zbgg_init&id=%s' % info[
                    'DT_RowId']
                link = 'https://zbtb.caac.gov.cn/sys-content/findAnnounceById.html?id=%s'%info['DT_RowId']
                print(dic_obj)
                # sleep(30)
                yield scrapy.Request(url=link,callback=self.parse_zbggdetail,dont_filter=True,meta={'dic_obj': dic_obj})
            except Exception as e:
                print('error:  ',e)
    def parse_qtgg(self, response):
        for info in response.json()['aaData']:
            dic_obj = {}
            try:
                dic_obj['site'] = 'zbtb.caac.gov.cn'
                dic_obj['title'] = info['announcementName']
                dic_obj['issue_time'] = info['announceTime']
                dic_obj['subclass'] = '其它公告'
                dic_obj['page_url'] = 'https://zbtb.caac.gov.cn/sys-content/initPage.html?url=qtggText&id=%s' % info[
                    'DT_RowId']
                link = 'https://zbtb.caac.gov.cn/sys-content/getOtherAnnouncementById.html?id=%s' % info['DT_RowId']
                # sleep(30)
                yield scrapy.Request(url=link, callback=self.parse_qtggdetail, dont_filter=True, meta={'dic_obj': dic_obj})
            except Exception as e:
                print('error:',e)
    def parse_tzgg(self, response):
        for info in response.json()['aaData']:
            dic_obj = {}
            try:
                dic_obj['site'] = 'zbtb.caac.gov.cn'
                dic_obj['title'] = info['name']
                dic_obj['issue_time'] = info['lastUpdateTime']
                dic_obj['subclass'] = '通知公告'
                dic_obj['page_url'] = 'https://zbtb.caac.gov.cn/sys-content/index/tzggText.html?t=%s' % info['DT_RowId']
                link = 'https://zbtb.caac.gov.cn/sys-content/index/tzggText.html?t=%s'% info['DT_RowId']
                # sleep(30)
                yield scrapy.Request(url=link, callback=self.parse_tzggdetail, dont_filter=True, meta={'dic_obj': dic_obj})
            except Exception as e:
                print('error:',e)
    def parse_tzggdetail(self,response):
        dic_obj = response.meta['dic_obj']
        cc = response.xpath('//*[@id="content"]').get()
        now_time = datetime.datetime.now()
        sql = "INSERT INTO ztbRawInfo (subclass,site,page_url,title,issue_time,creation_time,end_time) VALUES ('%s','%s','%s','%s','%s','%s','%s')" \
              % (dic_obj['subclass'], dic_obj['site'], dic_obj['page_url'], dic_obj['title'], dic_obj['issue_time'],
                 now_time,
                 now_time)
        insert_id = insert_mysql(sql)
        c = pymysql.escape_string(cc)
        print(insert_id, '***')
        if insert_id != None:
            insert_mysql("INSERT INTO ztbRawInfoContent (raw_data_id,content) VALUES (%s,'%s')" % (insert_id, c))
    def parse_qtggdetail(self,response):
        dic_obj = response.meta['dic_obj']
        cc = """<p align="center" style="margin-top:15px;font-size:14px; font-weight:bold;" class="title_p">
			<span id="announcementName">{}</span>
		</p>""".format(dic_obj['title'])+response.json()['announcement']['announcementContent']
        now_time = datetime.datetime.now()
        sql = "INSERT INTO ztbRawInfo (subclass,site,page_url,title,issue_time,creation_time,end_time) VALUES ('%s','%s','%s','%s','%s','%s','%s')" \
              % (dic_obj['subclass'], dic_obj['site'], dic_obj['page_url'], dic_obj['title'], dic_obj['issue_time'],
                 now_time,
                 now_time)
        insert_id = insert_mysql(sql)
        c = pymysql.escape_string(cc)
        print(insert_id, '***')
        if insert_id != None:
            insert_mysql("INSERT INTO ztbRawInfoContent (raw_data_id,content) VALUES (%s,'%s')" % (insert_id, c))
    def parse_zbgsdetail(self,response):
        dic_obj = response.meta['dic_obj']
        p = response.json()
        dic = {}
        try:
            dic = dict(p['bidEvaluationResults'][0], **p['bidEvaluationResult'])
        except IndexError:
            dic = p['bidEvaluationResult']
        if dic.get('sectInfo') == None:dic['sectInfo'] = ''
        if dic.get('downAddr') == None:dic['downAddr'] = ''
        if dic.get('projOwnerName') == None:dic['projOwnerName'] = ''
        if dic.get('contbProp') == None:dic['contbProp'] = ''
        if dic.get('downStaTime') == None:dic['downStaTime'] = ''
        if dic.get('proDesc') == None:dic['proDesc'] = ''
        if dic.get('fundsSource') == None:dic['fundsSource'] = ''
        if dic.get('bidderQualification') == None:dic['bidderQualification'] = ''
        if dic.get('signStaTime') == None:dic['signStaTime'] = ''
        if dic.get('signEndTime') == None:dic['signEndTime'] = ''
        if dic.get('agencyTel') == None:dic['agencyTel'] = ''
        if dic.get('agencyFax') == None:dic['agencyFax'] = ''
        if dic.get('downEndTime') == None:dic['downEndTime'] = ''
        if dic.get('agencyEmail') == None:dic['agencyEmail'] = ''
        if dic.get('applicationMaterials') == None:dic['applicationMaterials'] = ''
        if dic.get('buyStaTime') == None:dic['buyStaTime'] = ''
        if dic.get('buyEndTime') == None:dic['buyEndTime'] = ''
        if dic.get('tendBank') == None:dic['tendBank'] = ''
        if dic.get('buyAddr') == None:dic['buyAddr'] = ''
        if dic.get('thirdCandidateQuote') == None:dic['thirdCandidateQuote'] = ''
        if dic.get('filePrice') == None:dic['filePrice'] = ''
        if dic.get('secondCandidateQuote') == None:dic['secondCandidateQuote'] = ''
        if dic.get('postPrice') == None:dic['postPrice'] = ''
        if dic.get('postDay') == None:dic['postDay'] = ''
        try:
            cc = '''
            <div id="div_zbgs" style="margin:20px 40px 40px;overflow:hidden;">
                            <p align="center" style="margin-top:15px;font-size:14px; font-weight:bold;" class="title_p">
                                <span id="projName">{projName}</span>
                                <label id="zbhxrgs">中标候选人公示</label>
                            </p>
                            <div id="div_gsjs" style="margin-top:-70px;float:right;margin-right:20px;display:none;"><div class="gsjs">公示结束</div></div>
                            <p class="second" style="margin-top:30px;">项目名称：
                                <span id="projName1">{projName}</span>
                                备案记录编号：
                                <span id="projCode">{projCode}</span>
                                项目类型：
                                <span id="projType">{projType}</span>
                                <label id="label_str">项目的招标评标工作已经结束，经专家评审，评标委员会推荐了本项目中标候选人</label>
                                <span id="changeReason" style="display:none;"></span>
                                ，公示期
                                <span id="pubPeriodStartTime">{pubPeriodStartTime}</span>至&nbsp;<span id="pubPeriodEndTime">{pubPeriodEndTime}</span>。<label id="ggsyjs" style="display:none;">该公示已结束。</label>
                            </p>
                            <div id="addtable" style="margin: 10px 20px;"><div id="div_remark_0" style="display:none;color:red;margin-top:15px;margin-bottom:0px;font-weight:bold">提示：项目负责人<label style="font-weight:bold" id="firstRemark_0"></label><label style="font-weight:bold" id="secondRemark_0"></label><label style="font-weight:bold" id="thirdRemark_0"></label>已中标其他项目！</div><table id="pro_section_0" class="pro_add_table" border="0" style="margin-top:10px"><tbody><tr><td>中标候选人</td><td>第一候选人</td><td>第二候选人</td><td>第三候选人</td></tr><tr><td>单位名称</td><td><label id="firstCandidateName_0" name="firstCandidateName_0">{firstCandidateName}</label></td><td><label id="secondCandidateName_0" name="secondCandidateName_0">{secondCandidateName}</label></td><td><label id="thirdCandidateName_0" name="thirdCandidateName_0">{thirdCandidateName}</label></td></tr><tr><td>综合总得分</td><td><label id="firstCandidateTotalScore_0" name="firstCandidateTotalScore_0">{firstCandidateTotalScore}</label></td><td><label id="secondCandidateTotalScore_0" name="secondCandidateTotalScore_0">{secondCandidateTotalScore}</label></td><td><label id="thirdCandidateTotalScore_0" name="thirdCandidateTotalScore_0">{thirdCandidateTotalScore}</label></td></tr><tr id="candidatePMTr_0"><td>项目负责人姓名</td><td><label id="firstCandidatePM_0" name="firstCandidatePM_0">{firstCandidatePM}</label></td><td><label id="secondCandidatePM_0" name="secondCandidatePM_0">{secondCandidatePM}</label></td><td><label id="thirdCandidatePM_0" name="thirdCandidatePM_0">{thirdCandidatePM}</label></td></tr><tr id="certificateNameTr_0"><td>项目负责人证书名称</td><td><label id="firstCertificateName_0" name="firstCertificateName_0">{firstCertificateName}</label></td><td><label id="secondCertificateName_0" name="secondCertificateName_0">{secondCertificateName}</label></td><td><label id="thirdCertificateName_0" name="thirdCertificateName_0">{thirdCertificateName}</label></td></tr><tr id="certificateCodeTr_0"><td>项目负责人证书编号</td><td><label id="firstCertificateCode_0" name="firstCertificateCode_0">{firstCertificateCode}</label></td><td><label id="secondCertificateCode_0" name="secondCertificateCode_0">{secondCertificateCode}</label></td><td><label id="thirdCertificateCode_0" name="thirdCertificateCode_0">{thirdCertificateCode}</label></td></tr><tr><td>投标人业绩</td>
                            <td><label id="firstCandidateAchievements_0" name="firstCandidateAchievements_0">{firstCandidateAchievements}</label></td>
                            <td><label id="secondCandidateAchievements_0" name="secondCandidateAchievements_0">{secondCandidateAchievements}</label></td>
                            <td><label id="thirdCandidateAchievements_0" name="thirdCandidateAchievements_0">{thirdCandidateAchievements}</label></td></tr><tr>
                            <td>投标报价（元）</td>
                            <td><label id="firstCandidateQuote_0" name="firstCandidateQuote_0" readonly="readonly" class="liad-form-control">{firstCandidateQuote}</label></td>
                            <td><label id="secondCandidateQuote_0" name="secondCandidateQuote_0" readonly="readonly" class="liad-form-control">{secondCandidateQuote}</label></td>
                            <td><label id="thirdCandidateQuote_0" name="thirdCandidateQuote_0" readonly="readonly" class="liad-form-control">{thirdCandidateQuote}</label></td></tr>
                            <tr><td>质量</td><td><label id="firstCandidateQuality_0" name="firstCandidateQuality_0">{firstCandidateQuality}</label></td>
                            <td><label id="secondCandidateQuality_0" name="secondCandidateQuality_0">{secondCandidateQuality}</label></td>
                            <td><label id="thirdCandidateQuality_0" name="thirdCandidateQuality_0">{thirdCandidateQuality}</label></td></tr><tr><td>工期</td>
                            <td><label id="firstCandidateTime_0" name="firstCandidateTime_0">{firstCandidateTime}</label></td>
                            <td><label id="secondCandidateTime_0" name="secondCandidateTime_0">{secondCandidateTime}</label></td>
                            <td><label id="thirdCandidateTime_0" name="thirdCandidateTime_0">{thirdCandidateTime}</label></td></tr>
                            <tr><td>评标情况</td><td><label id="firstCandidateCondition_0" name="firstCandidateCondition_0">{firstCandidateCondition}</label></td>
                            <td><label id="secondCandidateCondition_0" name="secondCandidateCondition_0">{secondCandidateCondition}</label></td>
                            <td><label id="thirdCandidateCondition_0" name="thirdCandidateCondition_0">{thirdCandidateCondition}</label></td></tr></tbody></table></div>
                            <p class="second" id="note">根据《中华人民共和国招标投标实施条例》第五十四条及第六十条规定。投标人或者其他利害关系人对依法必须进行招标的项目的评标结果有异议的，应当在中标候选人公示期间提出。招标人应当自收到异议之日起3日内作出答复；作出答复前，应当暂停招标投标活动。投标人或者其他利害关系人认为招标投标活动不符合法律、行政法规规定的，可以自知道或者应当知道之日起10日内向有关行政监督部门投诉。投诉应当有明确的请求和必要的证明材料。</p>
                            <table id="other" style="">
                                <tbody><tr>
                                    <td>异议受理部门（招标单位）：</td>
                                    <td><span id="objectionAcceptanceDep">{objectionAcceptanceDep}</span></td>
                                </tr>
                                <tr>
                                    <td>联系人：</td>
                                    <td><span id="contName">{contName}</span></td>
                                </tr>
                                <tr>
                                    <td>联系电话：</td>
                                    <td><span id="contTel">{contTel}</span></td>
                                </tr>
                                <tr>
                                    <td>投诉受理部门：</td>
                                    <td><span id="complaintAcceptanceDep">{complaintAcceptanceDep}</span></td>
                                </tr>
                                <tr>
                                    <td>地址：</td>
                                    <td><span id="complaintAcceptanceDepAddr">{complaintAcceptanceDepAddr}</span></td>
                                </tr>
                                <tr>
                                    <td>电话：</td>
                                    <td><span id="complaintAcceptanceDepTel">{complaintAcceptanceDepTel}</span></td>
                                </tr>
                            </tbody></table>
                            <table id="other1" align="right" style="margin-right: 20px;">
                                <tbody><tr>
                                    <td align="right">招标单位：</td>
                                    <td><span id="tendName">{tendName}</span></td>
                                </tr>
                                <tr>
                                    <td align="right">日期：</td>
                                    <td><span id="bidEvaluationResultTime">{bidEvaluationResultTime}</span></td>
                                </tr>
                            </tbody></table>
                    </div>
                '''.format(projName=dic['projName'], projCode=dic['projCode'], projType=dic['projType'],
                           pubPeriodStartTime=dic['pubPeriodStartTime'], pubPeriodEndTime=dic['pubPeriodEndTime'],
                           firstCandidateName=dic['firstCandidateName'], secondCandidateName=dic['secondCandidateName'],
                           thirdCandidateName=dic['thirdCandidateName'],
                           firstCandidateTotalScore=dic['firstCandidateTotalScore'],
                           secondCandidateTotalScore=dic['secondCandidateTotalScore'],
                           thirdCandidateTotalScore=dic['thirdCandidateTotalScore'],
                           firstCandidatePM=dic['firstCandidatePM'], secondCandidatePM=dic['secondCandidatePM'],
                           thirdCandidatePM=dic['thirdCandidatePM'], firstCertificateName=dic['firstCertificateName'],
                           secondCertificateName=dic['secondCertificateName'], thirdCertificateName=dic['thirdCertificateName'],
                           firstCertificateCode=dic['firstCertificateCode'], secondCertificateCode=dic['secondCertificateCode'],
                           thirdCertificateCode=dic['thirdCertificateCode'],
                           firstCandidateAchievements=dic['firstCandidateAchievements'],
                           secondCandidateAchievements=dic['secondCandidateAchievements'],
                           thirdCandidateAchievements=dic['thirdCandidateAchievements'],
                           firstCandidateQuote=dic['firstCandidateQuote'], secondCandidateQuote=dic['secondCandidateQuote'],
                           thirdCandidateQuote=dic['thirdCandidateQuote'], firstCandidateQuality=dic['firstCandidateQuality'],
                           secondCandidateQuality=dic['secondCandidateQuality'],
                           thirdCandidateQuality=dic['thirdCandidateQuality'],
                           firstCandidateTime=dic['firstCandidateTime'], secondCandidateTime=dic['secondCandidateTime'],
                           thirdCandidateTime=dic['thirdCandidateTime'], firstCandidateCondition=dic['firstCandidateCondition'],
                           secondCandidateCondition=dic['secondCandidateCondition'],
                           thirdCandidateCondition=dic['thirdCandidateCondition'],
                           objectionAcceptanceDep=dic['objectionAcceptanceDep'], contName=dic['contName'],
                           contTel=dic['contTel'],
                           complaintAcceptanceDep=dic['complaintAcceptanceDep'],
                           complaintAcceptanceDepAddr=dic['complaintAcceptanceDepAddr'],
                           complaintAcceptanceDepTel=dic['complaintAcceptanceDepTel'], tendName=dic['tendName'],
                           bidEvaluationResultTime=dic['bidEvaluationResultTime'])
            now_time = datetime.datetime.now()
            if dic_obj.get('business_type') == None:
                dic_obj['business_type'] = ''
            if dic_obj.get('city_name') == None:
                dic_obj['city_name'] = ''
            if dic_obj.get('purchase_type') == None:
                dic_obj['purchase_type'] = ''
            sql = "INSERT INTO ztbRawInfo (subclass,site,page_url,title,issue_time,creation_time,end_time,business_type,city_name,purchase_type) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                  % (dic_obj['subclass'], dic_obj['site'], dic_obj['page_url'], dic_obj['title'], dic_obj['issue_time'],
                     now_time,
                     now_time, dic_obj['business_type'], dic_obj['city_name'], dic_obj['purchase_type'])
            insert_id = insert_mysql(sql)
            c = pymysql.escape_string(cc)
            print(insert_id,'***')
            if insert_id != None:
                insert_mysql("INSERT INTO ztbRawInfoContent (raw_data_id,content) VALUES (%s,'%s')" % (insert_id, c))
        except Exception as e:
            print(e, '-----')
    def parse_zbggdetail(self, response):
        dic_obj = response.meta['dic_obj']
        p = response.json()
        dic = dict(p['biddingScheme'],**p['biddingAnnouncement'])
        if dic.get('sectInfo') == None:dic['sectInfo'] = ''
        if dic.get('downAddr') == None:dic['downAddr'] = ''
        if dic.get('projOwnerName') == None:dic['projOwnerName'] = ''
        if dic.get('contbProp') == None:dic['contbProp'] = ''
        if dic.get('downStaTime') == None:dic['downStaTime'] = ''
        if dic.get('proDesc') == None:dic['proDesc'] = ''
        if dic.get('fundsSource') == None:dic['fundsSource'] = ''
        if dic.get('bidderQualification') == None:dic['bidderQualification'] = ''
        if dic.get('signStaTime') == None:dic['signStaTime'] = ''
        if dic.get('signEndTime') == None:dic['signEndTime'] = ''
        if dic.get('agencyTel') == None:dic['agencyTel'] = ''
        if dic.get('agencyFax') == None:dic['agencyFax'] = ''
        if dic.get('downEndTime') == None:dic['downEndTime'] = ''
        if dic.get('agencyEmail') == None:dic['agencyEmail'] = ''
        if dic.get('applicationMaterials') == None:dic['applicationMaterials'] = ''
        if dic.get('buyStaTime') == None:dic['buyStaTime'] = ''
        if dic.get('buyEndTime') == None:dic['buyEndTime'] = ''
        if dic.get('tendBank') == None:dic['tendBank'] = ''
        if dic.get('buyAddr') == None:dic['buyAddr'] = ''
        if dic.get('thirdCandidateQuote') == None:dic['thirdCandidateQuote'] = ''
        if dic.get('filePrice') == None:dic['filePrice'] = ''
        if dic.get('secondCandidateQuote') == None:dic['secondCandidateQuote'] = ''
        if dic.get('postPrice') == None:dic['postPrice'] = ''
        if dic.get('postDay') == None:dic['postDay'] = ''
        try:
            cc = '''
                    <div id="div_zbgg" style="padding-top:30px;padding-bottom:20px;overflow: hidden;">
                    		<p id="announcementName_title" align="center" style="margin-top:5px;" class="title_p">
                    			<span id="projName_zbgg" class="title_p">{projName}</span>
                    			<span id="sectInfo_zbgg" class="title_p"></span>{sectInfo}
                    		</p>
                    		<div id="div_bmjs" style="margin-top:-70px;float:right;margin-right:20px;display:none;"><div class="bmjs">登记结束</div></div>
                    		<p class="title_p">1.招标条件</p>
                    		<p class="second">本招标项目
                    			<span id="projName1_zbgg">{projName}</span>已由
                    			<span id="projApprDept_zbgg">{projApprDept}</span>以
                    			<span id="projApprNumber_zbgg">{projApprNumber}</span>批准建设，项目业主为
                    			<span id="projOwnerName_zbgg">{projOwnerName}</span>，建设资金来自
                    			<span id="fundsSource_zbgg">{fundsSource}</span>，项目出资比例为
                    			<span id="contbProp_zbgg">{contbProp}</span>，招标人为
                    			<span id="tendName_zbgg">{tendName}</span>。项目已具备招标条件，现对该项目的施工进行公开招标。
                    		</p>
                    		<p class="title_p" id="proDesc_zbgg">{proDesc}</p>
                    		<p class="title_p">3.投标人资格要求 </p>
                    		<p class="second" id="bidderQualification_zbgg">{bidderQualification}</p>
                    		<p class="second"><span style="white-space: pre-wrap;">3.1投标人须是中华人民共和国境内正式注册并具有有效独立法人资格的法人或其他组织，须具备建设行政主管部门颁发的机场场道工程专业承包壹级资质，且具有有效的安全生产许可证。</span></p>
                    		<p class="second"><span style="white-space: pre-wrap;">3.2拟派项目经理须具有国家一级注册建造师证书（民航机场工程），及有效的安全生产考核合格证书（B证），拟派项目经理若有其他在建工程，须符合《民航局机场司关于进一步明确注册建造师担任施工项目负责人有关意见的通知》的要求。</span></p><p class="second">
                    		<span style="white-space: pre-wrap;">3.3单位负责人为同一人或者存在控股、管理关系的不同单位，不得同时参加本招标项目投标。</span></p><p class="second"><span style="white-space: pre-wrap;">3.4在同行业中有较好的信誉，2017年 01月01日至投标截止之日未因施工质量问题受到民航行政主管部门的行政处罚并在人员、设备、资金等方面具备相应的施工能力。</span></p><p class="second"><span style="white-space: pre-wrap;">3.5本次招标不接受被人民法院列为失信被执行人的单位投标，以“信用中国”网站（www.creditchina.gov.cn）或各级信用信息共享平台查询信息为准。</span></p><p class="second"><span style="white-space: pre-wrap;">3.6本次招标不接受联合体投标。</span></p>
                    		<p class="title_p">4.投标登记</p>
                    		<p class="second">4.1  请投标人于
                    			<span id="signStaTime_zbgg">{signStaTime}</span>至
                    			<span id="signEndTime_zbgg">{signEndTime}</span>（法定公休日、法定节假日除外），携带登记资料在
                    			<span id="agencyAddr_zbgg">{agencyAddr}</span>进行投标登记或将登记资料传真至
                    			<span id="agencyFax_zbgg">{agencyFax}</span>进行投标登记或将登记资料扫描件电子版发送至 
                    			<span id="agencyEmail_zbgg">{agencyEmail}</span>进行投标登记②。 
                    		</p>
                    		<p class="second" id="applicationMaterials_zbgg">登记资料包括：</p><p class="second">
                    		<span style="white-space: pre-wrap;">{applicationMaterials}</span></p>
                    		<p><label style="color: red;padding-left: 23px;">提示：投标人需在民航专业工程建设项目招标投标管理系统（https://zbtb.caac.gov.cn）网上完成注册和投标登记。</label></p>
                    		<p class="title_p">5.招标文件的获取 </p>
                    		<p class="second">5.1  请投标人于
                    			<span id="buyStaTime_zbgg">{buyStaTime}</span>至
                    			<span id="buyEndTime_zbgg">{buyEndTime}</span>（法定公休日、法定节假日除外），在
                    			<span id="buyAddr_zbgg">{buyAddr}</span>购买招标文件。或 请投标人于 
                    			<span id="downStaTime_zbgg">{downStaTime}</span>至
                    			<span id="downEndTime_zbgg">{downEndTime}</span>（法定公休日、法定节假日除外），在
                    			<span id="downAddr_zbgg">{downAddr}</span>下载招标文件，并于递交投标文件的截止时间之前购买纸版招标文件，并以纸版招标文件为准。 
                    		</p>
                    		<p class="second">5.2 招标文件每标段售价
                    			<span id="filePrice_zbgg">{filePrice}</span>元，技术资料等售价
                    			<span id="techFilePrice_zbgg">/</span>元，售后不退。
                    		</p>
                    		<p class="second">5.3 邮购招标文件的，需另加手续费（含邮费）
                    			<span id="postPrice_zbgg">{postPrice}</span>元。招标人在收到邮购款（含手续费）后
                    			<span id="postDay_zbgg">{postDay}</span>日内寄送。 
                    		</p>
                    		<p class="title_p">6.投标文件的递交 </p>
                    		<p class="second">6.1 投标文件递交的截止时间（投标截止时间，下同）为
                    			<span id="commDeadline_zbgg">{commDeadline}</span>，地点为
                    			<span id="commAddr_zbgg">{commAddr}</span>。
                    		</p>
                    		<p class="second">6.2 逾期送达的或者未送达指定地点的投标文件，招标人不予受理。</p>
                    		<p class="title_p">7.发布公告的媒介 </p>
                    		<p class="second">本次招标公告同时在
                    			<span id="pubMedia_zbgg">{pubMedia}</span>上发布。
                    		</p>
                    		<p class="title_p">8. 联系方式 </p>
                    		<table id="ContNameInfo" align="center">
                    			<tbody><tr>
                    				<td align="right">招 标 人：</td>
                    				<td align="left"><span id="tendName1_zbgg">{tendName}</span></td>
                    				<td style="width:100px"></td>
                    				<td align="right">招标代理机构：</td>
                    				<td align="left"><span id="agencyName_zbgg">{agencyName}</span></td>
                    			</tr>
                    			<tr>
                    				<td align="right">地       址：</td> <!-- 招标人地址  -->
                    				<td align="left"><span id="tendAddr_zbgg">{tendAddr}</span></td><!-- 招标人地址  -->
                    				<td style="width:100px"></td>
                    				<td align="right">地       址：</td><!-- 招标代理地址  -->
                    				<td align="left"><span id="agencyAddr1_zbgg">{agencyAddr1}</span></td><!-- 招标代理地址  -->
                    			</tr>
                    			<tr>
                    				<td align="right">邮       编：</td><!-- 招标人邮编  -->
                    				<td align="left"><span id="tendPostCode_zbgg">{tendPostCode}</span></td><!-- 招标人邮编  -->
                    				<td style="width:100px"></td>
                    				<td align="right">邮       编：</td><!-- 招标代理邮编  -->
                    				<td align="left"><span id="agencyPostCode_zbgg">{agencyPostCode}</span></td><!-- 招标代理邮编  -->
                    			</tr>
                    			<tr>
                    				<td align="right">联 系 人：</td><!-- 招标人联系人 -->
                    				<td align="left"><span id="tendContName_zbgg">{tendContName}</span></td><!-- 招标人联系人 -->
                    				<td style="width:100px"></td>
                    				<td align="right">联 系 人：</td><!-- 招标代理联系人  -->
                    				<td align="left"><span id="agencyContName_zbgg">{agencyContName}</span></td><!-- 招标代理联系人  -->
                    			</tr>
                    			<tr>
                    				<td align="right">电       话：</td><!-- 招标人电话  -->
                    				<td align="left"><span id="tendTel_zbgg">{tendTel}</span></td><!-- 招标人电话  -->
                    				<td style="width:100px"></td>
                    				<td align="right">电       话：</td><!-- 招标代理电话  -->
                    				<td align="left"><span id="agencyTel_zbgg">{agencyTel}</span></td><!-- 招标代理电话  -->
                    			</tr>
                    			<tr>
                    				<td align="right">传       真：</td><!-- 招标人传真  -->
                    				<td align="left"><span id="tendFax_zbgg">{tendFax}</span></td><!-- 招标人传真  -->
                    				<td style="width:100px"></td>
                    				<td align="right">传       真：</td><!-- 招标代理传真  -->
                    				<td align="left"><span id="agencyFax1_zbgg">{tendFax}</span></td><!-- 招标代理传真  -->
                    			</tr>
                    			<tr>
                    				<td align="right">电子邮件：</td><!-- 招标人电子邮箱  -->
                    				<td align="left"><span id="tendEmail_zbgg">{tendEmail}</span></td><!-- 招标人电子邮箱  -->
                    				<td style="width:100px"></td>
                    				<td align="right">电子邮件：</td><!-- 招标代理电子邮箱 -->
                    				<td align="left"><span id="agencyEmail1_zbgg">{agencyEmail1}</span></td><!-- 招标代理电子邮箱  -->
                    			</tr>
                    			<tr>
                    				<td align="right">网       址：</td><!-- 招标人网址 -->
                    				<td align="left"><span id="tendWebsite_zbgg">{tendWebsite}</span></td><!-- 招标人网址  -->
                    				<td style="width:100px"></td>
                    				<td align="right">网       址：</td><!-- 招标代理网址  -->
                    				<td align="left"><span id="agencyWebsite_zbgg">{agencyWebsite}</span></td><!-- 招标代理网址  -->
                    			</tr>
                    			<tr>
                    				<td align="right">开户银行：</td><!-- 招标人开户银行  -->
                    				<td align="left"><span id="tendBank_zbgg">{tendBank}</span></td><!-- 招标人开户银行  -->
                    				<td style="width:100px"></td>
                    				<td align="right">开户银行：</td><!-- 招标代理开户银行  -->
                    				<td align="left"><span id="agencyBank_zbgg">{agencyBank}</span></td><!-- 招标代理开户银行  -->
                    			</tr>
                    			<tr>
                    				<td align="right">帐       号：</td><!-- 招标人开户银行账号  -->
                    				<td align="left"><span id="tendBankAccount_zbgg">{tendBankAccount}</span></td><!-- 招标人开户银行账号  -->
                    				<td style="width:100px"></td>
                    				<td align="right">帐       号：</td><!-- 招标代理开户银行账号  -->
                    				<td align="left"><span id="agencyBankAccount_zbgg">{agencyBankAccount}</span></td><!-- 招标代理开户银行账号  -->
                    			</tr>
                    		</tbody></table>
                    		<p align="right">
                    			日期：<span id="annoPubDate_zbgg">{annoPubDate}</span>
                    		</p>
                    		<hr>
                    		<p style="line-height:15px;font-size:11px;">注：<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    			①资质的要求应符合建设行政主管部门颁发的有关民航专业工程的资质规定，凡是民航专业工程资质范围内允许承担的工程内容，不得增加或采用非民航专业工程的资质要求。
                    			<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;②投标登记时间不得少于 5 日，无论采用何种登记方式，招标人或招标代理机构应及时向登记单位以书面形式出具登记确认函。
                    		</p>
                    		<div id="btn_area" style="width: 100%;padding: 20px 20px 0px 20px;display:none;">
                    			<button id="btn_return" class="btn btn-primary"><i class="fa fa-table"></i> 返回列表</button>
                    			<button id="add-btn" class="btn btn-primary" disabled="disabled" style="float: right;"><i class="fa fa-star-o"></i> 收藏项目</button>
                    		</div>
                    	</div>
                    '''.format(projName=dic['projName'], sectInfo=dic['sectInfo'],
                               projApprDept=dic['projApprDept'], projApprNumber=dic['projApprNumber'],
                               projOwnerName=dic['projOwnerName'],proDesc=dic['proDesc'],signEndTime=dic['signEndTime'],
                               fundsSource=dic['fundsSource'], contbProp=dic['contbProp'], tendName=dic['tendName'],
                               bidderQualification=dic['bidderQualification'], signStaTime=dic['signStaTime'],
                               agencyAddr=dic['agencyAddr'], agencyFax=dic['agencyFax'], agencyEmail=dic['agencyEmail'],
                               applicationMaterials=dic['applicationMaterials'], buyStaTime=dic['buyStaTime'],
                               buyEndTime=dic['buyEndTime'],downAddr=dic['downAddr'],tendBank=dic['tendBank'],
                               buyAddr=dic['buyAddr'], downStaTime=dic['downStaTime'], downEndTime=dic['downEndTime'],
                               filePrice=dic['filePrice'], postPrice=dic['postPrice'],postDay=dic['postDay'],
                               commDeadline=dic['commDeadline'], commAddr=dic['commAddr'], pubMedia=dic['pubMedia'],
                               tendName1=dic['tendName1'],tendAddr=dic['tendAddr'], tendPostCode=dic['tendPostCode'],
                               tendContName=dic['tendContName'],tendTel=dic['tendTel'],
                               tendFax=dic['tendFax'], tendEmail=dic['tendEmail'], tendWebsite=dic['tendWebsite'],
                               tendBankAccount=dic['tendBankAccount'], agencyName=dic['agencyName'],
                               agencyAddr1=dic['agencyAddr1'],agencyTel=dic['agencyTel'],
                               agencyPostCode=dic['agencyPostCode'], agencyContName=dic['agencyContName'],
                               agencyEmail1=dic['agencyEmail1'], agencyWebsite=dic['agencyWebsite'],
                               agencyBank=dic['agencyBank'], agencyBankAccount=dic['agencyBankAccount'],
                               annoPubDate=dic['annoPubDate'])
            now_time = datetime.datetime.now()
            if dic_obj.get('business_type') == None:
                dic_obj['business_type'] = ''
            if dic_obj.get('city_name') == None:
                dic_obj['city_name'] = ''
            if dic_obj.get('purchase_type') == None:
                dic_obj['purchase_type'] = ''
            sql = "INSERT INTO ztbRawInfo (subclass,site,page_url,title,issue_time,creation_time,end_time,business_type,city_name,purchase_type) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                  % (dic_obj['subclass'], dic_obj['site'], dic_obj['page_url'], dic_obj['title'], dic_obj['issue_time'], now_time,
                     now_time, dic_obj['business_type'], dic_obj['city_name'], dic_obj['purchase_type'])
            insert_id = m.insert(sql)
            c = pymysql.escape_string(cc)
            print(insert_id,'***')
            if insert_id != None:
                m.insert("INSERT INTO ztbRawInfoContent (raw_data_id,content) VALUES (%s,'%s')"%(insert_id,c))
        except Exception as e:
            print(e,'-----')

if __name__ == '__main__':
    os.system('scrapy crawl mh')











