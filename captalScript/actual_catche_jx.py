# -*-  coding:utf-8 -*-
# @TIME :2019-12-12 09:28
# @Author : Richard
# @File :actual_catch.py

import time
import MySQLdb
import settings
import datetime
import ztbutils
import prjutils
import db2mongo
import os
import re
import json
import logging
import requests
import sys
import pprint

from apscheduler.schedulers.blocking import BlockingScheduler

actual_state = True
diffcounts = 0
counts = 0

DATABASE_SERVER = settings.DATABASES['default']['HOST']
DATABASE_PORT = int(settings.DATABASES['default']['PORT'])
DATABASE_USR = settings.DATABASES['default']['USER']
DATABASE_PASS = settings.DATABASES['default']['PASSWORD']
DATABASE_NAME = settings.DATABASES['default']['NAME']

# targetdir = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyTarget/'
# rpath = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyFile/'
# outputdir = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyOutput/'
# csvFile = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyOutput/' + outFile + '.csv'
# csvDetailFile = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyOutput/' + outFile + 'detail.csv'

targetdir = 'D:/jinxiaoDB/historyTarget/'
rpath = 'D:/jinxiaoDB/historyFile/'
outputdir = 'D:/jinxiaoDB/historyOutput/'


def load_attachments(title, info_id):
    objects = []
    sql = "select a.file_path, a.html_path, a.sole_uuid, a.sheet_name, b.name from ztbInfoAccessoryDocToHtml as a left join ztbInfoAttachment as b on a.info_attach_id=b.id where a.info_id = %s" % info_id
    try:
        print(sql)
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
                obj = db2mongo.Attachment()
                obj.filepath = record[0]
                obj.fileurl = db2mongo.URL_ROOT + record[2] + ".html"  # record[1]
                obj.sole_uuid = record[2]
                obj.sheetname = record[3]
                obj.name = record[4]
                objects.append(obj)
        cur.close()
        conn.commit()
        conn.close()
    except Exception as e:
        # logger.error("failed to select t:%s" % e)
        print(e)
    return objects


class ObjectValue:
    title = None
    content = None
    infodate = None
    site = None
    guild_id = None
    business_type = None
    minor_business_type = None
    infoId = None


def find_relate_ex(title, date_begin, date_end):
    # print('title',title)
    # print('date_begin', date_begin)
    # print('date_end', date_end)
    sql = "select a.page_title, b.content, a.purchase_date, a.site, a.guild_id, a.business_type, a.minor_business_type,a.id from ztbInfo as a left join ztbInfoContent as b on a.id = b.info_id where a.page_title LIKE '%%%s%%' AND a.purchase_date BETWEEN '%s' AND '%s'" % (
    title, date_begin, date_end)
    objs = mysql_query(sql)
    # print('objs1111111111111111',objs)
    print('actual ------96 -------objs', objs)
    # records = my_set.find({'$and':[{"publishedDate":{"$gte":date_begin}, "publishedDate":{"$lt":date_end}, "title" : {"$regex" : title}, }]}).sort([("publishedDate",1)])

    return objs


def process_obj(obj, rpath, obj_type=None, with_attachments=False):
    # 附件信息处理
    print('进入process_obj函数--------actual--104')
    objs = None
    newtitle = obj.title.replace("/", "-").replace(' ', '').replace('\t', '')
    if len(newtitle) >= 84:
        tlen = len(newtitle)
        newtitle = newtitle[:77] + newtitle[tlen - 6: tlen]
    filename = rpath + newtitle + ".txt"
    hfilename = rpath + newtitle + ".html"

    if obj is not None:
        html = obj.content
        # objs = process_html(html)
        if html is None:
            return None
        ztbutils.dumphtml(html, hfilename)
        # attachobjs = db2mongo.getattachments(obj['title'], obj['publishedDate'])

        attachobjs = db2mongo.load_attachments(obj.title, obj.infoId)
        print('--------actual--122------attachobjs', attachobjs)
        attachments = []
        candidates = []
        backup = []

        for attobj in attachobjs:
            logging.debug(attobj.filepath)
            # print(attobj)
            backup.append(attobj.fileurl)
            fnames = attobj.filepath.split('/')
            if len(fnames) > 0:
                # print(fnames)
                keyword = re.findall(ztbutils.KEYWORDS_FN, fnames[len(fnames) - 1])
                if len(keyword) == 0:
                    keyword = re.findall(ztbutils.KEYWORDS_FN, attobj.name)
                if len(keyword) > 0:
                    # print(attobj.filepath, attobj.fileurl, attobj.name, attobj.sheetname)
                    logging.info("got attach:%s %s %s" % (attobj.filepath, attobj.fileurl, attobj.sheetname))
                    if attobj.sheetname is not None and len(
                            attobj.sheetname) > 0 and not attobj.sheetname.lower().startswith('sheet'):
                        keyword = re.findall(ztbutils.KEYWORDS_FN, attobj.sheetname)
                        if len(keyword) > 0:
                            # print(attobj.sheetname)
                            logging.info("processing attach:%s" % attobj.sheetname)
                            attachments.append(attobj.fileurl)
                        else:
                            logging.info("skip attach:%s" % attobj.sheetname)
                            candidates.append(attobj.fileurl)
                    else:
                        attachments.append(attobj.fileurl)

        if len(candidates) == 1 and len(attachments) == 0:
            # print("add attach from candidate:%s" % candidates[0])
            attachments.append(candidates[0])
        if len(attachments) == 0 and len(backup) > 0:
            attachments.extend(backup)
        if len(attachments) == 0 and with_attachments:
            return None
        objs = ztbutils.process_url(None, attachments, html, obj.title, obj.infodate.strftime("%Y-%m-%d"), obj.infoId,
                                    obj_type)

        print('objs-----', objs)

        objs['business_type'] = obj.business_type
        objs['minor_business_type'] = obj.minor_business_type
        objs['site'] = obj.site
        objs['guild_id'] = obj.guild_id
        # objs['url'] = db2mongo.geturl(obj['title'], obj['publishedDate'])
        objs['purchase_method'] = ztbutils.getpurchasemethod(obj.title)
        print('actual ----- 170 -----objs')
        pprint.pprint(objs)
    return objs


def find_relate(title, publishedDate, seqmode):
    # title = ztbutils.process_biaoex(title,False,True,seqmode)
    # print('findRelate----------',title)
    date_begin = publishedDate + datetime.timedelta(days=-90)
    date_end = publishedDate + datetime.timedelta(days=90)
    # print('12345---------------',find_relate_ex(title, date_begin, date_end))
    return find_relate_ex(title, date_begin, date_end)


def mysql_query(sql):
    global diffcounts, counts
    if True:
        objects = []
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
            # print('records------',records)
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
                    obj.infoId = record[7]
                    obj.title = title.replace(' ', '')
                    obj.title = obj.title.replace('\t', '')
                    if title != obj.title:
                        diffcounts += 1
                    objects.append(obj)
            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
        print('objects:   ', objects)

        # for n in objects:
        #     print('n', n.title)
        #     print('n', n.infodate)
        #     print('n', n.site)
        #     print('n', n.guild_id)
        #     print('n', n.business_type)
        #     print('n', n.infoId)
        #     print('n', n.content)

        return objects


def mysql_query_newJson(sql):
    if True:
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
                    obj = ObjectValue()
                    obj.infodate = record[0] - 1
                    break
            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
        return obj


def actual_process(source):
    typeID = [1, 2, 3, 4]
    if source not in typeID:
        print('Have not input_id.Please input 1 or 2 or 3 or 4')
        return None
    del typeID

    try:
        fp = open('actual_id' + str(source) + '.json', 'r')
        data_back = json.load(fp)
        start_id = data_back['actual_id']
        fp.close()
    except:
        exc = "SELECT id FROM ztbInfo WHERE guild_id = {} ORDER BY created ASC LIMIT 1".format(source)
        objs = mysql_query_newJson(exc)

        with open('actual_id' + str(source) + '.json', 'w')as f:
            ddict = {}
            ddict['actual_id'] = str(objs.infodate)
            json.dump(ddict, f)
            f.close()
            del ddict
        start_id = ddict['actual_id']

    # sql = "select a.page_title, b.content, a.purchase_date, a.site, a.guild_id, a.business_type, a.minor_business_type,a.id from ztbInfo as a left join ztbInfoContent as b on a.id = b.info_id where a.id > %s and a.guild_id = %s LIMIT 10" % (int(start_id),source)
    sql = "select a.page_title, b.content, a.purchase_date, a.site, a.guild_id, a.business_type, a.minor_business_type,a.id from ztbInfo as a left join ztbInfoContent as b on a.id = b.info_id where a.id = %s and a.guild_id = %s" % (
    int(start_id), source)

    objs = mysql_query(sql)
    logging.info(sql)

    if len(objs) > 0:

        ret = []
        sknum = 0
        forcemode = False
        seqmode = False
        attachmode = False

        startId = objs[0].infoId
        endId = startId
        # endId = objs[len(objs) - 1].infoId
        outFile = str(startId) + '_' + str(endId) + '_' + str(source)

        if os.path.isfile(outputdir + outFile + '.csv'):
            print("file exists:%s" % (outputdir + outFile + '.csv'))
        else:
            prjutils.dumphead(outputdir, outFile)

        for num, obj in enumerate(objs):
            print('------------------------', num)
            curr = obj.infoId
            fp = open('curreList', 'a')
            fp.write(str(curr) + ',')
            fp.close()
            sknum += 1
            newtitle = obj.title.replace("/", "-").replace(' ', '').replace('\t', '')
            if len(newtitle) >= 84:
                tlen = len(newtitle)
                newtitle = newtitle[:77] + newtitle[tlen - 6: tlen]
            filename = rpath + newtitle + ".txt"
            hfilename = rpath + newtitle + ".html"

            # print('filename,forcemode',filename,forcemode)
            # print('filename,forcemode',os.path.isfile(filename))

            if os.path.isfile(filename) and not forcemode:
                print('if')
                print("%s exists" % filename)
                objs = ztbutils.readjson(filename)
                ret.append(objs)
            elif len(newtitle) >= 10:
                print('elif')
                print('obj.title', obj.title)
                subrecords = find_relate(obj.title, obj.infodate, seqmode)
                print('actual ---- 343 -----subrecords')
                for i in subrecords:
                    print(i)
                print('----346----end')

                # print(obj.infodate)
                # print(seqmode)
                print('subobj循环开始------------------------------------------------------------')
                for subobj in subrecords:
                    print('subobj', subobj)

                    subobjs = process_obj(subobj, rpath, None, attachmode)
                    # print('subobjs.infoId**************',subobj.infoId)
                    # print('str(curr)',curr)

                    fp = open('errorList', 'a')
                    fp.write('\n' + '-----' + str(curr))
                    fp.write('\n' + str(subobj.infoId))
                    fp.close()

                    # logging.info(subobj.infoId)
                    # print(subobj.infoId)
                    if subobjs is not None:
                        filename = rpath + ztbutils.filetitle(subobj.title) + ".txt"
                        ztbutils.dump2json(filename, subobjs)
                        ret.append(subobjs)
                objs = ret
                pprint.pprint(objs)
                print('actual------364------以上是 objs')

                while len(objs) > 0:
                    print('''actual------367----以下是 “while len(objs) > 0:”''')
                    v, objs = prjutils.parselist(objs, seqmode)

                    prjutils.dumpfiles([v], outFile, outputdir)


                    if targetdir is not None:
                        prj_name = v['project_name'].replace("/", "-").replace(' ', '').replace('\t', '')
                        print(prj_name)
                        if len(prj_name) >= 84:
                            prj_name = prj_name[0:77] + prj_name[len(prj_name) - 6:]
                        tfpath = os.path.join(targetdir, prj_name + ".json")
                        if os.path.isfile(tfpath):
                            print("file exists:%s" % tfpath)
                            continue
                        fp = open(tfpath, 'w')
                        try:
                            text = json.dumps(v, default=prjutils.json_default)
                            fp.write(text)
                        except Exception as e:
                            logging.error(e)
                            logging.error(prj_name)
                        fp.close()
            else:
                print('else')
                errorid = obj.infoId
                fp = open('errorList', 'a')
                fp.write(str(errorid) + ',')
                fp.close()

        url = 'http://ztb.uxuepai.net:9120/service/api/newInfoDataHandle/handleProjectAndPackageFile'
        csvFile = outputdir + outFile + '.csv'
        csvDetailFile = outputdir + outFile + 'detail.csv'
        csvsz = os.path.getsize(csvFile)

        detailsz = os.path.getsize(csvDetailFile)
        if int(csvsz) < 200:
            csv = None
        else:
            csv = open(csvFile, 'rb')
        if int(detailsz) < 300:
            csvDetail = None
        else:
            csvDetail = open(csvDetailFile, 'rb')

        exit()
        if csv != None and csvDetail != None:
            s = requests.session()
            s.keep_alive = False
            response = requests.post(url, files={'projectFile': csv, 'packFile': csvDetail})
        f = open('actual_id' + str(source) + '.json', 'r')
        data_back = json.load(f)
        f.close()
        f = open('actual_id' + str(source) + '.json', 'w')
        data_back['actual_id'] = str(endId)
        f.write(json.dumps(data_back))
        f.close()


if __name__ == "__main__":
    from test import del_file
    del_file()



    actual_process(2)


    # actual_process(1)

    # str1 = sys.argv[1]
    # while True:
    #    aa = actual_process(int(str1))
    #    del aa
    #    time.sleep(5)
    # scheduler = BlockingScheduler()
    # scheduler.add_job(actual_process, 'interval', args=(int(str1),),seconds=5)
    # scheduler.start()
    # actual_process(int(str1))
