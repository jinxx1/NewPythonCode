#!/usr/bin/env python
# -*- coding:utf-8 -*-
import bs4
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re
import sys
import json
import reutils
import keysutils
import nerutils
import datetime
import os
import db2mongo
import logging
import ciutils

logging.basicConfig(filename='logger_ztb2.log', level=logging.INFO)

def printobjs(objs):
    if len(objs) > 0:
        # print(objs)
        pass

#db.guangxi_insertoArticleInfo.find({title:/广西科联招标中心专用仪器设备采购/})

str_biao1 = "([\(（]?第*[1234567890一二三四五六七八九十]{1,2}标[段包]*.*?[\)）]?)"
str_biao2 = "([\(（]?[标包][段包]*[1234567890一二三四五六七八九十:：]{1,}.*?[\)）]?)"
#str_biao3 = "(包[1234567890一二三四五六七八九十]{1,})"
str_biao4 = "(中选候选人公示|中标候选人公示|成交结果公告|中选人公示|竞争性谈判公告|公开比选采购公告|单一来源采购信息公告|单一来源采购公示|比选资格预审公告|招标终止公告|成交候选人公示|比选失败公示|采购结果公示|比选结果公告|单一来源公示|中标结果公告|中选结果公示中|中标结果公示|中选结果公示)"
str_biao5 = "(中标公告|中标结果|采购公示|采购公告|询价结果|资格预审|报价公告|结果公示|结果公告|招标公告|招商公告|失败公告|比选公告|询价公告|中标公示|变更公告|竞标公告)"
keywords2 = ["中标","中选","采购","询价","报价","竞标","比选","招商","中 标","采 购","候选人","中选人","结果","变更","失败","中止","取消","成交","招标","单一来源","采购信息","竞争性","谈判","资格预审","终止","评选","及"]
keywords3 = ["中标","中选","采购","询价","报价","竞标","比选","招商","中 标","采 购","候选人","中选人","结果","变更","失败","中止","取消","成交","招标","单一来源","采购信息","竞争性","谈判","资格预审","终止","评选","及"]
#keywords3 = ["变更","失败","中止","取消","成交","招标"]
keywords1 = ["公告","公示","结果","公 告","公 示"]
keywords = ["成交供应商","入围供应商","定向谈判","候选供应商","评标","流选","成交人","选定","撤销","废标","比选)","比选）","集中招标","说明","澄清","暂停","变更)","变更）","【","推荐","重新","招标）","招标)","预审","（","(","公示)","公告）","入围",'招募',"（更正公告）","（变更公告）","中标人","评审","-采购项目","公开","公告","公示","结果","公 告","公 示","中标","中选","采购","询价","报价","竞标","比选","招商","中 标","采 购","候选人","中选人","结果","变更","更正","流标","失败","中止","取消","成交","招标","单一来源","采购信息","竞争性","谈判","资格预审","终止","评选","转","及","的","_","-","—","\t","(1)","(2)","(3)","(4)","（2）","（3）","（4）"]#"（第二次）","（第三次）","（第四次）","（二次）","（三次）","（四次）","(第二次)","(第三次)","(第四次)","(二次)","(三次)","(四次)","第二次","第三次","第四次","二次","三次","四次"]
keywords4 = ["两次","（第二次）","（第三次）","（第四次）","（二次）","（三次）","（四次）","(第二次)","(第三次)","(第四次)","(二次)","(三次)","(四次)","第二次","第三次","第四次","二次","三次","四次"]
kks = ["（重）","重开","（重新比选）","（重新采购）","重新","（重新公示）","（重新谈判）","（重新招标）","【重新招标】","（重新招募）","（重新）"]
keywords5 = ["1","2","3","4"]
keywords5e = ["段1","段2","段3","段4","包1","包2","包3","包4","项1","项2","项3","项4"]
keywords5P = ['段','包','项']
kks2 = ["项目招募","认证认证","认证项目认证","项目项目"]
kks3 = ["项目-认证","认证-认证"]

#str6 = "(成交|中选候选人|中标候选人|中选人|中标人|单一来源|候选人|采购结果|比选结果|中标结果|中选结果|中标公告|中标结果|结果公示|中标公示|结果公告|中选公示|中选公告|入围供应商)"
str6 = "(成交|中选|中标|单一来源|结果|入围供应商|候选)"
str7 = "流选|流标|失败|中止|取消|终止|废标|暂停|撤销|撤回"
KEYWORDS = ['招标','比选','单一来源']
KEYWORDS_RW = ['招募','入围','认证','单一']
str_type1 = "(中选候选人公示|中选候选人公告|中标候选人公示|中标候选人公告|成交结果公告|成交结果公示|成交人公示|成交人公告|中标人公示|中标人公告|中选人公示|中选人公告|单一来源采购信息公告|单一来源采购公示|单一来源采购公告|成交候选人公示|成交候选人公告|采购结果公示|采购结果公告|比选结果公告|比选结果公示|单一来源公示|单一来源公告|中标结果公告|中选结果公告|中标结果公示|中选结果公示|询价结果公示|询价结果公告|单一来源)"
str_typem1 = "(流标|失败|中止|取消|终止|废标|暂停|撤销|撤回)(公示|公告)"

#except:国标16A三孔/每个标包16人
#except:最多允许中标一个标段
str_p1 = "(([一二三四五六七八九]?[十一二三四五六七八九]{1,})([采比]?[购选]?[标包][段包]*))(.{0,50}?)(\d{1,12}\.?\d{0,6}?\s*?[元万亿])"
str_p2 = "(([A-Z123456789][0123456789]?)([采比]?[购选]?[标包][段包]*))(.{0,50}?)(\d{1,12}\.?\d{0,6}?\s*?[元万亿])"
str_p3 = "[^个国](([采比]?[购选]?[标包][段包]*)([一二三四五六七八九]?[十一二三四五六七八九]{1,2}))[^个](.{0,50}?)(\d{1,12}\.?\d{0,6}?\s*?[元万亿])"
str_p4 = "[^个国](([采比]?[购选]?[标包][段包]*)([A-Z123456789][0123456789]?))[^个](.{0,100}?)(\d{1,12}\.?\d{0,6}?\s*?[元万亿])"

str_k1 = "划分为?\d{1,2}个标[段包]"
str_k2 = "划分为?[两一二三四五六七八九十]个标[段包]"

str_x1 = "(([一二三四五六七八九]?[十一二三四五六七八九]{1,})([采比]?[购选]?[标包][段包]*)) (.{0,50}?)(\d{1,12}\.?\d{0,6}) "
str_x2 = "([A-Z123456789一二三四五六七八九]{1,}[采比]?[购选]?[标包][段包]*) (.*?)(\d{1,12}\.?\d{0,6}?) "
str_x3 = "[^个国](([采比]?[购选]?[标包][段包]*)([一二三四五六七八九]?十[一二三四五六七八九]?)) (.{0,50}?)(\d{1,12}\.?\d{0,6}?) "
str_x4 = "[^个国](([采比]?[购选]?[标包][段包]*)([A-Z123456789][0123456789])) (.{0,50}?)(\d{1,12}\.?\d{0,6}?) "

str_t1 = "(获取时间|售卖时间|比选文件|参加比选|参加应答|招标文件|询价文件|报名时间).{0,20}?(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2}).{0,16}?(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2})"
str_t2 = "(截止时间|响应文件|应答文件)\D{0,10}?(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2})"
str_t1a = "(关闭时间|获取时间|售卖时间|比选文件|招标文件|询价文件|报名时间|参加比选|参加应答).{0,50}?(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2})"
str_t3 = "(\D{0,10}?)(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2})\D{1,5}\d{1,2}\D{1,5}\d{1,2}\D{0,3}?[至到—]\D{0,3}(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2})"
str_t4 = "(\D{0,10}?)(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2})\D{1,5}\d{1,2}\D{0,3}?[至到—]\D{0,3}(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2})"
str_t5 = "(\D{0,10}?)(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2})\D{0,3}?[至到—]\D{0,3}(\d{4}\D{1,5}\d{1,2}\D{1,5}\d{1,2})"
str_tg = "采购文件|比选文件|招标文件|询价文件|报名|售卖|购买"
str_tg2 = "递交|响应文件|应答文件"

#str_b1 = "(第([123456789一二三四五六七八九])名?(中标|成交|中选|入围)?候?选?人?[:：\s](.{1,50}?)[\s,， ])"
#str_b2 = "((中标|成交|中选|签约|入围|合格)(人|厂家|公司|候选人|供应商).{0,6}?如下?[是为:：\s]\s*(.{1,}?)[\s,， ])"
#str_b3 = "(采购供应商[:：\s](.{1,}?)[\s,， ])"
str_b1 = "(第([123456789一二三四五六七八九])名?(中标|成交|中选|入围)?候?选?人?[:：\s](.{1,100}?)[\n。])"
str_b1a = "(第([123456789一二三四五六七八九])名?(中标|成交|中选|入围)?候?选?人?[:：\s](.{1,100}?)[\s,， ])"
str_b1b = "(第([123456789一二三四五六七八九])名?(中标|成交|中选|入围)?候?选?人?[:：\s](.{1,}))"
str_b2 = "((中标|成交|中选|签约|入围|合格)(人|厂家|公司|候选人|供应商).{0,6}?如下?[是为:：\s]\s*(.{1,}?)\n)"
str_b3 = "(采购供应商[:：\s](.{1,}?)\n)"
str_b2a = "((中标|成交|中选|签约|入围|合格|通过|通过审查)的?(人|厂家|公司|候选人|供应商|申请人).{0,6}?如下?[是为:：\s]\s*(.{1,}))"
str_b3a = "(采购供应商[:：\s](.{1,}))"


KEYWORDS_YJ=['业绩','注册资金','注册资本','供货金额','同类','单价','条件','具有','满足','合作','招标文件费用','采购文件','每套售价','招标文件','比选文件','累计','单项合同']
ZT_NUMBER = ['500元','400元','300元','200元','100元']

#pa = "(采\S?购\S?人|招\S?标\S?人|招\S?募\S?人|发布单位|比\S?选\S?人|招\S?商\S?人)(.{0,50}公司)"
pa = "(采\S?购|招\S?标|招\S?募|发布|比\S?选|招\S?商)\S?(人|机\S?构|单\S?位|公\S?司)名?称?[^/](.{0,50}公司)"
pb = "(代\S?理|商务支撑)(机\S?构|单\S?位|公\S?司)名?称?[^/](.{0,20}公司)"
pd = "(采购人|招标人|招募人|发布单位|比选人).{0,6}/.{0,6}代理(机构|单位|公司)名?称?[:；：](.{0,50}公司)"
pe = "(采购人|招标人|招募人|发布单位|比选人).{0,6}/.{0,6}代理(机构|单位|公司)名?称?[:：：](.*公司)[ /；、]{1,3}(.{0,50}公司)"

KEYWORDS_GQ = ['工期要求','供货期','交货期','计划工期','服务期限','开展期限','交货时间','总工期','施工工期','工期','建设进度','合作期限','项目周期']
KEYWORDS_FN = '(标段|标包|规模|划分|分配)'

KEYWORDS_TYPE = ['入围','拍卖','竞价','比选','竞争性磋商','竞争性谈判','单一来源','询价','邀请招标','招标']
KEYWORDS_TYPE0 = ['招募','入围','认证']

str_c1 = "中[标选]?候?选?人?[:：\s为是](.{1,50}?)[\s,，。 ]"


BLACK_LIST = ['比选','机构','中国','省公司','诚E招','比选人公司','招标代理公司','联合体','新禾联','国务院','纪委','一建']
REX_LIST = '(.高职$|.*建安$|.{2,4}部$|.*委员会$|.*评委会$|.*组委会$|.*代理机构$|.*办公室$|.*小组$|.*监察室$|.*招标网$|.*采购网$|.*失败$)'
OTHER_LIST = "([\w]+(\.[\w]+)*@[\w]+(\.[\w]+)+)"

def nerfilter(text,ner_type):
    # BLACK_LIST = ['比选', '机构', '中国', '省公司', '诚E招', '比选人公司', '招标代理公司', '联合体', '新禾联', '国务院', '纪委', '一建']
    # REX_LIST = '(.高职$|.*建安$|.{2,4}部$|.*委员会$|.*评委会$|.*组委会$|.*代理机构$|.*办公室$|.*小组$|.*监察室$|.*招标网$|.*采购网$|.*失败$)'
    # OTHER_LIST = "([\w]+(\.[\w]+)*@[\w]+(\.[\w]+)+)"

    if text is None or len(text) == 1:
        return False
    if text in BLACK_LIST:
        return False
    if ner_type == 'LOC':
        return False
    m1 = re.findall(REX_LIST, text)
    if len(m1) > 0:
        return False
    m1 = re.findall(OTHER_LIST, text)
    if len(m1) > 0:
        return False
    return True

def process_party(text):
    first_party = None
    broker = None
    tmp_party = None
    m5 = re.findall(pe, text)
    if len(m5) > 0:
        # print("m5:%s"%m5)
        first_party = m5[0][2]
        broker = m5[0][3]

    m4 = re.findall(pd, text)
    if len(m4) > 0:
        # print("m4:%s"%m4)
        tmp_party = m4[0][2]

    if first_party is None:
        m2 = re.findall(pa, text)
        if len(m2) > 0:
            # print("m2:%s"%m2)
            tmpc = m2[0][2]
            ner = nerutils.getner(tmpc)
            if len(ner) > 0 and ner[0]['ner_type'] == 'ORG':
               first_party = ner[0]['org']

    if broker is None:
        m3 = re.findall(pb, text)
        if len(m3) > 0:
            # print("m3:%s"%m3)
            tmpc = m3[0][2]
            ner = nerutils.getner(tmpc)
            if len(ner) > 0 and ner[0]['ner_type'] == 'ORG':
               broker = ner[0]['org']

    if tmp_party is not None and first_party is None:
        first_party = tmp_party
    return first_party,broker

def checkinfo(objs):
    print("checkinfo")
    if objs is None or len(objs) == 0:
        return False
    counts = 0
    for obj in objs:
        if 'mshares' in obj.keys() and len(obj['mshares']) > 0:
            counts += 1
    print(len(objs),counts)
    return (counts > 0)

def checkcandidate(objs):
    print("checkcandidate")
    ret = False
    for obj in objs:
        if 'candidate' in obj.keys():
            ret = True
            break
    return ret

TEXT_F1 = ["入围名单公示如下","中标结果如下","招募结果如下","谈判结果如下","招标结果如下","评审结果如下","评标结果如下","比选结果如下","中选人推荐如下","中标人推荐如下","采购供应商","供应商公示如下","中标人公示如下","中选人公示如下","中标候选人推荐如下","中选候选人推荐如下","中选人信息","中标人信息","招标结果如下","比选结果如下","中选候选人公示如下","中标候选人公示如下","中选人情况如下","中标人情况如下","中标候选人如下","中选候选人如下"]
TEXT_F1REX = "(((招募|谈判|招标|评审|评标|比选)结果如下)|(中标候选人及项目负责人信息|采购供应商)|((中选|中标|成交|签约|入围)?(单位|中选人|中标人|供应商|候选人)(结果|公示|推荐|情况|信息|名单){0,}?.{0,6}?(如下|：)))"
TEXT_F2 = ["单一来源采购的原因","单一来源采购原因","单一来源采购论证情况","成交候选人项目负责人","中标候选人项目负责人","中选候选人项目负责人","评审信息","公示时间","公示媒介","公示媒体","公示期","联系方式"]
TEXT_F2a = ["代理机构人员姓名：","代理机构：","采购代理：","比选代理：","采购人：","招标代理：","招标人：","比选人：","招 标 人","采 购 人","比 选 人","招标人名称：","采购人名称：","比选人名称："]
TEXT_F3 = ["中标候选人项目负责人","中选候选人项目负责人","成交候选人项目负责人"]
TEXT_F4 = ["评审信息","公示时间","公示媒介","公示媒体","公示的媒介","公示的媒体","公示期","公示日期","联系方式","监督部门"]
TEXT_F22 = TEXT_F2a
TEXT_F22.extend(TEXT_F4)
def textfilter(text, title = None, prj_name = None):
    # print(title, prj_name)
    p1 = 0
    p2 = len(text)
    if title is not None:
        ppos = text.find(title)
        if ppos >= 0 and ppos > p1:
            # print(ppos, title)
            p1 = ppos + len(title)
    if prj_name is not None:
        ppos = text.find(prj_name)
        if ppos >= 0 and ppos > p1:
            # print(ppos, prj_name)
            p1 = ppos + len(prj_name)
    for key in TEXT_F1:
        ppos = text.find(key)
        if ppos >= 0 and ppos > p1:
            # print(ppos, key)
            p1 = ppos
    if p1 == 0:
        m1 = re.findall(TEXT_F1REX, text)
        # print("F1REX:%s" % m1)
        if len(m1) > 0:
            key = m1[0][0]
            ppos = text.find(key)
            if ppos >= 0 and ppos > p1:
                # print(ppos, key)
                p1 = ppos
    for key in TEXT_F2:
        ppos = text.find(key)
        if ppos > p1 and ppos < p2:
            # print(ppos, key)
            p2 = ppos
    for key in TEXT_F22:
        ppos = text.find(key)
        if ppos > p1 and ppos < p2:
            # print(ppos, key)
            p2 = ppos
    return text[p1:p2], p2

def textfilter2(text):
    p1 = 0
    p2 = len(text)
    for key in TEXT_F3:
        ppos = text.find(key)
        if ppos >= 0:
            p1 = ppos
            break
    for key in TEXT_F4:
        ppos = text.find(key)
        if ppos >= 0:
            p2 = ppos
            break
    return text[p1:p2]

def textfiltero(text):
    ppos = text.find("项目负责人")
    if ppos < 0:
        ppos = text.find("采购代理")
    if ppos >= 0:
        text = text[0:ppos]
    return text

def process_bid(text):
    #Terry add this to remove the duplicate bid info
    #text,kpos = textfilter(text)
    # print(text)
    ret = []
    m1 = re.findall(str_b1b, text)
    i = 3
    """
    m1 = re.findall(str_b1, text)
    if len(m1) == 0:
        m1 = re.findall(str_b1a, text)
        i = 3
    if len(m1) == 0:
        m1 = re.findall(str_b2, text)
        i = 3 
    if len(m1) == 0:
        m1 = re.findall(str_b3, text)
        i = 1
    """
    if len(m1) == 0:
        m1 = re.findall(str_b2a, text)
        i = 3
    if len(m1) == 0:
        m1 = re.findall(str_b3a, text)
        i = 1
    # print(m1)
    ii = 0
    for m in m1:
        v = nerutils.getner(m[i])
        if len(v) < 1:
            ii += 1
            continue
        obj = v[0]
        if 'candidate' not in obj.keys():
            obj['candidate'] = obj['org']
        ret.append(obj)
        newtext = ''
        if ii < len(m1) - 1:
            mm = m1[ii+1]
            ppos = text.find(mm[0])
            if ppos >= 0:
                newtext = text[:ppos]
        else:
            mm = m
            ppos = text.find(mm[0])
            if ppos >= 0:
                newtext = text[ppos:]
        if newtext != '':
            mm1 = reutils.process_discount(newtext)
            mm2 = reutils.process_rmb(newtext)
            mm3 = reutils.process_share(newtext)
            # print(mm1,mm2,mm3)
            if mm1 is not None:
                if mm1[0] == '下浮':
                    obj['discount'] = 1 - mm1[1]
                else:
                    obj['discount'] = mm1[1]
                    # print(obj)
            if mm2 is not None:
                bflag, otext = budgetfilter(newtext, mm2[0][1])
                if not bflag:
                    obj['budget'] = keysutils.process_rmb(mm2[0][1])
            if mm3 is not None:
                obj['share'] = mm3[0][1]
        ii += 1
        """
        obj = {}
        obj['order'] = jsonutils.seq_order(m[1])
        if len(v) > 0:
            if 'candidate' in v[0].keys():
              obj['candidate'] = v[0]['candidate'] 
            elif 'org' in v[0].keys():
              obj['candidate'] = v[0]['org']
        print("xxxxxx:%s" % v)
        ret.append(obj)
        """
    return ret

from dateutil import parser
str_ann = '(公示期|公示时间)'
def process_datetime2(text):
    p_startdate = None
    p_enddate = None
    datetype = ''
    m3 = re.findall(str_t3, text)
    m4 = re.findall(str_t4, text)
    m5 = re.findall(str_t5, text)
    if len(m3) > 0:
        # print(m3)
        pos = len(m3) - 1
        datetype = m3[pos][0]
        p_startdate = m3[pos][1]
        p_enddate = m3[pos][2]
    if len(m4) > 0:
        # print(m4)
        pos = len(m4) - 1
        datetype = m4[pos][0]
        p_startdate = m4[pos][1]
        p_enddate = m4[pos][2]
    if len(m5) > 0:
        # print(m5)
        pos = len(m5) - 1
        datetype = m5[pos][0]
        p_startdate = m5[pos][1]
        p_enddate = m5[pos][2]
    if p_startdate is not None:
        p_startdate = p_startdate.replace('年','-').replace('月','-').replace(' ','').replace('\n','').replace('\t','').replace('\xa0','').replace('_','').replace('【','').replace('】','').replace('[','').replace(']','')
    if p_enddate is not None:
        p_enddate = p_enddate.replace('年','-').replace('月','-').replace(' ','').replace('\n','').replace('\t','').replace('\xa0','').replace('【','').replace('】','').replace('[','').replace(']','')
    m0 =  re.findall(str_ann, datetype)
    if len(m0) == 0:
        return p_startdate,p_enddate
    else:
        return p_startdate,p_enddate
    #TODO

def process_datetime(text):
    #print(text)
    p_startdate = None
    p_enddate = None
    t_enddate = None
    #dt = parser.parse(text)
    m1 = re.findall(str_t1, text)
    m2 = re.findall(str_t2, text)
    # print(m1)
    if len(m1) > 0:
       p_startdate = m1[0][1].replace('年','-').replace('月','-').replace(' ','').replace('\n','').replace('\t','')
       p_enddate = m1[0][2].replace('年','-').replace('月','-').replace(' ','').replace('\n','').replace('\t','')
    else:
       m1a = re.findall(str_t1a, text)
       # print(m1a)
       if len(m1a) > 0:
          p_enddate = m1a[0][1].replace('年','-').replace('月','-').replace(' ','').replace('\n','').replace('\t','')
    # print(m2)
    if len(m2) > 0:
       pos = len(m2) - 1
       t_enddate = m2[pos][1].replace('年','-').replace('月','-').replace(' ','').replace('\n','').replace('\t','')
    if p_enddate is None:
       p_startdate, p_enddate = process_datetime2(text)
    return p_startdate, p_enddate, t_enddate

#str_m1 = "(预算|规模|限价)\D{0,20}?(\d{1,12}[元万亿])"

def checkduan(duan):
            if len(re.findall('注册资金|注册资本|业绩|单价',duan)) > 0:
                # print(duan)
                return False
            if len(duan) >= 1:
                #承包二级
                if duan[0] == '级':
                    return False
            if len(duan) >= 2:
                #标包划分
                if duan[0:2] == '划分':
                   return False
            return True

#每个标包16人，3辆车
def checkbiao(text,biao):
    pos = text.find(biao)
    if pos > 0:
        if text[pos - 1] == '标':
            return False
    return True

def process_biaoduan(text,str_p4,str_p3,str_p2,str_p1):
    #print("process_biaoduan")
    #print(text)
    objs = []
    m3 = re.findall(str_p4, text)
    if len(m3) == 0:
        m3 = re.findall(str_p3, text)
    m1 = re.findall(str_p1, text)
    if len(m1) == 0:
        m1 = re.findall(str_p2, text)
    if len(m1) > 0 or len(m3) > 0:
        if len(m1) > 0:
          # print(m1)
          for tt in m1:
            # print(tt)
            if len(tt) < 4:
                continue
            if tt[3] in ZT_NUMBER:
                continue
            biao,btype,border,duan,qian = tt[0],tt[2],tt[1],tt[3],tt[4]
            if not checkduan(duan):
                continue
            if not checkbiao(text,biao):
                continue
            obj = {}
            obj['package'] = biao
            obj['package_type'] = btype
            obj['order'] = border
            obj['budget'] = qian
            objs.append(obj)
        if len(m3) > 0 and len(m1) != len(m3):
          for tt in m3:
            # print(tt)
            if len(tt) < 4:
                continue
            if tt[3] in ZT_NUMBER:
                continue
            biao,btype,border,duan,qian = tt[0],tt[1],tt[2],tt[3],tt[4]
            if not checkduan(duan):
                continue
            if not checkbiao(text,biao):
                continue
            obj = {}
            obj['package'] = biao
            obj['package_type'] = btype
            obj['order'] = border
            obj['budget'] = qian
            objs.append(obj)
        for i in range(len(objs)):
            obj = objs[i]
            newtext = None
            bpos = 0
            epos = 0
            if i == len(objs) - 1:
                bpos = text.find(obj['package'])
                if bpos >= 0:
                    bpos += len(obj['package'])
                    bpos = text[bpos:].find(obj['budget'])
                    if bpos >= 0:
                        bpos += len(obj['budget'])
                    newtext = text[bpos:]
                epos = bpos
            else:
                newobj = objs[i+1]
                bpos = text.find(obj['budget'])
                epos = text.find(newobj['package'])
                #pos += len(newobj['package'])
                #pos = text[pos:].find(obj['budget'])
                newtext = text[bpos:epos]
            if newtext:
                subobjs = jsonutils.process_fener(newtext)
                obj['mshares'] = subobjs
                """
                if len(subobjs) > 1:
                    obj['mshares'] = subobjs
                elif len(subobjs) == 1:
                    obj['share'] = subobjs[0]['share']
                """
                text = text[epos:]
    objs = jsonutils.process_json(objs)
    return objs

def find_top_pkg(newobjs, obj):
    for o in newobjs:
        if o['package'] == obj['package']:
            return True,o
    return False,obj

def process_package_level(objs):
    newobjs = []
    lastobj = None
    level = 0
    for obj in objs:
        if lastobj is None:
            lastobj = obj
            lastobj['objs'] = []
            objp = lastobj
            newobjs.append(lastobj)
            continue

        if lastobj['package_type'] != obj['package_type']:
          ret,oobj = find_top_pkg(newobjs,obj)
          if ret:
            objp = oobj
            #lastobj = objp
            #continue

          if level == 0:
            level = 1
          else:
            level = 0
          if jsonutils.seq_order(obj['order']) == 1:
            # print(objp)
            objp['objs'].append(obj)
            lastobj = obj
          elif level == 1:
            # print(objp)
            newobj = {}
            newobj['package_type'] = obj['package_type']
            newobj['budget'] = lastobj['budget']
            newobj['order'] = str(jsonutils.seq_order(obj['order']) - 1)
            #objp['budget'] = None
            objp['objs'].append(newobj)
            objp['objs'].append(obj)
            if lastobj != objp:
                newobjs.remove(lastobj)
            else:
                objp['budget'] = None
            lastobj = obj
          else:
            objp = obj
            objp['objs'] = []
            lastobj = objp
            newobjs.append(objp)
            level = 0
        elif level == 1:
          lastobj = obj
          objp['objs'].append(obj)
        else:
          lastobj = obj
          newobjs.append(obj)
    for o in newobjs:
        if 'order' in o.keys():
            o['order'] = jsonutils.seq_order(o['order'])
        if 'objs' in o.keys():
          for oo in o['objs']:
            if 'order' in oo.keys():
                oo['order'] = jsonutils.seq_order(oo['order'])

    #newobjs = jsonutils.postprocess_json(newobjs)
    return newobjs

from keysutils import keymap,getkey
import jsonutils

def process_biao(text):
    """
    p1 = re.findall(str4, text)
    if len(p1) == 0:
        p1 = re.findall(str5, text)

    if len(p1) > 0:
        ret = text.find(p1[0])
        name = text[0:ret]
        if name.endswith('_') or name.endswith('-') or name.endswith('(') or name.endswith('（'):
            ret -= 1
        text = text[0:ret]
    """
    #for i in range(8):
    haskeywords = True
    while haskeywords:
      haskeywords = False
      for keyword in keywords:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)].strip()
            haskeywords = True
      for keyword in kks:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)].strip()
            haskeywords = True
    """
    for keyword in keywords1:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)]
            #break
    text = text.strip()
    for keyword in keywords2:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)]
            #break
    text = text.strip()
    for keyword in keywords3:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)]
            #break
    """
    if text.endswith('_') or text.endswith('-') or text.endswith('(') or text.endswith('（'):
        text = text[0:len(text) - 1]
    return text

REX_KEYS = ['[',']','(',')','*','+','?','.','^','$','{','}','|']
def rex(text):
    #text = text.replace('[','\[').replace(']','\]').replace('(','\(').replace(')','\)').replace('*','\*').replace('?','\?').replace("'","\'").replace('"','\"').replace('+','\+')
    text = text.replace('\\', '\\\\')
    for key in REX_KEYS:
        newkey = '\\' + key
        text = text.replace(key, newkey)
    return text

PLACE_HOLDERS = ['PLACE_HOLDER_A','PLACE_HOLDER_B']
BEGIN_CHAR = ['“','[','【','《']
END_CHAR = ['”',']','】','》']

def process_biao0(text, ks45 = False):
    m1 = re.findall('（招标编号：.*?）$', text)
    if len(m1) > 0 and text.endswith(m1[0]):
        pos = text.find(m1[0])
        text = text[0:pos]
    haskeywords = True
    hasplaceholder = True
    placeholders = []
    while hasplaceholder:
      hasplaceholder = False
      for key in PLACE_HOLDERS:
        if text.endswith(key):
          text = text[0:len(text) - len(key)]
          hasplaceholder = True
          placeholders.append(key)
    while haskeywords:
      haskeywords = False
      for keyword in keywords:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)].strip()
            haskeywords = True
      """
      if ks45:
        for keyword in keywords4:
          if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)].strip()
            haskeywords = True
      """
      for keyword in kks:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)].strip()
            haskeywords = True
      text2 = text
      cc = 0
      if ks45:
        for keyword in keywords5:
          if text2.endswith(keyword) and text2[len(text2) - 2:len(text2) - 1] not in keywords5P:
            text2 = text2[0:len(text) - len(keyword)].strip()
            cc += 1
      if cc == 1:
          text = text[0:len(text) - 1]
      if text.endswith('-'):
          text = text[0:len(text) - 1]
      for key in kks2:
          if text.endswith(key):
              text = text[0:len(text) - 2]
      for key in kks3:
          if text.endswith(key):
              text = text[0:len(text) - 3]
    ichar = 0
    for char in BEGIN_CHAR:
        if text.startswith(char):
            text = text[1:]
        nchar = END_CHAR[ichar]
        if text.endswith(nchar):
            text = text[:len(text) - 1]
        ichar += 1
    """
    for char in END_CHAR:
        if text.endswith(char):
            text = text[:len(text) - 1]
    """
    for i in range(len(placeholders)):
        key = placeholders[len(placeholders) - 1 - i]
        text += key
    return text,placeholders

def process_biao1(text):
    keywords = ["成交供应商", "入围供应商", "定向谈判", "候选供应商", "评标", "流选", "成交人", "选定", "撤销", "废标", "比选)", "比选）", "集中招标", "说明",
                "澄清", "暂停", "变更)", "变更）", "【", "推荐", "重新", "招标）", "招标)", "预审", "（", "(", "公示)", "公告）", "入围", '招募',
                "（更正公告）", "（变更公告）", "中标人", "评审", "-采购项目", "公开", "公告", "公示", "结果", "公 告", "公 示", "中标", "中选", "采购", "询价",
                "报价", "竞标", "比选", "招商", "中 标", "采 购", "候选人", "中选人", "结果", "变更", "更正", "流标", "失败", "中止", "取消", "成交",
                "招标", "单一来源", "采购信息", "竞争性", "谈判", "资格预审", "终止", "评选", "转", "及", "的", "_", "-", "—", "\t", "(1)", "(2)",
                "(3)", "(4)", "（2）", "（3）",
                "（4）"]  # "（第二次）","（第三次）","（第四次）","（二次）","（三次）","（四次）","(第二次)","(第三次)","(第四次)","(二次)","(三次)","(四次)","第二次","第三次","第四次","二次","三次","四次"]
    kks = ["（重）", "重开", "（重新比选）", "（重新采购）", "重新", "（重新公示）", "（重新谈判）", "（重新招标）", "【重新招标】", "（重新招募）", "（重新）"]
    keywords5P = ['段', '包', '项']
    keywords5 = ["1", "2", "3", "4"]

    haskeywords = True

    # text == xxxxx项1 （重新采购）资格预审。经过以下循环后，会输出成   text == xxxx项1
    while haskeywords:
      haskeywords = False
      for keyword in keywords:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)].strip()
            haskeywords = True
      for keyword in kks:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)].strip()
            haskeywords = True


    # text == xxxx项1
    if True:
      text2 = text
      cc = 0
      for keyword in keywords5:
          # 如果text2最后一个字符是["1", "2", "3", "4"]，并且倒数第二个字符不是 ['段', '包', '项']
          if text2.endswith(keyword) and text2[len(text2) - 2:len(text2) - 1] not in keywords5P:
              # 删掉最后一个字符
            text2 = text2[0:len(text) - len(keyword)].strip()
            cc += 1

      if cc == 1:
          text = text[0:len(text) - 1]
      if text.endswith('-'):
          text = text[0:len(text) - 1]
    return text

def process_biaoex(text, userex = True, biaoflag = True, seqflag = True):


    # str_biao1 = "([\(（]?第*[1234567890一二三四五六七八九十]{1,2}标[段包]*.*?[\)）]?)"
    str_biao1 = "([\(（]?第*[1234567890一二三四五六七八九十]{1,2}批[段包]*.*?[\)）]?)"
    str_biao2 = "([\(（]?[标包][段包]*[1234567890一二三四五六七八九十:：]{1,}.*?[\)）]?)"
    keywords4 = ["两次", "（第二次）", "（第三次）", "（第四次）", "（二次）", "（三次）", "（四次）", "(第二次)", "(第三次)", "(第四次)", "(二次)", "(三次)",
                 "(四次)", "第二次", "第三次", "第四次", "二次", "三次", "四次"]

    biao = ''
    seq = ''
    text = process_biao1(text)
    # print('text',text)
    # text = '南方电网公司2012年一级物资集中招标第四批（二次设备类12-5-4批）项目'
    if True:
      p1 = re.findall(str_biao1, text)
      # print('p1', p1)

      if len(p1) == 0:
        p1 = re.findall(str_biao2, text)

      # if len(p1) == 0:
      #    p1 = re.findall(str_biao3, text)
      #


      if len(p1) > 0:
        biao = p1[0]
        text = text.replace(biao,'PLACE_HOLDER_B')
        # print('text',text)
    if True:
        for keyword in keywords4:
          if text.find(keyword) >= 0:
            seq = keyword
            text = text.replace(keyword, 'PLACE_HOLDER_A')
    # print('text',text)


    title,placeholders = process_biao0(text, True)
    # print('title',title)
    # print('placehlders',placeholders)

    if userex:
      title = rex(title)
      if biaoflag and 'PLACE_HOLDER_B' in placeholders:
          title = title.replace('PLACE_HOLDER_B',".*?" + rex(biao))
      else:
          title = title.replace('PLACE_HOLDER_B',rex(biao))
      if seqflag and 'PLACE_HOLDER_A' in placeholders:
          title = title.replace('PLACE_HOLDER_A',".*?" + rex(seq))
      else:
          title = title.replace('PLACE_HOLDER_A',rex(seq))
    else:
      if biaoflag:
        title = title.replace('PLACE_HOLDER_B',biao)
      else:
        title = title.replace('PLACE_HOLDER_B','')
      if seqflag:
        title = title.replace('PLACE_HOLDER_A',seq)
      else:
        title = title.replace('PLACE_HOLDER_A','')
    return title

def process_biao2(text):
    p1 = re.findall(str_biao1, text)
    if len(p1) == 0:
        p1 = re.findall(str_biao2, text)
    #if len(p1) == 0:
    #    p1 = re.findall(str_biao3, text)
    if len(p1) == 0:
        p1 = re.findall(str_biao4, text)
    if len(p1) == 0:
        p1 = re.findall(str_biao5, text)

    if len(p1) > 0:
        ret = text.find(p1[0])
        name = text[0:ret]
        if name.endswith('_') or name.endswith('-') or name.endswith('(') or name.endswith('（'):
            ret -= 1
        text = text[0:ret]

    #for i in range(8):
    haskeywords = True
    while haskeywords:
      haskeywords = False
      for keyword in keywords:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)].strip()
            haskeywords = True
      for keyword in kks:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)].strip()
            haskeywords = True
    """
    for keyword in keywords1:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)]
            #break
    text = text.strip()
    for keyword in keywords2:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)]
            #break 
    text = text.strip()
    for keyword in keywords3:
        if text.endswith(keyword):
            text = text[0:len(text) - len(keyword)]
            #break
    """
    if text.endswith('_') or text.endswith('-') or text.endswith('(') or text.endswith('（'):
        text = text[0:len(text) - 1]
    return text

IMPORTANT_KEYS = ['标段','标包','子项','包段','采购包','选包']
def checkheader(keys):
    ret = True
    for key in keys:
        for kk in IMPORTANT_KEYS:
          if key.find(kk) >= 0:
            ret = True
            break
    return ret

def makeduplicate(obj,key,counts = 0):
    if 'duplicate' not in obj.keys():
        obj['duplicate'] = ""
    obj['duplicate'] = obj['duplicate'] + key + "."
    if 'duplicate_counts' not in obj.keys():
        obj['duplicate_counts'] = ''
    obj['duplicate_counts'] += str(counts) + "."

def rtablefilter(table,alltext):
    name = None
    text = table.text
    pos = alltext.find(text)
    if pos >= 0:
        allsentences = alltext[:pos]
        sentences = allsentences.split('\n')
        cc = len(sentences)
        while cc >0:
            tt = sentences[cc-1].strip()
            cc -= 1
            if tt != '':
                name = tt
                break
    trs = table.findAll('tr')
    num = len(trs)
    cc = ciutils.ratetext(text, num - 1)
    # print("r table rate:%f" % cc)
    logging.info("%s r table rate:%f" % (name,cc))
    if cc < 0.15 or num < 3:
        return False,name
    else:
        return True,name

def getint(str1):
    ret = 0
    try:
        ret = int(str1)
    except Exception as e:
        print(e)
    return ret

def process_table(table,alltext,prj_type = '0'):
    trs = None
    rtable, tablename = rtablefilter(table,alltext)
    if rtable and prj_type == '1':
      logging.info("not a good table:%s" % tablename)
      logging.debug(table.text)
      objs = reutils.process_biaoinfo(table.text)
      if len(objs) > 0:
        return objs,None,tablename
      return None,None,tablename
    """
    thead = table.find("thead")
    print(thead)
    if thead:
        trs = thead.findAll("tr")
    else:
        trs = table.findAll("tr")
    print(table.children)
    for cc in table.children:
        print(cc)
        print(type(cc))
        if type(cc) is not bs4.element.Tag:
            continue
        for ccc in cc.children:
            print(ccc)
    """
    trs = table.findAll("tr")
    rows = 0
    keys = []
    objs = []
    mkeys = [0] * 512
    mvalues = [''] * 512
    all_rowspan = 0
    rowspan_in_th = False
    skip_first_row = 0
    for tr in trs:
        #print(tr)
        #skip_first_row = False
        if tr.text == '':
            print("wrong tr, skip")
            continue
        if rows == 0:
            ths = tr.findAll('th')
            if len(ths) <= 0:
                print('no th')
                ths = tr.findAll('td')
            if len(ths) < 1:
                print("wrong ths")
                return None,None,tablename
            elif len(ths) <= 1:
                print("wrong header")
                #if len(ths[0].text) >= 100:
                #    print("not a good table")
                #    return None, None
                #skip the first row if it is not a true header
                continue
            elif len(ths) < 2:
                print("wrong table")
                return None,None,tablename
            thc = 0
            tmp_rows = 0
            hasrowspan = False
            for th in ths:
                thc += 1
                text = th.text.strip()
                text = text.replace("\xa0 ","")
                text = text.replace("\xa0","")
                text = text.replace("\n","")
                text = text.replace("\r","")
                if len(text) == 0:
                    print("wrong key:empty")
                    continue
                if len(text) >= 50:
                    # print("wrong key! return!:%s"%text)
                    print("wrong key! return!:text--980")
                    return None,None,tablename
                #terry comment out to skip colspan in header
                if hasrowspan and 'colspan' in th.attrs.keys() and getint(th['colspan']) > 1:
                    for i in range(getint(th['colspan'])):
                        keys.append(text+"--")
                    print("found rowspan and colspan in header")
                    tmp_rows += getint(th['colspan'])
                elif 'rowspan' in th.attrs.keys():
                    hasrowspan = True
                    if getint(th['rowspan']) > 2:
                      if len(text) >= 30:
                        # print("key too long:%s" % text)
                        print("key too long:---993")
                        continue
                    else:
                      keys.append(text)
                elif 'colspan' in th.attrs.keys() and getint(th['colspan']) > 1:
                    for i in range(getint(th['colspan'])):
                        keys.append(text+str(i))
                    print("found colspan in header")
                else:
                    if skip_first_row > 0:
                      for i in range(len(keys)):
                        key = keys[i]
                        if key.endswith("--"):
                            keys[i] = "S--" + key + text
                            skip_first_row -= 1
                            break
                    else:
                      keys.append(text)
                if 'rowspan' in th.attrs.keys():
                    rowspan_in_th = True
            skip_first_row += tmp_rows
            #keys = keymap(keys)
        #elif rows == 1 and rowspan_in_th:
        #    pass
        else:
            tds = tr.findAll("td")
            obj= {}
            j = 0
            found_rowspan = False
            for td in tds:
                text = td.text.strip()
                text = text.replace("\n","")
                text = text.replace("\r","")
                if len(text) >= 50 and 'colspan' in td.attrs.keys():
                    # print("wrong value! return!:%s"%text)
                    print("wrong value! return!:---1028" )
                    break
                if 'colspan' in td.attrs.keys() and getint(td['colspan']) > 1:
                    tdrs = td['colspan']
                    cols = getint(tdrs)
                    toadd = 0
                    for i in range(cols):
                        if j+i >= len(keys):
                            print("wrong colspan:%d expected len:%d" % (cols,len(keys)))

                            break
                        obj[keys[j+i]] = text
                        toadd += 1
                    j += toadd
                    continue

                for k in range(j,len(keys)):
                    # print('C',k,mkeys[k])
                    if mkeys[k] != 0 and k <= j:
                        #print(mkeys[k], mvalues[k])
                        mkeys[k] -= 1
                        if mkeys[k] == 0:
                            all_rowspan -= 1
                        obj[keys[k]] = mvalues[k]
                        j += 1
                        """
                        if 'duplicate' not in obj.keys():
                            obj['duplicate'] = ""
                        obj['duplicate'] = obj['duplicate'] + getkey(keys[k]) + "."
                        """
                        makeduplicate(obj, keys[k])
                    else:
                        break

                if 'rowspan' in td.attrs.keys():
                    tdrs = td['rowspan']
                    jj = j
                    #TODO need checking the comment out
                    """
                    if j == 0:
                        jj += all_rowspan
                        j += 1
                    else:
                        j += 1
                    """
                    while mkeys[jj] > 0:
                        jj += 1
                    # print(jj,text,j,all_rowspan)
                    mkeys[jj] = getint(tdrs) - 1
                    mvalues[jj] = text
                    if jj >= len(keys):
                        print("error key index:%d"%jj)
                        continue
                    obj[keys[jj]] = text
                    all_rowspan += 1
                    found_rowspan = True
                    if True:
                        makeduplicate(obj, keys[jj], getint(tdrs))
                    j += 1
                    continue
                else:
                  found_rowspan = False
                  # print('b',j,text)
                  if j >= len(keys):
                      # print(mkeys,all_rowspan)
                      print("b error key index:%d"%j)
                      continue
                  obj[keys[j]] = text
                j += 1
            if not found_rowspan:
                for k in range(j,len(keys)):
                    # print('c',k,mkeys[k])
                    if mkeys[k] != 0:
                        # print(mkeys[k], mvalues[k])
                        mkeys[k] -= 1
                        if mkeys[k] == 0:
                            all_rowspan -= 1
                        obj[keys[k]] = mvalues[k]
                        j += 1
                        makeduplicate(obj,keys[k])
                    else:
                        break
            objs.append(obj)
        if skip_first_row <= 0:
            if not checkheader(keys):
                # print("invalid keys:%s" % keys)
                return None,None,tablename
            rows += 1
    return objs,keys,tablename

#中国移动四川公司2017-2019年通信工程全业务及室分施工二级集中（补充采购）项目_招标公告
def gettypefromtitle(text):
    # str6 = "(成交|中选|中标|单一来源|结果|入围供应商|候选)"
    # str7 = "流选|流标|失败|中止|取消|终止|废标|暂停|撤销|撤回"
    ret = '0'
    m1 = re.findall(str6, text)
    if len(m1) > 0:
        ret = '1'
    m1 = re.findall(str7, text)
    if len(m1) > 0:
        ret = '-1'
    return ret

def gettypefromcontent(text):
    ret = '0'
    if len(text) > 200:
        text = text[:200]
    m1 = re.findall(str_type1, text)
    if len(m1) > 0:
        ret = '1'
    m1 = re.findall(str_typem1, text)
    if len(m1) > 0:
        ret = '-1'
    return ret

def getline(text, pos):
    text1 = text[0:pos]
    text2 = text[pos:]
    pos1 = text1.rfind('\n')
    pos2 = text2.find('\n')
    pos1_b = text1.rfind(' ')
    pos2_b = text2.find(' ')
    if pos1_b > pos1:
       pos1 = pos1_b
    if pos2_b < pos2:
       pos2 = pos2_b
    if pos1 < 0:
       pos1 = 0
    if pos2 < 0:
       pos2 = len(text)
    newtext = text1[pos1:] + text2[:pos2]
    return newtext,pos1

def getline2(text, pos):
    text1 = text[0:pos]
    pos1 = text1.rfind('\n')
    pos1_b = text1.rfind(' ')
    pos1_c = text1.rfind('。')
    if pos1_c > pos1 and pos1_c > pos1_b:
       pos1 = pos1_c
    elif pos1_b > pos1:
       pos1 = pos1_b
    if pos1 < 0:
       pos1 = 0
    newtext = text1[pos1:]
    return newtext,pos1

def budgetfilter(plaintext,m):
    # print(plaintext)
    if m in ZT_NUMBER:
        return False, plaintext
    pos = plaintext.find(m)
    if pos >= 0:
        #text,tpos = getline(plaintext, pos)
        text,tpos = getline2(plaintext, pos)
        # print(tpos)
        # print(text)
        for c in KEYWORDS_YJ:
            cpos = text.find(c)
            if cpos >= 0:
                print("************%d" % cpos)
                #return False,plaintext[tpos+len(text):]
                return False,plaintext[pos + len(m):]
        return True,plaintext[pos + len(m):]
    return True,plaintext

def process_misc(plaintext,prj,title=None):
    d1,d2,d3 = process_datetime(plaintext)
    # print(d1,d2,d3)
    budgets = []
    budget = 0
    money = reutils.process_rmb0(plaintext)
    # print(money)
    if money:
        pos = 0
        text = plaintext
        for m in money:
            budgetflag, text = budgetfilter(text, m[1])
            if not budgetflag:
                # print("not a budget flag:%s" % (m[1]))
                continue
            mm = keysutils.unit_convert(m[1])
            # print("budget flag:%s" % mm)
            budgets.append(mm)
            if mm > budget:
                budget = mm

    budget2 = 0
    money = reutils.process_rmb2(plaintext)
    # print(money)
    if money:
        pos = 0
        text = plaintext
        for m in money:
            budgetflag, text = budgetfilter(text, m[1])
            if not budgetflag:
                # print("not a budget2 flag:%s" % (m[1]))
                print("not a budget2 flag:---1223" % (m[1]))
                continue
            mm = keysutils.unit_convert(m[1])
            # print("budget2 flag:%s" % mm)
            if mm not in budgets:
                budgets.append(mm)
            if mm > budget2:
                budget2 = mm
    if budget2 == 0:
        budget2 = budget
    # print(budget, budget2, budgets)
    prj['stype'] = 0

    #if title is not None:
    #    prj['type'] = gettypefromtitle(title)
    prj['reg_start_date'] = d1
    prj['reg_end_date'] = d2
    prj['enroll_date'] = d3
    prj['budget'] = budget
    prj['budget2'] = budget2
    prj['budgets'] = budgets
    for keyword in KEYWORDS_RW:
        if title.find(keyword) >= 0:
            prj['stype'] = 1
            break

def tablefilter(tables):
    ret = []
    for table in tables:
        tt = True
        cc = 0
        kk = 0
        trs = table.findAll("tr")
        for tr in trs:
            tds = tr.findAll("td")
            if len(tds) > 1:
                kk += 1
            if len(tds) <= 1:
               cc += 1
            else:
               cc = 0
            if cc >= 2 and kk < 2:
               tt = False
               break
        if tt:
            ret.append(table)
    return ret

def hastable(html):
    bsObj = BeautifulSoup(html)
    #print(bsObj)
    tables = bsObj.findAll("table")
    print("found tables:%d" % len(tables))
    tables = tablefilter(tables)
    return len(tables) > 0

def checkkeys(keys):
    keycounts = 0
    newkeys = keysutils.keymap(keys)
    for key in newkeys:
        if key in keysutils.keymaps:
            keycounts += 1
    return (keycounts > 1)

def getbudgetsharekeys(keys):
    keycounts = 0
    newkeys = keysutils.keymap(keys)
    for key in newkeys:
        if key in ['budget','share']:
            keycounts += 1
    return keycounts

KEYWORDS_NORMAL = ["包段","产品名称","产品单位","需求数量"]
def checknormal(keys):
    counts = 0
    for key in keys:
        if key in KEYWORDS_NORMAL:
            counts += 1
    if counts >= 4:
        return True
    else:
        return False

KEYWORDS_BD = "标包号|标段号|标段|标包|^包$|采购包|比选包|选包|子项"
def checkobj(keys):
    ret = False
    for key in keys:
        m1 = re.findall(KEYWORDS_BD, key)
        if len(m1) > 0:
            ret = True
    return ret

def getbudgetfromtable(objs):
    budget = 0
    mm = 1
    if len(objs) < 1:
        return 0
    keys = objs[0].keys()
    for key in keys:
        if keysutils.getkey(key) == 'budget':
            if key.find('万元') >= 0:
                mm = 10000
            else:
                mm = 1
            budget = keysutils.unit_convert(objs[0][key])
            break
    return budget * mm

def gettablesize(table):
    return len(table.text)

def process_html(html, prj_type = '0', prj = None):
    keys = None
    objs = []
    objs2 = []
    bsObj = None
    try:
        bsObj = BeautifulSoup(html,'lxml')
    except Exception as e:
        print(e)
        return None
    #print(bsObj)

    tables = bsObj.findAll("table")
    print("found tables:%d" % len(tables))
    tables = tablefilter(tables)
    print("processing tables:%d" % len(tables))
    tablesize = 0
    keysize = 0
    for table in tables:
        #print(table)
        ret,ikeys,tablename = process_table(table,bsObj.text,prj_type)
        # print(ret,ikeys,tablename)
        if ret is None or ikeys is None:
            continue
        if not checkkeys(ikeys):
            # print("skip keys:%s" % ikeys)
            budget = getbudgetfromtable(ret)
            # print("budget:%f" % budget)
            if prj is not None and budget > prj['budget2']:
                prj['budget'] = budget
                prj['budget2'] = budget
            continue
        tablesize += gettablesize(table)
        keysize += getbudgetsharekeys(ikeys)
        obj = jsonutils.process_json(ret)
        if len(obj) == 0:
           print("no table objs found")
           continue
        o = obj[0].keys()
        """/TODO
        if 'share' not in o and 'budget' not in o:
            break 
        """
        merge = keysutils.getmerge(ikeys)
        obj = jsonutils.postprocess_json(obj,'package',merge)
        if tablename is not None:
            packages = reutils.getbiaometa(tablename)
            # print("processing package merge:%s %s" % (tablename,packages))
            logging.info("got packages:%s" % packages)
            if not checkobj(ikeys):
              if len(packages) == 2:
                obj = [{'package':packages[0]+packages[1], 'mshares':obj}]
              elif len(packages) == 1:
                obj = [{'package':packages[0], 'mshares':obj}]
        #print(obj)
        isnormal = checknormal(ikeys)
        if isnormal:
          pass
          #objs.append({"keys":ikeys,"objs":obj,'type':'normal'})
        else:
          objs.append({"keys":ikeys,"objs":obj, "tablename":tablename})
    printobjs(objs)
    print("=============")


    text = bsObj.text
    #text = ''
    if len(text) < 50:
      print("text too short")
      ps = bsObj.findAll("p")
      for p in ps:
        text += p.text
      if len(text) < 100:
        ps = bsObj.findAll("span")
        for p in ps:
          if text.find(p.text) < 0:
              text += p.text
      if len(text) < 50:
        sps = bsObj.findAll(["span","p"])
        # print(len(sps))
        for sp in sps:
          stext = ''
          brs = [x for x in sp.contents if getattr(x, 'name', None) != 'br']
          for br in brs:
            stext += str(br) + " "
          text += stext
    otext = text
    if prj_type == '0':
      objs2 = process_biaoduan(text,str_p4,str_p3,str_p2,str_p1)
      printobjs(objs2)
      print("A=============")
      stype = 1
      if objs2 is None or len(objs2) == 0:
          stype = 2
          objs2 = process_biaoduan(text,str_x4,str_x3,str_x2,str_x1)
      objs2 = process_package_level(objs2)
      if len(objs2) > 0:
          objs.append({"keys":None,"type":"package","stype":stype,"objs":objs2})
          return objs,None
    else:
      text,kpos = textfilter(text)
      print('table size:%d, key size:%d' % (tablesize,keysize))
      if (len(text) > 0 and (tablesize * 1.0 / len(text)) > 0.7) or keysize >= 1:
          return objs, None
      # print("%d :%s" % (kpos,text[:100]))
      objs2 = reutils.process_biaoinfo(text)
      printobjs(objs2)
      if not checkinfo(objs2):
          print("false objs")
          if kpos < len(otext):
              text2 = otext[kpos:]
              # print(text2)
              objs2 = reutils.process_biaoinfo(text2)
              checkinfo(objs)
      if len(objs2) > 0:
          objs.append({"keys":None,"type":"package","objs":objs2})
          return objs,None

    sps = bsObj.findAll(["span","p"])
    #print(len(sps))
    for sp in sps:
      try:
        stext = ""
        brs = [x for x in sp.contents if getattr(x, 'name', None) != 'br']
        for br in brs:
            stext += str(br) + " "
        objs2 = process_biaoduan(stext,str_x4,str_x3,str_x2,str_x1)
        if len(objs) > 0:
            break
      except Exception as e:
        print(e)
    #print(objs2)
    if len(objs2) > 0:
        objs.append({"keys":None,"type":"package","stype":3,"objs":objs2})
        return objs,None

    print("C=============")
    objs2 = process_biaoduan(text,str_x4,str_x3,str_x2,str_x1)
    #print(objs2)
    if len(objs2) > 0:
        objs.append({"keys":None,"type":"package","stype":4,"objs":objs2})
        return objs,None

    """
    objs = jsonutils.process_fener(text)
    print(objs)
    if len(objs) > 0:
        mshares = {"mshares":objs}
        return [{"keys":keys,"objs":[mshares]}]
    """
    return objs,objs2

#this func is not imp at all, since it is done  in prjutils
def postprocess_prj(prj):
    if prj['budget'] == 0:
        if 'list' in prj.keys() and len(prj['list']) > 0:
            for item in prj['list']:
                if 'objs' not in item.keys():
                    continue
                for obj in item['objs']:
                    pass

def dump(objs):
    # print(objs)
    for obj in objs:
        #print(obj['keys'])
        for o in obj['objs']:
            if 'package' not in o.keys():
                o['package'] = ''
            if 'package2' not in o.keys():
                o['package2'] = ''
            if 'location' not in o.keys():
                o['location'] = ''
            if 'candidate' not in o.keys():
                o['candidate'] = ''
            if 'candidate2' not in o.keys():
                o['candidate2'] = ''
            if 'budget' not in o.keys():
                o['budget'] = ''
            if 'budget2' not in o.keys():
                o['budget2'] = ''
            tstr1 = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (o['package'],o['package2'],o['budget'],o['budget2'],o['candidate'],o['candidate2'],str(o['share']) if 'share' in o.keys() else "",o['location'])
            # print(tstr1)

def json_default(value):
    if isinstance(value, datetime.datetime):
        #return dict(year=value.year, month=value.month, day=value.day)
        return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return value.__dict__

def dump2json(filename,objs):
    if objs is None or len(objs) == 0:
        return
    print("write to:%s" % filename)

    fp = open(filename, 'w')
    text = json.dumps(objs, default=json_default)
    fp.write(text)
    fp.close()
    # print(text)
    # import pprint
    # pprint.pprint(objs)

def haspackagesorshares(prj):
    if 'list' not in prj.keys():
        return False
    for obj in prj['list']:
        if 'objs' in obj.keys() and obj['objs'] is not None and len(obj['objs']) > 0:
            if 'package' in obj['objs'][0].keys():
                return True
            if ('sequence' in obj['objs'][0].keys() or 'order' in obj['objs'][0].keys()) and 'budget' in obj['objs'][0].keys():
                return True
    return False

MAX_LEN=300
def process_url(url,attachments,html_content=None,title=None,issue_time=None,infoId=None,project_type=None):
    objs = None
    objlist = None
    html = html_content
    from urllib.request import urlopen
    if html_content is None:
        html = urlopen(url)
    bsObj = BeautifulSoup(html,'lxml')
    max_len = MAX_LEN
    plaintext = bsObj.text
    plaintext = plaintext.replace("\xa0", '')
    plaintext = plaintext.replace('\u3000', '')
    epos = plaintext.find('中国移动通信版权所有')
    if epos >= 0:
        plaintext = plaintext[0:epos]

    prj = {}
    prj['first_party'] = None
    prj['broker'] = None

    if title is not None:
        prj['title'] = title
        prj['project_name'] = process_biaoex(title,False,True,True)
        prj['project_group_name'] = process_biaoex(title,False,False,False)
        plaintext = plaintext.replace(prj['project_name'],'')
        if project_type is None:
            prj['type'] = gettypefromtitle(title)
        else:
            prj['type'] = project_type
    else:
        prj['title'] = None
        prj['project_name'] = None

    text_len = len(plaintext)

    prj['issue_time'] = issue_time
    process_misc(plaintext,prj,title)

    prj['first_party'], prj['broker'] = process_party(plaintext)
    prj['shares'] = []
    prj['list'] = []
    prj['attachments'] = attachments
    prj['infoId'] = infoId
    prj['proceed_attachments'] = []

    # print("processing html and attahcments:%d" % len(attachments))
    if True:
      if html_content is None:
          html = urlopen(url)
      objs,objs2 = process_html(html,prj['type'],prj)
      if len(objs) > 0:
          objlist = objs
          prj['list'].extend(objs)
      if objs2 is not None and len(objs2) > 0:
          prj['shares'] = objs2

    if prj['type'] == '0' and not haspackagesorshares(prj):
      # print('processing attachments')
      for attachment in attachments:
        if attachment == '':
            continue
        logging.info("processing attach html:%s" % attachment)
        # print("doing:%s" % attachment)
        prj['proceed_attachments'].append(attachment)
        ahtml = urlopen(attachment)
        objs = process_html(ahtml,prj['type'],prj)
        if objs is None:
            continue
        hasobj = False
        for obj in objs:
            if obj is None:
                continue
            hasobj = True
        if hasobj:
          prj['backuplist'] = prj.pop('list')
          prj['list'] = []
          for obj in objs:
            logging.info(obj)
            if isinstance(obj, list):
                prj['list'].extend(obj)
            else:
                prj['list'].append(obj)


    kobjs = None
    if prj['first_party'] is None or prj['broker'] is None:
      logging.info("process ner party")
      kobjs = nerutils.getner(plaintext)
      for obj in kobjs:
        if obj['type'] == '招标':
            if prj['first_party'] is not None:
              if len(obj['org']) > len(prj['first_party']) and len(prj['first_party']) < 4:
                prj['first_party'] = obj['org']
            else:
              prj['first_party'] = obj['org']
        elif obj['type'] == '代理' and obj['ner_type'] == 'ORG':
            if obj['org'].find('公司') < 0:
                continue
            if prj['broker'] is not None:
              if len(obj['org']) > len(prj['broker']):
                prj['broker'] = obj['org']
            else:
              prj['broker'] = obj['org']
      if prj['first_party'] is None:
        for obj in kobjs:
          if obj['type'] == '' and obj['ner_type'] == 'ORG':
            if prj['first_party'] is None:
              prj['first_party'] = obj['org']
            elif len(obj['org']) > len(prj['first_party']):
              prj['first_party'] = obj['org']

    if prj['type'] == '1':
      otext = plaintext
      if len(prj['shares']) < 1 and (objlist is None or len(objlist) < 1):
        logging.info("process fener")
        print("process fener")
        plaintext,kpos = textfilter(plaintext, prj['title'], prj['project_name'])
        objs = jsonutils.process_fener(plaintext)
        if objs is None or len(objs) <= 1 or not checkcandidate(objs):
            objs = reutils.process_biaoinfo2(plaintext)
            if len(objs) < 1:
                logging.info("process bid")
                print("process bid")
                objs = process_bid(plaintext)
                #scan all the text
                #if len(objs) < 1:
                #    objs = process_bid(otext)
            else:
                for obj in objs:
                  if 'candidate' not in obj.keys():
                    obj['candidate'] = obj['org']
            prj['shares'].extend(objs)
        else:
          prj['shares'].extend(objs)
      if len(prj['shares']) < 1 and (objlist is None or len(objlist) < 1):
          logging.info("process ner bid")
          print("process ner bid")
          #plaintext,kpos = textfilter(plaintext)
          objs = nerutils.getner(plaintext)
          for obj in objs:
            if obj['type'] == '中选' and nerfilter(obj['org'],obj['ner_type']):
              prj['shares'].append(obj)
          if len(prj['shares']) < 1:
            if kobjs is not None:
              for obj in kobjs:
                if obj['type'] == '中选' and nerfilter(obj['org'],obj['ner_type']):
                  prj['shares'].append(obj)
      if len(prj['shares']) < 1 and (objlist is None or len(objlist) < 1):
          print("process ner bid2")
          #scan all the text
          objs = nerutils.getner(otext)
          for obj in objs:
            if obj['type'] == '中选' and nerfilter(obj['org'],obj['ner_type']):
              prj['shares'].append(obj)
    elif prj['type'] == '0':
      if len(prj['shares']) < 1 and (objlist is None or len(objlist) < 1):
        logging.info("process fener")
        objs = jsonutils.process_fener(plaintext)
        prj['shares'].extend(objs)

    return prj

def readjson(filename):
    obj = None
    fp = open(filename, 'r')
    try:
      text = fp.read()
      obj = json.loads(text)
    except Exception as e:
      print(e)
    fp.close()
    return obj

def dumphtml(html, filename):
    fp = open(filename, 'w',encoding='utf-8',errors='ignoer')
    fp.write(html)
    fp.close()

def getpurchasemethod(title):
    ret = '招标'
    for key in KEYWORDS_TYPE0:
        pos = title.find(key)
        if pos >= 0:
            ret = KEYWORDS_TYPE[0]
            return ret
    for key in KEYWORDS_TYPE:
        pos = title.find(key)
        if pos >= 0:
            ret = key
            break
    return ret

LNUM=30
JSON_PATH = "/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/ztb/json/"
HTML_PATH = "/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/ztb/html/"
DATA_PATH = "/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/info/"
def dump_titles(regex_str, rpath, begin_date, mdb = 'ztb', mset = 'ztb', sknum = 0, business_types = ".*"):
  date_time_obj_en = datetime.datetime.strptime(begin_date, '%Y-%m-%d')#(' %H:%M:%S')
  conn = MongoClient('127.0.0.1', 27017)
  db = conn[mdb]
  my_set = db[mset]
  ret = []
  #sknum = 0
  toRun = True
  fp = open(rpath,'w')
  while toRun:
   toRun = False
   records = None
   try:
      records = my_set.find({'$and':[{"publishedDate":{"$gte":date_time_obj_en}, "title" : {"$regex" : regex_str}, "businessType":{"$regex":business_types}}]}).sort([("publishedDate",1)]).limit(LNUM).skip(sknum)
   except Exception as e:
      print(e)
      logging.info("failed at :%d" % sknum)
      sknum += 1
   for obj in records:
    sknum += 1
    toRun = True
    print(obj['title'])
    fp.write(obj['title'])
    fp.write('\n')
  fp.close()

def loadobj(infoId, mdb = 'ztb', mset = 'ztb'):
  ret = None
  conn = MongoClient('127.0.0.1', 27017)
  db = conn[mdb]
  my_set = db[mset]
  records = my_set.find({"infoId": infoId})
  for obj in records:
    ret = obj
    break
  return ret

def loadtext(infoId, mdb = 'ztb', mset = 'ztb'):
  ret = None
  html = None
  obj = loadobj(infoId, mdb, mset)
  if obj is not None:
    html = obj['content']
  if html is not None:
    bsObj = BeautifulSoup(html)
    ret = bsObj.text
  return ret

def process_obj(obj, rpath, obj_type=None, with_attachments=False):
    objs = None
    newtitle = obj['title'].replace("/","-").replace(' ','').replace('\t','')
    if len(newtitle) >= 84:
       tlen = len(newtitle)
       newtitle = newtitle[:77] + newtitle[tlen - 6: tlen]
    filename = rpath + newtitle + ".txt"
    hfilename = rpath + newtitle + ".html"
    if obj is not None:
      html = obj['content']
      #objs = process_html(html)
      if html is None:
        return None
      dumphtml(html,hfilename)
      #attachobjs = db2mongo.getattachments(obj['title'], obj['publishedDate'])
      attachobjs = db2mongo.load_attachments(obj['title'], obj['infoId'])
      attachments = []
      candidates = []
      backup = []
      for attobj in attachobjs:
          logging.debug(attobj.filepath)
          # print(attobj)
          backup.append(attobj.fileurl)
          fnames = attobj.filepath.split('/')
          if len(fnames) > 0:
              # print(fnames)
              keyword = re.findall(KEYWORDS_FN,fnames[len(fnames)-1])
              if len(keyword) == 0:
                  keyword = re.findall(KEYWORDS_FN, attobj.name)
              if len(keyword) > 0:
                  # print(attobj.filepath, attobj.fileurl, attobj.name, attobj.sheetname)
                  logging.info("got attach:%s %s %s" % (attobj.filepath, attobj.fileurl, attobj.sheetname))
                  if attobj.sheetname is not None and len(attobj.sheetname) > 0 and not attobj.sheetname.lower().startswith('sheet'):
                      keyword = re.findall(KEYWORDS_FN,attobj.sheetname)
                      if len(keyword) > 0:
                          # print(attobj.sheetname)
                          logging.info("processing attach:%s" % attobj.sheetname)
                          attachments.append(attobj.fileurl)
                      else:
                          logging.info("skip attach:%s" % attobj.sheetname)
                          #candidates.append(attobj.fileurl)
                  else:
                      attachments.append(attobj.fileurl)
      if len(candidates) == 1 and len(attachments) == 0:
          # print("add attach from candidate:%s" % candidates[0])
          attachments.append(candidates[0])
      if len(attachments) == 0 and len(backup) > 0:
          attachments.extend(backup)
      if len(attachments) == 0 and with_attachments:
          return None
      objs = process_url(None, attachments, html, obj['title'], obj['publishedDate'].strftime("%Y-%m-%d"),obj['infoId'],obj_type)
      objs['business_type'] = obj['businessType']
      objs['minor_business_type'] = obj['minorBusinessType']
      objs['site'] = obj['site']
      objs['guild_id'] = obj['guild_id']
      #objs['url'] = db2mongo.geturl(obj['title'], obj['publishedDate'])
      objs['purchase_method'] = getpurchasemethod(obj['title'])
    return objs

def find_relate_ex(db, mset, title, date_begin, date_end):
  my_set = db[mset]
  records = my_set.find({'$and':[{"publishedDate":{"$gte":date_begin}, "publishedDate":{"$lt":date_end}, "title" : {"$regex" : title}, }]}).sort([("publishedDate",1)])
  return records

def find_relate(mdb, mset, title, publishedDate,seqmode):
  conn = MongoClient('127.0.0.1', 27017)
  db = conn[mdb]
  my_set = db[mset]
  title = process_biaoex(title,True,True,seqmode)
  date_begin = publishedDate + datetime.timedelta(days=-90)
  date_end = publishedDate + datetime.timedelta(days=90)
  return find_relate_ex(db, mset, title, date_begin, date_end)

def filetitle(title):
    newtitle = title.replace("/","-").replace(' ','').replace('\t','')
    if len(newtitle) >= 84:
       tlen = len(newtitle)
       newtitle = newtitle[:77] + newtitle[tlen - 6: tlen]
    return newtitle

def process_mongo(regex_str, rpath, begin_date, mdb = 'ztb', mset = 'ztb', sknum = 0, business_types = ".*",forcemode=False,attachmode=False, seqmode = False):
  # print("rex:%s, path:%s, date:%s, db:%s, set:%s, num:%s" % (regex_str, rpath, begin_date, mdb, mset, sknum))
  #date_time_str_en = '2018-10-01 00:00:00'
  date_time_obj_en = datetime.datetime.strptime(begin_date, '%Y-%m-%d')#(' %H:%M:%S')
  ret = []
  #sknum = 0
  toRun = True
  while toRun:
   toRun = False
   records = None
   try:
      conn = MongoClient('127.0.0.1', 27017)
      db = conn[mdb]
      my_set = db[mset]
      records = my_set.find({'$and':[{"publishedDate":{"$gte":date_time_obj_en}, "title" : {"$regex" : regex_str}, "businessType":{"$regex":business_types}}]}).sort([("publishedDate",1)]).limit(LNUM).skip(sknum)
   except Exception as e:
      print(e)
      logging.info("failed at :%d" % sknum)
      sknum += 1
   todolist = []
   for obj in records:
       todolist.append(obj)
   for obj in todolist:
    sknum += 1
    toRun = True
    # print(obj['title'])
    newtitle = obj['title'].replace("/","-").replace(' ','').replace('\t','')
    if len(newtitle) >= 84:
       tlen = len(newtitle)
       newtitle = newtitle[:77] + newtitle[tlen - 6: tlen]
    filename = rpath + newtitle + ".txt"
    hfilename = rpath + newtitle + ".html"
    """
    if os.path.isfile(filename) and not forcemode:
      print("%s exists" % filename)
      objs = readjson(filename)
      ret.append(objs)
    else:
    """
    if True:
      #objs = process_obj(obj, rpath, None, attachmode)
      subrecords = find_relate(mdb, mset, obj['title'], obj['publishedDate'],seqmode)
      sublist = []
      for subobj in subrecords:
          sublist.append(subobj)
      for subobj in sublist:
          subobjs = process_obj(subobj, rpath, None, attachmode)
          if subobjs is not None:
            filename = rpath + filetitle(subobj['title']) + ".txt"
            if os.path.isfile(filename) and not forcemode:
              # print("%s exists" % filename)
              objs = readjson(filename)
              if objs is not None:
                ret.append(objs)
            else:
              dump2json(filename, subobjs)
              ret.append(subobjs)
      """
      html = obj['content']
      #objs = process_html(html)
      if html is None:
        continue
      dumphtml(html,hfilename)
      #attachobjs = db2mongo.getattachments(obj['title'], obj['publishedDate'])
      attachobjs = db2mongo.load_attachments(obj['title'], obj['infoId'])
      attachments = []
      for attobj in attachobjs:
          logging.debug(attobj.filepath)
          print(attobj)
          fnames = attobj.filepath.split('/')
          if len(fnames) > 0:
              keyword = re.findall(KEYWORDS_FN,fnames[len(fnames)-1])
              if len(keyword) > 0:
                  logging.info("got attach:%s %s %s" % (attobj.filepath, attobj.fileurl, attobj.sheetname))
                  if attobj.sheetname is not None and len(attobj.sheetname) > 0 and not attobj.sheetname.lower().startswith('sheet'):
                      keyword = re.findall(KEYWORDS_FN,attobj.sheetname)
                      if len(keyword) > 0:
                          logging.info("processing attach:%s" % attobj.sheetname)
                          attachments.append(attobj.fileurl)
                      else:
                          logging.info("skip attach:%s" % attobj.sheetname)
                  else:
                      attachments.append(attobj.fileurl) 
      objs = process_url(None, attachments, html, obj['title'], obj['publishedDate'].strftime("%Y-%m-%d"),obj['infoId'])
      objs['business_type'] = obj['businessType']
      objs['minor_business_type'] = obj['minorBusinessType']
      objs['site'] = obj['site']
      objs['guild_id'] = obj['guild_id']
      #objs['url'] = db2mongo.geturl(obj['title'], obj['publishedDate'])
      objs['purchase_method'] = getpurchasemethod(obj['title'])
      #dump(objs)
      """
      #if objs is not None:
      #  print(obj['title'])
      #  print(objs['project_name'])
      #  dump2json(filename,objs)
      #  ret.append(objs)
  return ret

if __name__ == "__main__":
  #regex_str = "广西科联招标中心专用仪器设备采购.*"
  regex_str = ".*"
  filename = "test.json"
  attachments = []
  title = None
  datapath = DATA_PATH
  begin_date = '2000-01-01'
  str3 = 'ztb'
  str4 = 'ztb'
  sknum = 0

  if len(sys.argv) > 1:
    regex_str = sys.argv[1]
  if len(sys.argv) > 2:
    #filename = sys.argv[2]
    attachments = sys.argv[2].split(' ')
    datapath = sys.argv[2]
  if len(sys.argv) > 3:
    title = sys.argv[3]
    begin_date = sys.argv[3]
  if len(sys.argv) > 4:
    str3 = sys.argv[4]
  if len(sys.argv) > 5:
    str4 = sys.argv[5]
  if len(sys.argv) > 6:
    sknum = int(sys.argv[6])
  if regex_str.startswith("http"):
    objs = process_url(regex_str, attachments, title)
    dump2json(filename,objs)
  else:
    objs = process_mongo(regex_str,datapath,begin_date,str3,str4,sknum)
  #print(objs)

def test_mongo(regex_str):
  conn = MongoClient('127.0.0.1', 27017)
  db = conn.ztb
  my_set = db.guangxi_insertoArticleInfo
  for obj in my_set.find({"title" : {"$regex" : regex_str}}):
    html = obj['content']
    bsObj = BeautifulSoup(html)
    #print(bsObj.text)
    #print(obj['title'])
    ret = process_biao(obj['title'])
    #print(ret)
    if len(sys.argv) > 1:
        # print(html)
        # print(bsObj.text)
        # print(obj['issueTime'])
        # print(obj['capturedTime'])
        pass
