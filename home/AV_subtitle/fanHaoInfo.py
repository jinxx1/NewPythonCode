import re

import requests
import os, sys, csv, json, datetime, pprint
import random, time
from requests.adapters import HTTPAdapter
import lxml
import lxml.html
from lxml.html import HtmlComment
from lxml import etree
from urllib import parse as urlparse
import logging
from DB_ORM import *
from redis_dup import BloomFilter

LOGINGFOMAT = '''ERROR massage:\t%(message)s
ERROR LEVEL:\t%(levelname)s
ERROR LOCATION:\t%(pathname)s\t%(lineno)d
%(funcName)s
ERROR TIME:\t%(asctime)s
-----------------------------------------------------------
'''
logging.basicConfig(filename='requests_HubError.log', format=LOGINGFOMAT)
bl = BloomFilter('uxue:url')

headers_Word = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: keep-alive
Cookie: _xs=1e744314e9d96d9f; _sf=Rk5KVlBYQ3ATGjc4OT4RUUp5GnYCThxQAigzAH9fQx1LBjgdRnZFTg; __51cke__=; PHPSESSID=8rgf49uakru2lorb8s7cn8b4v1; __tins__20932147=%7B%22sid%22%3A%201634448746209%2C%20%22vd%22%3A%202%2C%20%22expires%22%3A%201634451144010%7D; __51laig__=9
Host: www.33fanhao.com
Referer: https://www.33fanhao.com/vod-show-id-1-p-2.html
sec-ch-ua: "Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'''

Root = os.getcwd()
fan_hao_db_path = os.path.join(Root, 'fan_hao_db')

timestr = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_{}.json'
jsonFileName_json = os.path.join(fan_hao_db_path, timestr)

HEA = dict(line.split(": ", 1) for line in headers_Word.split("\n") if line != '')


def getInfo(HTML, hubUrl, baseurl):
	doc = lxml.html.fromstring(HTML)
	link = doc.xpath("//div[@class='table-responsive']//td[@class = 'td2']/a/@href")
	# pprint.pprint(link)
	print(hubUrl)
	llist = []
	for num, href in enumerate(link):
		ddict = {}

		try:
			id_and_title = doc.xpath('//*[@href="{}"]/text()'.format(href))
			ddict['id'] = id_and_title[0].strip()
			ddict['page_url'] = urlparse.urljoin(baseurl, href)
			ddict['title'] = id_and_title[1].strip()
		except Exception as ff:
			errormsg = 'hub id、title、page_url error ：\n' + ff + '\n' + hubUrl + '\n'
			logging.error(msg=errormsg)
			continue

		try:
			ddict['issue_time'] = doc.xpath("//*[@href='{}']/../../td[3]/text()".format(href))[0]
		except Exception as ff:
			errormsg = 'hub issue_time error ：\n' + ff + '\n' + hubUrl + '\n'
			logging.error(msg=errormsg)
			ddict['issue_time'] = ''

		try:
			ddict['company'] = doc.xpath("//*[@href='{}']/../../td[@class='td4']/text()".format(href))[0]
		except:
			errormsg = 'hub company error ：\n' + hubUrl + '\n'
			logging.error(msg=errormsg)
			ddict['company'] = ''

		try:
			ddict['duration'] = doc.xpath("//*[@href='{}']/../../td[5]/text()".format(href))[0]
		except:
			errormsg = 'hub duration error ：\n' + hubUrl + '\n' + str(num)
			logging.error(msg=errormsg)
			ddict['duration'] = ''
		llist.append(ddict)
	return llist


class fanhaoDB():
	import sqlite3
	sqlite_conn = sqlite3.connect(r"D:\PythonCode\home\AV_subtitle\fanHaoSeach.db")
	sqlite_coursor = sqlite_conn.cursor()
	sqlite_coursor.execute('''CREATE TABLE IF NOT EXISTS fanHaoTable(
	                       id TEXT PRIMARY KEY,
	                       page_url TEXT,
	                       title TEXT,
	                       issue_time TEXT,
	                       company TEXT,
	                       actorname TEXT);''')
	sqlite_conn.commit()

	def add_info(self, info):
		if isinstance(info, tuple):
			try:
				self.sqlite_coursor.execute("INSERT INTO fanHaoTable values(?,?,?,?,?,?)", info)
				self.sqlite_conn.commit()
			except Exception as ff:
				print(ff)
				self.sqlite_conn.rollback()
		elif isinstance(info, list):
			try:
				self.sqlite_coursor.executemany("INSERT INTO fanHaoTable values(?,?,?,?,?,?)", info)
				self.sqlite_conn.commit()
			except Exception as ff:
				print(ff)
				self.sqlite_conn.rollback()
		else:
			raise 'must list or tuple'

	def find_info(self, byid=None):
		if not byid:
			exc = '''SELECT * FROM fanHaoTable;'''
		if byid:
			exc = '''SELECT * FROM fanHaoTable WHERE id="{}";'''.format(byid.upper())

		info = self.sqlite_coursor.execute(exc)
		return tuple([x for x in info])


def read_json(jsonpath):
	try:
		with open(jsonpath, 'r', encoding='utf-8') as ff:
			aa = json.load(ff)
		return aa
	except Exception as ff:
		logging.basicConfig(filename='JSON_READ_ERROR.log', format=LOGINGFOMAT)
		errormsg = 'json read error ：\nff\n{}'.format(jsonpath)
		logging.error(msg=errormsg)
		print(jsonpath)
		return None


def file_name_walk(file_dir=None):
	for root, dirs, files in os.walk(file_dir):
		dictTemp = {}
		dictTemp['root'] = root  # 当前目录路径
		dictTemp['dirs'] = dirs  # 当前路径下所有子目录
		dictTemp['files'] = files  # 当前路径下所有非目录子文件
		if not dictTemp['files']:
			continue
		for x in dictTemp['files']:
			sp = os.path.splitext(x)[-1][1:]
			if sp == 'json':
				jsonF = os.path.join(root, x).replace('\\', '/')

				yield jsonF


if __name__ == '__main__':

	fDB = fanhaoDB()
	sDB = subTitle_OBJ()
	# a = 'STARS-053'
	a = None
	fanhaoDB = fDB.find_info(byid=a)
	subDB = sDB.find_info(byid=a, method=False)
	# print(len(fanhaoDB),len(subDB))
	llist = []
	ddict = {}
	for num, finddb in enumerate([fanhaoDB, subDB]):
		print(num)
		print(len(finddb))
		for i in finddb:
			if num == 0:
				strSplit = i[0].split('-')
			else:
				try:
					strSplit = i[1].split('-')
				except:
					print(i)
					continue
			if len(strSplit[0].replace(' ','').replace('\n','').replace('\t','')) == 1:
				continue
			llist.append(strSplit[0])
	# print(len(llist))

	addList = ['SKY', 'SNIS', 'DV', 'GG', 'FC2PPV', 'AP', 'FC-2PPV', 'PPV','FLNS','MXNB','TMWD']
	nelist2 = llist + addList
	nelist3 = list(set(nelist2))
	nelist4 = []
	for ll in nelist3:

		aa = ll.replace(' ', '').replace('\t', '').replace('\n', '')

		if aa:
			nelist4.append(aa+'-')
	nelist5 = nelist4 + nelist3
	nelist5.sort(key=lambda x: len(x), reverse=True)

	with open('00FanHaoAll.json', 'w') as ff:
		json.dump(nelist5, ff)
		ff.flush()
		ff.close()

	print(len(nelist5))
	if 'IMG' in nelist5:
		print('got')



	exit()
	req = requests.session()
	req.headers = HEA
	req.mount('http://', HTTPAdapter(max_retries=3))
	req.mount('https://', HTTPAdapter(max_retries=3))
	baseUrl = "https://www.33fanhao.com/"
	page_num = "vod-show-id-1-p-{}.html"
	for num in range(1, 2):
		url = baseUrl + page_num.format(str(num))
		jsonF = jsonFileName_json.format(str(num))
		brow = req.get(url=url, timeout=(10, 10))
		# print(brow.text)
		infoJson = getInfo(HTML=brow.text, baseurl=baseUrl, hubUrl=url, )
		existsMark = 0
		if infoJson:
			for jsonT in infoJson:

				yn = bl.exists(jsonT['id'])
				if not yn:
					bl.insert(jsonT['id'])
					info = tuple([str(jsonT[x]) for x in jsonT.keys()])
					db.add_info(info)
				else:
					print(jsonT['id'])
					existsMark += 1

		if existsMark == len(infoJson):
			print('本页全部抓去过，退出程序')
			print(url)
			break
