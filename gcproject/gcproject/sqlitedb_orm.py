# coding=utf-8
import os
import sqlite3
import pandas as pd


class sqlite_OBJ():

	def __init__(self, dbName):
		self.dbName = dbName
		self.sqlite_conn = sqlite3.connect('sqliteDB.db')
		self.sqlite_coursor = self.sqlite_conn.cursor()
		# id,page_url,title,status
		db_exec = f"CREATE TABLE IF NOT EXISTS {self.dbName}(id INTEGER PRIMARY KEY,page_url TEXT,title TEXT,status INTEGER);"
		self.sqlite_coursor.execute(db_exec)
		self.sqlite_conn.commit()

	def add_info(self, info):
		self.sqlite_coursor.execute(f"INSERT INTO {self.dbName} values{info}")
		self.sqlite_conn.commit()

	def find_info(self, statusNum=0):

		# exc = f'''SELECT * FROM {self.dbName} WHERE status = {statusNum} LIMIT 1000;'''
		exc = f'''SELECT * FROM {self.dbName} WHERE status = {statusNum};'''
		info = self.sqlite_coursor.execute(exc)
		if info:
			llist = []
			for i in info:
				ddict = {}
				ddict['id'] = i[0]
				ddict['page_url'] = i[1]
				ddict['title'] = i[2]
				ddict['status'] = i[3]
				# yield ddict
				llist.append(ddict)
			return llist
		else:
			return None

	def search_status(self, stats):
		# exc = f'''SELECT * FROM {self.dbName} WHERE status = {stats} LIMIT 102;'''
		exc = f'''SELECT * FROM {self.dbName} WHERE status = {stats};'''

		info = self.sqlite_coursor.execute(exc)
		if info:
			llist = []
			for i in info:
				ddict = {}
				ddict['id'] = i[0]
				ddict['page_url'] = i[1]
				ddict['title'] = i[2]
				ddict['status'] = i[3]
				llist.append(ddict)
			if llist:
				self.sqlite_conn.close()
				return llist
			else:
				self.sqlite_conn.close()
				return False
		else:
			self.sqlite_conn.close()
			return False

	def get_count_0(self, status):
		exc = f'''SELECT count(*) FROM {self.dbName} WHERE status = {status};'''

		info = self.sqlite_coursor.execute(exc)
		return info

	def update_info(self, updateKey, updateValue, whereKey, whereValue):

		exc = f"UPDATE {self.dbName} SET {updateKey} = {updateValue} WHERE {whereKey} = {whereValue};"
		self.sqlite_coursor.execute(exc)
		self.sqlite_conn.commit()


if __name__ == '__main__':
	import sys
	from mysqlprecess import mysqlcon

	# inputStatus = sys.argv[1]
	inputStatus = 1

	try:
		isinstance(int(inputStatus), int)
	except:
		print('pls input int')
		exit()
	if int(inputStatus) not in [0, 1, 2, 3, 4, 5, 6, 7]:
		print('pls input 0,1,2,3,4,5,6,7')
		exit()

	TableName = "atobaccobidTable"
	sqlitDB11 = sqlite_OBJ(dbName=TableName)
	# a = sqlitDB11.get_count_0(status=inputStatus)
	a = sqlitDB11.search_status(stats=inputStatus)
	llist = []
	if a:
		for i in a:
			llist.append(i)

	import pandas as pd

	df = pd.DataFrame(llist)
	df.to_sql(name='temp_jx_20211201', con=mysqlcon, if_exists='append', index=False, chunksize=1000)

	exit()
	df = pd.read_csv('atobaccobid.csv')
	# print(df)
	# for i in range(len(df)):
	# 	info = (df.iloc[i].id,df.iloc[i].page_url,df.iloc[i].title,0)
	# 	sqlitDB.add_info(info)

	# sqlitDB.update_info(updateKey='status',updateValue=2,whereKey='id',whereValue=1)
	for num, i in enumerate(sqlitDB11.find_info(statusNum=0)):
		if num > 20:
			break
		print(i)
		print('----------------------')
