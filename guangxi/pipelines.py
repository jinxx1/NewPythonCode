# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
from lxml import etree
from lxml import html
import pymysql
class GuangxiPipeline:
    def process_item(self, item, spider):
        sql = "INSERT INTO `uxsq`.`ztbrawinfo` (`site`, `page_url`, `subclass`, `title`, `issue_time`,) VALUES ('{}', '{}', '{}', '{}', '{}');"
        self.cursor.execute(sql.format(item["site"]["page_url"]["subclass"]["title"]["issue_time"]))
        self.conn.commit()
        raw_id = self.conn.insert_id()
        sql_text = "INSERT INTO `uxsq`.`ztbrawinfocontent` (`raw_data_id`, `content`) VALUES ('{}', '{}')"
        self.cursor(sql_text.format(raw_id,item['text']))
        self.conn.commit()
    def open_spider(self,spider):
        self.conn = pymysql.connect(host="localhost", user='root')
        self.cursor = self.conn.cursor()
    def close_spider(self,spider):
        self.conn.close()
