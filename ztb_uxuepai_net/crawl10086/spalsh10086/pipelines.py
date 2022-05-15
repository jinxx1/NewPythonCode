# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from spalsh10086.scrapyParse import *
import pprint

class Spalsh10086Pipeline(object):
    def process_item(self, item, spider):
        try:
            get_pageNum = item['get_pageNum']
            del item['get_pageNum']
        except Exception as e:
            get_pageNum = e

        a = save_api(item)
        item['content'] = len(item['content'])
        item['get_pageNum'] = get_pageNum
        pprint.pprint(item)

        print(a)
        print('------------------------')
        return item
