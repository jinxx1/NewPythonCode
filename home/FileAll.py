import os
import pprint
import re

import akshare.fund.cons


def file_name_walk(file_dir=None):
	cutS = []
	cutSplit = ['', 'CHM', 'asf', 'idx', 'torrent', 'gif', 'nfo', '3gp', 'txt', 'png', 'SRT', 'm3u8', 'PNG', 'db',
	            'mht', 'URL', 'qdl2', 'xlsx', 'lnk', 'JPG', 'DAT', 'jpg', 'ass', 'smi', 'm4v', 'url', 'ssa', 'BUP',
	            'IFO', 'jpeg', 'html', 'DS_Store', 'mhtml', 'vtt', 'apk', 'dmp', 'srt', 'chm', 'bc!', 'xltd', 'zip',
	            'sub', 'bmp', 'rar', 'qt', 'htm', 'ASS']

	cutSplit = []

	if not file_dir:
		file_dir = "D:\迅雷下载\深田咏美（深田えいみ-Fukada Eimi）3"
	# file_dir = r"Z:\x299\寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\org"
	listpath = []
	mark = 0
	for root, dirs, files in os.walk(file_dir):
		dictTemp = {}
		dictTemp['root'] = root  # 当前目录路径
		dictTemp['dirs'] = dirs  # 当前路径下所有子目录
		dictTemp['files'] = files  # 当前路径下所有非目录子文件
		if not dictTemp['files'] or '原创文宣' in root:
			continue
		for x in dictTemp['files']:
			sp = os.path.splitext(x)[-1][1:]
			cutS.append(sp)
			if "!" not in sp:
				ddict = {}
				ddict['dir'] = root.replace('\\', '/')
				ddict['filepath'] = os.path.join(root, x).replace('\\', '/')
				ddict['fanhao'] = regexFanhao(ddict['filepath'])
				ddict['suffix'] = sp
				mark += 1
				pprint.pprint(ddict)

				# print(ddict['filepath'])
				print('-' * 60, mark)
				listpath.append(ddict)
	print(list(set(cutS)))
	return listpath

class sqliteOBJ():
	import sqlite3
	sqlite_conn = sqlite3.connect('AV_subtitle/fanHao.db')
	sqlite_coursor = sqlite_conn.cursor()
	sqlite_coursor.execute('''CREATE TABLE IF NOT EXISTS fanHaoSRT(
	                       id TEXT PRIMARY KEY,
	                       fanhao TEXT,
	                       path TEXT,
	                       suffix TEXT,
	                       mark1 TEXT,
	                       mark2 TEXT);''')
	sqlite_conn.commit()

	def add_info(self, info):
		self.sqlite_coursor.execute("INSERT INTO fanHaoSRT values(?,?,?)", info)
		self.sqlite_conn.commit()

	def find_info(self, byid=None):
		if not byid:
			exc = '''SELECT * FROM fanHaoSRT;'''
		if byid:
			exc = '''SELECT * FROM fanHaoSRT WHERE id="{}";'''.format(byid.upper())

		info = self.sqlite_coursor.execute(exc)
		return tuple([x for x in info])


def regexFanhao(strWord):
	reg = re.compile("[A-Za-z]+-[0-9]+|[A-Za-z0-9]+-[0-9]+")
	getreg = reg.search(strWord)
	if getreg:
		return getreg.group()
	else:
		return None



if __name__ == '__main__':

	PATH = r"Z:\x299\寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\new_org"
	PATH = r"Z:\x299\寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\org_old\000-000-1"
	a = file_name_walk(file_dir=PATH)
	pprint.pprint(a)
	# print(a)
