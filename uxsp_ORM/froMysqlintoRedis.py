# -*- coding: utf-8 -*-
import pprint
import sys
import redis
from mysqlORM import UXUE, LOCAL
uXue_Session = UXUE()
local_Session = LOCAL()


import sqlalchemy,re
from sqlalchemy import create_engine, Column, Integer, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import json
import datetime
import asyncio

from redis_dup import BloomFilter
import redis

redis_db = redis.StrictRedis(host='localhost', port=6379, db=1, decode_responses=True, encoding='utf-8')
bl = BloomFilter(redis_db, 'uxue:url')



def show_memory(unit='KB', varmemory=None,word=''):
	import sys
	'''查看变量占用内存情况

	:param unit: 显示的单位，可为`B`,`KB`,`MB`,`GB`
	:param threshold: 仅显示内存数值大于等于threshold的变量
	'''
	from sys import getsizeof
	scale = {'B': 1024**0, 'KB': 1024**1, 'MB': 1024**2, 'GB': 1024**3}[unit]
	a = sys.getsizeof(varmemory)

	print('{word1}内存占用为：{a1} {a2}'.format(word1=word, a1=round(a/scale,5),a2=unit))

async def ztbinfo_main():
	global uXue_Session, local_Session
	while True:
		try:
			get_local_infoid_desc = local_Session.get_InfoNO1_id()
		except:
			get_local_infoid_desc = 0
		print('ztbinfo_main\t', get_local_infoid_desc)
		get_uxue_infoList1 = uXue_Session.get_Info_List(count=10000, num=get_local_infoid_desc)
		show_memory(unit='KB', varmemory=get_uxue_infoList1,word='ztbinfo_main')

		if not get_uxue_infoList1:
			break
		for info in get_uxue_infoList1:
			yn = bl.exists(info['page_url'])
			if not yn:
				bl.insert(info['page_url'])
			local_Session.add_Info(info)
		await asyncio.sleep(0.1)


async def ztbinfoContent_main():
	global uXue_Session, local_Session
	while True:
		try:
			get_local_infoid_desc = local_Session.get_InfoContentNO1_id()
		except:
			get_local_infoid_desc = 0
		print('ztbinfoContent_main\t', get_local_infoid_desc)
		get_uxue_infoList2 = uXue_Session.get_InfoContent_List(count=10500, num=get_local_infoid_desc)
		show_memory(unit='KB',varmemory=get_uxue_infoList2,word='ztbinfoContent_main')

		if not get_uxue_infoList2:
			break
		bugList = [11434614,11446576,14511816]
		for info in get_uxue_infoList2:
			if int(info['id']) in bugList:
				continue
			# info['content'] = info['content'].replace('AAAA','')
			reg = re.findall("(<!--.*-->)", info['content'], re.M | re.S)
			for i in reg:
				info['content'] = info['content'].replace(i, '')
			try:
				local_Session.add_InfoContent(info)
			except Exception as excinfo:
				print(excinfo)

				continue

		await asyncio.sleep(0.1)


async def ztb_raw_info_attached_main():
	global uXue_Session, local_Session
	while True:
		try:
			get_local_infoid_desc = local_Session.get_raw_info_attachedNO1_id()
		except:
			get_local_infoid_desc = 0
		print('ztb_raw_info_attached_main\t', get_local_infoid_desc)
		get_uxue_infoList3 = uXue_Session.get_raw_info_attached_List(count=10000, num=get_local_infoid_desc)
		show_memory(unit='KB', varmemory=get_uxue_infoList3,word='ztb_raw_info_attached_main')
		if not get_uxue_infoList3:
			break
		for info in get_uxue_infoList3:

			local_Session.add_raw_Info_attached(info)
		await asyncio.sleep(0.1)


async def ztbinfoattachment_main():
	global uXue_Session, local_Session
	while True:
		try:
			get_local_infoid_desc = local_Session.get_ztbInfoAttachmentNO1_id()
		except:
			get_local_infoid_desc = 0
		print('ztbinfoattachment_main\t', get_local_infoid_desc)
		get_uxue_infoList4 = uXue_Session.get_InfoAttachment_List(count=10000, num=get_local_infoid_desc)
		show_memory(unit='KB', varmemory=get_uxue_infoList4,word='ztbinfoattachment_main')
		if not get_uxue_infoList4:
			break
		for info in get_uxue_infoList4:
			local_Session.add_Infoattachment(info)
		await asyncio.sleep(0.1)


async def main():
	task1 = asyncio.create_task(ztbinfo_main())
	task2 = asyncio.create_task(ztbinfoContent_main())
	task3 = asyncio.create_task(ztbinfoattachment_main())
	task4 = asyncio.create_task(ztb_raw_info_attached_main())
	await task1
	await task2
	await task3
	await task4
if __name__ == '__main__':
	asyncio.run(main())