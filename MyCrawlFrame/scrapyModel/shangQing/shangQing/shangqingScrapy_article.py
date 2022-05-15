# -*- coding: utf-8 -*-
import os, time, datetime

crawlNamePath = 'shangqingScrapy.txt'
sec = 1
while True:
	with open(crawlNamePath) as f:
		str = f.read()
	crawlList = [i for i in str.split('\n')]
	for crawlName in crawlList:
		excWord = '''nohup scrapy crawl {} -a goon=article >/dev/null 2>&1 &'''.format(crawlName)
		os.system(excWord)
	time.sleep(60 * sec)
