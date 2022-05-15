# -*- coding: utf-8 -*-
from newscrapy.scrapyParse import *
import json,time
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class NewscrapyPipeline(object):
    def process_item(self, item, spider):
        # print('进入PIPELINES')
        contentNum = 'xx'
        pageNum = 'xx'
        if 'pageNum' and 'contentNum' in item.keys():
            contentNum = item['contentNum']
            pageNum = item['pageNum']
            del item['pageNum']
            del item['contentNum']
        if item:
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(nowTime)
            # print('即将录入数据库')
            # insertmysql = save_api(item)
            #
            # if insertmysql['msg'] != 'success':
            #     item['content'] = len(item['content'])
            #     item['msg'] = insertmysql['msg']
            #     item['errortime'] = nowTime
            #     print('error')
            #     print(item['msg'])
            #     print('第{}页，文章{}篇'.format(pageNum,contentNum))
            #     print('error_end')
            #     print('-----------------------------')
            # else:
            #     print(nowTime)
        return item

