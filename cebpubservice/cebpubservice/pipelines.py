# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql



class CebpubserviceMYSQLPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):

        self.db = pymysql.connect(self.host, self.user, self.password, self.database, port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        keysWord = ""
        valueWord = ""
        insert_code = ""

        inser_excut = insert_code.format(
            summary = pymysql.escape_string(item['summary']),
            body = pymysql.escape_string(item['body']),
            programa_dictionaries = item['programa_dictionaries'],
            subtopic_dictionaries = item['subtopic_dictionaries'],
            publishTime = pymysql.escape_string(item['publishTime']),
            source = pymysql.escape_string(item['source']),
            title = pymysql.escape_string(item['title']),
            url = pymysql.escape_string(item['url']),
            created = pymysql.escape_string(TTime),
            updated = pymysql.escape_string(TTime),
            staticPath = pymysql.escape_string(item['staticPath']),
            cover = pymysql.escape_string(item['cover'])
        )
        # self.cursor.execute(inser_excut)
        # self.db.commit()



        return item


class CebpubservicePipeline:
    def process_item(self, item, spider):
        return item
