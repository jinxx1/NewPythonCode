# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pandas as pd
import pprint
import sqlalchemy

# 设置数据库信息
MYSQLINFO = {
    "HOST": "120.24.4.84",
    "DBNAME": "crawlURL",
    "USER": "xey",
    "PASSWORD": "85f0a9e2e63b47c0b56202824195fb70#AAA",
    "PORT":3306
}
conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(
    USER=MYSQLINFO['USER'], PASSWORD=MYSQLINFO['PASSWORD'], HOST=MYSQLINFO['HOST'], PORT=MYSQLINFO['PORT'],
    DBNAME=MYSQLINFO['DBNAME'])

mysqlcon = sqlalchemy.create_engine(conStr)



class ZhilucrawlPipeline(object):
    def process_item(self, item, spider):
        return item
