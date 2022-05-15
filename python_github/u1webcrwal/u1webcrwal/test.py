# -*- coding: utf-8 -*-
import os,re,json
import pymysql
from bs4 import BeautifulSoup
import requests
import base64
from io import BytesIO
from PIL import Image
import datetime,time
import difflib

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

if __name__ == '__main__':
    # today_str = datetime.date.today().strftime('%Y/%m%d')
    # print(today)
    wword = "2020/5/9 16:22:49"
    a1 = date_to_timestamp(wword,'%Y/%m/%d %H:%M:%S')
    print(a1)

    wword = '''<p class="">来源： 南方电网&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日期：20.05.09</p>'''
    b = re.findall("来源：(.*?)日期",wword)[0]
    a = b.strip().replace('&nbsp;','')
    print(a)





    word = '''国网、南网、国家电网、南方电网、电网、综合能源、智慧能源、电力工程、充电桩、输电工程、配电工程、用户接入工程、农网'''.split('、')
    ddict = {}
    ddict['both'] = []
    ddict['single'] = word

    print(ddict)
#
    str1 = '''{'both': [], 'single': ['国网', '南网', '国家电网', '南方电网', '电网', '综合能源', '智慧能源', '电力工程', '充电桩', '输电工程', '配电工程', '用户接入工程', '农网']}'''
    str1 =str1.replace("\'","\"")
    print(str1)


