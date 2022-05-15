import pprint
import pymysql
import time
from datetime import datetime
from ggzy.settings import MYSQLINFO
from uxue_orm import *
mysql_db_orm = mysql_orm()


try:
    from pymysql.converters import escape_string
except:
    from pymysql import escape_string


from ggzy.redis_dup import BloomFilter
bl = BloomFilter('uxue:url')

class MysqlPipLine():
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
        self.db = pymysql.connect(host=self.host, user=self.user, passwd=self.password, db=self.database, port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self,item,spider):
        ztbHubInfo_obj = ZtbHubInfo()
        item['creation_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['end_time'] = item['creation_time']
        item['craw_status'] = 1

        ztbHubInfo_obj.issue_time = item['issue_time']
        ztbHubInfo_obj.subclass = item['subclass']
        ztbHubInfo_obj.site = item['site']
        ztbRawInfo_insert_id = mysql_db_orm.ztbRawInfo_add_single(hubInfo=ztbHubInfo_obj, articleInfo=item)
        if not ztbRawInfo_insert_id:
            return None
        mysql_db_orm.ztbRawInfoContent_add_single(content=item['content'], rawid=ztbRawInfo_insert_id)
        if 'attchment' in item.keys():
            attchment = []
            for i in item['attchment']:
                ddict = {}
                ddict['download_url'] = i['download_url']
                ddict['download_filename'] = i['name']
                attchment.append(ddict)
            mysql_db_orm.ztbInfoAttaChment_add_single(info=attchment, rawid=ztbRawInfo_insert_id)

        # print('录入info--------------')
        #
        # item['raw_data_id'] = self.insert_ztbRawInfo_getID(item)
        #
        # item['raw_id'] = item['raw_data_id']
        #
        #
        # # print('录入content--------------')
        # self.insert_ztbRawInfoContent_getID(item)
        #
        # # print('录入attchment--------------')
        # self.insert_ztbInfoAttachment(item)
        #
        # self.insert_ztb_raw_info_attached(item)

        item['content'] = len(item['content'])
        import pprint
        pprint.pprint(item)
        print('-------------------------------已经录入成功')
        bl.insert(item['page_url'])
        return item

    def insert_ztbRawInfo_getID(self,item):
        comparisonKeys = ('subclass', 'site', 'page_url', 'title', 'issue_time', 'creation_time', 'end_time')
        keysList = [i for i in item.keys() if i in comparisonKeys]

        valueList = ["'" + item[i].replace('%','%%') + "'" for i in keysList]
        keys = ','.join(keysList)+ ',craw_status'
        valuesall = ','.join(valueList) + ',1'
        exc = "insert into ztbRawInfo ({keys}) values ({valuesall});".format(keys=keys,valuesall=valuesall)
        self.db.ping(reconnect=True)
        self.cursor.execute(exc)
        primaryID = self.db.insert_id()
        self.db.commit()
        return str(primaryID)

    def insert_ztbRawInfoContent_getID(self, item):
        exc = '''insert into ztbRawInfoContent (raw_data_id,content) values ({raw_data_id},"{content}");'''.format(raw_data_id=item['raw_data_id'],
                                content=escape_string(item['content']))


        self.db.ping(reconnect=True)
        self.cursor.execute(exc)
        self.db.commit()

    def insert_ztbInfoAttachment(self, item):

        if 'attchment' not in item.keys():
            return item
        for i in item['attchment']:
            exc = "insert into ztbInfoAttachment (raw_id,download_url,name,status) values ({raw_id},'{download_url}','{name}',0);".format(
                raw_id=item['raw_id'],
                download_url=escape_string(i['download_url'].replace('%','%%')),
                name=escape_string(i['name'].replace('%','%%')))
            self.db.ping(reconnect=True)
            self.cursor.execute(exc)
            self.db.commit()

    def insert_ztb_raw_info_attached(self, item):
        tempDict = {}
        publickey = ('business_type','source','province_name','industry')

        for keyName in publickey:
            try:
                if item[keyName]:
                    tempDict[keyName] = item[keyName]
            except:
                pass
        if not tempDict:
            return None
        for keyName in tempDict.keys():
            exc = "INSERT INTO ztb_raw_info_attached (raw_info_id,tag_key,tag_value,created) VALUES ({raw_info_id},'{tag_key}','{tag_value}','{created}');"
            self.db.ping(reconnect=True)
            self.cursor.execute(exc.format(
                raw_info_id=item['raw_data_id'],
                tag_key=escape_string(keyName.replace('%','%%')),
                tag_value=escape_string(tempDict[keyName].replace('%','%%')),
                created=item['creation_time'],
            ))
            self.db.commit()

class GgzyPipeline:
    def process_item(self, item, spider):
        return item