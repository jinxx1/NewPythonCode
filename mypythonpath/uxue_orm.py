import pprint

from sqlalchemy.dialects import mysql
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Integer, Float, text
import datetime, pprint
import sqlalchemy
from model import Base
import platform, sys, os, json
from sqlalchemy.orm import sessionmaker
from redisBloomHash import *
import logging

import platform, sys, os, json

mysystem = platform.system()
if mysystem == 'Windows':
    mysqlInfo_json_path = r"D:\PythonCode\mypythonpath\mysqlInfo.json"
    mysql_pool_logPath = r"D:\PythonCode\mypythonpath\crawlLog\mysql_pool\{}_pool_echo.log".format(
        datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S"))
elif mysystem == "Linux":
    mysqlInfo_json_path = "/home/mysqlInfo.json"
    mysql_pool_logPath = "/home/terry/crawlLog/mysql_pool/{}_pool_echo.log".format(
        datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S"))
else:
    raise 'not Windows or Linux'

logging.basicConfig(filename=mysql_pool_logPath)
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

with open(mysqlInfo_json_path, 'r') as ff:
    jsoninfo = json.load(ff)

import threading


class mysql_orm(object):
    _instance_lock = threading.Lock()

    def __init__(self):

        creat_Str = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'
        mysqlJson = jsoninfo['uxuepai_sql']
        conStr = creat_Str.format(USER=mysqlJson['USER'], PASSWORD=mysqlJson['PASSWORD'], HOST=mysqlJson['HOST'],
                                  PORT=mysqlJson['PORT'], DBNAME=mysqlJson['DBNAME'])
        engine = sqlalchemy.create_engine(conStr,
                                          echo_pool=True,
                                          pool_pre_ping=True,
                                          pool_size=200,
                                          echo=False)
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def ztbhubinfo_all_insert(self, llist):
        info_all = []
        for i in llist:
            ZtbHubInfo1 = ZtbHubInfo()
            ZtbHubInfo1.create_time = datetime.datetime.now()
            ZtbHubInfo1.update_time = datetime.datetime.now()
            ZtbHubInfo1.craw_status = 0
            ZtbHubInfo1.page_url = i['page_url']

            ZtbHubInfo1.site = i['site']
            ZtbHubInfo1.title = i['title']
            ZtbHubInfo1.craw_id = i['site']

            try:
                ZtbHubInfo1.purchase_type = i['purchase_type']
            except:
                pass

            try:
                ZtbHubInfo1.issue_time = i['issus_time']
            except:
                ZtbHubInfo1.issue_time = i['issue_time']

            try:
                ZtbHubInfo1.province_name = i['province_name']
            except:
                pass

            try:
                ZtbHubInfo1.subclass = i['subclass']
            except:
                pass
            try:
                ZtbHubInfo1.city_name = i['city_name']
            except:
                pass

            try:
                ZtbHubInfo1.business_type = i['business_type']
            except:
                pass

            try:
                ZtbHubInfo1.ztb_ztbInfoType_tenderType = i['ztb_ztbInfoType_tenderType']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfoType_infoType = i['ztb_ztbInfoType_infoType']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfoType_sourceType = i['ztb_ztbInfoType_sourceType']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfo_qualification = i['ztb_ztbInfo_qualification']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfo_registerMoney = i['ztb_ztbInfo_registerMoney']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfo_resultsAmount = i['ztb_ztbInfo_resultsAmount']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfo_buyTenderStartTime = i['ztb_ztbInfo_buyTenderStartTime']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfo_buyTenderEndTime = i['ztb_ztbInfo_buyTenderEndTime']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfo_bidDate = i['ztb_ztbInfo_bidDate']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfo_network = i['ztb_ztbInfo_network']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_project_tenderer = i['ztb_project_tenderer']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_project_agent = i['ztb_project_agent']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_project_candidate = i['ztb_project_candidate']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_ztbInfo_qualification_raw = i['ztb_ztbInfo_qualification_raw']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_project_period_raw = i['ztb_project_period_raw']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_project_startTime_raw = i['ztb_project_startTime_raw']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_project_PersonInChargeRequirement = i['ztb_project_PersonInChargeRequirement']
            except:
                pass
            try:
                ZtbHubInfo1.ztb_project_ProjectTeamRequirements = i['ztb_project_ProjectTeamRequirements']
            except:
                pass
            try:
                ZtbHubInfo1.project_amount = i['project_amount']
            except:
                pass
            try:
                ZtbHubInfo1.str1 = i['str1']
            except:
                pass
            try:
                ZtbHubInfo1.str2 = i['str2']
            except:
                pass
            try:
                ZtbHubInfo1.int1 = i['int1']
            except:
                pass
            try:
                ZtbHubInfo1.int2 = i['int2']
            except:
                pass
            try:
                ZtbHubInfo1.json1 = i['json1']
            except:
                pass
            info_all.append(ZtbHubInfo1)

        # try:
        self.session.add_all(info_all)
        self.session.commit()
        for i in llist:
            if not bh.exists(i['page_url']):
                bh.insert(i['page_url'])
        return 'insert all sucess'

    def ztbhubinfo_insert(self, item):
        i = item

        ZtbHubInfo1 = ZtbHubInfo()
        ZtbHubInfo1.create_time = datetime.datetime.now()
        ZtbHubInfo1.update_time = datetime.datetime.now()
        ZtbHubInfo1.craw_status = 0
        ZtbHubInfo1.page_url = i['page_url']

        ZtbHubInfo1.site = i['site']
        ZtbHubInfo1.title = i['title']
        ZtbHubInfo1.craw_id = i['site']

        try:
            ZtbHubInfo1.purchase_type = i['purchase_type']
        except:
            pass

        try:
            ZtbHubInfo1.issue_time = i['issus_time']
        except:
            ZtbHubInfo1.issue_time = i['issue_time']

        try:
            ZtbHubInfo1.province_name = i['province_name']
        except:
            pass

        try:
            ZtbHubInfo1.subclass = i['subclass']
        except:
            pass
        try:
            ZtbHubInfo1.city_name = i['city_name']
        except:
            pass

        try:
            ZtbHubInfo1.business_type = i['business_type']
        except:
            pass

        try:
            ZtbHubInfo1.ztb_ztbInfoType_tenderType = i['ztb_ztbInfoType_tenderType']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfoType_infoType = i['ztb_ztbInfoType_infoType']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfoType_sourceType = i['ztb_ztbInfoType_sourceType']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfo_qualification = i['ztb_ztbInfo_qualification']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfo_registerMoney = i['ztb_ztbInfo_registerMoney']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfo_resultsAmount = i['ztb_ztbInfo_resultsAmount']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfo_buyTenderStartTime = i['ztb_ztbInfo_buyTenderStartTime']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfo_buyTenderEndTime = i['ztb_ztbInfo_buyTenderEndTime']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfo_bidDate = i['ztb_ztbInfo_bidDate']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfo_network = i['ztb_ztbInfo_network']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_project_tenderer = i['ztb_project_tenderer']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_project_agent = i['ztb_project_agent']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_project_candidate = i['ztb_project_candidate']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_ztbInfo_qualification_raw = i['ztb_ztbInfo_qualification_raw']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_project_period_raw = i['ztb_project_period_raw']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_project_startTime_raw = i['ztb_project_startTime_raw']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_project_PersonInChargeRequirement = i['ztb_project_PersonInChargeRequirement']
        except:
            pass
        try:
            ZtbHubInfo1.ztb_project_ProjectTeamRequirements = i['ztb_project_ProjectTeamRequirements']
        except:
            pass
        try:
            ZtbHubInfo1.project_amount = i['project_amount']
        except:
            pass
        try:
            ZtbHubInfo1.str1 = i['str1']
        except:
            pass
        try:
            ZtbHubInfo1.str2 = i['str2']
        except:
            pass
        try:
            ZtbHubInfo1.int1 = i['int1']
        except:
            pass
        try:
            ZtbHubInfo1.int2 = i['int2']
        except:
            pass
        try:
            ZtbHubInfo1.json1 = i['json1']
        except:
            pass

        try:
            self.session.add(ZtbHubInfo1)
            self.session.commit()
            if not bh.exists(ZtbHubInfo1.page_url):
                bh.insert(ZtbHubInfo1.page_url)
            return ZtbHubInfo1.id
        except Exception as fhub:
            self.session.rollback()
            return fhub

    def get_ztbhubinfo(self, site):
        a = self.session.query(ZtbHubInfo).filter(ZtbHubInfo.site == site).filter(ZtbHubInfo.craw_status == 0).order_by(
            ZtbHubInfo.issue_time.desc()).limit(10)
        return a

    def update_ztbHubInfo(self, update_dict, hubInfo_id):

        try:
            self.session.query(ZtbHubInfo).filter(ZtbHubInfo.id == hubInfo_id).update(update_dict)
            self.session.commit()
            return True
        except Exception as fff:
            print(fff)
            self.session.rollback()
            return None

    def insertInfo(self, articleInfo, hubid):
        # 录入ztbRawInfo
        ztb_RawInfo = ZtbRawInfo()
        ztb_RawInfo.issue_time = articleInfo['issue_time']
        ztb_RawInfo.subclass = articleInfo['subclass']
        ztb_RawInfo.page_url = articleInfo['page_url']
        ztb_RawInfo.title = articleInfo['title']
        ztb_RawInfo.craw_status = 1
        ztb_RawInfo.site = articleInfo['site']
        ztb_RawInfo.creation_time = articleInfo['create_time']
        ztb_RawInfo.process_status = 0
        try:
            self.session.add(ztb_RawInfo)
            self.session.commit()
            bl.insert(ztb_RawInfo.page_url)

        except Exception as frawinfo:
            self.session.rollback()
            if '链接唯一索引' in str(frawinfo):
                bl.insert(ztb_RawInfo.page_url)
                self.update_ztbHubInfo(update_dict={"craw_status": 1},
                                       hubInfo_id=hubid)
                return '链接唯一索引'
            else:
                self.update_ztbHubInfo(update_dict={"craw_status": 2, 'str2': f"RawInfo 录入失败:{frawinfo}"[:254]},
                                       hubInfo_id=hubid)
                return frawinfo
        print('ztbRawInfo sucess id:', ztb_RawInfo.id)

        # 录入ztbRawInfoContent
        ztb_RawContent = ZtbRawInfoContent()
        ztb_RawContent.content = articleInfo['content']
        ztb_RawContent.raw_data_id = ztb_RawInfo.id
        try:
            self.session.add(ztb_RawContent)
            self.session.commit()
        except Exception as fcontent:
            self.session.rollback()
            print('ERROR ztbRawInfoContent')
            self.session.query(ZtbRawInfo).filter(ZtbRawInfo.id == ztb_RawInfo.id).update({"craw_status": 2})
            self.session.commit()
            self.update_ztbHubInfo(update_dict={"craw_status": 2, 'str2': f"Content 录入失败:{fcontent}"[:254]},
                                   hubInfo_id=hubid)
            return None
        print('ztbRawInfoContent sucess id:', ztb_RawContent.id)
        # 录入ZtbInfoAttaChment
        if 'attchments' in articleInfo.keys():
            for i in articleInfo['attchments']:
                ztb_InfoAttaChment = ZtbInfoAttaChment()
                ztb_InfoAttaChment.raw_id = ztb_RawInfo.id
                ztb_InfoAttaChment.download_url = i['download_url']
                ztb_InfoAttaChment.name = i['download_filename']
                try:
                    self.session.add(ztb_InfoAttaChment)
                    self.session.commit()
                except Exception as ff:
                    self.session.rollback()
                print('ztbInfoAttaChment insert sucess id:', ztb_InfoAttaChment.id)

        # 录入ZtbInfoAttaChment
        ztb_tags = self.ztb_Attached_add_single(info=articleInfo, rawid=ztb_RawInfo.id)

        self.update_ztbHubInfo(update_dict={"craw_status": 1},
                               hubInfo_id=hubid)
        return ztb_RawInfo.id

    def ztbRawInfo_add_single(self, hubInfo, articleInfo):
        ztb_RawInfo = ZtbRawInfo()
        if not articleInfo['issue_time']:
            ztb_RawInfo.issue_time = hubInfo.issue_time
        else:
            ztb_RawInfo.issue_time = articleInfo['issue_time']
        ztb_RawInfo.subclass = hubInfo.subclass
        ztb_RawInfo.content = articleInfo['content']
        ztb_RawInfo.page_url = articleInfo['page_url']
        ztb_RawInfo.title = articleInfo['title']
        ztb_RawInfo.craw_status = 1
        ztb_RawInfo.site = hubInfo.site
        ztb_RawInfo.creation_time = datetime.datetime.now()
        ztb_RawInfo.process_status = 0
        try:
            self.session.add(ztb_RawInfo)
            self.session.commit()
            self.update_ztbHubInfo(update_dict={"craw_status": 1}, hubInfo_id=hubInfo.id)
            print('ztbRawInfo insert sucess.  id:', ztb_RawInfo.id)
            bl.insert(ztb_RawInfo.page_url)
            return ztb_RawInfo.id
        except Exception as ff:
            self.session.rollback()
            if '链接唯一索引' in str(ff):
                print('唯一', hubInfo.id)
                bl.insert(ztb_RawInfo.page_url)
                if ztb_RawInfo.site != "b2b.10086.cn":
                    self.update_ztbHubInfo(update_dict={"craw_status": 1}, hubInfo_id=hubInfo.id)
                return 1
            else:
                print('ERROR ztbRawInfo')
                if ztb_RawInfo.site != "b2b.10086.cn":
                    self.update_ztbHubInfo(update_dict={"craw_status": 2}, hubInfo_id=hubInfo.id)
                return 2

    def ztbRawInfoContent_add_single(self, content, rawid):
        ztb_RawContent = ZtbRawInfoContent()
        ztb_RawContent.content = content
        ztb_RawContent.raw_data_id = rawid
        try:
            self.session.add(ztb_RawContent)
            self.session.commit()
            print('ztbRawInfoContent insert sucess')
            return ztb_RawContent.id
        except Exception as ff:
            self.session.rollback()
            self.session.query(ZtbRawInfo).filter(ZtbRawInfo.id == rawid).update({"craw_status": 2})
            self.session.commit()
            return 2

    def ztbInfoAttaChment_add_single(self, info, rawid):
        for i in info:
            ztb_InfoAttaChment = ZtbInfoAttaChment()
            ztb_InfoAttaChment.raw_id = rawid
            ztb_InfoAttaChment.download_url = i['download_url']
            ztb_InfoAttaChment.name = i['download_filename']
            try:
                self.session.add(ztb_InfoAttaChment)
                self.session.commit()
                print('ztbInfoAttaChment insert sucess')
                return 'sucess'
            except Exception as ff:
                self.session.rollback()
                print('ERROR ztbInfoAttaChment')
                print(ff)

    def ztb_Attached_add_single(self, info, rawid):

        keysNameList_1 = '''ztb:ztbInfoType:tenderType
ztb:ztbInfoType:infoType
ztb:ztbInfoType:sourceType
ztb:ztbInfo:qualification
ztb:ztbInfo:registerMoney
ztb:ztbInfo:resultsAmount
ztb:ztbInfo:buyTenderStartTime
ztb:ztbInfo:buyTenderEndTime
ztb:ztbInfo:bidDate
ztb:ztbInfo:serviceType
ztb:ztbInfo:network
ztb:project:tenderer
ztb:project:agent
ztb:project:candidate
ztb:ztbInfo:qualification:raw
ztb:project:period:raw
ztb:project:startTime:raw
ztb:project:PersonInChargeRequirement
ztb:project:ProjectTeamRequirements'''.split('\n')
        keysNameList_2 = '''province_name
city_name
purchase_type
project_amount
business_type'''.split('\n')

        attachList = []

        for key_1 in keysNameList_1:

            if key_1.replace(':', '-') in info.keys():
                if not info[key_1]:
                    continue
                attach = Ztb_Raw_Info_Attached()
                attach.raw_info_id = rawid
                attach.created = datetime.datetime.now()
                attach.tag_key = key_1
                attach.tag_value = info[key_1.replace(':', '-')]
                attachList.append(attach)

        for key_2 in keysNameList_2:

            if key_2 in info.keys():
                if not info[key_2]:
                    continue
                attach = Ztb_Raw_Info_Attached()
                attach.raw_info_id = rawid
                attach.created = datetime.datetime.now()
                attach.tag_key = key_2
                attach.tag_value = info[key_2]
                attachList.append(attach)

        if attachList:
            try:
                self.session.add_all(attachList)
                self.session.commit()
                print('ztb_Attached_tag insert sucess')
                return True
            except Exception as ff:
                self.session.rollback()
                print('ERROR Attached_tag')
                print(ff)
                return False

    def __new__(cls, *args, **kwargs):
        if not hasattr(mysql_orm, "_instance"):
            with mysql_orm._instance_lock:
                if not hasattr(mysql_orm, "_instance"):
                    mysql_orm._instance = object.__new__(cls)
        return mysql_orm._instance

    def __sessionClose__(self):
        self.session.close()


class ZtbHubInfo(Base):
    # 表的名字:
    __tablename__ = 'ztbhubinfo'
    # 表的结构:
    id = Column(mysql.INTEGER(display_width=30), primary_key=True, autoincrement=True, comment='自增主ID')
    page_url = Column(mysql.VARCHAR(length=255), nullable=False, comment='链接地址')
    site = Column(mysql.VARCHAR(length=100), nullable=False, comment='网站域名')
    title = Column(mysql.VARCHAR(length=100), nullable=False, comment='标题')
    issue_time = Column(mysql.DATETIME, nullable=False, comment='发布时间')
    craw_id = Column(mysql.VARCHAR(length=100), nullable=False, comment='爬虫规则编号')
    province_name = Column(mysql.VARCHAR(length=20), nullable=False, comment='省名称')
    subclass = Column(mysql.VARCHAR(length=255), nullable=False, comment='子类型')

    city_name = Column(mysql.VARCHAR(length=20), comment='市名称')
    craw_status = Column(mysql.TINYINT(display_width=1), default=0, comment='爬取状态：默认为0，未曾抓取。1为抓取成功，2为抓取失败')
    ztb_ztbInfoType_tenderType = Column(mysql.VARCHAR(length=20), comment='招标方类型')
    ztb_ztbInfoType_infoType = Column(mysql.VARCHAR(length=20), comment='公告类型')
    ztb_ztbInfoType_sourceType = Column(mysql.VARCHAR(length=20), comment='发标方类型')
    ztb_ztbInfo_qualification = Column(mysql.VARCHAR(length=20), comment='资质要求')
    ztb_ztbInfo_registerMoney = Column(mysql.VARCHAR(length=20), comment='注册资金')
    ztb_ztbInfo_resultsAmount = Column(mysql.VARCHAR(length=20), comment='业绩金额')
    ztb_ztbInfo_buyTenderStartTime = Column(mysql.VARCHAR(length=20), comment='购买标书时间')
    ztb_ztbInfo_buyTenderEndTime = Column(mysql.VARCHAR(length=20), comment='购买标书截止时间')
    ztb_ztbInfo_bidDate = Column(mysql.VARCHAR(length=20), comment='投标时间')
    ztb_ztbInfo_network = Column(mysql.VARCHAR(length=20), comment='网络类型')
    ztb_project_tenderer = Column(mysql.VARCHAR(length=20), comment='招标方')
    ztb_project_agent = Column(mysql.VARCHAR(length=20), comment='代理方')
    ztb_project_candidate = Column(mysql.VARCHAR(length=20), comment='中标候选人')
    ztb_ztbInfo_qualification_raw = Column(mysql.VARCHAR(length=20), comment='资质要求: 原始数据')
    ztb_project_period_raw = Column(mysql.VARCHAR(length=20), comment='项目周期原始数据')
    ztb_project_startTime_raw = Column(mysql.VARCHAR(length=20), comment='项目的开始与结束时间原始数据')
    ztb_project_PersonInChargeRequirement = Column(mysql.VARCHAR(length=20), comment='项目负责人要求')
    ztb_project_ProjectTeamRequirements = Column(mysql.VARCHAR(length=20), comment='项目团队要求')
    project_amount = Column(mysql.VARCHAR(length=20), comment='项目金额')
    str1 = Column(mysql.VARCHAR(length=20), comment='预留str字段1长度20')
    str2 = Column(mysql.VARCHAR(length=20), comment='预留str字段2长度20')
    int1 = Column(mysql.INTEGER(display_width=1), comment='预留int字段1长度1')
    int2 = Column(mysql.INTEGER(display_width=1), comment='预留int字段2长度1')
    json1 = Column(mysql.LONGTEXT, comment='存储json')
    create_time = Column(mysql.TIMESTAMP, )
    update_time = Column(mysql.TIMESTAMP, )
    business_type = Column(mysql.VARCHAR(length=255), comment='业务类型')
    purchase_type = Column(mysql.VARCHAR(length=255), comment='采购类型')

    def __repr__(self):
        returnSTR = '''
(START)  ------- ZtbHubInfo -------  (START)
id\t=\t{id},
page_url\t=\t{page_url},
site\t=\t{site},
title\t=\t{title},
issue_time\t=\t{issue_time},
craw_id\t=\t{craw_id},
subclass\t=\t{subclass},
province_name\t=\t{province_name},
city_name\t=\t{city_name},
craw_status\t=\t{craw_status},
ztb_ztbInfoType_tenderType\t=\t{ztb_ztbInfoType_tenderType},
ztb_ztbInfoType_infoType\t=\t{ztb_ztbInfoType_infoType},
ztb_ztbInfoType_sourceType\t=\t{ztb_ztbInfoType_sourceType},
ztb_ztbInfo_qualification\t=\t{ztb_ztbInfo_qualification},
ztb_ztbInfo_registerMoney\t=\t{ztb_ztbInfo_registerMoney},
ztb_ztbInfo_resultsAmount\t=\t{ztb_ztbInfo_resultsAmount},
ztb_ztbInfo_buyTenderStartTime\t=\t{ztb_ztbInfo_buyTenderStartTime},
ztb_ztbInfo_buyTenderEndTime\t=\t{ztb_ztbInfo_buyTenderEndTime},
ztb_ztbInfo_bidDate\t=\t{ztb_ztbInfo_bidDate},
ztb_ztbInfo_network\t=\t{ztb_ztbInfo_network},
ztb_project_tenderer\t=\t{ztb_project_tenderer},
ztb_project_agent\t=\t{ztb_project_agent},
ztb_project_candidate\t=\t{ztb_project_candidate},
ztb_ztbInfo_qualification_raw\t=\t{ztb_ztbInfo_qualification_raw},
ztb_project_period_raw\t=\t{ztb_project_period_raw},
ztb_project_startTime_raw\t=\t{ztb_project_startTime_raw},
ztb_project_PersonInChargeRequirement\t=\t{ztb_project_PersonInChargeRequirement},
ztb_project_ProjectTeamRequirements\t=\t{ztb_project_ProjectTeamRequirements},
project_amount\t=\t{project_amount},
str1\t=\t{str1},
str2\t=\t{str2},
int1\t=\t{int1},
int2\t=\t{int2},
json1\t=\t{json1},
create_time\t=\t{create_time},
update_time\t=\t{update_time},
business_type\t=\t{business_type} 
purchase_type\t=\t{purchase_type}


(END)  ------- ZtbHubInfo -------  (END)'''
        word = returnSTR.format(
            id=self.id,
            page_url=self.page_url,
            site=self.site,
            title=self.title,
            issue_time=self.issue_time,
            craw_id=self.craw_id,
            subclass=self.subclass,
            province_name=self.province_name,
            city_name=self.city_name,
            craw_status=self.craw_status,
            ztb_ztbInfoType_tenderType=self.ztb_ztbInfoType_tenderType,
            ztb_ztbInfoType_infoType=self.ztb_ztbInfoType_infoType,
            ztb_ztbInfoType_sourceType=self.ztb_ztbInfoType_sourceType,
            ztb_ztbInfo_qualification=self.ztb_ztbInfo_qualification,
            ztb_ztbInfo_registerMoney=self.ztb_ztbInfo_registerMoney,
            ztb_ztbInfo_resultsAmount=self.ztb_ztbInfo_resultsAmount,
            ztb_ztbInfo_buyTenderStartTime=self.ztb_ztbInfo_buyTenderStartTime,
            ztb_ztbInfo_buyTenderEndTime=self.ztb_ztbInfo_buyTenderEndTime,
            ztb_ztbInfo_bidDate=self.ztb_ztbInfo_bidDate,
            ztb_ztbInfo_network=self.ztb_ztbInfo_network,
            ztb_project_tenderer=self.ztb_project_tenderer,
            ztb_project_agent=self.ztb_project_agent,
            ztb_project_candidate=self.ztb_project_candidate,
            ztb_ztbInfo_qualification_raw=self.ztb_ztbInfo_qualification_raw,
            ztb_project_period_raw=self.ztb_project_period_raw,
            ztb_project_startTime_raw=self.ztb_project_startTime_raw,
            ztb_project_PersonInChargeRequirement=self.ztb_project_PersonInChargeRequirement,
            ztb_project_ProjectTeamRequirements=self.ztb_project_ProjectTeamRequirements,
            project_amount=self.project_amount,
            str1=self.str1,
            str2=self.str2,
            int1=self.int1,
            int2=self.int2,
            json1=self.json1,
            create_time=self.create_time,
            update_time=self.update_time,
            purchase_type=self.purchase_type,
            business_type=self.business_type
        )
        return word


class ZtbRawInfo(Base):
    # 表的名字:
    __tablename__ = 'ztbRawInfo'
    # 表的结构:
    id = Column(mysql.INTEGER(display_width=11), primary_key=True, autoincrement=True, comment='自增主ID')
    page_url = Column(mysql.VARCHAR(length=200), nullable=False, comment='链接地址')
    subclass = Column(mysql.VARCHAR(length=255), nullable=False, comment='子类型')
    site = Column(mysql.VARCHAR(length=40), nullable=False, comment='网站域名')
    title = Column(mysql.VARCHAR(length=200), nullable=False, comment='标题')
    issue_time = Column(mysql.DATETIME, nullable=False, comment='发布时间')
    creation_time = Column(mysql.TIMESTAMP, nullable=False, comment='抓取开始时间')

    ztb_type = Column(mysql.INTEGER(display_width=2), comment='公告类型 1为采购公告 2中标结果3,4,5,6,7')
    craw_status = Column(mysql.TINYINT(display_width=1), default=0, comment='爬取状态：默认为0，未曾抓取。1为抓取成功，2为抓取失败')
    process_status = Column(mysql.INTEGER(display_width=2), comment='处理状态：0未处理 1处理中 2处理成功 3处理失败 ')

    end_time = Column(mysql.TIMESTAMP, comment='抓取结束时间')
    modified_time = Column(mysql.TIMESTAMP, comment='修改时间')
    error_record_id = Column(mysql.INTEGER(display_width=11), comment='错误记录表id')

    def __repr__(self):
        returnSTR = '''
 (START)  ------- ZtbRawInfo -------  (START)
id \t= \t{id}
page_url \t= \t{page_url}
subclass \t= \t{subclass}
site \t= \t{site}
title \t= \t{title}
issue_time \t= \t{issue_time}
creation_time \t= \t{creation_time}
ztb_type \t= \t{ztb_type}
craw_status \t= \t{craw_status}
process_status \t= \t{process_status}
end_time \t= \t{end_time}
modified_time \t= \t{modified_time}
error_record_id \t= \t{error_record_id}
(END)  ------- ZtbRawInfo -------  (END)'''
        word = returnSTR.format(
            id=self.id,
            page_url=self.page_url,
            subclass=self.subclass,
            site=self.site,
            title=self.title,
            issue_time=self.issue_time,
            creation_time=self.creation_time,
            ztb_type=self.ztb_type,
            craw_status=self.craw_status,
            process_status=self.process_status,
            end_time=self.end_time,
            modified_time=self.modified_time,
            error_record_id=self.error_record_id,
        )
        return word


class ZtbRawInfoContent(Base):
    # 表的名字:
    __tablename__ = 'ztbRawInfoContent'
    # 表的结构:
    id = Column(mysql.INTEGER(display_width=11), primary_key=True, autoincrement=True, comment='自增主ID')
    raw_data_id = Column(mysql.INTEGER, ForeignKey('ztbRawInfo' + '.id'), comment='ztbRawInfo表id')
    content = Column(mysql.LONGTEXT, nullable=False, comment='公告内容')
    content_ZtbRawInfo = relationship('ZtbRawInfo', backref='content_to_ZtbRawInfo')

    def __repr__(self):
        returnSTR = '''
 (START)  ------- ZtbRawInfoContent -------  (START)
id \t= \t{id}
raw_data_id \t= \t{raw_data_id}
content \t= \t{content}
(END)  ------- ZtbRawInfoContent -------  (END)'''
        word = returnSTR.format(id=self.id, raw_data_id=self.raw_data_id, content=self.content)
        return word


class ZtbInfoAttaChment(Base):
    # 表的名字:
    __tablename__ = 'ztbInfoAttachment'
    # 表的结构:
    id = Column(mysql.INTEGER(display_width=11), primary_key=True, autoincrement=True, comment='自增主ID')
    info_id = Column(mysql.INTEGER(display_width=11), comment='原始数据的id[录入不用管]')
    raw_id = Column(mysql.INTEGER, ForeignKey('ztbRawInfo' + '.id'), comment='ztbRawInfo表id')
    download_url = Column(mysql.VARCHAR(length=500), comment='原始网站的附件下载地址')
    file_name = Column(mysql.VARCHAR(length=500), comment='存储在本地的文件名')
    name = Column(mysql.VARCHAR(length=500), comment='文件对应的名称,如文件名为123.xls,name为广州招标')
    status = Column(mysql.INTEGER(display_width=1), comment='爬取状态：0未下载 1下载成功 2爬取失败')
    temptype = Column(mysql.INTEGER(display_width=1), comment='临时类型')

    AttaChment_ZtbRawInfo = relationship('ZtbRawInfo', backref='AttaChment_to_ZtbRawInfo')

    def __repr__(self):
        returnSTR = '''
(START)  ------- ZtbInfoAttaChment -------  (START)
id\t=\t{id}
info_id\t=\t{info_id}
raw_id\t=\t{raw_id}
download_url\t=\t{download_url}
file_name\t=\t{file_name}
name\t=\t{name}
status\t=\t{status}
temptype\t=\t{temptype}
(END)  ------- ZtbInfoAttaChment -------  (END)'''
        word = returnSTR.format(id=self.id, info_id=self.info_id, raw_id=self.raw_id, download_url=self.download_url,
                                file_name=self.file_name, name=self.name, status=self.status, temptype=self.temptype)
        return word


class Ztb_Raw_Info_Attached(Base):
    # 表的名字:
    __tablename__ = 'ztb_raw_info_attached'
    # 表的结构:
    id = Column(mysql.INTEGER(display_width=11), primary_key=True, autoincrement=True, comment='自增主ID')
    raw_info_id = Column(mysql.INTEGER, ForeignKey('ztbRawInfo' + '.id'), comment='ztbRawInfo表id')
    tag_key = Column(mysql.VARCHAR(length=50), nullable=False, comment='关键字')
    tag_value = Column(mysql.VARCHAR(length=255), nullable=False, comment='值')
    created = Column(mysql.DATETIME, nullable=False, comment='创建时间')
    Raw_Info_Attached_ZtbRawInfo = relationship('ZtbRawInfo', backref='Raw_Info_Attached_to_ZtbRawInfo')

    def __repr__(self):
        returnSTR = '''
(START)  ------- Ztb_Raw_Info_Attached -------  (START)
id\t=\t{id}
raw_info_id\t=\t{raw_info_id}
tag_key\t=\t{tag_key}
tag_value\t=\t{tag_value}
created\t=\t{created}
(END)  ------- Ztb_Raw_Info_Attached -------  (END)'''
        word = returnSTR.format(id=self.id, raw_info_id=self.raw_info_id, tag_key=self.tag_key,
                                tag_value=self.tag_value,
                                created=self.created)
        return word


class ZtbTagU(Base):
    # 表的名字:
    __tablename__ = 'ztbTag'
    # 表的结构:
    id = Column(mysql.INTEGER(display_width=11), primary_key=True, autoincrement=True, comment='自增主ID')
    code = Column(mysql.VARCHAR(length=50), nullable=False, comment='标签code')
    name = Column(mysql.VARCHAR(length=255), nullable=False, comment='标签名称')
    created = Column(mysql.TIMESTAMP, nullable=False, comment='创建时间')

    def __repr__(self):
        returnSTR = '''
(START)  ------- ZtbTag -------  (START)
id\t=\t{id}
code\t=\t{code}
name\t=\t{name}
created\t=\t{created}
(END)  ------- ZtbTag -------  (END)'''
        word = returnSTR.format(id=self.id, code=self.code, name=self.name, created=self.created)
        return word


if __name__ == '__main__':
    mySession = mysql_orm()
    # sitename = "www.ccgp-beijing.gov.cn"
    sitename = "www.ccgp-shaanxi.gov.cn"
    for i in range(0,10000):

        exc = f'''SELECT id FROM ztbRawInfo WHERE site="{sitename}" and craw_status=0 limit 1000'''
        aa = mySession.session.execute(exc)
        status = [{"id": x[0], "craw_status": 1} for x in aa]
        print(len(status))
        if not status:
            break
        mySession.session.bulk_update_mappings(ZtbRawInfo, status)
        mySession.session.commit()
        print('----------------sucess',)

    exit()
    print(aa)
    for i in aa:
        print(i)
        idnum = i[0]
        eexc = '''UPDATE ztbRawInfo SET craw_status=1 where id={}'''.format(idnum)
        mySession.session.execute(eexc)
        mySession.session.commit()

    exit()
    br = True
    while br:
        a = mySession.session.query(ZtbRawInfo.id).filter(
            ZtbRawInfo.site == "www.ccgp-beijing.gov.cn" and ZtbRawInfo.craw_status == 0)[:1000]
        totla = len(a)
        if totla == 0:
            br = False
            continue
        status = [{"id": x[0], "craw_status": 1} for x in a]
        mySession.session.bulk_update_mappings(ZtbRawInfo, status)
    exit()

    print(a)
    exit()
    print(totla)
    status = [{"id": x[0], "craw_status": 1} for x in a]
    mySession.session.bulk_update_mappings(ZtbRawInfo, status)
    exit()
    for i in a:
        # print(i)

        mySession.session.query(ZtbRawInfo).filter(ZtbRawInfo.id == i[0]).update({"craw_status": 1})
        mySession.session.commit()
        print('共{}篇，id:{}'.format(totla, i))
    # print(len(a))
