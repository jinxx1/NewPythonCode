# -*- coding: utf-8 -*-
import datetime
from guangxiArtile.MongoTEST import *

MongoDB_ArticleInfo = MongoDB_guangxi_ArticleInfo()
MongoDB_ContentUrl = MongoDB_guangxi_ContentUrl()



# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class GuangxiartilePipeline(object):
    def process_item(self, item, spider):
        item['capturedTime'] = datetime.datetime.now()
        insertID = MongoDB_ArticleInfo.insertDB(item)
        MongoDB_ContentUrl.updateDB(item['url'])

        print(item['title'])
        print(item['url'])
        print(item['issueTime'])
        print(item['subclass'])
        print(len(item['content']))
        print(item['attachments'])
        print(item['capturedTime'])
        print('--------------------------------------------------------------------{}'.format(insertID))

        return item


