# -*- coding: utf-8 -*-
from lxml import html
import re,pprint,requests


import csv,ssl
ssl._create_default_https_context = ssl._create_unverified_context
import time,datetime,random
import lxml.html
etree = lxml.html.etree
from  urllib.parse import urljoin
import sys
import json

def urllist():
	aabb =[{
			'catName': '广西省_区本级_中标公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_zbgg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_区本级_采购公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_cggg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_区本级_更正公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_gzgg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_区本级_成交公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_cjgg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_区本级_其他公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_qtgg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_区本级_单一来源公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_dylygg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_区本级_招标文件预公示',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-shengji_zbwjygg/param_bulletin/20/page_{}.html'
		},

		{
			'catName': '广西省_市县级_其他公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_qtgg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_市县级_单一来源公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_dylygg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_市县级_成交公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_cjgg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_市县级_更正公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_gzgg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_市县级_中标公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_zbgg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_市县级_采购公告',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_cggg/param_bulletin/20/page_{}.html'
		}, {
			'catName': '广西省_市县级_招标文件预公示',
			'url': 'http://www.ccgp-guangxi.gov.cn/CmsNewsController/getCmsNewsList/channelCode-sxjcg_zbwjygs/param_bulletin/20/page_{}.html'
		}
	]

	listCat = '''950
	1990
	482
	1056
	210
	147
	634
	2138
	382
	11249
	4810
	7078
	19326
	1946'''.split('\n')


	newlist = []
	for num1,i in enumerate(aabb):
		for num2,n in enumerate(listCat):
			if num1 == num2:
				i['allpageNum'] = int(n)
				i['bei_10'] = i['allpageNum']//10
				i['yu_10']= i['allpageNum']%10
				i['code'] = ''.join(random.sample('zyxwvutsrqponmlk0123456789jihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ',4))
				newlist.append(i)

	pprint.pprint(newlist)
	print(newlist)

TODAYTIME = '2019-07-22'
rURL = 'http://ztb.uxuepai.net:8035/pc/api/info/source/getInfoPurchaseSourceNumByDate?day={}&isRawInfo=true'.format(TODAYTIME)

responseELEMENT= requests.get(url=rURL)

print(responseELEMENT.text)

def emailsend():
	import smtplib
	from email.mime.text import MIMEText
	from email.header import Header

	mail_host = "smtp.exmail.qq.com"  # 设置服务器
	mail_port = 465 # 设置服务器端口
	mail_user = "umservice@uxuepai.net"  # 用户名
	mail_pass = "Um20170927"  # 口令

	sender = 'from@uxuepai.net'
	# receivers = ['jinxx1@163.com','zhuweidong@uxuepai.net','hanshuangyi@uxuepai.net']
	receivers = ['jinxx1@163.com']

	mail_msg = '''
	测试邮件，收到请微信告知靳潇
	'''

	message = MIMEText(mail_msg,'plain','utf-8')
	message['From'] = Header('爬虫数据监控系统','utf-8')
	message['To'] = Header('测试','utf-8')

	# try:
	smtpObj = smtplib.SMTP()

	smtpObj.connect(mail_host,465)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(mail_user,mail_pass)
	smtpObj.sendmail(sender,receivers,message.as_string())
	print('邮件发送成功')
	# except smtplib.SMTPException:
	# 	print('ERROR,无法发送邮件')

# emailsend()

