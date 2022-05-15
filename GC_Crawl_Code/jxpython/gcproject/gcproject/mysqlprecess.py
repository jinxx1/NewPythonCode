# -*- coding: utf-8 -*-

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
from gcproject.settings import MYSQLINFO


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
    return llist



if __name__ == '__main__':
    pass