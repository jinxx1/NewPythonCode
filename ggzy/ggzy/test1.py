# -*- coding: utf-8 -*-
import json
import pprint
import re
import time, os
from lxml import etree

import requests


def reTime(timelocation):
	time_local = time.localtime(int(timelocation) / 1000)
	dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
	return dt


def file_name_walk(file_dir):
	import os
	listpath = []
	for root, dirs, files in os.walk(file_dir):
		dictTemp = {}
		dictTemp['root'] = root  # 当前目录路径
		dictTemp['dirs'] = dirs  # 当前路径下所有子目录
		dictTemp['files'] = files  # 当前路径下所有非目录子文件
		listpath.append(dictTemp)
	llistpath = []
	for i in listpath:
		if i['files']:
			for n in i['files']:
				pathName = os.path.join(i['root'], n)
				llistpath.append(pathName)
	return llistpath


def stmeTime(time_str):
	import time
	timeArray = time.strptime(time_str, "%Y-%m-%d")
	ddict = {}
	ddict['sd'] = time.mktime(timeArray)
	ddict['ed'] = ddict['sd'] + (60 * 60 * 23.9998)
	ddict['sd'] = ddict['sd'] * 1000
	ddict['ed'] = ddict['ed'] * 1000
	return ddict


def sendEmail(ddict):
	import smtplib
	from email.mime.text import MIMEText
	from email.header import Header
	mail_host = 'smtp.exmail.qq.com'
	mail_user = 'umservice@uxuepai.net'
	mail_pass = 'Um20170927'
	mail_port = 465
	sender = mail_user
	receivers = ['jinxx1@163.com', '491887462@qq.com']
	message = MIMEText(ddict['body'], 'plain', 'utf-8')
	message['To'] = Header(';'.join(receivers), 'utf-8')
	message['Subject'] = Header(ddict['title'], 'utf-8')
	smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
	smtpObj.ehlo()
	smtpObj.login(mail_user, mail_pass)
	smtpObj.sendmail(sender, receivers, message.as_string())
	smtpObj.quit()


def get_timestr(date, outformat="%Y-%m-%d %H:%M:%S", combdata=False):
	import time
	time_array = ''
	format_string = [
		"%Y年%m月%d日 %H时%M分%S秒",
		"%Y-%m-%d %H:%M:%S",
		"%Y-%m-%d %H:%M",
		"%Y-%m-%d %H",
		"%Y-%m-%d",
		"（%Y-%m-%d %H:%M:%S）",
		"（%Y-%m-%d %H:%M）",
		"（%Y-%m-%d %H）",
		"（%Y-%m-%d）",
		"%Y/%m/%d %H:%M:%S",
		"%Y/%m/%d %H:%M",
		"%Y/%m/%d %H",
		"%Y/%m/%d",
		"%Y.%m.%d %H:%M:%S",
		"%Y.%m.%d %H:%M",
		"%Y.%m.%d %H",
		"%Y.%m.%d",
		"%Y年%m月%d日 %H:%M:%S",
		"%Y年%m月%d日 %H:%M",
		"%Y年%m月%d日 %H",
		"%Y年%m月%d日",
		"%Y_%m_%d %H:%M:%S",
		"%Y_%m_%d %H:%M",
		"%Y_%m_%d %H",
		"%Y_%m_%d",
		"%Y%m%d%H:%M:%S",
		"%Y%m%d %H:%M:%S",
		"%Y%m%d %H:%M",
		"%Y%m%d %H",
		"%Y%m%d",
		"%Y%m%d%H%M%S",
		"%Y%m%d %H%M%S",
		"%Y%m%d %H%M",
		"%Y%m%d %H",
		"%Y%m%d",
		"%Y\%m\%d %H:%M:%S",
		"%Y\%m\%d %H:%M",
		"%Y\%m\%d %H",
		"%Y\%m\%d",
		"%Y年%m月%d日%H时%M分",
		"%Y年%m月%d日%H:%M:%S",
		"%Y年%m月%d日%H:%M",
		"%Y年%m月%d日%H",
		"%Y年%m月%d日",

	]
	for i in format_string:
		try:
			time_array = time.strptime(date, i)
		except:
			continue
	if not time_array:
		return None
	timeL1 = int(time.mktime(time_array))
	timeL = time.localtime(timeL1)
	if combdata:
		return time.strftime(outformat, timeL), timeL1
	else:
		return time.strftime(outformat, timeL)


def attmenSTR(downLoad):
	import cgi
	from urllib.parse import unquote

	import requests
	ddict = {}
	ddict['download_url'] = downLoad
	response = requests.head(url=downLoad, timeout=(5, 5))
	print(response.headers)

	try:
		value, params = cgi.parse_header(response.headers['Content-Disposition'])
		name = params['filename'].encode('ISO-8859-1').decode('utf8')
		ddict['name'] = unquote(name, 'utf-8')
	except:
		ddict['name'] = downLoad.split('/')[-1]
	response.ok
	return ddict


def attmenSTR1(downLoad):
	from urllib.parse import unquote
	import requests
	ddict = {}
	ddict['download_url'] = downLoad
	brow = requests.get(url=downLoad)
	try:
		soureAttachment = re.findall('''attachment; filename=\"(.*?)\"''', brow.headers['Content-Disposition'])[0]
	except:
		return None
	ddict['name'] = unquote(soureAttachment, 'utf-8')
	return ddict


def hh():
	pass


def atment(baseurl):
	from urllib import parse as urlparse

	# baseurl = "/cms/newscontent/contentupload/file/2021-08/74ee93ab_3f1b_4b1f_bdfb_cd2104d4c27f.pdf"

	# baseurl = "https://ggzy.yibin.gov.cn/ybin-jingjia-file/downloadFile.do?fileGuid=c110e047-7756-4efc-9d6c-dfab0d49487b"
	# baseurl = "http://202.61.88.152:9080/TPFrame/jsgcztbmis2/pages/zbfilereg/downAttach4WebActionSCZXXT.action?cmd=download&AttachGuid=d1c67b9f-1882-45b5-8ef9-c0b5dffd63bd&FileCode=Z300&ClientGuid=596f4992-f3e7-4819-9ac3-3cfc9e38de5d"
	url = urlparse.urljoin('http://www.ccgp-sichuan.gov.cn', baseurl)
	print(url)

	brow = attmenSTR(url)
	print(brow)


def c_nm(n, m):
	import math

	c = math.factorial(n) / (math.factorial(m) * math.factorial(n - m))
	return c

def main(yes):
	n = 20
	m = yes
	nm = n - m

	c = c_nm(n, m)
	ps = 0.25 ** m
	qs = 0.75 ** nm

	result = c * ps * qs
	return '{:.5f}%'.format(result*100)




if __name__ == '__main__':

	winrate = 0.02
	n = 1
	for n in range(1,41):
		p1 = (1-winrate)**n
		p = 1-p1
		print("投资{}次，至少一次能成功的概率为{:.3f}%".format(n,p*100))
