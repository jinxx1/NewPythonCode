# -*- coding: utf-8 -*-
import pprint
import time, re, datetime
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dateutil.relativedelta import relativedelta
import json
from bs4 import BeautifulSoup
from mysqlODM import urlIsExist
import pysnooper
from redis_dup import BloomFilter
bl = BloomFilter('uxue:url')

def get_timestr(date, outformat="%Y-%m-%d", combdata=False):
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

def encode64_forDonload(s):
	import base64
	s1 = s.encode('utf-8')
	a = base64.b64encode(s1)
	baseUrl = 'http://www.ccgp-hubei.gov.cn:8090/gpmispub/download?id={}'.format(a.decode('utf-8'))
	return baseUrl

def getBetweenDay(begin_date):
	date_list = []
	begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
	end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
	while begin_date <= end_date:
		date_str = begin_date.strftime("%Y-%m-%d")
		date_list.append(date_str)
		begin_date += datetime.timedelta(days=1)
	return date_list


def betweenTime(beginTime,lastdays):
	llist = []
	# print(relativedelta(days=1))
	llist = []
	for i in range(0,lastdays):
		ddict ={}
		ddict['datatime'] = beginTime.strftime("%Y/%m/%d")
		ddict['pageNum'] = 1
		ddict['ttlpage'] = 0
		llist.append(ddict)
		beginTime -= relativedelta(days=1)
	print(len(llist))
	with open('ccgp_hubei.json','w') as ff:
		json.dump(llist,ff)
		ff.flush()
		ff.close()

	return llist


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
	pageUrl = "http://www.ccgp-hubei.gov.cn:9040/quSer/searchXmgg.html"
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

def timeCovert(timeword):
	try:
		GMT_FORMAT = '%a %b %d %H:%M:%S GMT+08:00 %Y'
		time_format = datetime.datetime.strptime(timeword, GMT_FORMAT).strftime("%Y-%m-%d %H:%M:%S")
	except:
		time_format = get_timestr(timeword,"%Y-%m-%d %H:%M:%S")
	return time_format


def get_list(cooki,HEA,Time,pageNum):
	global SITE
	postDate = {
	"queryInfo.type": "xmgg",
	"queryInfo.city": "湖北省",
	"queryInfo.district": "全省",
	"queryInfo.begin": Time,
	"queryInfo.end": Time,
	"queryInfo.pageNo": pageNum,
	"queryInfo.pageSize": '15',
}
	url = "http://www.ccgp-hubei.gov.cn:9040/quSer/search"
	brow = requests.post(url=url,data=postDate,headers=HEA,cookies=cooki)

	soup = BeautifulSoup(brow.text,'lxml')
	element = soup.find_all('li', class_='serach-page-results-item')
	llist = []
	for i in element:
		ddict = {}
		ddict['url'] = i.find('div', class_='title ellipsis').find('a').get('href')
		ddict['issueTime'] = timeCovert(i.find(name='div', class_='time').get_text())
		ddict['subclass'] = i.find(name='div', attrs={'class': "type-col"}).find('font').get_text()
		ddict['title'] = i.find('div', class_='title ellipsis').find('a').get_text()
		ddict['site'] = SITE
		llist.append(ddict)
	return llist

def dupcutUrl(llist):
	global DUPURL
	urllist = [x['url'] for x in llist]
	while True:
		retD = urlIsExist(urllist)

		if retD != 'error':
			break

	newList = []
	for num,n in enumerate(llist):
		if n['url'] in retD:
			newList.append(n)
	return newList


def save_api(dict1):
	try:
		dict1['attachmentListJson'] = json.dumps(dict1['attachmentListJson'], ensure_ascii=False)
	except:
		pass

	HEA = {
		"Connection": "close",
	}
	try:
		a = requests.post(url='http://183.6.136.70:8035/pc/api/caijiApi/save', data=dict1, headers=HEA)
		bl.insert(dict1['url'])
		return json.loads(a.text)
	except Exception as f:
		print('save ERROR ---')
		print(f)
		return None

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

def get_content(url):
	global HEA, index_cookies
	brow = requests.get(url=url, headers=HEA, cookies=index_cookies)
	htmll = brow.text.encode(brow.encoding).decode('utf-8')
	ddict = {}
	soup = BeautifulSoup(htmll,'lxml')
	# soup.prettify()
	print('url-----------------------------',url)
	ddict['content'] = soup.find('div',class_='art_con').prettify()

	hrefall = soup.find_all(href=re.compile("downloadFile"))
	ddict['attachmentListJson'] = []
	for nn in hrefall:
		ddict1 = {}
		download_url = nn.get('href')
		url = re.findall("encodeBase64\(\'(.*?)\'\)",download_url)
		ddict1['download_url'] = encode64_forDonload(''.join(url))
		ddict1['name'] = nn.get('download')
		if not ddict1['name']:
			continue
		ddict['attachmentListJson'].append(ddict1)
	return ddict

def input_no():
	ttime = datetime.datetime.now().strftime("%Y/%m/%d")
	# ttime = '2021/12/25'
	global UA, HEA, index_cookies, SITE
	for nn in range(1,100):
		print('into for ',nn)
		time.sleep(3)
		infoList = get_list(cooki=index_cookies, HEA=HEA, Time=ttime, pageNum=nn)
		print('infoList1-----------------------', len(infoList))
		if len(infoList) == 0:
			# pass
			break
		infoList = dupcutUrl(infoList)
		if not infoList:
			# pass
			break
		else:
			for cNum, contentInfo in enumerate(infoList):
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
				print('-----------------------------------------------------',nn,cNum)


def input_chose(ttime):
	global UA, HEA, index_cookies, SITE

	for nn in range(1,100):
		print('into for ',nn)
		time.sleep(1)
		infoList = get_list(cooki=index_cookies, HEA=HEA, Time=ttime, pageNum=nn)
		print('infoList1-----------------------', len(infoList))
		if len(infoList) == 0:
			break
		infoList = dupcutUrl(infoList)
		if not infoList:
			continue
		else:
			for cNum, contentInfo in enumerate(infoList):
				time.sleep(3)
				if contentInfo['url']=='http://www.ccgp-hubei.gov.cn':
					continue

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
				print('-----------------------------------------------------',nn,cNum,ttime)


if __name__ == '__main__':
	import sys
	inputWord = sys.argv[1]
	# inputWord = 'no'
	if not inputWord or inputWord not in ['yes','no','chose']:
		print('not input')

	SITE = "www.ccgp-hubei.gov.cn"
	UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
	HEA = {"User-Agent": UA}
	if inputWord == 'yes':
		index_cookies = webdriver_getCookie()
		input_yes()
	if inputWord == 'no':
		try:
			index_cookies = webdriver_getCookie()
			input_no()
		except Exception as fff:
			print('ERROR:\t',fff)
		print('本次抓取完成--', datetime.datetime.now())

	if inputWord == 'chose':
		timeNow = datetime.date.today()
		lastM = timeNow - relativedelta(months=4)
		aa = getBetweenDay('2021-11-9')
		ttimeList = [x.replace('-', '/') for x in aa]
		for ttime in ttimeList:
			print(ttime)
			index_cookies = webdriver_getCookie()
			input_chose(ttime)