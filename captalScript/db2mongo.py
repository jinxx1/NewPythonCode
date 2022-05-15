import MySQLdb
from pymongo import MongoClient
import re
import sys
import settings
import datetime

DATABASE_SERVER = settings.DATABASES['default']['HOST']
DATABASE_PORT = int(settings.DATABASES['default']['PORT'])
DATABASE_USR = settings.DATABASES['default']['USER']
DATABASE_PASS = settings.DATABASES['default']['PASSWORD']
DATABASE_NAME = settings.DATABASES['default']['NAME']
diffcounts = 0
counts = 0


class ObjectValue:
    title = None
    content = None
    infodate = None
    site = None
    guild_id = None
    business_type = None
    minor_business_type = None


class Attachment:
    # filename = None
    filepath = None
    fileurl = None
    sole_uuid = None
    sheetname = None
    name = None


# URL_ROOT = "http://192.168.1.2:8075/infoContent/"

URL_ROOT = "http://183.6.136.67:8075/infoContent/"


def load_attachments(title, info_id):
    objects = []
    sql = "select a.file_path, a.html_path, a.sole_uuid, a.sheet_name, b.name from ztbInfoAccessoryDocToHtml as a left join ztbInfoAttachment as b on a.info_attach_id=b.id where a.info_id = %s" % info_id
    try:

        mongoconn = MongoClient('0.0.0.0', 27017)
        # mongoconn = MongoClient('localhost', 27017)
        db = mongoconn.ztb
        my_set = db.ztbattachment

        conn = MySQLdb.connect(
            host=DATABASE_SERVER,
            port=DATABASE_PORT,
            user=DATABASE_USR,
            passwd=DATABASE_PASS,
            db=DATABASE_NAME,
            charset="utf8"
        )
        cur = conn.cursor()

        ret = cur.execute(sql)

        records = cur.fetchall()

        print('db2mongo----59-------------------', records)
        if ret:
            for record in records:
                obj = Attachment()
                obj.filepath = record[0]
                obj.fileurl = URL_ROOT + record[2] + ".html"  # record[1]
                obj.sole_uuid = record[2]
                obj.sheetname = record[3]
                obj.name = record[4]
                newobj = {"title": title, "infoId": info_id, "filepath": obj.filepath, "url": obj.fileurl,
                          "uuid": obj.sole_uuid, "sheetname": obj.sheetname, "name": obj.name}
                my_set.insert(newobj)
                objects.append(obj)
        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        # logger.error("failed to select t:%s" % e)
        print(e)
    return objects


def getinfoId(title, issueDate, like=False):
    info_id = None
    sql = None
    if like:
        sql = "select id from ztbInfo where page_title like '%s%s%s' order by abs(datediff(purchase_date,'%s'))" % (
        '', title, '%', issueDate)
    else:
        sql = "select id from ztbInfo where page_title = '%s' order by abs(datediff(purchase_date,'%s'))" % (
        title, issueDate)
    try:
        conn = MySQLdb.connect(
            host=DATABASE_SERVER,
            port=DATABASE_PORT,
            user=DATABASE_USR,
            passwd=DATABASE_PASS,
            db=DATABASE_NAME,
            charset="utf8"
        )
        cur = conn.cursor()

        ret = cur.execute(sql)

        records = cur.fetchall()
        if ret:
            for record in records:
                info_id = record[0]
                break
        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        # logger.error("failed to select t:%s" % e)
        print(e)
    return info_id


def getattachments(title, issueDate):
    ret = []
    info_id = getinfoId(title, issueDate)
    if info_id:
        print("find info:%s" % info_id)
        attachments = load_attachments(title, info_id)
        return attachments
        # for attach in attachments:
        #   ret.append(attach.fileurl) 
    return ret


URL = "http://ztb.uxuepai.net:8075/bidc/#/tender/tenderDetail?dataObj="


def geturl(title, issueDate):
    infoId = getinfoId(title, issueDate, True)
    url = URL + str(infoId)
    return url


def mysql_query(sql, mdb='ztb', mset='ztb'):
    global diffcounts, counts
    if True:
        objects = []
        try:
            mongoconn = MongoClient('127.0.0.1', 27017)
            db = mongoconn[mdb]
            my_set = db[mset]
            conn = MySQLdb.connect(
                host=DATABASE_SERVER,
                port=DATABASE_PORT,
                user=DATABASE_USR,
                passwd=DATABASE_PASS,
                db=DATABASE_NAME,
                charset="utf8"
            )
            cur = conn.cursor()

            ret = cur.execute(sql)

            records = cur.fetchall()
            if ret:
                for record in records:
                    counts += 1
                    obj = ObjectValue()
                    title = record[0]
                    obj.content = record[1]
                    obj.infodate = record[2]
                    obj.site = record[3]
                    obj.guild_id = record[4]
                    obj.business_type = record[5]
                    obj.minor_business_type = record[6]
                    infoId = record[7]
                    obj.title = title.replace(' ', '')
                    obj.title = obj.title.replace('\t', '')
                    if title != obj.title:
                        diffcounts += 1
                        # print(title)
                    newobj = {"infoId": infoId, "title": obj.title, "content": obj.content,
                              "publishedDate": obj.infodate, "site": obj.site, "guild_id": obj.guild_id,
                              "businessType": obj.business_type, "minorBusinessType": obj.minor_business_type}
                    my_set.insert(newobj)
                    # objects.append(obj)
            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            # logger.error("failed to select t:%s" % e)
            print(e)
        return objects
    return None


def mongo_insert(objs, mdb='ztb', mset='ztb'):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn[mdb]
    my_set = db[mset]
    for obj in objs:
        newobj = {"title": obj.title, "content": obj.content, "publishedDate": obj.infodate}
        my_set.insert(newobj)


MDB = 'ztb'
MSET = 'ztb'


def load_obj(date, sites, source):
    ss = sites.split(",")
    site = "'" + ss[0] + "'"
    for i in range(1, len(ss)):
        site += ",'" + ss[i] + "'"
    sql = "select a.page_title, b.content, a.purchase_date, a.site, a.guild_id, a.business_type, a.minor_business_type,a.id from ztbInfo as a left join ztbInfoContent as b on a.id = b.info_id where a.purchase_date >= '%s'" % date
    if sites != "*":
        sql += " and a.site in (%s)" % site
    if source != "*":
        sql += " and a.purchase_source = %s" % source
    print(sql)
    objs = mysql_query(sql, MDB, MSET)
    print("%d records, %d different" % (counts, diffcounts))
    # print(objs)
    # mongo_insert(objs)


def load_attachments_test(info_id):
    sql = "select id from ztbInfoAccessoryDocToHtml where info_id = %s" % info_id
    conn = MySQLdb.connect(
        host=DATABASE_SERVER,
        port=DATABASE_PORT,
        user=DATABASE_USR,
        passwd=DATABASE_PASS,
        db=DATABASE_NAME,
        charset="utf8"
    )
    cur = conn.cursor()
    cur.execute(sql)

    records = cur.fetchall()

    return records


def load_ztbinfo_2_test():
    # sql = "select id from ztbInfo limit 100"
    sql = "select id from ztbInfo WHERE guild_id = 2"

    conn = MySQLdb.connect(
        host=DATABASE_SERVER,
        port=DATABASE_PORT,
        user=DATABASE_USR,
        passwd=DATABASE_PASS,
        db=DATABASE_NAME,
        charset="utf8"
    )
    cur = conn.cursor()
    cur.execute(sql)

    records = cur.fetchall()
    a = list(x[0] for x in records)

    return a


if __name__ == "__main__":

    infoid = load_ztbinfo_2_test()
    print(len(infoid))
    for n in infoid:
        # print(n)
        aa = load_attachments_test(str(n))
        if len(aa) > 0:
            print(n)
            print('------------------------')
    # aa = load_attachments_test(str(2618475))
    # print(len(aa))

# default_sites = "b2b.10086.cn,www.chinaunicombidding.cn,caigou.chinatelecom.com.cn,www.tower.com.cn,txzb.miit.gov.cn"
# sites = default_sites
# qdate = datetime.datetime.now().strftime("%Y-%m-%d")
# if len(sys.argv) > 5:
#   source = sys.argv[5]
# if len(sys.argv) > 4:
#   MSET = sys.argv[4]
# if len(sys.argv) > 3:
#   MDB = sys.argv[3]
# if len(sys.argv) > 2:
#   sites = sys.argv[2]
# if len(sys.argv) > 1:
#   qdate = sys.argv[1]
# load_obj(qdate, sites, source)
