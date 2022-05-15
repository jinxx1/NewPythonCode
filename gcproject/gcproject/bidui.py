# -*- coding: utf-8 -*-
import pprint, datetime
import pandas as pd
import numpy as np
from pandas import Series

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import sqlalchemy

MYSQLINFO = {
    "HOST": "172.16.10.94",
    "DBNAME": "shangqing",
    "USER": "gzcez",
    "PASSWORD": "1234@Qwer",
    "PORT": 3306
}

conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(
USER=MYSQLINFO['USER'],
PASSWORD=MYSQLINFO['PASSWORD'],
HOST=MYSQLINFO['HOST'],
PORT=MYSQLINFO['PORT'],
DBNAME=MYSQLINFO['DBNAME']
)

mysqlcon = sqlalchemy.create_engine(conStr)

def info_sql(site):
    sqlexc = '''select page_url from ztbRawInfo where site = "{}"'''.format(site)
    gettouple = mysqlcon.execute(sqlexc)
    llist = [x[0] for x in gettouple]
    return tuple(llist)
def raw_sql(site):
    sqlexc = '''select page_url,id from ztbRawInfoStatistics where site = "{}"'''.format(site)
    gettouple = mysqlcon.execute(sqlexc)
    llist = [x for x in gettouple]
    return tuple(llist)


def chrome_headerless(url,xpath):

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    chrome_opt = Options()
    chrome_opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_opt.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_opt,executable_path='chromedriver.exe')
    driver.get(url)
    aa = driver.find_element_by_xpath(xpath).get_attribute("outerHTML")
    driver.quit()

    return aa

if __name__ == '__main__':

    url = 'https://bulletin.cebpubservice.com/biddingBulletin/2021-01-16/4284174.html'
    xpath = '//*'
    a = chrome_headerless(url,xpath)
    print(a)



    # url = 'https://www.szjsjy.com.cn:8001/jyw/jyw/zbgs_View.do?Guid=6d9bf701-26b5-4056-b3b7-a3df8af88101'
    # xpath = "//div[@class = 'detail_contect']"
    # a = chrome_headerless(url,xpath)
    # print(a)
    # exit()

    # site = 'www.gdebidding.com'
    site = 'www.szjsjy.com.cn'

    info = info_sql(site)
    raw = raw_sql(site)

    llist = []
    for i_raw in raw:
        if i_raw[0] not in info:
            llist.append(i_raw)
    pprint.pprint(llist)
    print(len(llist))
