import pprint

import pandas as pd
import sqlalchemy
import re
import os, sys

import json
from bs4 import BeautifulSoup

root = os.getcwd()

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

def htmlget(html1):
    soup = BeautifulSoup(html1, 'lxml')
    try:
        img = soup.find('img')
        img_html = '''<img src="{}">'''.format(img.get('src'))
        html_title = "<p>" + img_html + "</p>" + "<h2>" + filter_tags(html1) + "</h2>"
    except:
        html_title = "<h2>" + filter_tags(html1) + "</h2>"
    return html_title



def filter_tags(htmlstr):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', htmlstr)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  # 替换实体
    return s.replace('\n', '').replace('"', '').replace('\\', '').replace("   、 ", '、').replace("?n",
                                                                                                '?</h2><h2>').replace(
        "  ", '')


def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  # entity全称，如&gt;
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            # 以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr



def get_mysqlinfo(limit=None):
	if not limit:
		exc = '''select exam_title,quest_answers,title,A,B,C,D,quest_analysis,quest_id,wrong,exam_id from exam_copy1 where wrong >0;'''
	else:
		exc = '''select exam_title,quest_answers,title,A,B,C,D,quest_analysis,quest_id,wrong,exam_id from exam_copy1 where wrong >0 LIMIT {};'''.format(
			limit)

	a = mysqlcon.execute(exc)
	llist = []
	for i in a:
		title = htmlget(i[2])
		ddict = {}
		ddict['exam_title'] = i[0]
		ddict['quest_answers'] = i[1]
		ddict['title'] = title
		ddict['A'] = i[3]
		ddict['B'] = i[4]
		ddict['C'] = i[5]
		ddict['D'] = i[6]
		ddict['quest_analysis'] = i[7]
		ddict['quest_id'] = i[8]
		ddict['wrong'] = i[9]
		ddict['exam_id'] = i[10]
		llist.append(ddict)
	return llist

def html_get(allinfo):
	mark = 0
	tempH = '''
				<p>{exam_title}<p>
				{title}
				<p>A、{A}</p>
				<p>B、{B}</p>
				<p>C、{C}</p>
				<p>D、{D}</p>
				<b title="{analysisall}">鼠标移到此处，查看答案和解析</b>
				<p hidden="hidden">{quest_id}</p>
				<p>本题做错过{wrong}次</p>
				<hr />
				'''
	keyWord = '全部错题'
	temp_final = "<h1> {} 相关</h1><hr />".format(keyWord)
	exam_path = os.path.join('wrong', keyWord + '.html')
	exam_filePathName = os.path.join(root, exam_path)
	for i in allinfo:
		if i['quest_id'] == 13104:
			continue
		analysis = '正确答案为：{quest_answers}\n题目解析：{quest_analysis}'.format(quest_answers=i['quest_answers'],
		                                                                 quest_analysis=i['quest_analysis'].replace(
			                                                                 '"',
			                                                                 ''))
		html_temp = tempH.format(exam_title=i['exam_title'],
		                         title=i['title'],
		                         A=i['A'].replace('A', '', 1),
		                         B=i['B'].replace('B', '', 1),
		                         C=i['C'].replace('C', '', 1),
		                         D=i['D'].replace('D', '', 1),
		                         quest_id=i['quest_id'],
		                         analysisall=analysis,
		                         wrong=i['wrong'])
		temp_final += html_temp
		mark += 1
		print(i)
		print('---------------------', mark)
	soup = BeautifulSoup(temp_final, 'lxml')
	with open(exam_filePathName, 'w', encoding='utf-8') as file:
		file.write(soup.prettify())
		file.flush()
		file.close()


if __name__ == '__main__':

	allinfo = get_mysqlinfo()
	html_get(allinfo)
