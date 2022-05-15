# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pprint
from shangQing.items import ShangqingItem, ShangqingHubItem, ShangqingArticleItem
from uxue_orm import *
import datetime

mysqlSession = mysql_orm()


class ShangqingPipeline:
    def process_item(self, item, spider):

        if isinstance(item, ShangqingItem) or isinstance(item, ShangqingArticleItem):
            item['create_time'] = datetime.datetime.now()
            insert_id = mysqlSession.insertInfo(articleInfo=item, hubid=item['hubid'])
            item['content'] = len(item['content'])
            pprint.pprint(item)
            print('录入完毕，生成的ID为：',insert_id)
            print('----------------------------------------')
            return item



        if isinstance(item, ShangqingHubItem):
            insert_id = mysqlSession.ztbhubinfo_insert(item=item)
            pprint.pprint(item)
            print('----------------------------------------录入完毕，生成的ID为：', insert_id)
            return item
