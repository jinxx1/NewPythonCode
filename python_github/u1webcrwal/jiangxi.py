# -*- coding: utf-8 -*-
import sqlalchemy
import time
import requests
import json
from lxml import html
import lxml.html
etree = lxml.html.etree




MYSQL_HOST = '183.6.136.67'
MYSQL_DATABASE = 'uxsq'
MYSQL_PORT = 3306
MYSQL_USER = 'xey'
MYSQL_PASSWORD = 'xey123456'



conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQL_USER,
                                                                                           PASSWORD=MYSQL_PASSWORD,
                                                                                           HOST=MYSQL_HOST,
                                                                                           PORT=MYSQL_PORT,
                                                                                           DBNAME=MYSQL_DATABASE)



mysqlcon = sqlalchemy.create_engine(conStr)



def getnoTileUrl():
    exc = "www.ccgp-jiangxi.gov.cn"
    aa = mysqlcon.execute('''SELECT raw_data_id,page_url FROM ztbInfo WHERE site = "{}" AND LENGTH(page_title) < 15;'''.format(exc))
    for i in aa:
        ddict = {}
        ddict['raw_data_id'] = i[0]
        ddict['url'] = i[1]
        yield ddict

def getErrorInfo():
    aa = mysqlcon.execute('''SELECT id,url FROM ztbError;''')
    ddict = {}
    ddict['id'] = []
    ddict['url'] = []
    for i in aa:
        ddict['id'].append(i[0])
        ddict['url'].append(i[1])
    return ddict

def inputErrorInfo(ddict,act):
    if act == "insert":
        exc = '''INSERT INTO ztbError (typecat,url,remark) values ("{typecat}","{url}","{remark}");'''.format(remark = ddict['remark'],typecat = ddict['typecat'],url = ddict['url'])
    elif act == "update":
        exc = "UPDATE ztbError SET remark='{remark}' WHERE id={id};".format(remark = ddict['remark'],id = ddict['id'])
    else:
        return None
    mysqlcon.execute(exc)


def jsonload(jsonPath):
    try:
        with open(jsonPath, 'r') as jf:
            jsonLoad = json.load(jf)
            jf.close()
    except:
        with open(jsonPath, 'w') as jf:
            jsonLoad = {}
            jsonLoad['timeOut'] = []
            jsonLoad['errorCode'] = []
            jsonLoad['nonTitle'] = []
            jsonLoad['errorOther'] = []
            json.dump(jsonLoad, jf)
            jf.close()
    return jsonLoad

def jsonwrite(jsonPath,item):
    with open(jsonPath, 'w') as jf:
        json.dump(item,jf)
        jf.close()

def update(value,id):
    exc_ztbInfo = "UPDATE ztbInfo SET page_title='{}' WHERE raw_data_id={};".format(value[:189],id)
    exc_ztbRawInfo = "UPDATE ztbRawInfo SET title='{}' WHERE id={};".format(value[:189], id)
    try:
        mysqlcon.execute(exc_ztbInfo)
    except:
        pass

    try:
        mysqlcon.execute(exc_ztbRawInfo)
    except:
        pass

def delectmysql(id):
    exc_ztbInfo = "DELETE FROM ztbInfo WHERE raw_data_id={};".format(id)
    exc_ztbRawInfo = "DELETE FROM ztbRawInfo WHERE id={};".format(id)
    try:
        mysqlcon.execute(exc_ztbInfo)
    except:
        pass
    try:
        mysqlcon.execute(exc_ztbRawInfo)
    except:
        pass

def requestsBrow(url='',step=0,errjson={}):
    # ip_proxy = proxy_ip()
    if step > 4:
        if url not in errjson['url']:
            ddict = {}
            ddict['url'] = url
            ddict['typecat'] = 'ConnectTimeout'
            ddict['remark'] = ''
            inputErrorInfo(act='insert', ddict=ddict)
            del ddict
        return None

    try:
        # brow = requests.get(url, proxies = ip_proxy)
        brow = requests.get(url,headers = {'Connection':'close'})
        if brow.status_code != 200:
            if url not in errjson['url']:
                ddict = {}
                ddict['url'] = url
                ddict['typecat'] = str(brow.status_code)
                ddict['remark'] = ''
                inputErrorInfo(act='insert', ddict=ddict)
                del ddict
            return None
    except requests.exceptions.ReadTimeout:
        if url not in errjson['url']:
            ddict = {}
            ddict['url'] = url
            ddict['typecat'] = 'timeOut'
            ddict['remark'] = ''
            inputErrorInfo(act='insert', ddict=ddict)
            del ddict
        return None
    except requests.exceptions.ConnectTimeout:
        step += 1
        return requestsBrow(url=url, step=step)
    return brow



def main():
    errjson = getErrorInfo()
    for i in getnoTileUrl():

        if 'temp' in i['url']:
            delectmysql(i[i['raw_data_id']])
            continue

        brow = requestsBrow(i['url'],errjson=errjson)

        if not brow:
            continue

        browHtml = html.fromstring(brow.text)
        h1xpath = browHtml.xpath("//h1//text()")
        title = ''.join(h1xpath)

        if not title:
            if i['url'] not in errjson['url']:
                ddict = {}
                ddict['url'] = i['url']
                ddict['typecat'] = 'nonTitle'
                ddict['remark'] = ''
                inputErrorInfo(act='insert',ddict=ddict)
                del ddict
            continue

        print(title)
        update(title, i['raw_data_id'])
        print('---------------------')



if __name__ == '__main__':
    main()