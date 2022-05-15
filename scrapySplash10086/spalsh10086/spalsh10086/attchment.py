# -*- coding: utf-8 -*-
import pymysql,datetime
import re
import pandas as pd
import numpy as np
from pandas import Series
from bs4 import BeautifulSoup
# pd.set_option('display.max_columns',None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.width', 5000)
# pd.set_option('display.unicode.ambiguous_as_wide', True)
# pd.set_option('display.unicode.east_asian_width', True)
import sqlalchemy


MYSQLINFO = {
    "HOST": "183.6.136.67",
    "DBNAME": "uxsq",
    "USER": "xey",
    "PASSWORD": "xey123456",
    "PORT":3306
}

conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
                                                                                               'DBNAME'])
mysqlcon = sqlalchemy.create_engine(conStr)

def attchment_get(HTMLcontent):
    soup = BeautifulSoup(HTMLcontent, 'lxml')
    hrefall = soup.find_all(href=re.compile("commonDownload\.html\?attId"))
    attchment = []
    for nn in hrefall:
        ddict = {}
        download_url = nn.get('href')
        ddict['download_url'] = "https://b2b.10086.cn" + download_url
        ddict['name'] = nn.get_text()
        attchment.append(ddict)
    return attchment

def update_attchment(raw_id,item):
    exc ='''INSERT INTO ztbInfoAttachment (raw_id,status,download_url,name) VALUES ({raw_id},{status},'{download_url}','{name}')'''
    # exc = '''UPDATE ztbInfoAttachment SET raw_id={raw_id},status={status},download_url='{download_url}',name='{name}';'''
    excWord = exc.format(raw_id=raw_id,
                         download_url=item['download_url'],
                         name=item['name'],
                         status=0)
    mysqlcon.execute(excWord)

def get_info_id():
    excWord = "SELECT id,raw_data_id FROM ztbInfo WHERE site='b2b.10086.cn' and created between date_sub(now(),interval 6 month) and now();"
    mysqltop = mysqlcon.execute(excWord)
    llist = []
    for i in mysqltop:
        ddict = {}
        ddict['raw_data_id'] = i[1]
        ddict['id'] = i[0]
        llist.append(ddict)
    return llist

def get_ztbInfoAttachment_id():
    excWord = "SELECT info_id FROM ztbInfoAttachment;"
    mysqltop = mysqlcon.execute(excWord)
    llist = [x[0] for x in mysqltop if x[0]]
    return tuple(llist)

def get_content(info_id):
    excWord = "SELECT content FROM ztbInfoContent where info_id={};".format(str(info_id))
    mysqltop = mysqlcon.execute(excWord)
    hhtml = [x[0] for x in mysqltop]
    return (''.join(hhtml))


def attmenSTR(downLoad):
    from urllib.parse import unquote
    import requests
    HEA = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "b2b.10086.cn",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"
    }

    ddict = {}
    ddict['download_url'] = downLoad
    brow = requests.get(url=downLoad,verify=False,headers=HEA)
    print(brow.headers)
    print(brow.text)
    try:
        soureAttachment = re.findall('''attachment; filename=\"(.*?)\"''',brow.headers['Content-Disposition'])[0]
    except Exception as f:
        print(f)
        return None
    ddict['name'] = unquote(soureAttachment,'utf-8')
    return ddict

if __name__ == '__main__':
    url = "https://b2b.10086.cn/b2b/main/commonDownload.html?attId=f7ca2e4864644febb9f9386f92a72e68"
    abc = attmenSTR(url)
    print(abc)

    exit()




    df = pd.read_csv('aaa.csv',index_col=0)
    for i in range(len(df)):
        if df.iloc[i].status == 1:
            continue
        content_html = get_content(df.iloc[i].id)
        attchment = attchment_get(content_html)
        if attchment:
            df.iloc[i].download = 1
            df.to_csv('aaa.csv')
            try:
                for n in attchment:
                    update_attchment(raw_id=df.iloc[i].raw_data_id,item=n)
                df.iloc[i].status = 1
                df.to_csv('aaa.csv')
            except:
                continue

    exit()



    info_id = 9017992
    get_content(info_id)
    exit()
    infoAttachment_allid = get_ztbInfoAttachment_id()
    llist = []
    for i in get_info_id():
        if i['id'] in infoAttachment_allid:
            continue
        llist.append(i)
    df = pd.DataFrame(llist)
    df.to_csv('aaa.csv')
    print(df)




