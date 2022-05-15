# -*- coding: utf-8 -*-
import pprint
import sys

import sqlalchemy,re
from sqlalchemy import create_engine, Column, Integer, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import json
import datetime
import asyncio


with open('mysqlInfo.json', 'r', encoding='utf-8') as f:
	mysqlJson = json.load(f)


def to_dict(self):
	return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


def mysqlcontnect(MYSQLINFO1):
	conStr1 = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO1['USER'],
	                                                                                            PASSWORD=MYSQLINFO1[
		                                                                                            'PASSWORD'],
	                                                                                            HOST=MYSQLINFO1['HOST'],
	                                                                                            PORT=MYSQLINFO1['PORT'],
	                                                                                            DBNAME=MYSQLINFO1[
		                                                                                            'DBNAME'])
	mysqlcon1 = sqlalchemy.create_engine(conStr1, pool_pre_ping=True, pool_size=0)
	return mysqlcon1

class CCGPmysql(object):

	def __init__(self, baseName):
		if baseName == 'uxue':
			self.MYSQLCON = mysqlcontnect(mysqlJson['uxuepai_sql'])
		elif baseName == 'local':
			self.MYSQLCON = mysqlcontnect(mysqlJson['local_sql'])
		else:
			raise 'pls input baseName'
		self.Base_automap_base = automap_base()
		self.Base_automap_base.prepare(self.MYSQLCON, reflect=True)
		self.Base_keys = self.Base_automap_base.classes.keys()
		self.session_fac = sessionmaker(bind=self.MYSQLCON)
		self.session = self.session_fac()

	def add_Info(self, ddict):
		info = self.ztbrawinfo(**ddict)
		self.session.add(info)
		self.session.commit()

	def add_InfoContent(self, ddict):
		info = self.ztbrawinfocontent(**ddict)
		self.session.add(info)
		self.session.commit()

	def add_raw_Info_attached(self, ddict):
		info = self.ztb_raw_info_attached(**ddict)
		self.session.add(info)
		self.session.commit()

	def add_Infoattachment(self, ddict):
		info = self.ztbinfoattachment(**ddict)
		self.session.add(info)
		self.session.commit()

	def get_Info_List(self, stratid=0, count=100, num=None):
		if count == 0:
			count = 1
		if not num:
			query_all = self.session.query(self.ztbrawinfo).order_by(self.ztbrawinfo.id)[stratid:count]
			return [to_dict(x) for x in query_all]
		else:
			query_all = self.session.query(self.ztbrawinfo).filter(self.ztbrawinfo.id > num)[stratid:count]
			return [to_dict(x) for x in query_all]

	def get_InfoContent_List(self, stratid=0, count=100, num=None):
		if count == 0:
			count = 1
		if not num:
			query_all = self.session.query(self.ztbrawinfocontent).order_by(self.ztbrawinfocontent.id)[stratid:count]
			return [to_dict(x) for x in query_all]
		else:
			query_all = self.session.query(self.ztbrawinfocontent).filter(self.ztbrawinfocontent.id > num)[
			            stratid:count]
			return [to_dict(x) for x in query_all]

	def get_raw_info_attached_List(self, stratid=0, count=100, num=None):
		if count == 0:
			count = 1
		if not num:
			query_all = self.session.query(self.ztb_raw_info_attached).order_by(self.ztb_raw_info_attached.id)[
			            stratid:count]
			return [to_dict(x) for x in query_all]
		else:
			query_all = self.session.query(self.ztb_raw_info_attached).filter(self.ztb_raw_info_attached.id > num)[
			            stratid:count]
			return [to_dict(x) for x in query_all]

	def get_InfoAttachment_List(self, stratid=0, count=100, num=None):
		if count == 0:
			count = 1
		if not num:
			query_all = self.session.query(self.ztbinfoattachment).order_by(self.ztbinfoattachment.id)[stratid:count]
			return [to_dict(x) for x in query_all]
		else:
			query_all = self.session.query(self.ztbinfoattachment).filter(self.ztbinfoattachment.id > num)[
			            stratid:count]
			return [to_dict(x) for x in query_all]

	def get_InfoNO1_id(self):
		getNO1_id = self.session.query(self.ztbrawinfo).order_by(self.ztbrawinfo.id.desc())[0]
		return int(to_dict(getNO1_id)['id'])

	def get_InfoContentNO1_id(self):
		getNO1_id = self.session.query(self.ztbrawinfocontent).order_by(self.ztbrawinfocontent.id.desc())[0]
		return int(to_dict(getNO1_id)['id'])

	def get_raw_info_attachedNO1_id(self):
		getNO1_id = self.session.query(self.ztb_raw_info_attached).order_by(self.ztb_raw_info_attached.id.desc())[0]
		return int(to_dict(getNO1_id)['id'])

	def get_ztbInfoAttachmentNO1_id(self):
		getNO1_id = self.session.query(self.ztbinfoattachment).order_by(self.ztbinfoattachment.id.desc())[0]
		return int(to_dict(getNO1_id)['id'])
	def get_ztbInfo_url_all(self):
		getNO1_id = self.session.query(self.ztbrawinfo.page_url,self.ztbrawinfo.site)[0:1000000]
		# getNO1_id = self.session.query(self.ztbrawinfo.page_url,self.ztbrawinfo.site).all()
		return [{'page_url':x[0],'site':x[1]} for x in getNO1_id if x]


class LOCAL(CCGPmysql):
	def __init__(self):
		baseName = 'local'
		super(LOCAL, self).__init__(baseName)
		self.ztbrawinfo = self.Base_automap_base.classes.ztbrawinfo
		self.ztbrawinfocontent = self.Base_automap_base.classes.ztbrawinfocontent
		self.ztb_raw_info_attached = self.Base_automap_base.classes.ztb_raw_info_attached
		self.ztbinfoattachment = self.Base_automap_base.classes.ztbinfoattachment


class UXUE(CCGPmysql):
	def __init__(self):
		baseName = 'uxue'
		super(UXUE, self).__init__(baseName)
		self.ztbrawinfo = self.Base_automap_base.classes.ztbRawInfo
		self.ztbrawinfocontent = self.Base_automap_base.classes.ztbRawInfoContent
		self.ztb_raw_info_attached = self.Base_automap_base.classes.ztb_raw_info_attached
		self.ztbinfoattachment = self.Base_automap_base.classes.ztbInfoAttachment


uXue_Session = UXUE()
local_Session = LOCAL()



if __name__ == '__main__':
	pass


	# local_Session = LOCAL()
	# varpage_url = local_Session.get_ztbInfo_url_all()
	# show_memory(unit='MB',varmemory=varpage_url,word='varpage_url')
