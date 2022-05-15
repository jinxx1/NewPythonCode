#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import datetime
import bs4
from pymongo import MongoClient
from bs4 import BeautifulSoup
import db2mongo
LNUM = 100
def process_mongo(regex_str, begin_date, mdb = 'ztb', mset = 'ztb', mset2 = 'ztb2', sknum = 0, business_types = ".*"):
  print("rex:%s, date:%s, db:%s, set:%s, set2:%s, num:%s" % (regex_str, begin_date, mdb, mset, mset2, sknum))
  #date_time_str_en = '2018-10-01 00:00:00'
  date_time_obj_en = datetime.datetime.strptime(begin_date, '%Y-%m-%d')#(' %H:%M:%S')
  conn = MongoClient('127.0.0.1', 27017)
  db = conn[mdb]
  my_set = db[mset]
  my_set2 = db[mset2]
  ret = []
  #sknum = 0
  toRun = True
  while toRun:
   toRun = False
   records = my_set.find({'$and':[{"publishedDate":{"$gte":date_time_obj_en}, "title" : {"$regex" : regex_str}, "businessType":{"$regex":business_types}}]}).sort([("publishedDate",1)]).limit(LNUM).skip(sknum)
   for obj in records:
    sknum += 1
    toRun = True
    print(obj['title'])
    newobj = obj
    atts = ''
    attachments = db2mongo.load_attachments(obj['title'],obj['infoId'])
    for attachment in attachments:
        atts += attachment.filepath + str(attachment.name) + str(attachment.sheetname) + ":" 
    if len(atts) > 0:
        newobj['has_attachments'] = True
    else:
        newobj['has_attachments'] = False
    newobj['attachments'] = atts 
    html = obj['content']
    if html is not None:
      bsObj = BeautifulSoup(html)
      content = bsObj.text
      newobj['content'] = None
      newobj['plaintext'] = content
    my_set2.insert(newobj)

def dump_title(regex_str, begin_date, mdb, mset, dpath):
  date_time_obj_en = datetime.datetime.strptime(begin_date, '%Y-%m-%d')#(' %H:%M:%S')
  conn = MongoClient('127.0.0.1', 27017)
  db = conn[mdb]
  my_set = db[mset]
  fp = open(dpath,'w')
  sknum = 0
  toRun = True
  while toRun:
    toRun = False
    records = my_set.find({'$and':[{"publishedDate":{"$gte":date_time_obj_en}, "title" : {"$regex" : regex_str}}]}).sort([("publishedDate",1)]).limit(LNUM).skip(sknum)
    for obj in records:
      sknum += 1
      toRun = True
      print(obj['title'])
      fp.write(obj['title'] + '\n')
  fp.close()


def dump_attach_title(regex_str, begin_date, mdb, mset, dpath):
  date_time_obj_en = datetime.datetime.strptime(begin_date, '%Y-%m-%d')#(' %H:%M:%S')
  conn = MongoClient('127.0.0.1', 27017)
  db = conn[mdb]
  my_set = db[mset]
  fp = open(dpath,'w')
  sknum = 0
  toRun = True
  while toRun:
    toRun = False
    records = my_set.find({"$and":[{'has_attachments': {'$eq': True}},{"attachments" : {"$regex" : regex_str}}]}).sort([("publishedDate",1)]).limit(LNUM).skip(sknum)
    for obj in records:
      sknum += 1
      toRun = True
      print(obj['title'])
      print(obj['attachments'])
      fp.write(obj['title'] + '\n')
  print("got title:%d" % sknum)
  fp.close()

if __name__ == "__main__":
  if sys.argv[1] == '2mongo':
    process_mongo(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]) 
  elif sys.argv[1] == '2file':
    dump_title(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
  elif sys.argv[1] == 'attach':
    dump_attach_title(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
