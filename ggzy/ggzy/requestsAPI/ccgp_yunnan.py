# -*- coding: utf-8 -*-
import pprint
import time, re, datetime
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dateutil.relativedelta import relativedelta
import json
from bs4 import BeautifulSoup
from mysqlODM import urlIsExist,save_api
from redis_dup import BloomFilter
bl = BloomFilter('uxue:url')

SITE = "www.ccgp-yunnan.gov.cn"
def get_timestr(date, outformat="%Y-%m-%d %H:%M:%S", combdata=False):
	time_array = ''
	format_string = [
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


def openJson():
	with open('ccgp_hubei.json','r') as ff:
		jsonT = json.load(ff)
		ff.close()
	return jsonT

def writeJson(jsonT):
	with open('ccgp_hubei.json','w') as ff:
		json.dump(jsonT,ff)
		ff.flush()
		ff.close()

def webdriver_getCookie():
	global UA
	pageUrl = "http://www.ccgp-yunnan.gov.cn/bulletin.do?method=moreList"
	from selenium.webdriver import Chrome
	from selenium.webdriver.chrome.options import Options
	import os
	root = os.getcwd()
	stealthPath = os.path.join(root, "wd/stealth.min.js")
	chrodriverPath = os.path.join(root, "wd/chromedriver")
	# proxIP = "118.24.219.151:16818"

	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument(
		'user-agent={}'.format(UA))
	chrome_options.add_argument("--disable-blink-features=AutomationControlled")
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('blink-settings=imagesEnabled=false')
	chrome_options.add_argument('--disable-gpu')
	chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
	driver = Chrome(chrodriverPath, options=chrome_options)
	with open(stealthPath, 'r') as f:
		js = f.read()
	driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
	driver.get(pageUrl)
	time.sleep(3)
	driver.refresh()
	c = driver.get_cookies()
	cookies = {}
	# 获取cookie中的name和value,转化成requests可以使用的形式
	for cookie in c:
		cookies[cookie['name']] = cookie['value']
	driver.quit()
	return cookies



def dupcutUrl(llist):
	global DUPURL
	urllist = [x['url'] for x in llist]
	while True:
		retD = urlIsExist(urllist)
		if retD != 'error':
			# print('------------------------未被录入的条目有：',len(retD))
			break

	newList = []
	for num,n in enumerate(llist):
		if n['url'] in retD:
			newList.append(n)
	return newList

def input_yes():
	global UA,HEA,index_cookies,SITE
	jsonT = openJson()
	for num, i in enumerate(jsonT):
		if i['pageNum'] == i['ttlpage']:
			continue
		for nn in range(i['pageNum'],i['ttlpage']+1):
			time.sleep(3)
			infoList = get_list(cooki=index_cookies, HEA=HEA, Time=i['datatime'], pageNum=nn)
			if not infoList:
				break
			infoList = dupcutUrl(infoList)
			if not infoList:
				continue
			for cNum,contentInfo in enumerate(infoList):
				time.sleep(3)
				content = get_content(contentInfo['url'])
				infoList[cNum]['attachmentListJson'] = ''
				if content['attachmentListJson']:
					infoList[cNum]['attachmentListJson'] = content['attachmentListJson']
				else:
					del infoList[cNum]['attachmentListJson']
				infoList[cNum]['content'] = content['content']
				a = save_api(infoList[cNum])
				infoList[cNum]['content'] = len(infoList[cNum]['content'])
				pprint.pprint(infoList[cNum]['url'])
				print(a)
				print('-----------------------------------------------------')
			jsonT[num]['pageNum'] = nn
			writeJson(jsonT)

def get_content(url,id,index_cookies):
	global HEA
	HEA1 = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
		"Cache-Control": "max-age=0",
		"Connection": "close",
		"Host": "www.ccgp-yunnan.gov.cn",
	}
	brow = requests.get(url=url, headers=HEA1, cookies=index_cookies)
	htmll = brow.text
	ddict = {}
	ddict['url'] = url
	soup = BeautifulSoup(htmll,'lxml')
	ddict['content'] = soup.find('div',class_='table').prettify().replace('''style="display: block;"''','')
	attmentUrl =  "http://www.ccgp-yunnan.gov.cn/filemanager.do?method=listnew&business_id=2000&pk_id={}&candel=0&flag=1".format(id)
	HEAJSON = {
		"Accept": "*/*",
		"Accept-Encoding": "gzip, deflate",
		"Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
		"Connection": "keep-alive",
		"Host": "www.ccgp-yunnan.gov.cn",
		"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		"Origin": "http://www.ccgp-yunnan.gov.cn",
		"Referer": url,
	}
	postdate = {'current': '1',
		'rowCount': '50',
		'searchPhrase':''}
	attmentBrow = requests.post(data=postdate,url=attmentUrl, cookies=index_cookies,headers=HEAJSON)
	attJsonT = json.loads(attmentBrow.text)
	if attJsonT['rows']:
		attachmentListJson = []
		from urllib.parse import quote
		for i in attJsonT['rows']:
			ddict1 = {}
			ddict1['download_url'] = "http://www.ccgp-yunnan.gov.cn/filemanager.do?method=downloadFile&file_id={id}&file_name={pdfname}&completeurl={downurl}".format(
			# pdfname = quote(i['file_name'], 'utf-8'),
			# downurl = quote(i['completeurl'], 'utf-8'),
			# id = quote(i['file_id'], 'utf-8'))
			pdfname = i['file_name'],
			downurl = i['completeurl'],
			id = i['file_id'])
			ddict1['name'] = i['file_name']
			attachmentListJson.append(ddict1)
		ddict['attachmentListJson'] = attachmentListJson

	return ddict

def get_list(cooki,HEA,pageNum,query_sign,Times,getallpageNum=True):
	global SITE
	postDate = {
		'current': str(pageNum),
		'rowCount': str(100),
		'query_sign': str(query_sign),
		'query_startTime':str(Times),
		'query_endTime': str(Times)
	}
	url = "http://www.ccgp-yunnan.gov.cn/bulletin.do?method=moreListQuery"
	brow = requests.post(url=url,data=postDate,headers=HEA,cookies=cooki)
	jsonT = json.loads(brow.text)
	# print('页面中共有：',len(jsonT['rows']))

	if not getallpageNum:
		llist = []
		for num, info in enumerate(jsonT['rows']):
			# if num > 1:
			# 	continue
			ddict = {}
			ddict['issueTime'] = get_timestr(info['finishday'])
			ddict['subclass'] = info['bulletinclasschina']
			ddict['title'] = info['bulletintitle']
			ddict['site'] = SITE
			ddict['bulletin_id'] = info['bulletin_id']
			ddict['url'] = "http://www.ccgp-yunnan.gov.cn/newbulletin_zz.do?method=preinsertgomodify&operator_state=1&flag=view&bulletin_id={}".format(
				info['bulletin_id'])
			llist.append(ddict)
		return llist
	else:
		return int(jsonT['totlePageCount'])


def body(Times):
	global SITE,UA,HEA
	index_cookies = webdriver_getCookie()
	for subclassID in range(1,8):
		if subclassID == 6:
			continue
		print('类别为：',subclassID)
		pageALL = get_list(cooki=index_cookies,HEA=HEA,pageNum=1,query_sign=subclassID,Times=Times,getallpageNum=True)
		for pageNum in range(1, pageALL + 1):
			infoList = get_list(cooki=index_cookies,HEA=HEA,pageNum=pageNum,query_sign=subclassID,Times=Times,getallpageNum=False)
			if not infoList:
				print('------------------------本页没有文章可被录入')
				continue
			infoList = dupcutUrl(infoList)
			if not infoList:
				continue
			else:
				for cNum, contentInfo in enumerate(infoList):
					time.sleep(3)
					content = get_content(url=contentInfo['url'],id=contentInfo['bulletin_id'],index_cookies=index_cookies)
					final_dict = {**contentInfo,**content}
					a = save_api(final_dict)
					final_dict['content'] = len(final_dict['content'])
					pprint.pprint(final_dict['url'])
					print(a)
					# pprint.pprint(final_dict)
					print(datetime.datetime.now())
					print('-----------------------------------------------------第{}页中的第{}篇文章,时间为{}'.format(pageNum,cNum+1,Times))


if __name__ == '__main__':

	import sys
	inputWord = sys.argv[1]
	# inputWord = 'no'
	if not inputWord or inputWord not in ['yes','no']:
		print('not input')
	SITE = "www.ccgp-yunnan.gov.cn"
	UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
	HEA = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
		'Connection': 'keep-alive',
		'Content-Length': '49',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'User-Agent': UA,
		}
	if inputWord == 'no':
		Times = datetime.datetime.now().strftime("%Y-%m-%d")
		body(Times=Times)
		print('本次抓取结束')
	elif inputWord == 'yes':
		TimesList = ["2021-07-15",
		         "2021-07-14",
		         "2021-07-13",
		         "2021-07-12",
		         "2021-07-11",
		         "2021-07-10",
		         "2021-07-09",
		         "2021-07-08",
		         "2021-06-27",
		         "2021-06-26",
		         "2021-06-25"]
		for Times in TimesList:
			body(Times=Times)
			time.sleep(3 * 2)




