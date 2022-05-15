# -*- coding: utf-8 -*-
import os, time, datetime, sys

input_key = sys.argv[1]

if input_key == 'article':
	timeSleep = 30
elif input_key == 'hub':
	timeSleep = 60 * 5
else:
	timeSleep = 0
	print('pls input hub or article')
	exit()
while True:
	# try:
	# 	os.system("ps -ef|grep ccgp_cq.py|grep -v grep|cut -c 9-15|xargs kill -9")
	# 	os.system("ps -ef|grep home/terry/jxpython/wd/chromedriver|grep -v grep|cut -c 9-15|xargs kill -9")
	# except:
	# 	pass
	# os.system("nohup python ccgp_cq.py {} >/dev/null 2>&1 &".format(input_key))
	os.system("python ccgp_cq.py {}".format(input_key))
	time.sleep(timeSleep)
