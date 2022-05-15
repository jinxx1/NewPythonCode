# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import datetime
import pymysql
from gc_project.db_helper import insert_mysql,MysqlPool
from concurrent.futures import ThreadPoolExecutor


m = MysqlPool()


class GcProjectPipeline:
    def __init__(self) -> None:
        super().__init__()
        self.id = 0

    def process_item(self, item, spider):
        if item.get('page_url') != None:
            now_time = datetime.datetime.now()
            if item.get('business_type') == None:
                item['business_type'] = ''
            if item.get('city_name') == None:
                item['city_name'] = ''
            if item.get('purchase_type') == None:
                item['purchase_type'] = ''
            sql = "INSERT INTO ztbRawInfoStatistics (subclass,site,page_url,title,issue_time,creation_time,end_time,business_type,city_name,purchase_type) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                  % (item['subclass'], item['site'], item['page_url'], item['title'], item['issue_time'], now_time,
                     now_time,item['business_type'],item['city_name'],item['purchase_type'])
            self.id = m.insert(sql)
            print('save MySQL-------', self.id)
            # if self.id != None:
            #     c = pymysql.escape_string(item['content'])
            #     sql_1 = "INSERT INTO ztbRawInfoContent (raw_data_id,content) VALUES (%s,'%s')" % (self.id, c)
            #     pool.submit(insert_mysql, sql_1)
            # if self.id != None and item.get('download_url') != None and item.get('name') != None:
            #     sql_2 = "INSERT INTO ztbInfoAttachment (raw_id,download_url,name,status) VALUES (%s,'%s','%s',%s)" % (
            #         self.id, item['download_url'], item['name'], 0)
            #     pool.submit(insert_mysql, sql_2)
            #     print('插入附件表！！！！！！！！！！！！！！！1')
        return item
