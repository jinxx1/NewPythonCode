# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import main
top_drib = main.TOP_DRIB

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from pymysql.converters import escape_string
import logging
MYSQLINFO = {
    "HOST": "localhost",
    "DBNAME": "uxsq",
    "USER": "root",
    "PASSWORD": "",
    "PORT":3306,
    "DABSE":"uxsq"
}
MYSQL_SET = MYSQLINFO
HOST = MYSQL_SET["HOST"]
USER = MYSQL_SET["USER"]
DABSE = MYSQL_SET["DABSE"]
PAW = MYSQL_SET["PASSWORD"]

class GxzhengfuPipeline:
    s = 0
    def open_spider(self,spider):
        self.conn = pymysql.connect(host=HOST, user=USER,db=DABSE,password=PAW)
        self.cursor = self.conn.cursor()
        spider.log("数据库连接成功"+"!"*30)
    def process_item(self, item, spider):
        spider.log("数据准备录入~~~~~~~~~~~~~~~~!")
        craw_status = 1
        status = 0
        sql = """INSERT INTO `ztbrawinfo` (`craw_status`,`subclass`, `site`, `page_url`, `title`, `issue_time`) VALUES ('{}', '{}', '{}', '{}', '{}','{}');"""
        check_sql = """SELECT * FROM ztbRawInfo o WHERE o.page_url = '{}' limit 1;"""
        self.cursor.execute(check_sql.format(item["page_url"]))
        data = self.cursor.fetchone()
        if data:
            self.s += 1
            if self.s == top_drib:
                spider.crawler.engine.close_spider(spider, "无有效信息，关闭spider")
                # sys.exit()
        elif not data:
            self.cursor.execute(sql.format(craw_status, str(item["subclass"]), str(item["site"]), item["page_url"], item["title"],item["issue_time"]))
            raw_id = self.conn.insert_id()
            print("数据录入info"+"-"*30)
            self.conn.commit()
            content = escape_string(str(item['content']))
            # print(content)
            sql_text = """INSERT INTO `ztbrawinfocontent` (`raw_data_id`, `content`) VALUES ('{}', '{}');"""
            self.cursor.execute(sql_text.format(raw_id, content))
            print("文本数据info"+"+"*30)
            self.conn.commit()

        # try:
            if item["download_url"]:
                for k,v in item["download_url"][0].items():
                    sql_flie = """INSERT INTO `ztbinfoattachment` (`raw_id`, `download_url`, `name`, `status`) VALUES ('{}', '{}', '{}', '{}');"""
                    self.cursor.execute(sql_flie.format(raw_id, v, k, status))
                    print("附件info"+"="*30)
                    self.conn.commit()
            logging.error(GxzhengfuPipeline)
       # except:
        #     print(item["title"]+'\n'+"无附件！！！！")
    def close_spider(self,spider):
        spider.log("爬虫执行完毕！！！")
        self.conn.close()
