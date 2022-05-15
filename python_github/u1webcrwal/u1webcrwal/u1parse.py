# -*- coding: utf-8 -*-
import sqlalchemy
import pprint
import time,datetime
import requests
import json
from PIL import Image
import re,os,sys
import pymysql
import jieba,random
from lxml import html
from bs4 import BeautifulSoup
import lxml.html
etree = lxml.html.etree
import pandas as pd
from urllib import parse
import difflib

from u1webcrwal.settings import MYSQL_DATABASE,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD,MYSQL_HOST



conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQL_USER,
                                                                                           PASSWORD=MYSQL_PASSWORD,
                                                                                           HOST=MYSQL_HOST,
                                                                                           PORT=MYSQL_PORT,
                                                                                           DBNAME=MYSQL_DATABASE)



mysqlcon = sqlalchemy.create_engine(conStr)

def get_catJson():
    get_catKeys = mysqlcon.execute("select id,keysJson,catName from U1LINK_post_cat")
    llist = []
    for i in get_catKeys:
        ddict = {}
        ddict['ID'] = i[0]
        ddict['json'] = json.loads(i[1])
        ddict['catName'] = i[2]
        llist.append(ddict)
    return llist



def printline(word = None):
    if word:
        print('------------------------------{}'.format(str(word)))
    else:
        print('------------------------------{}'.format('-'))

def precessSummary(html):
    soup = BeautifulSoup(html, 'lxml')
    noneSummary = '本文无简介'
    soupList = soup.find_all('p')
    if not soupList:
        soupList = soup.find_all('a')
    if not soupList:
        soupList = soup.find_all('span')
    if not soupList:
        return noneSummary

    allWord = []
    for num,htmlBODY in enumerate(soupList):
        decodeWord = htmlBODY.get_text().replace('\u00A0','').replace('\u0020','').replace('\u3000','').replace('\n','').replace('\t','').replace('\r','')
        if '【'in decodeWord or '作者' in decodeWord or '编辑' in decodeWord or '欢迎关注' in decodeWord or '来源：' in decodeWord or '点击下方' in decodeWord or '文末推荐' in decodeWord or '扫码关注' in decodeWord:
            continue
        elif '】'in decodeWord or '点击上方' in decodeWord or '扫码联系' in decodeWord or '获取更多' in decodeWord or '▽' in decodeWord or '文/' in decodeWord or '原标题' in decodeWord or '今日看点' in decodeWord:
            continue
        elif '一键关注'in decodeWord or '查看更多' in decodeWord or '更多通信行业分析' in decodeWord or  '中电新闻网讯通讯员' in decodeWord:
            continue
        else:
            allWord.append(decodeWord.strip('，').strip(''))

    decodeWord = ''.join(allWord)
    returnSummaryWord = decodeWord[0:60] + "..."

    if len(returnSummaryWord) > 10:
        return returnSummaryWord.replace('%','%%')
    else:
        return noneSummary

def getUrlCode():
    ttime = str(int(time.time()) * 1000)
    ranStr = random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', 26, )
    slugUrl = ttime + '_' + ''.join(ranStr)
    return slugUrl

def date_to_timestamp(date, format_string="%Y-%m-%d"):
    ddict = {}
    time_array = time.strptime(date, format_string)
    timeL1 = int(time.mktime(time_array))
    timeL = time.localtime(timeL1)

    timeYmd = time.strftime("%Y%m%d",timeL)
    timeYmdHMS = time.strftime("%Y-%m-%d %H:%M:%S",timeL)
    ddict['publish'] = timeYmdHMS
    ddict['created'] = str(datetime.datetime.now())
    ddict['updated'] = str(datetime.datetime.now())
    ddict['timeYmd'] = timeYmd
    return ddict

def timeall(ctime = None):
    ddict = {}
    if ctime:
        timeL = time.localtime(int(ctime))
    else:
        timeL = time.localtime()

    timeYmd = time.strftime("%Y%m%d",timeL)
    timeYmdHMS = time.strftime("%Y-%m-%d %H:%M:%S",timeL)
    ddict['publish'] = timeYmdHMS
    ddict['created'] = str(datetime.datetime.now())
    ddict['updated'] = str(datetime.datetime.now())
    ddict['timeYmd'] = timeYmd
    return ddict

def nowTime(num = 0):
    timeL = time.localtime()
    if num == 0:
        timeYmdHMS = time.strftime("%Y-%m-%d",timeL)
    if num == 1:
        timeYmdHMS = time.strftime("%Y-%m-%d %H", timeL)
    if num == 2:
        timeYmdHMS = time.strftime("%Y-%m-%d %H:%M", timeL)
    if num == 3:
        timeYmdHMS = time.strftime("%Y-%m-%d %H:%M:%S", timeL)
    return timeYmdHMS

def get_dbdupinfo(keysName,pubtime = None):
    if pubtime:
        exc = '''SELECT title,ArtUrl FROM U1LINK_post WHERE media_id = '{}' and DATE_FORMAT(publish, "%%Y%%m%%d") = "{}";'''.format(
            keysName, pubtime)
    else:
        exc = '''SELECT title,ArtUrl FROM U1LINK_post WHERE media_id = '{}';'''.format(keysName)

    ddict = {}
    ddict['title'] = []
    ddict['ArtUrl'] = []
    for i in mysqlcon.execute(exc):
        ddict['title'].append(i[0])
        ddict['ArtUrl'].append(i[1])
    return ddict

def get_3days_title():
    exc = '''select title from U1LINK_post where DATE_SUB(CURDATE(),INTERVAL 3 DAY) <= DATE(created);'''

    ddict = []
    for i in mysqlcon.execute(exc):
        ddict.append(i[0])
    return ddict

def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

def get_html(brow):
    delHtml = re.findall("<!--.*-->", brow)
    delscript = re.findall("<script.*script>", brow, re.M | re.S)
    deltechquotation = re.findall("<div class=\"tech-quotatio.*/span>.</div>", brow, re.M | re.S)
    hrefCUT = re.findall("<a.*?\">|</a>", brow)
    # aa1 = re.findall("<p>.*作者.*?</p>", brow)
    # aa4 = re.findall("<p>.*编辑.*?</p>", brow)
    # aa3 = re.findall("<p>.*图像.*?</p>", brow)
    # aa2 = re.findall("<p>.*来源.*?</p>", brow)
    # aalist = [aa1, aa2, aa3, aa4, delHtml, delscript, deltechquotation, hrefCUT]
    aalist = [delHtml, delscript, deltechquotation,hrefCUT]
    for nn in aalist:
        for i in nn:
            brow = brow.replace(i, '')
    return brow.replace('\n', '')



def get_type(title,keysListall,input_id=None,next=True):

    cutWord = ['焚烧发电','加工厂']
    for i in cutWord:
        if i in title:
            return 5

    jiebacutlist = jieba.lcut_for_search(title)

    if input_id and int(input_id) not in [1,2,3,4,6,7,8,9,10]:
        print('id输入错误，请输入1、2、3、4、6')
        return 5
    if input_id:
        for num, keyList in enumerate(keysListall):
            if keyList['ID'] != input_id:
                continue
            retC = list(set(jiebacutlist).intersection(set(keyList['json']['single'])))
            if retC:
                typenum = keyList['ID']
                # print(retC)
                return typenum
            elif not retC and keyList['json']['both']:
                for num, bothkeys in enumerate(keyList['json']['both']):
                    if bothkeys[0] in jiebacutlist and bothkeys[1] in jiebacutlist:
                        typenum = keyList['ID']
                        # print(bothkeys[0],bothkeys[1])
                        return typenum
            else:
                if not next:
                    return 5
                else:
                    for num, keyList in enumerate(keysListall):
                        if keyList['ID'] == input_id:
                            continue
                        retC = list(set(jiebacutlist).intersection(set(keyList['json']['single'])))
                        if retC:
                            typenum = keyList['ID']
                            # print(retC)
                            return typenum
                        elif not retC and keyList['json']['both']:
                            for num, bothkeys in enumerate(keyList['json']['both']):
                                if bothkeys[0] in jiebacutlist and bothkeys[1] in jiebacutlist:
                                    typenum = keyList['ID']
                                    # print(bothkeys[0],bothkeys[1])
                                    return typenum

    if not input_id:
        for num, keyList in enumerate(keysListall):
            retC = list(set(jiebacutlist).intersection(set(keyList['json']['single'])))
            if retC:
                typenum = keyList['ID']
                # print(retC)
                return typenum
            elif not retC and keyList['json']['both']:
                for num, bothkeys in enumerate(keyList['json']['both']):
                    if bothkeys[0] in jiebacutlist and bothkeys[1] in jiebacutlist:
                        typenum = keyList['ID']
                        # print(bothkeys[0],bothkeys[1])
                        return typenum

    return 5

if __name__ == '__main__':

    catJson = get_catJson()


    titile = '中国网民规模达9.04亿 在线应用有较大增长空间'

    a = get_type(titile,keysListall=catJson)
    print(a)
    exit()
    wordList = word.split('\n')
    for i in wordList:
        if i:
            a = get_type(i)
            if a ==2:
                print(i)
                print(a)
                print('----------------------')
