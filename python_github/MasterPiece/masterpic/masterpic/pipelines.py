# -*- coding: utf-8 -*-
import pymongo
import time,datetime,random
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pprint

class MasterpicPipeline(object):
    def process_item(self, item, spider):
        return item

class Pic_DownLoad_Pipeline(ImagesPipeline):
    default_headers = {
        ":authority":"gallerix.asia",
        ":method":"GET",
        ":scheme":"https",
        "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding":"gzip, deflate, br",
        "accept-language":"zh-CN,zh;q=0.9,zh-TW;q=0.8",
        "cache-control":"max-age=0",
        "upgrade-insecure-requests":"1",
        "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }

    def get_media_requests(self,item,info):
        self.default_headers[':path'] = item['PicFullUrl']
        self.default_headers['referer'] = item['referer']
        yield scrapy.Request(item['PicFullUrl'], headers=self.default_headers)

    def item_completed(self,results,item,info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['PicLocalPath'] = image_paths

        return item








class Mongo_getUrl_Pipline(object):
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
        item['PicSize'] = 0
        b = str(int(time.time() * 1000000))
        item['_id'] = b + ''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ', 10))

        collName = item['collName']
        del item['collName']

        self.db[collName].insert(dict(item))
        pprint.pprint(item)
        print('--------------------------------------------------录入成功')
        return item

    def close_spider(self, spider):
        self.client.close()