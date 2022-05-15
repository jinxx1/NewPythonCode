# -*- coding: utf-8 -*-

import csv,json,sqlalchemy,pymysql
import requests

header_raw = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Cookie: __jsluid_s=1a475f19b079afb73db7c6ff9c50092d; KUID=jewx971602834313818; _ga=GA1.2.201920505.1602834315; koolearn_netalliance_cookie=ff80808138fed9e801390002fcd60001#d541dd6e1a1e4716a6e4e8db2b646717; easeMobPassword=koolearn1602835139607462352; easeMobId=koolearn1602835139607462352; pt_ref_1783e324=; Qs_lvt_143225=1602835141; gr_user_id=60a0a1fb-debd-4de7-9177-8d9934f7cead; grwng_uid=d8bcf905-e46b-4aa5-a08e-7631023b497a; mp_ec424f4c03f8701f7226f5a009d90586_mixpanel=%7B%22distinct_id%22%3A%20%22175306b690196b-0542893a83e6b7-c781f38-1fa400-175306b6902934%22%2C%22%24device_id%22%3A%20%22175306b690196b-0542893a83e6b7-c781f38-1fa400-175306b6902934%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; koolearn_netalliance_criteo=ff80808138fed9e801390002fcd60001#d541dd6e1a1e4716a6e4e8db2b646717; MEIQIA_TRACK_ID=1f1UFsAbt4kmUSnRXmXfFtfHl1V; MEIQIA_VISIT_ID=1ix2w3IvwcjyF8sHFWjq4gc28qy; Hm_lvt_00a4345015fdaa4f88bd12eae0383335=1602835282; Qs_pv_143225=4541550899028449300%2C3388269734397273600%2C4245475576269903000; pt_1783e324=uid=txuG4RVKM0V1wKflb83S9Q&nid=1&vid=Xe9ZP8FFEdTMrnp50h6/cg&vn=1&pvn=2&sact=1602835288141&to_flag=0&pl=pgBpjcisQ4oSH2TDEl8T0g*pt*1602835141704; prelogid=8f1c837118d7bed23f67625cf0dbc6df; _csrf=a71c61dc4b6d111278622d073bd6b2fcab270e2d73ffeaaf6255a82dc49ab13fa%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22nsmDFJ70q4YZ_yfOkhPfPKgmRn-xRGlf%22%3B%7D; php-webapp-dict=5d045529760d99a05493219d3c025fb7; koo.line=www; Hm_lvt_5023f5fc98cfb5712c364bb50b12e50e=1602835141,1603025927; _gid=GA1.2.1214992843.1603025927; wwwad=true; Hm_lpvt_5023f5fc98cfb5712c364bb50b12e50e=1603027690
Host: www.koolearn.com
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')

MYSQLINFO = {
    "HOST": "localhost",
    "DBNAME": "english",
    "USER": "root",
    "PASSWORD": "040304",
    "PORT": 3306
}
conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
                                                                                               'DBNAME'])
mysqlcon = sqlalchemy.create_engine(conStr)
import pandas as pd
from bs4 import BeautifulSoup
from collections import namedtuple
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)



def getall_tag():
    exc = "SELECT id,tag FROM stardict WHERE tag IS NOT NULL;"
    info = mysqlcon.execute(exc)
    llist = []
    for i in info:
        ddict ={}
        ddict['id'] = i[0]
        tagList = i[1].split(' ')
        ddict['tagList'] = tagList
        llist.append(ddict)
        # import pprint
        # pprint.pprint(ddict)
        # print('---------------------')
    return llist

def getall_word():
    exc = "SELECT id,word FROM stardict WHERE mba is null;"
    # exc = "SELECT id,word FROM stardict WHERE word = 'vague';"
    info = mysqlcon.execute(exc)
    llist = []
    for i in info:
        ddict ={}
        ddict['id'] = i[0]
        ddict['word'] = i[1]
        llist.append(ddict)
    return llist

def get_gre_co_pandas():
    exc = "SELECT id,word,translation FROM stardict WHERE gre=1;"

    info = mysqlcon.execute(exc)
    llist = []
    for i in info:
        ddict ={}
        ddict['id'] = i[0]
        ddict['word'] = i[1]
        ddict['translation'] = i[2]
        llist.append(ddict)
    df = pd.DataFrame(llist)
    return df

if __name__ == '__main__':
    df = get_gre_co_pandas()
    print(df)
    exit()





    import pprint

    # mysql_df = pd.DataFrame(getall_word())
    # print(mysql_df)
    # exit()

    base = "https://www.koolearn.com/dict/tag_329_{}.html"
    llist = []
    for pageid in range(1,40):
        url = base.format(str(pageid))

        brow = requests.get(url=url,headers = HEA)
        html = brow.text.encode(brow.encoding).decode('utf-8','ignore')
        soup = BeautifulSoup(html,'lxml')
        word = soup.find('div',attrs={'class':'word-box'}).find_all('a',attrs={'class':'word'})
        for i in word:
            signword = i.get_text()
            ddict = {}
            ddict['url'] = pageid
            ddict['word'] = signword
            llist.append(ddict)

    request_df = pd.DataFrame(llist)
    request_df.to_csv('aaa.csv')

    exit()

    request_df = pd.DataFrame(llist,columns=['word'])
    print(request_df,len(request_df))
    request_df.drop_duplicates('word',keep='first',inplace=True)
    print('request_df',len(request_df))


    mysql_df = pd.DataFrame(getall_word())
    print('mysql_df',len(mysql_df))
    result = pd.merge(left=request_df,right=mysql_df,how='inner',on=['word'])
    print('result',len(result))
    for nn in result.index:
        id = result.iloc[nn]['id']
        exc = '''UPDATE stardict SET mba=1 WHERE id = {};'''.format(id)
        a = mysqlcon.execute(exc)

        # print(a)


    exit()


    for info in allinfo:
        l1 = [x + "=1" for x in info['tagList']]
        l1_str = ','.join(l1)
        exc = '''UPDATE stardict SET {} WHERE id = {};'''.format(l1_str,info['id'])
        a = mysqlcon.execute(exc)
        print(a)

    exit()



    # csvFile = r'D:\PythonCode\ECDICT-master\ecdict.mini.csv'
    csvFile = r"D:\PythonCode\ECDICT-master\stardict.csv"
    df = pd.read_csv(csvFile)
    print('33-------end')
    df.drop_duplicates(subset='word',keep='first',inplace=True)
    print('35-------end')
    df.to_sql(name='stardict', con=mysqlcon, if_exists='replace', index=False,chunksize=1000)
    print('37-------end')
