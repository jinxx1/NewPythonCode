import datetime
import os.path
import pprint
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import lxml.html
import sys, json, re
import sqlalchemy
import requests
import pandas as pd

def save_api(dict1):
	HEA = {"Connection": "close"}
	try:
		a = requests.post(url='https://umxh.xue2you.cn/pc/api/caijiApi/save', data=dict1, headers=HEA)
		return json.loads(a.text)
	except:
		return None

def urlIsExist(urllist):
	HEA = {"Connection": "close"}
	posturlapi = 'https://umxh.xue2you.cn/pc/api/caijiApi/urlIsExist'
	str_c = json.dumps(urllist)
	dataApi = {"urlListJson": str_c}
	try:
		a = requests.post(url=posturlapi, data=dataApi, headers=HEA)
		jsonT = json.loads(a.text)
		return jsonT['data']
	except:
		return None

def depcut(llist):
	crawlList = [x['page_url'] for x in llist]
	nomysqllist = urlIsExist(crawlList)
	allist = []
	for i in nomysqllist:
		for n in llist:
			if i == n['page_url']:
				allist.append(n)
	return allist

def get_timestr(date, outformat="%Y-%m-%d", combdata=False):
	import time
	time_array = ''
	format_string = [
		"%Y-%m-%d %H:%M:%S",
		"%Y-%m-%d %H:%M",
		"%Y-%m-%d %H",
		"%Y-%m-%d",
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

def get_content(html):
	soup = BeautifulSoup(html, 'lxml')
	ddict = {}
	try:
		ddict['title'] = soup.h1.get_text()
	except:
		return None
	try:
		ddict['content'] = str(soup.find(attrs={'class': 'zb_table'}))
	except:
		return None
	hrefall = soup.find_all(href=re.compile("commonDownload\.html\?attId"))
	attachmentListJsonList = []
	for nn in hrefall:
		dic = {}
		download_url = nn.get('href')
		dic['download_url'] = "https://b2b.10086.cn" + download_url
		dic['name'] = nn.get_text()
		attachmentListJsonList.append(dic)
	if attachmentListJsonList:
		ddict['attachmentListJson'] = json.dumps(attachmentListJsonList, ensure_ascii=False)
	return ddict

def get_urlList():
	excWord = "SELECT id,page_url,issue_time,subclass FROM listform10086 WHERE process_status = 0 ORDER BY issue_time DESC;"
	alltoup = mysqlcon.execute(excWord)
	llist = []
	for n in alltoup:
		ddict = {}
		ddict['id'] = n[0]
		ddict['page_url'] = n[1]
		ddict['issue_time'] = str(n[2])
		ddict['subclass'] = n[3]
		llist.append(ddict)
	return llist

def update_stats(artID):
	excWord = '''UPDATE listform10086 SET process_status=1 WHERE id={};'''.format(artID)
	mysqlcon.execute(excWord)

def artcleMain(driver):
	llist = get_urlList()
	if not llist:
		return None
	for num, i in enumerate(llist):
		driver.get(i['page_url'])
		time.sleep(3)
		content_info = get_content(driver.page_source)
		item = {}
		item['title'] = content_info['title']
		item['content'] = content_info['content']
		item['subclass'] = i['subclass']
		item['issueTime'] = i['issue_time']
		item['url'] = i['page_url']
		item['site'] = "b2b.10086.cn"
		item['itemID'] = i['id']
		if 'attachmentListJson' in content_info.keys():
			item['attachmentListJson'] = content_info['attachmentListJson']
		a = save_api(item)
		item['content'] = len(item['content'])
		pprint.pprint(item)
		print(a)
		print('-----' * 8,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		update_stats(i['id'])

def artcleMain1(driver,ddict):
	driver.get(ddict['page_url'])
	time.sleep(3)
	content_info = get_content(driver.page_source)
	item = {}
	item['title'] = content_info['title']
	item['content'] = content_info['content']
	item['subclass'] = ddict['subclass']
	item['issueTime'] = ddict['issue_time']
	item['url'] = ddict['page_url']
	item['site'] = "b2b.10086.cn"

	if 'attachmentListJson' in content_info.keys():
		item['attachmentListJson'] = content_info['attachmentListJson']
	a = save_api(item)
	item['content'] = len(item['content'])
	pprint.pprint(item)
	print(a)
	print('-----' * 8,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def urlListUrl():
	wword = '''采购公告	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2
资格预审公告	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=3
候选人公示	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=7
中选结果公示	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=16
单一来源采购信息公告	https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=1'''.split('\n')
	llist = []
	for i in wword:
		n = i.split('\t')
		ddict = {}
		ddict['subclass'] = n[0]
		ddict['listUrl'] = n[1]
		llist.append(ddict)
	return llist

def get_IDandTIME(html):
	llist = []
	artcle_urls = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id={}'
	resID = re.findall("selectResult\(\'(.*?)\'\)", html)
	soup = BeautifulSoup(html, 'lxml')
	for id in resID:
		all_tr = soup.find_all(attrs={'onclick': "selectResult('{id}')".format(id=id)})
		for i in all_tr:
			try:
				timeWord = re.findall("(\d{4}-\d{1,2}-\d{1,2})", str(i))[0]
				timeWord = get_timestr(timeWord, "%Y-%m-%d %H:%M:%S")
			except:
				print('no timeWord')
				continue
			ddict = {'issue_time': timeWord, 'page_url': artcle_urls.format(id)}
			llist.append(ddict)
	return depcut(llist)

def mainCrawl():
	brow = requests.get('http://120.79.3.69:8050/')
	if brow.status_code != 200:
		print('Please contact the jinxiao')
		return None
	else:
		pass
	MYSQLINFO = {
		"HOST": "183.6.136.67",
		"DBNAME": "jxtest",
		"USER": "jinxiao_67",
		"PASSWORD": "Jinxiao1234@qwer",
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
	root = os.getcwd()
	stealthPath = os.path.join(root, "wd/stealth.min.js")
	chrodriverPath = os.path.join(root, "wd/chromedriver")

	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument(
		'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko')
	chrome_options.add_argument("--disable-blink-features=AutomationControlled")
	chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
	driver = Chrome(chrodriverPath, options=chrome_options)
	with open(stealthPath, 'r') as f:
		js = f.read()
	driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
	artcleMain(driver)
	for num, i in enumerate(urlListUrl()):
		driver.get(i['listUrl'])
		time.sleep(5)
		while True:
			if "zb_table_tr" not in driver.page_source:
				driver.refresh()
				time.sleep(3)
			else:
				source = driver.page_source
				browList = get_IDandTIME(source)
				break
		df = pd.DataFrame(browList, columns=['issue_time', 'page_url'])
		df['subclass'] = i['subclass'].strip()
		insertInfo = df.to_sql(name='listform10086', con=mysqlcon, if_exists='append', index=False,
							   chunksize=1000)
		print(i['subclass'],len(df),datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
	time.sleep(10)
	artcleMain(driver)
	driver.quit()
	print('===================本次抓取全部完成===================',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == '__main__':

	while True:
		try:
			mainCrawl()
		except Exception as f:
			print('出现了问题：',f)
		time.sleep(600)