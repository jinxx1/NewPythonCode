# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from pymysql.converters import escape_string
import logging

MYSQLINFO = {
    "HOST": "127.0.0.1",
    "DBNAME": "uxsq",
    "USER": "root",
    "PASSWORD": "",
    "PORT":3306
}
MYSQL_SET = MYSQLINFO
HOST = MYSQL_SET["HOST"]
USER = MYSQL_SET["USER"]
DABSE = MYSQL_SET["DBNAME"]
PAW = MYSQL_SET["PASSWORD"]

class GxzhengfuPipeline:
    def open_spider(self,spider):
        self.conn = pymysql.connect(host=HOST, user=USER,db=DABSE,password=PAW)
        self.cursor = self.conn.cursor()
        spider.log("数据库连接成功"+"!"*30)
    def process_item(self, item, spider):
        spider.log("数据准备录入~~~~~~~~~~~~~~~~!")
        craw_status = 1
        status = 0
        sql = """INSERT INTO `ztbRawInfo` (`craw_status`,`subclass`, `site`, `page_url`, `title`, `issue_time`) VALUES ('{}', '{}', '{}', '{}', '{}','{}');"""
        check_sql = """SELECT * FROM ztbRawInfo o WHERE o.page_url = '{}' limit 1;"""
        self.cursor.execute(check_sql.format(item["page_url"]))
        data = self.cursor.fetchone()
        if not data:
            self.cursor.execute(sql.format(craw_status, str(item["subclass"]), str(item["site"]), item["page_url"], item["title"],item["issue_time"]))
            raw_id = self.conn.insert_id()
            print("数据录入info"+"-"*30)
            self.conn.commit()
            content = escape_string(str(item['content']))
            # print(content)
            sql_text = """INSERT INTO `ztbRawInfoContent` (`raw_data_id`, `content`) VALUES ('{}', '{}');"""
            self.cursor.execute(sql_text.format(raw_id, content))
            print("文本数据info"+"+"*30)
            self.conn.commit()

        # try:
            if item["download_url"]:

                    for k,v in item["download_url"][0].items():
                        check_sql = """SELECT * FROM ztbInfoAttachment o WHERE o.download_url = '{}' limit 1;"""
                        self.cursor.execute(check_sql.format(v))
                        data_download_url = self.cursor.fetchone()
                        if not data_download_url:
                            sql_flie = """INSERT INTO `ztbInfoAttachment` (`raw_id`, `download_url`, `name`, `status`) VALUES ('{}', '{}', '{}', '{}');"""
                            self.cursor.execute(sql_flie.format(raw_id, v, k, status))
                            print("附件info"+"="*30)
                            self.conn.commit()
            logging.error(GxzhengfuPipeline)
       # except:
        #     print(item["title"]+'\n'+"无附件！！！！")
    def close_spider(self,spider):
        spider.log("爬虫执行完毕！！！")
        self.conn.close()
