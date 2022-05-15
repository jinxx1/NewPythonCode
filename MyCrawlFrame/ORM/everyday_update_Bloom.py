# -*- coding: utf-8 -*-
import pprint
import sys, os

import sqlalchemy, re
from sqlalchemy import create_engine, Column, Integer, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import json
import datetime
import asyncio
from sqlalchemy.dialects import mysql
from redis_dup import BloomFilter

bl = BloomFilter('uxue:url')
# jsoninfo = {
# 	"uxuepai_sql": {"HOST": "183.6.136.67", "DBNAME": "uxsq", "USER": "jinxiao_67", "PASSWORD": "Qwer1234AQ", "PORT": 3306},
# 	"local_sql": {"HOST": "localhost", "DBNAME": "uxsq", "USER": "root", "PASSWORD": "040304", "PORT": 3306}
# }
with open('../mysqlInfo.json', 'r') as ff:
	jsoninfo = json.load(ff)
mysqlJson = jsoninfo['uxuepai_sql']


def to_dict(self):
	return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


def mysqlcontnect(dbName):
	if dbName != 'uxuepai_sql' and dbName != 'local_sql':
		raise 'pls input uxuepai_spl or local_sql'
	with open('../mysqlInfo.json', 'r') as ff:
		jsoninfo = json.load(ff)
	MYSQLINFO1 = jsoninfo[dbName]
	conStr1 = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO1['USER'],
	                                                                                            PASSWORD=MYSQLINFO1[
		                                                                                            'PASSWORD'],
	                                                                                            HOST=MYSQLINFO1['HOST'],
	                                                                                            PORT=MYSQLINFO1['PORT'],
	                                                                                            DBNAME=MYSQLINFO1[
		                                                                                            'DBNAME'])
	mysqlcon1 = sqlalchemy.create_engine(conStr1, pool_pre_ping=True, pool_size=100)
	return mysqlcon1


class CCGPmysql(object):

	def __init__(self, baseName):
		self.MYSQLCON = mysqlcontnect(baseName)
		self.Base_automap_base = automap_base()
		self.Base_automap_base.prepare(self.MYSQLCON, reflect=True)
		self.Base_keys = self.Base_automap_base.classes.keys()
		self.session_fac = sessionmaker(bind=self.MYSQLCON)
		self.session = self.session_fac()

	def __sessionClose__(self):
		self.session.close()

	def add_table(self, tableName, ddict):
		info = tableName(**ddict)
		try:
			self.session.add(info)
			self.session.commit()
		except Exception as ff:
			print(ff)
			self.session.rollback()

	def get_Info_List(self, tableName, stratid=0, count=100, num=None):
		if count == 0:
			count = 1
		if not num:
			query_all = self.session.query(tableName).order_by(tableName.id)[stratid:count]
			return [to_dict(x) for x in query_all]
		else:
			query_all = self.session.query(tableName).filter(tableName.id > num)[stratid:count]
			return [to_dict(x) for x in query_all]

	def get_ztbInfo_url_all(self, count=None):
		if not count:
			getNO1_id = self.session.query(self.ztbrawinfo.page_url).all()
		else:
			getNO1_id = self.session.query(self.ztbrawinfo.page_url)[0:count]
		return [x[0] for x in getNO1_id if x]


class uxue_mysql(CCGPmysql):
	def __init__(self):
		baseName = 'uxuepai_sql'
		super(uxue_mysql, self).__init__(baseName)
		self.ztbrawinfo = self.Base_automap_base.classes.ztbRawInfo
		self.ztbrawinfocontent = self.Base_automap_base.classes.ztbRawInfoContent
		self.ztb_raw_info_attached = self.Base_automap_base.classes.ztb_raw_info_attached
		self.ztbinfoattachment = self.Base_automap_base.classes.ztbInfoAttachment
		self.ztbhubinfo = self.Base_automap_base.classes.ztbhubinfo


class local_mysql(CCGPmysql):
	def __init__(self):
		baseName = 'local_sql'
		super(local_mysql, self).__init__(baseName)
		self.ztbrawinfo = self.Base_automap_base.classes.ztbrawinfo
		self.ztbrawinfocontent = self.Base_automap_base.classes.ztbrawinfocontent
		self.ztb_raw_info_attached = self.Base_automap_base.classes.ztb_raw_info_attached
		self.ztbinfoattachment = self.Base_automap_base.classes.ztbinfoattachment
		self.ztbhubinfo = self.Base_automap_base.classes.ztbhubinfo


def local_TongBu_uxue_ztbRawInfo():
	uxueOBJ = uxue_mysql()
	localOBJ = local_mysql()
	for i in range(1000):
		local_newest_id1 = \
		localOBJ.session.query(localOBJ.ztbrawinfo.id).order_by(localOBJ.ztbrawinfo.id.desc())[0:1][0][0]
		print(local_newest_id1)
		getInfo = uxueOBJ.get_Info_List(tableName=uxueOBJ.ztbrawinfo, num=local_newest_id1, count=10000)
		for info in getInfo:
			if info:
				localOBJ.add_table(tableName=localOBJ.ztbrawinfo, ddict=info)
			else:
				continue

		local_newest_id2 = \
		localOBJ.session.query(localOBJ.ztbrawinfo.id).order_by(localOBJ.ztbrawinfo.id.desc())[0:1][0][0]
		print(local_newest_id2)
		if local_newest_id1 == local_newest_id2:
			break
		print('---------------------', i)
	uxueOBJ.__sessionClose__()
	localOBJ.__sessionClose__()


def main():
	uxue_obj = uxue_mysql()
	today = datetime.date.today()
	yestoday = today - datetime.timedelta(days=1)
	print(today, yestoday)
	a = uxue_obj.session.query(uxue_obj.ztbrawinfo.page_url).filter(uxue_obj.ztbrawinfo.creation_time <= today).filter(
		uxue_obj.ztbrawinfo.creation_time >= yestoday).order_by(uxue_obj.ztbrawinfo.creation_time.desc()).all()
	print(len(a))
	for i in a:
		if bl.exists(i[0]):
			continue
		else:
			bl.insert(i[0])
	print('end')


if __name__ == '__main__':
	main()
	exit()
	from apscheduler.schedulers.blocking import BlockingScheduler
	import os

	sched = BlockingScheduler()
	sched.add_job(main, 'cron', hour=3, minute=1)
	sched.start()
