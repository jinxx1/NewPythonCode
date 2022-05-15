# coding=utf-8
import os
import sqlite3


class subTitle_OBJ():
	sqlite_conn = sqlite3.connect('subTitle.db')
	sqlite_coursor = sqlite_conn.cursor()
	sqlite_coursor.execute('''CREATE TABLE IF NOT EXISTS subTitleTable(
	                       id TEXT PRIMARY KEY,
	                       fanhao TEXT,
	                       fileFolder TEXT,
	                       filePath TEXT,
	                       fileName TEXT,
	                       suffix TEXT,
	                       mark1 TEXT,
	                       mark2 TEXT);''')
	sqlite_conn.commit()

	def add_info(self, info):
		self.sqlite_coursor.execute("INSERT INTO subTitleTable values(?,?,?,?,?,?,?,?)", info)
		self.sqlite_conn.commit()

	def find_info(self, byid=None,method=True):
		if not byid:
			exc = '''SELECT * FROM subTitleTable;'''
		if byid:
			exc = '''SELECT * FROM subTitleTable WHERE fanhao="{}";'''.format(byid.upper())

		info = self.sqlite_coursor.execute(exc)
		if info:
			if method:
				llist = []
				for i in info:
					ddict = {}
					ddict['id'] = i[0]
					ddict['fanhao'] = i[1]
					ddict['fileFolder'] = i[2]
					ddict['filePath'] = i[3]
					ddict['fileName'] = i[4]
					ddict['suffix'] = i[5]
					ddict['mark1'] = i[6]
					ddict['mark2'] = i[7]
					llist.append(ddict)
				return llist

			else:
				return tuple([x for x in info])
		else:
			return None


if __name__ == '__main__':


	print(os.sep)
	print(os.path.dirname(os.getcwd()))
	a = subTitle_OBJ()
	fh = "NHDTB-599"
	b = a.find_info(byid=fh)
	print(b)
