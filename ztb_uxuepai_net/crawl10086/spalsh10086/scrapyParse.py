# -*- coding: utf-8 -*-

import platform
import requests
import json
import os
import time,re
import random
import pymysql
from bs4 import BeautifulSoup
from PIL import Image




def get_mysql_allurl(site):
    db = pymysql.connect(
        host="183.6.136.67",
        db="uxsq",
        user="xey",
        passwd="xey123456",
        charset="utf8",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = db.cursor()
    search_todaydate = '''SELECT page_url FROM ztbRawInfo WHERE site = "{}"'''.format(site)

    cursor.execute(search_todaydate)
    resultes = cursor.fetchall()
    llist = []
    for i in resultes:
        llist.append(i['page_url'])

    cursor.close()
    db.close()
    return llist



def urlIsExist(urllist):
    HEA = {
        "Connection": "close",
    }
    posturlapi = 'https://umxh.xue2you.cn/pc/api/caijiApi/urlIsExist'
    str_c = json.dumps(urllist)
    dataApi = {"urlListJson": str_c}
    try:
        a = requests.post(url=posturlapi, data=dataApi, headers=HEA)
        jsonT = json.loads(a.text)
        return jsonT['data']
    except:
        return None


def save_api(dict1):
    HEA = {
        "Connection": "close",
    }
    try:
        a = requests.post(url='https://umxh.xue2you.cn/pc/api/caijiApi/save', data=dict1, headers=HEA)
        return json.loads(a.text)
    except:
        exit()

def get_IDandTIME(html):
    llist = []
    artcle_urls ='https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id={}'
    resID = re.findall("selectResult\(\'(.*?)\'\)",html)
    soup = BeautifulSoup(html,'lxml')
    for id in resID:
        all_tr = soup.find_all(attrs={'onclick': "selectResult('{id}')".format(id=id)})
        for i in all_tr:



            try:
                timeWord = re.findall("(\d{4}-\d{1,2}-\d{1,2})",str(i))[0]
                timeWord = get_timestr(timeWord)
            except:
                print('no timeWord')
                continue
            ddict = {'id':id,'time':timeWord,'url':artcle_urls.format(id)}
            llist.append(ddict)

    return llist

def get_timestr(date,outformat = "%Y-%m-%d",combdata = False):
    import time
    time_array = ''
    format_string = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d %H",
        "%Y/%m/%d",
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d %H:%M",
        "%Y.%m.%d %H",
        "%Y.%m.%d",
        "%Y年%m月%d日 %H:%M:%S",
        "%Y年%m月%d日 %H:%M",
        "%Y年%m月%d日 %H",
        "%Y年%m月%d日",
        "%Y_%m_%d %H:%M:%S",
        "%Y_%m_%d %H:%M",
        "%Y_%m_%d %H",
        "%Y_%m_%d",
        "%Y%m%d%H:%M:%S",
        "%Y%m%d %H:%M:%S",
        "%Y%m%d %H:%M",
        "%Y%m%d %H",
        "%Y%m%d",
        "%Y%m%d%H%M%S",
        "%Y%m%d %H%M%S",
        "%Y%m%d %H%M",
        "%Y%m%d %H",
        "%Y%m%d",
        "%Y\%m\%d %H:%M:%S",
        "%Y\%m\%d %H:%M",
        "%Y\%m\%d %H",
        "%Y\%m\%d",
        "%Y年%m月%d日%H:%M:%S",
        "%Y年%m月%d日%H:%M",
        "%Y年%m月%d日%H",
        "%Y年%m月%d日",
    ]
    for i in format_string:

        try:
            time_array = time.strptime(date, i)
        except:
            continue

    if not time_array:
        return None
    timeL1 = int(time.mktime(time_array))
    timeL = time.localtime(timeL1)
    if combdata:
        return time.strftime(outformat, timeL),timeL1
    else:
        return time.strftime(outformat,timeL)


def get_mysql_allurl1(site):
    import pprint
    db = pymysql.connect(
        host="183.6.136.67",
        db="uxsq",
        user="xey",
        passwd="xey123456",
        charset="utf8",
        use_unicode=True,
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = db.cursor()
    search_todaydate = '''SELECT id FROM ztbRawInfo WHERE site = "{}" and issue_time like "201%" and creation_time like "2020-06-03%";'''.format(site)

    cursor.execute(search_todaydate)
    resultes = cursor.fetchall()
    llist = []
    for num,i in enumerate(resultes):
        llist.append(str(i['id']))


    info_id_ListCut = getList(baseList=llist)
    infoContent_id_ListCut = []

    for i in info_id_ListCut:
        istr = [str(x) for x in i]
        info_id_str_all = ','.join(istr)
        exword = '''SELECT id FROM ztbRawInfoContent WHERE raw_data_id IN ({});'''.format(info_id_str_all)
        cursor.execute(exword)
        resultes = cursor.fetchall()
        llist1 = []
        for num, i in enumerate(resultes):
            llist1.append(str(i['id']))
        infoContent_id_ListCut.append(llist1)

    for i in info_id_ListCut:
        STRList = [str(x) for x in i]
        STRw = ','.join(STRList)
        exword = '''DELETE FROM ztbRawInfo WHERE id IN ({});'''.format(STRw)
        cursor.execute(exword)
        db.commit()
    for i in infoContent_id_ListCut:
        STRList = [str(x) for x in i]
        STRw = ','.join(STRList)
        exword = '''DELETE FROM ztbRawInfoContent WHERE id IN ({});'''.format(STRw)
        cursor.execute(exword)
        db.commit()

    cursor.close()
    db.close()




def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    ddict = {}

    # try:
    #     time1 = soup.find_all(attrs={'id':'time'})[0]
    # except:
    #     return None
    # ddict['issueTime'] = time1.get_text().replace(' 星期四 ',' ').replace(' 星期一 ',' ').replace(' 星期二 ',' ').replace(' 星期三 ',' ').replace(' 星期五 ',' ').replace(' 星期六 ',' ').replace(' 星期日 ',' ')

    try:
        ddict['title'] = soup.h1.get_text()
    except:
        return None

    try:
        ddict['content'] = str(soup.find(attrs={'class':'zb_table'}))
    except:
        return None

    return ddict

def depcut(llist):

    crawlList = [x['url'] for x in llist]
    nomysqllist = urlIsExist(crawlList)
    allist = []
    for i in nomysqllist:
        for n in llist:
            if i == n['url']:
                allist.append(n)

    return allist



if __name__ == '__main__':


    aa = 'b2b.10086.cn'
    llist = [{'id': '684800', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684800111'}, {'id': '684799', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684799'}, {'id': '684777', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684777'}, {'id': '684797', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684797'}, {'id': '684773', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684773'}, {'id': '684795', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684795'}, {'id': '684793', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684793'}, {'id': '684791', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684791'}, {'id': '684769', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684769'}, {'id': '684768', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684768'}, {'id': '684771', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684771'}, {'id': '684767', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684767'}, {'id': '684750', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684750'}, {'id': '684749', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684749'}, {'id': '684763', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684763'}, {'id': '684762', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684762'}, {'id': '684761', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684761'}, {'id': '684743', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684743'}, {'id': '684740', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684740'}, {'id': '684759', 'time': '2020-08-21', 'url': 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=684759'}]



    c = depcut(llist)
    print(c)
