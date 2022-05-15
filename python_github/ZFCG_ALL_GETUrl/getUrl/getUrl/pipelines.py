# -*- coding: utf-8 -*-
import datetime,random,time,pprint,pymongo
NowTime = datetime.datetime.now()
# from getUrl.DB_object import *
# MongoDB = MongoDB_obj()
# CouchDB = Couch_obj()


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GeturlPipeline(object):
    def process_item(self, item, spider):
            return item


class MongoPipline(object):
    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url = crawler.settings.get('MONGO_url'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        item['capturedTime'] = NowTime
        item['couchdb_id'] = 'null'
        item['mongoContent_id'] = 'null'
        item['insert_status'] = 0
        b = str(int(time.time() * 1000000))
        item['_id'] = b + 'MongoDB' + ''.join(random.sample('zyxwvutsrqponmlkjih0123456789gfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ', 10))
        collName = item['collName']
        del item['collName']

        try:
            # self.db[collName].insert(dict(item))
            # pprint.pprint(item)
            print('-------------------------{}--------------------------录入成功'.format(NowTime))
        except:
            import json
            with open('ErrorReSponse.txt','a') as file:
                dateJson = json.dumps(item)
                file.write(';')
                file.write(dateJson)
                print('-------------------------ErrorReSponse--------------------------')

        return item

    def close_spider(self, spider):
        self.client.close()
