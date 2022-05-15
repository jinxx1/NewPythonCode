# -*- coding: utf-8 -*-

import platform
import requests
import json
import os
import time
import random
import pymysql
from PIL import Image
from newscrapy.api_png import *


def cleanList(llist):
    newlist = []
    for i in llist:
        n = i.strip()
        if n:
            newlist.append(n)
    return newlist

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
    # posturlapi = 'https://umxh.xue22222222222222you.cn/pc/api/caijiApi/urlIsExist'
    str_c = json.dumps(urllist)
    dataApi = {"urlListJson": str_c}
    try:
        a = requests.post(url=posturlapi, data=dataApi, headers=HEA)
        jsonT = json.loads(a.text)
        return jsonT['data']
    except:
        print('链接筛选api--有故障，等待3秒后，重新发送请求')
        time.sleep(3)
        urlIsExist(urllist)


def save_api(dict1):
    HEA = {
        "Connection": "close",
    }
    try:
        a = requests.post(url='https://umxh.xue2you.cn/pc/api/caijiApi/save', data=dict1, headers=HEA)
        return json.loads(a.text)
    except:
        exit()


def jsonload(jsonPath):
    with open(jsonPath, 'r', encoding='utf-8') as jf:
        jsonLoad = json.load(jf)
        jf.close()
    return jsonLoad


def get_cookies_by_headlessChrome(key=None, run=0):
    if run == 0:
        return None

    if not key:
        catList = ['GCJS', 'ZFCG', 'GYCQ']
        listnum = random.randint(0, 2)
        url1 = "https://ggzyfw.fujian.gov.cn/Website/JYXXNew.aspx?T={}".format(catList[listnum])
    else:
        url1 = "https://ggzyfw.fujian.gov.cn/Website/JYXXNew.aspx?T={}".format(key)

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    chrome_opt = Options()

    chrome_opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_opt.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_opt)
    driver.get(url1)
    driver.implicitly_wait(60)
    cookiess = driver.get_cookies()
    driver.quit()
    jar = requests.sessions.RequestsCookieJar()
    for i in cookiess:
        jar.set(i['name'], i['value'])

    return requests.utils.dict_from_cookiejar(jar)


def get_jsonPath_ccgp_fujian():
    import platform
    osName = platform.platform()
    root_json = r"C:/PthonCode/jxweixincrawl/ccgp_fujian_json/"
    if 'Windows' not in osName:
        root_json = "/home/terry/jxpython/ccgp_fujian_json/"

    return root_json


def date_to_timestamp():
    timeL = time.localtime()
    ddict = {}
    ddict['Ymd_HMS'] = time.strftime("%Y%m%d_%H%M%S", timeL)
    ddict['Y-m-d'] = time.strftime("%Y-%m-%d", timeL)
    ddict['today'] = time.strftime("%Y-%m-%d %H:%M:%S", timeL)

    return ddict


def file_name_walk(file_dir):
    listpath = []
    llist = []
    # rootPath = os.getcwd().replace('\\', '/')
    for root, dirs, files in os.walk(file_dir):
        dictTemp = {}
        dictTemp['root'] = root  # 当前目录路径
        dictTemp['dirs'] = dirs  # 当前路径下所有子目录
        dictTemp['files'] = files  # 当前路径下所有非目录子文件
        listpath.append(dictTemp)
    for tis in listpath:
        if tis['files']:
            for num, fileName in enumerate(tis['files']):
                winPath = tis['root'] + '/' + fileName
                filePath = winPath.replace('\\', '/')
                llist.append(filePath)
    return llist


def get_cookies_by_headlessChrome_for_zfcgfujian(url,pathabs):
    timestr = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    savePath = pathabs + "/lianzhong_shibie/{}/".format(timestr)

    isExists = os.path.exists(savePath)
    if not isExists:
        os.makedirs(savePath)


    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    chrome_opt = Options()
    chrome_opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_opt.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_opt)
    driver.get(url)
    driver.implicitly_wait(60)

    driver.set_window_size(1024,768)
    csrfmiddlewaretoken = driver.find_element_by_xpath("//input[@name = 'csrfmiddlewaretoken']").get_attribute('value')

    element = driver.find_element_by_id("verifycode")

    full_pic_path = savePath + "/full.png"
    cover_pic_path = savePath + "/cover.png"
    driver.save_screenshot(full_pic_path)

    xPiont = element.location['x']
    yPiont = element.location['y']
    # 获取element的宽、高
    element_width = xPiont + element.size['width']
    element_height = yPiont + element.size['height']

    picture = Image.open(full_pic_path)

    pic = picture.crop((xPiont, yPiont, element_width, element_height))
    pic.save(cover_pic_path)



    cookiess = driver.get_cookies()
    jar = requests.sessions.RequestsCookieJar()
    for i in cookiess:
        jar.set(i['name'], i['value'])
    scrapy_jar = requests.utils.dict_from_cookiejar(jar)

    print('无头浏览器的jar：',scrapy_jar)
    print('无头浏览器的抓取到的csrfmiddlewaretoken：',csrfmiddlewaretoken.strip())
    print('无头浏览器截图的cover：',cover_pic_path)
    print('验证图的savePath：',savePath)
    info = {
        'scrapy_jar':scrapy_jar,
        'csrfmiddlewaretoken':csrfmiddlewaretoken,
        'cover_pic_path':cover_pic_path,
        'savePath':savePath
    }

    driver.quit()
    return info

def get_timestr(date,outformat = "%Y-%m-%d %H:%M:%S",combdata = False):
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


def aa():
    import pandas as pd
    rootPath = os.getcwd().replace('\\', '/')
    jsonpath = rootPath + "/ccgp_artall"
    jsonpathList = file_name_walk(jsonpath)
    for path in jsonpathList:
        df = pd.read_json(path_or_buf=path,orient='index')
        df['path'] = path
        for i in range(len(df)):
            if df.loc[i,'mark'] != 0:
                print(df.loc[i])
        # print(df.index)
        # ind = df.index
        # print(ind)

        # with open(path) as ff:
        #     aa = json.load(ff)
        #     for ii in aa:
        #         if aa[ii]['mark'] != 0:
        #             continue
        #         ddict = aa[ii]
        #         ddict['jsonpath'] = path
        #         yield ddict


def getList(baseList):

    NUM = 5000
    yu = len(baseList) % NUM
    chu = (len(baseList) - yu) / NUM
    list_2 = []
    for n in range(0, int(chu)+1):
        if n == 0:
            star = n
            end = n + NUM
            list_son = baseList[star:end]
            list_2.append(list_son)
        elif n > int(chu):
            print('n == chu')
            star = end
            end = star + yu
            list_son = baseList[star:end]
            list_2.append(list_son)
            break
        else:
            star = end
            end = star + NUM
            list_son = baseList[star:end]
            list_2.append(list_son)
    return list_2
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






    # for list_1 in ListNum:
    #     l1 = [llist[x] for x in list_1]
    #     # l1_str = ','.join(l1)
    #     ListCut.append(l1)
    # pprint.pprint([[x[0],x[-1]] for x in ListCut])


    #
    # ztbRawInfo_idstr = ','.join(llist)
    # sqlexe = '''DELETE FROM t_leave_info WHERE id IN ({});'''.format(ztbRawInfo_idstr)



    cursor.close()
    db.close()
    # return llist


if __name__ == '__main__':


    site = 'www.ccgp.gov.cn'
    mysql_allurl = get_mysql_allurl(site)

    print(mysql_allurl)
    import os,sys
    # a = ','.join(mysql_allurl)
    # print(a)
    print(type(mysql_allurl))
    print(len(mysql_allurl))
    print(sys.getsizeof(mysql_allurl))