#-*-  coding:utf-8 -*-
#@TIME :2019-12-12 09:28
#@Author : Richard
#@File :actual_catch.py

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
actual_state = True
diffcounts = 0
counts = 0

DATABASE_SERVER = settings.DATABASES['default']['HOST']
DATABASE_PORT = int(settings.DATABASES['default']['PORT'])
DATABASE_USR = settings.DATABASES['default']['USER']
DATABASE_PASS = settings.DATABASES['default']['PASSWORD']
DATABASE_NAME = settings.DATABASES['default']['NAME']


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
    sql = "select a.page_title, b.content, a.purchase_date, a.site, a.guild_id, a.business_type, a.minor_business_type,a.id from ztbInfo as a left join ztbInfoContent as b on a.id = b.info_id where a.page_title LIKE '%%%s%%' AND a.purchase_date BETWEEN '%s' AND '%s'" % (title,date_begin,date_end)
    objs = mysql_query(sql)
  # records = my_set.find({'$and':[{"publishedDate":{"$gte":date_begin}, "publishedDate":{"$lt":date_end}, "title" : {"$regex" : title}, }]}).sort([("publishedDate",1)])

    return objs


def process_obj(obj, rpath, obj_type=None, with_attachments=False):
    objs = None
    newtitle = obj.title.replace("/","-").replace(' ','').replace('\t','')
    if len(newtitle) >= 84:
       tlen = len(newtitle)
       newtitle = newtitle[:77] + newtitle[tlen - 6: tlen]
    filename = rpath + newtitle + ".txt"
    hfilename = rpath + newtitle + ".html"
    if obj is not None:
      html = obj.content
      #objs = process_html(html)
      if html is None:
        return None
      ztbutils.dumphtml(html,hfilename)
      #attachobjs = db2mongo.getattachments(obj['title'], obj['publishedDate'])
      attachobjs = db2mongo.load_attachments(obj.title, obj.infoId)
      attachments = []
      candidates = []
      backup = []
      for attobj in attachobjs:
          logging.debug(attobj.filepath)
          print(attobj)
          backup.append(attobj.fileurl)
          fnames = attobj.filepath.split('/')
          if len(fnames) > 0:
              print(fnames)
              keyword = re.findall(ztbutils.KEYWORDS_FN,fnames[len(fnames)-1])
              if len(keyword) == 0:
                  keyword = re.findall(ztbutils.KEYWORDS_FN, attobj.name)
              if len(keyword) > 0:
                  print(attobj.filepath, attobj.fileurl, attobj.name, attobj.sheetname)
                  logging.info("got attach:%s %s %s" % (attobj.filepath, attobj.fileurl, attobj.sheetname))
                  if attobj.sheetname is not None and len(attobj.sheetname) > 0 and not attobj.sheetname.lower().startswith('sheet'):
                      keyword = re.findall(ztbutils.KEYWORDS_FN,attobj.sheetname)
                      if len(keyword) > 0:
                          print(attobj.sheetname)
                          logging.info("processing attach:%s" % attobj.sheetname)
                          attachments.append(attobj.fileurl)
                      else:
                          logging.info("skip attach:%s" % attobj.sheetname)
                          #candidates.append(attobj.fileurl)
                  else:
                      attachments.append(attobj.fileurl)
      if len(candidates) == 1 and len(attachments) == 0:
          print("add attach from candidate:%s" % candidates[0])
          attachments.append(candidates[0])
      if len(attachments) == 0 and len(backup) > 0:
          attachments.extend(backup)
      if len(attachments) == 0 and with_attachments:
          return None
      objs = ztbutils.process_url(None, attachments, html, obj.title, obj.infodate.strftime("%Y-%m-%d"),obj.infoId,obj_type)
      objs['business_type'] = obj.business_type
      objs['minor_business_type'] = obj.minor_business_type
      objs['site'] = obj.site
      objs['guild_id'] = obj.guild_id
      #objs['url'] = db2mongo.geturl(obj['title'], obj['publishedDate'])
      objs['purchase_method'] = ztbutils.getpurchasemethod(obj.title)
    return objs

def find_relate(title, publishedDate,seqmode):
  title = ztbutils.process_biaoex(title,False,True,seqmode)
  date_begin = publishedDate + datetime.timedelta(days=-90)
  date_end = publishedDate + datetime.timedelta(days=90)
  return find_relate_ex(title, date_begin, date_end)

def mysql_query(sql):
    global diffcounts,counts
    if True:
        objects = []
        try:
            conn= MySQLdb.connect(
            host=DATABASE_SERVER,
            port = DATABASE_PORT,
            user=DATABASE_USR,
            passwd=DATABASE_PASS,
            db =DATABASE_NAME,
            charset="utf8"
            )
            cur = conn.cursor()

            ret = cur.execute(sql)

            records=cur.fetchall()
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
                    obj.title = title.replace(' ','')
                    obj.title = obj.title.replace('\t','')
                    if title != obj.title:
                        diffcounts += 1
                    objects.append(obj)
            cur.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
        return objects
def actual_process():

    fp = open('history_id.json', 'r')
    data_back = json.load(fp)
    start_id = data_back['infoId']
    fp.close()

    sql = "select a.page_title, b.content, a.purchase_date, a.site, a.guild_id, a.business_type, a.minor_business_type,a.id from ztbInfo as a left join ztbInfoContent as b on a.id = b.info_id where a.id > %s LIMIT 10" % (int(start_id))

    print(sql)
    objs = mysql_query(sql)

    if len(objs) > 0:
        ret = []
        sknum = 0
        forcemode = False
        seqmode = False
        attachmode = False
        targetdir = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyTarget/'
        rpath = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyFile/'
        outputdir = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyOutput/'

        startId = objs[0].infoId
        endId = objs[len(objs) - 1].infoId
        outFile = str(startId) + '_' + str(endId)
        if os.path.isfile(outputdir + outFile + '.csv'):
            print("file exists:%s" % (outputdir + outFile + '.csv'))
        else:
            prjutils.dumphead(outputdir, outFile)

        for obj in objs:
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

            if os.path.isfile(filename) and not forcemode:
                print("%s exists" % filename)
                objs = ztbutils.readjson(filename)
                ret.append(objs)
            elif len(newtitle) >= 10:
                subrecords = find_relate(obj.title, obj.infodate, seqmode)
                for subobj in subrecords:
                    subobjs = process_obj(subobj, rpath, None, attachmode)
                    if subobjs is not None:
                        filename = rpath + ztbutils.filetitle(subobj.title) + ".txt"
                        ztbutils.dump2json(filename, subobjs)
                        ret.append(subobjs)
                objs = ret


                while len(objs) > 0:
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
                errorid = obj.infoId
                fp = open('errorList', 'a')
                fp.write(str(errorid) + ',')
                fp.close()

        url = 'http://ztb.uxuepai.net:9120/service/api/newInfoDataHandle/handleProjectAndPackageFile'
        csvFile = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyOutput/' + outFile + '.csv'
        csvDetailFile = '/media/terry/4f8380e6-1b3f-4715-97d7-e840b14a8443/historyOutput/' + outFile + 'detail.csv'
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

        if csv != None and csvDetail != None:
            s = requests.session()
            s.keep_alive = False
            response = requests.post(url, files={'projectFile': csv, 'packFile': csvDetail})
        f = open('history_id.json', 'w')
        data_back['infoId'] = str(endId)
        f.write(json.dumps(data_back))
        f.close()

if __name__ == "__main__":

    actual_process()

    # while True:
    #     aa = actual_process()
    #     del aa
    #     time.sleep(5)