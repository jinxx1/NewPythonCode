# -*- coding: utf-8 -*-
import os, time, datetime

crawlNamePath = 'spiderName.txt'
sec = 15
while True:
	with open(crawlNamePath) as f:
		str = f.read()
	crawlList = [i for i in str.split('\n')]
	for crawlName in crawlList:
		excWord = '''nohup python {} hub >/dev/null 2>&1 &'''.format(crawlName)
		os.system(excWord)
	time.sleep(60 * sec)
