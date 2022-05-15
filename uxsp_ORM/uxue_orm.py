# -*- coding: utf-8 -*-
import pprint
import sys

import sqlalchemy, re
from sqlalchemy import create_engine, Column, Integer, SmallInteger, String, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship,backref
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



engin = mysqlcontnect(mysqlJson['uxuepai_sql'])
metadata = MetaData()
metadata.reflect(engin, only=['ztb_raw_info_attached', 'ztbInfoAttachment', 'ztbRawInfo', 'ztbRawInfoContent'])
Base = automap_base(metadata=metadata)
Base.prepare()

ztb_raw_info_attached = Base.classes.ztb_raw_info_attached
ztbInfoAttachment = Base.classes.ztbInfoAttachment
ztbRawInfo = Base.classes.ztbRawInfo
ztbRawInfoContent = Base.classes.ztbRawInfoContent


class ZtbRawInfoContent_OBJ(Base):
	__tablename__ = ztbRawInfoContent.__tablename__
	id = relationship('id',order_by='ztbRawInfoContent.id')
	_raw_data_id = Column(Integer,ForeignKey('ztbRawInfo.id'))


if __name__ == '__main__':




	pass

# for i in range(len(dir(ztbRawInfo))):
# 	print(i)
# 	print(ztbRawInfo[i])
# 	print('--*50')
