# -*- coding: utf-8 -*-
import pymysql
import pymongo
import datetime,time,pprint,random
b = datetime.datetime.now().strftime("%Y-%m-%d")
nowTime = datetime.datetime.strptime(b, "%Y-%m-%d")
strnowTime = str(nowTime).split(' ')[0]

MYSQLINFO = {
    "HOST": "120.24.4.84",
    "DBNAME": "crawlURL",
    "USER": "xey",
    "PASSWORD": "85f0a9e2e63b47c0b56202824195fb70#AAA",
    "PORT":3306
}

MONGO_INFO = {'MongoClient':'mongodb://localhost:27017/',
    'MongoDBname':'ztb'}

class MYSQLDB():
    db = pymysql.connect(host=MYSQLINFO['HOST'], port=MYSQLINFO['PORT'], user=MYSQLINFO['USER'],
                           passwd=MYSQLINFO['PASSWORD'], db=MYSQLINFO['DBNAME'])

    def closeDB(self):
        self.db.close()

    def get_someInfo(self):
        cursor = self.db.cursor()
        # sqlCode = '''SELECT * FROM chinaUniconUrl where remark=0 and issueTime="{}"'''.format(strnowTime)
        sqlCode = '''SELECT * FROM chinaUniconUrl where remark=0'''
        cursor.execute(sqlCode)
        seeAll = cursor.fetchall()
        llist = []
        for i in seeAll:
            ddict ={}
            ddict['sql_id'] = i[0]
            ddict['site'] = i[1]
            ddict['domain'] = i[2]
            ddict['from_Page'] = i[4]
            # ddict['issueTime'] = datetime.datetime.strptime(i[5], "%Y-%m-%d")
            ddict['issueTime'] = i[5] + " 00:00:00"
            ddict['subclass'] = i[6]
            ddict['title'] = i[7]
            ddict['url'] = i[8]
            ddict['capturedTime'] = datetime.datetime.now()
            ddict['couchdb_id'] = ''
            ddict['mongoContent_id'] = ''
            ddict['insert_status'] = 0
            llist.append(ddict)
        cursor.close()
        return llist

    def update_remark(self,item):
        cursor = self.db.cursor()
        sqlCode = '''UPDATE chinaUniconUrl set remark=1 where id={}'''.format(item['sql_id'])
        cursor.execute(sqlCode)
        self.db.commit()
        cursor.close()


class MongoDB_obj(object):
    myclinent = pymongo.MongoClient(MONGO_INFO['MongoClient'])
    db = myclinent[MONGO_INFO['MongoDBname']]

    def insert_mongo(self,item):
        b = str(int(time.time() * 1000000))
        item['_id'] = b + 'MongoDB' + '_' + ''.join(random.sample('zyxwvutsrqponmlkjih0123456789gfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ', 15))
        self.db['monitorUrl'].insert_one(dict(item))
    def closeMongo(self):
        self.myclinent.close()


if __name__ == "__main__":
    mysqldb = MYSQLDB()
    mongodb = MongoDB_obj()
    for info in mysqldb.get_someInfo():
        mongodb.insert_mongo(info)
        mysqldb.update_remark(info)

    mongodb.closeMongo()
    mysqldb.closeDB()

