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
from FileAll import file_name_walk
from redis_dup import BloomFilter

bl = BloomFilter('uxue:url')

LOGINGFOMAT = '''ERROR massage:\t%(message)s
ERROR LEVEL:\t%(levelname)s
ERROR LOCATION:\t%(pathname)s\t%(lineno)d
%(funcName)s
ERROR TIME:\t%(asctime)s
-----------------------------------------------------------
'''
logging.basicConfig(filename='requests_HubError.log', format=LOGINGFOMAT)

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
HEA = dict(line.split(": ", 1) for line in headers_Word.split("\n") if line != '')
Root = os.getcwd()
fan_hao_db_path = os.path.join(Root, 'fan_hao_db')

timestr = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '_{}.json'
jsonFileName_json = os.path.join(fan_hao_db_path, timestr)




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


class sqliteOBJ():
	import sqlite3
	sqlite_conn = sqlite3.connect('AV_subtitle/fanHao.db')
	sqlite_coursor = sqlite_conn.cursor()
	sqlite_coursor.execute('''CREATE TABLE IF NOT EXISTS fanHaoTable(
	                       id TEXT PRIMARY KEY,
	                       page_url TEXT,
	                       title TEXT,
	                       issue_time TEXT,
	                       company TEXT,
	                       duration TEXT);''')
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

	def find_info(self,byid=None):
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


def jsonTOsqlite():
	jsonPathList = file_name_walk(fan_hao_db_path)
	mark = 0
	existsMark = 0
	insertMark = 0
	for num, i in enumerate(jsonPathList):
		# if num >1:
		# 	continue
		jsonHub = read_json(i)
		if jsonHub:
			for jsonT in jsonHub:
				mark += 1
				yn = bl.exists(jsonT['id'])
				if not yn:
					bl.insert(jsonT['id'])
					insertMark += 1
				else:
					existsMark += 1
					continue
				info = tuple([str(jsonT[x]) for x in jsonT.keys()])
				db.add_info(info)
			print('已经浏览了{}条'.format(mark))
			print('已经筛选掉{}条'.format(existsMark))
			print('已经inset{}条'.format(insertMark))
			print(i)


if __name__ == '__main__':
	db = sqliteOBJ()
	print(db.find_info(byid='BANK-062'))

	# exit()

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
