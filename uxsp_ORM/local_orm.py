# -*- coding: utf-8 -*-
import pprint
import sys

import sqlalchemy, re
from sqlalchemy import create_engine, Column, Integer, SmallInteger, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship, backref
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


engin = mysqlcontnect(mysqlJson['local_sql'])
metadata = MetaData()
metadata.reflect(engin, only=['ztb_raw_info_attached', 'ztbinfoattachment', 'ztbrawinfo', 'ztbrawinfocontent'])
Base = automap_base(metadata=metadata)

Base.prepare()

ztb_raw_info_attached = Base.classes.ztb_raw_info_attached
ztbInfoAttachment = Base.classes.ztbinfoattachment
ztbRawInfo = Base.classes.ztbrawinfo
ztbRawInfoContent = Base.classes.ztbrawinfocontent

DBsession = sessionmaker(bind=engin)

class ZtbRawInfo_OBJ(Base):
	__tablename__ = "ztbRawInfo"
	# id = relationship('ztbRawInfo', order_by='ztbRawInfo.id')
	# id = Column(Integer,primary_key=True,autoincrement=True)

	subclass = relationship('ztbRawInfo', order_by='ztbRawInfo.subclass')
	site = relationship('ztbRawInfo', order_by='ztbRawInfo.site')
	page_url = relationship('ztbRawInfo', order_by='ztbRawInfo.page_url')
	title = relationship('ztbRawInfo', order_by='ztbRawInfo.title')
	creation_time = relationship('ztbRawInfo', order_by='ztbRawInfo.creation_time')
	end_time = relationship('ztbRawInfo', order_by='ztbRawInfo.end_time')
	issue_time = relationship('ztbRawInfo', order_by='ztbRawInfo.issue_time')

	# ztb_type = relationship('ztbRawInfo', order_by='ztbRawInfo.ztb_type')
	# remark = relationship('ztbRawInfo', order_by='ztbRawInfo.remark')
	# process_status = relationship('ztbRawInfo', order_by='ztbRawInfo.process_status')
	# craw_status = relationship('ztbRawInfo', order_by='ztbRawInfo.craw_status')
	# modified_time = relationship('ztbRawInfo', order_by='ztbRawInfo.modified_time')
	# error_record_id = relationship('ztbRawInfo', order_by='ztbRawInfo.error_record_id')

	def __repr__(self):
		text_str = '''
issue_time:\t{issue_time}
creation_time:\t{creation_time}
end_time:\t{end_time}
site:\t{creation_time}
page_url:\t{page_url}
title:\t{title}
subclass:\t{subclass}
		'''.format(
		           issue_time=self.issue_time,
		           creation_time = self.creation_time,
		           end_time = self.end_time,
		           site=self.site,
                   title=self.title,
                   subclass=self.subclass,
                   page_url = self.page_url
		           )
		return text_str
	# content = relationship('ztbRawInfoContent', backref=backref('ztbRawInfoContent',order_by=ztbRawInfoContent.id))


# class ztbRawInfoContent_OBJ(Base):
# 	__tablename__ = ztbRawInfoContent.__tablename__
# 	ztbRawInfoContent_id = relationship('ztbRawInfoContent', order_by='ztbRawInfoContent.id')
# 	raw_data_id = relationship('ztbRawInfoContent', order_by='ztbRawInfoContent.raw_data_id',backref=backref('ZtbRawInfo_OBJ',order_by=ZtbRawInfo_OBJ.id))
# 	content = relationship('ztbRawInfoContent', order_by='ztbRawInfoContent.content')


if __name__ == '__main__':
	jack = ZtbRawInfo_OBJ(

		subclass='测试',
		title='测试标题',
		issue_time="2021-09-07 00:00:00",
		creation_time="2021-09-07 00:00:00",
		end_time="2021-09-07 00:00:00",
		site = "text.site",
		page_url="http://xxx.x1x2x.xxx/1x2x3x.html",
	)
	print(jack)


	pass
	# jack = ZtbRawInfo_OBJ(
	# 	subclass='测试',
	# 	title='测试标题',
	# 	issue_time="2021-09-07 00:00:00",
	# 	creation_time="2021-09-07 00:00:00",
	# 	end_time="2021-09-07 00:00:00",
	# 	site = "text.site",
	# 	page_url="http://xxx.x1x2x.xxx/1x2x3x.html",
	# )
	# print(dir(Base))
	# print(Base.classes.ztbrawinfocontent)
	# print(dir(Base.classes.ztbrawinfocontent))
