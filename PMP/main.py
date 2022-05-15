import pprint
import re

import requests
import json
import csv
from bs4 import BeautifulSoup

import sqlalchemy

MYSQLINFO = {
	"HOST": "localhost",
	"DBNAME": "pmp",
	"USER": "root",
	"PASSWORD": "040304",
	"PORT": 3306
}

conStr = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?charset=utf8mb4'.format(USER=MYSQLINFO['USER'],
                                                                                           PASSWORD=MYSQLINFO[
	                                                                                           'PASSWORD'],
                                                                                           HOST=MYSQLINFO['HOST'],
                                                                                           PORT=MYSQLINFO['PORT'],
                                                                                           DBNAME=MYSQLINFO[
	                                                                                           'DBNAME'])

mysqlcon = sqlalchemy.create_engine(conStr)
# 登录，并获取cookies
def get_loginCookise():
	login_url = "https://public.huixiangtiandi.com/pcApi/user/login"
	login_post = {
		'mobile': '13501189465',
		'user_pwd': 'dd34913198230ad56e8cb1dd79763589',
		'sub_id': '14',
	}

	login_brow = requests.post(url=login_url, data=login_post)
	return login_brow.cookies
# 获取题目的html代码
def question(quest_id, exam_id, cookies, num, exam_title):
	question_url = "https://public.huixiangtiandi.com/question/Question"
	question_post = {
		'quest_id': str(quest_id),
		'exam_id': str(exam_id),
		'exam_type': '0',
		'sub_id': '14',
	}
	question_brow = requests.post(url=question_url, data=question_post, cookies=cookies)
	soup = BeautifulSoup(question_brow.text, 'lxml')

	# print(soup.prettify())
	# print(re.findall("该题我做过\d次，做错(\d)次", soup.prettify()))
	ddict = {}
	wrong = ''.join(re.findall("该题我做过\d次，做错(\d)次", soup.prettify()))
	if not wrong:
		wrong = 0
	else:
		wrong = int(wrong)
	ddict['wrong'] = wrong
	ddict['exam_title'] = exam_title
	ddict['quest_answers'] = soup.find(id="quest_answers").get('value')
	quest_title = soup.find(class_="quiz-title")
	ddict['title'] = "<span>" + str(num) + "</span>" + quest_title.prettify().replace('/image/ueditor/',
	                                                                                  'http://public.huixiangtiandi.com/image/ueditor/')

	ul_soup = soup.find('ul')
	for letter in ['A', 'B', 'C', 'D']:
		a = ul_soup.find(value=letter)
		atext = a.find_all('span')
		aa = [x.get_text().strip() for x in atext]
		ddict[letter] = ' '.join(aa)
	ddict['quest_analysis'] = soup.find(id="quest_analysis").get_text().replace('\\n', '').replace('\n', '').replace(
		'\\', '')

	return ddict
# 获取模拟测试题库id
def paperlist(cookies):
	url = "https://public.huixiangtiandi.com/pcApi/question/paperList"
	postdate = {'sub_id': '14'}
	brow = requests.post(url=url, data=postdate, cookies=cookies)
	jsonT = json.loads(brow.text)
	jsonT = jsonT['result']['list']['2']['children']

	llist = []
	for i in jsonT:
		ddict = {}
		ddict['exam_title'] = i['exam_title']
		ddict['exam_id'] = i['id']
		# ddict['quest_number'] = i['quest_number']
		ddict['quest_id'] = listForExam(ddict['exam_id'], cookies)
		llist.append(ddict)

	return llist
# 获取某模拟题库内题目id
def listForExam(exam_id, cookies):
	postdate = {
		'exam_type': '0',
		'exam_id': exam_id,  # 50472
		'page': '1',
		'pageSize': '999',
		'sub_id': '14',
	}
	url = "https://public.huixiangtiandi.com/pcApi/question/listForExam"
	brow = requests.post(url, data=postdate, cookies=cookies)
	jsonT = json.loads(brow.text)['result']['list']
	print(jsonT)
	# mark = 0
	# for num,ii in enumerate(jsonT):
	# 	if ii['had_wrong'] and ii['had_wrong'] > 0:
	# 		mark+=1
	# print(mark)
	return [x['quest_id'] for x in jsonT]


# 获取章节练习题库id
def chapterList(cookies):
	url = "https://public.huixiangtiandi.com/pcApi/question/chapterList"
	postdate = {'sub_id': '14'}
	brow = requests.post(url=url, data=postdate, cookies=cookies)
	jsonT = json.loads(brow.text)
	jsonT = jsonT['result']['list']

	llist = []
	for i in jsonT:

		ddict = {}
		ddict['chapter_id'] = i['chapter_id']
		ddict['exam_title'] = i['name']
		ddict['exam_id'] = i['children'][0]['section_id']
		ddict['quest_id'] =listForChapter(section_id=ddict['exam_id'],chapter_id=ddict['chapter_id'],cookies=login_cookie)
		llist.append(ddict)

	return llist


# 获取章节练习题id
def listForChapter(section_id,chapter_id, cookies):
	postdate = {
		'section_id': section_id,
		'chapter_id': chapter_id,
		'exam_type': '0',
		'page': '1',
		'pageSize': '25',
		'sub_id': '14'
	}
	url = "https://public.huixiangtiandi.com/pcApi/question/listForChapter"
	brow = requests.post(url, data=postdate, cookies=cookies)
	jsonT = json.loads(brow.text)['result']['list']

	return [x['quest_id'] for x in jsonT]


# 获取章节练习题目html
def question_chapter(quest_id, section_id, chapter_id,cookies, num, chapter_title):
	question_url = "https://public.huixiangtiandi.com/question/Question"
	question_post = {
		'quest_id': str(quest_id),
		'section_id': str(section_id),
		'exam_type': '0',
		'sub_id': '14',
		'chapter_id':str(chapter_id)
	}
	question_brow = requests.post(url=question_url, data=question_post, cookies=cookies)
	soup = BeautifulSoup(question_brow.text, 'lxml')
	ddict = {}
	wrong = ''.join(re.findall("该题我做过\d次，做错(\d)次", soup.prettify()))
	if not wrong:
		wrong = 0
	else:
		wrong = int(wrong)
	ddict['wrong'] = wrong
	ddict['exam_title'] = chapter_title
	ddict['quest_answers'] = soup.find(id="quest_answers").get('value')
	quest_title = soup.find(class_="quiz-title")
	ddict['title'] = "<span>" + str(num) + "</span>" + quest_title.prettify().replace('/image/ueditor/',
	                                                                                  'http://public.huixiangtiandi.com/image/ueditor/')

	ul_soup = soup.find('ul')
	for letter in ['A', 'B', 'C', 'D']:
		a = ul_soup.find(value=letter)
		atext = a.find_all('span')
		aa = [x.get_text().strip() for x in atext]
		ddict[letter] = ' '.join(aa)
	ddict['quest_analysis'] = soup.find(id="quest_analysis").get_text().replace('\\n', '').replace('\n', '').replace(
		'\\', '')

	return ddict
if __name__ == '__main__':
	import pandas as pd
	login_cookie = get_loginCookise()
	chapter = chapterList(login_cookie)
	# paper = paperlist(login_cookie)
	# b = question(quest_id='11380', exam_id='50472', cookies=login_cookie, num=2, exam_title='远程PMP全真模拟二')
	print(chapter)
	#
	# exit()

	for i in chapter:
		if i['exam_title'] != 'PMP第10章  项目沟通管理':
			continue
		print(i)
		llist = []
		# print(i)
		for num, n in enumerate(i['quest_id']):
			print(n)
			# if num >0:
			# 	continue
			# b = question(quest_id=n, exam_id=i['exam_id'], cookies=login_cookie, num=num + 1,
			#              exam_title=i['exam_title'])
			b = question_chapter(quest_id=n, section_id=i['exam_id'], chapter_id=i['chapter_id'], cookies=login_cookie, num=num + 1, chapter_title=i['exam_title'])

			llist.append(b)
			b['quest_id'] = int(n)
			b['exam_id'] = i['exam_id']
			pprint.pprint(b)
			print('----------------------')
		# exceldf = pd.DataFrame(llist)
		# insertInfo = exceldf.to_sql(name='exam_copy1', con=mysqlcon, if_exists='append', index=False,
		#                             chunksize=1000)

# b = question(quest_id='11381',exam_id='50472',cookies=login_cookie,num=2,exam_title='远程PMP全真模拟二')
