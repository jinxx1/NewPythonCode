# -*- coding: utf-8 -*-
import pprint

import pymysql,datetime
import pandas as pd
import numpy as np
from pandas import Series
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import sqlalchemy
from ggzy.settings import MYSQLINFO






conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
                                                                                               'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
                                                                                               'DBNAME'])
mysqlcon = sqlalchemy.create_engine(conStr)


def get_dupurl(source):

    sqlexc = '''select page_url from ztbRawInfo where site = "{source}"'''.format(source=source)
    gettouple = mysqlcon.execute(sqlexc)
    llist = [x[0] for x in gettouple]
    return tuple(llist)

def file_name_walk():
    import json
    import pandas as pd

    file_dir = r"../ggzy/pageNum/ccgp_chongqing"
    import os
    listpath = []
    for root, dirs, files in os.walk(file_dir):
        for num,i in enumerate(files):
            # if num >1:
            #     continue
            file = os.path.join(root, i)
            with open(file, 'r',encoding='utf-8') as jf:
                jsonLoad = json.load(jf)
            for nn in jsonLoad:
                dditc = {}
                dditc['issueTime'] = nn['issueTime']
                dditc['articleId'] = int(nn['id'])
                dditc['status'] = nn['crawlStatus']
                # pprint.pprint(dditc)
                # print('-------------------------')
                listpath.append(dditc)


    return pd.DataFrame(listpath)




if __name__ == '__main__':
    import sys
    # sqlexc = '''select page_url from ztbRawInfo where site = "www.ccgp-shandong.gov.cn"'''
    sqlexc = '''select * from ztbRawInfoContent limit 1000;'''
    gettouple = mysqlcon.execute(sqlexc)
    llist = [x[0] for x in gettouple]
    touplist = tuple(llist)
    print(len(touplist))
    listsize = sys.getsizeof(llist)
    tuplesize = sys.getsizeof(touplist)
    ss = 1024*1024
    print(listsize/ss)
    print(tuplesize/ss)




    pass




    # print(MYSQLINFO)
    # exit()
    # from hyper.contrib import HTTP20Adapter
    # ADPTER = HTTP20Adapter()
    #
    #
    #
    #
    # import requests
    # # 公众号文章中说的用HTTP2的网站 spa16.scrape.center的数据API
    # url = "https://spa16.scrape.center/api/book/?limit=18&offset=0"
    # a = requests.Session()
    # a.mount(url,ADPTER)
    # htmlcode = a.get(url)
    # print(htmlcode.text)







    # a = get_dupurl("www.ccgp-chongqing.gov.cn")
    # print(len(a))
    # pass