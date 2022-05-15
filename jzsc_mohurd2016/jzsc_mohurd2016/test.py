import pprint
import pymysql
import sqlalchemy
import datetime
import time, json
import os


def get_fileCreatTime_nowTime_diff(path):
	import os, time, datetime
	datetimet = time.localtime(os.stat(path).st_ctime)
	tY = int(time.strftime('%Y', datetimet))
	tm = int(time.strftime('%m', datetimet))
	td = int(time.strftime('%d', datetimet))
	tH = int(time.strftime('%H', datetimet))
	tM = int(time.strftime('%M', datetimet))
	tS = int(time.strftime('%S', datetimet))
	nowTime = datetime.datetime.now()
	fileTime = datetime.datetime(tY, tm, td, tH, tM, tS)
	return abs((nowTime - fileTime).days)
def clearDebugLog(folder):
	import os
	for roots, dirs, files in os.walk(folder):
		if len(files) > 0:
			for file in files:
				filePath = os.path.join(roots, file)
				fileTimeDiff = get_fileCreatTime_nowTime_diff(filePath)
				if fileTimeDiff >= 10:
					os.remove(filePath)


folder = r'D:\PythonCode\jzsc_mohurd2016\jzsc_mohurd2016\hub_crawl_DEBUG-LOG'
path = r'D:\PythonCode\jzsc_mohurd2016\jzsc_mohurd2016\hub_crawl_DEBUG-LOG\2021-11-21_23-16-14_hub_crawl_DEBUG.log'
# print(get_fileCreatTime(path))
c = get_fileCreatTime_nowTime_diff(path)
print(c)
d = clearDebugLog(folder)
print(d)

# t = time.time()
# nowTime = lambda: int(round(t * 1000))
# nowTime = int(nowTime())
# print(nowTime)
# dtime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# print(dtime)
