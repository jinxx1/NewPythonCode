# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pprint
import pymysql
import time
from datetime import datetime
from gcproject.settings import MYSQLINFO
try:
    from pymysql.converters import escape_string
except:
    from pymysql import escape_string


class MysqlPipLine():

    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        self.db = pymysql.connect(host=self.host, user=self.user, passwd=self.password, db=self.database, port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self,item,spider):
        item['creation_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print('录入info--------------')
        item['raw_data_id'] = self.insert_ztbRawInfo_getID(item)
        item['raw_id'] = item['raw_data_id']
        # print('录入content--------------')
        self.insert_ztbRawInfoContent_getID(item)
        # print('录入attchment--------------')
        self.insert_ztbInfoAttachment(item)
        print('id:  {}  got it'.format(item['raw_data_id']))

        # item['content'] = len(item['content'])
        # import pprint
        # pprint.pprint(item)
        # print('-------------------------------')
        return item

    def insert_ztbRawInfo_getID(self,item):
        comparisonKeys = ('subclass', 'site', 'page_url', 'title', 'issue_time', 'creation_time', 'end_time',
                          'province_name', 'city_name', 'purchase_type', 'business_type', 'minor_business_type',
                          'money', 'data')
        keysList = [i for i in item.keys() if i in comparisonKeys]
        valueList = ["'" + item[i] + "'" for i in keysList]
        keys = ','.join(keysList)
        valuesall = ','.join(valueList)
        exc = "insert into ztbRawInfo ({keys}) values ({valuesall});".format(keys=keys,valuesall=valuesall)

        self.cursor.execute(exc)
        primaryID = self.db.insert_id()
        # print('---------------------------------info', primaryID)
        self.db.commit()
        return str(primaryID)

    def insert_ztbRawInfoContent_getID(self, item):
        exc = '''insert into ztbRawInfoContent (raw_data_id,content) values ({raw_data_id},"{content}");'''.format(raw_data_id=item['raw_data_id'],
                                                                                                        content=escape_string(item['content']))
        self.cursor.execute(exc)
        self.db.commit()

    def insert_ztbInfoAttachment(self, item):

        if 'attchment' not in item.keys():
            return item
        for i in item['attchment']:
            exc = "insert into ztbInfoAttachment (raw_id,download_url,name,status) values ({raw_id},'{download_url}','{name}',0);".format(
                raw_id=item['raw_id'],
                download_url=escape_string(i['download_url']),
                name=escape_string(i['name']))
            self.cursor.execute(exc)
            self.db.commit()


class GcprojectPipeline:
    def process_item(self, item, spider):
        return item

