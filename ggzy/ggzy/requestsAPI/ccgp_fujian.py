# -*- coding: utf-8 -*-
import pprint
import time, re, datetime
import requests,os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dateutil.relativedelta import relativedelta
import json
from bs4 import BeautifulSoup
from mysqlODM import urlIsExist
from urllib import parse as urlparse



header_raw = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: close
Host: zfcg.czt.fujian.gov.cn
Referer: https://zfcg.czt.fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/
sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
sec-ch-ua-mobile: ?0
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36
'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')
UA = HEA['User-Agent']




def webdriver_getCookie():
	from PIL import Image
	from selenium import webdriver
	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC
	import os
	global UA
	savePath = os.getcwd()

	cover_pic_path = os.path.join(savePath, "img_cover.png")
	cooikes_path = os.path.join(savePath,'cookies_fujian.json')
	pageUrl = "http://zfcg.czt.fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/"
	codeImgBase = "http://zfcg.czt.fujian.gov.cn/"
	from selenium.webdriver import Chrome
	from selenium.webdriver.chrome.options import Options
	import os
	root = os.getcwd()
	stealthPath = os.path.join(root, "wd/stealth.min.js")
	chrodriverPath = os.path.join(root, "wd/chromedriver")
	# proxIP = "118.24.219.151:16818"

	chrome_options = Options()
	# chrome_options.add_argument("--headless")
	chrome_options.add_argument(
		'user-agent={}'.format(UA))
	chrome_options.add_argument("--disable-blink-features=AutomationControlled")
	chrome_options.add_argument('--no-sandbox')
	# chrome_options.add_argument('blink-settings=imagesEnabled=false')
	# chrome_options.add_argument('--disable-gpu')
	chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
	driver = Chrome(chrodriverPath, options=chrome_options)
	with open(stealthPath, 'r') as f:
		js = f.read()
	driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
	driver.set_window_size(1024, 768)
	# try:
	driver.get(pageUrl)
	time.sleep(3)
	# print(driver.page_source)
	driver.set_window_size(1024, 768)
	csrfmiddlewaretoken = driver.find_element_by_xpath("//input[@name = 'csrfmiddlewaretoken']").get_attribute('value')
	verifycode = driver.find_element_by_xpath("//img[@id = 'verifycode']")
	verifycode.screenshot(cover_pic_path)

	element = WebDriverWait(driver, 30).until(
		EC.presence_of_element_located((By.CLASS_NAME, "gradeX"))
	)
	element.click()

	print(driver.page_source)
	print(csrfmiddlewaretoken)
	print(verifycode)

	c = driver.get_cookies()
	cookiesTemp = {}
	# 获取cookie中的name和value,转化成requests可以使用的形式
	for cookie in c:
		cookiesTemp[cookie['name']] = cookie['value']
	with open(cooikes_path,'w',encoding='utf-8') as cookieFile:
		json.dump(cookiesTemp,cookieFile)
		cookieFile.flush()
		cookieFile.close()


	driver.quit()

	# return {
	# 	"csrfmiddlewaretoken":csrfmiddlewaretoken
	# }


if __name__ == '__main__':

	# a = webdriver_getCookie()
	savePath = os.getcwd()

	cover_pic_path = os.path.join(savePath, "img_cover.png")
	cooikes_path = os.path.join(savePath,'cookies_fujian.json')

	url ="http://zfcg.czt.fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/?page={}"
	with open(cooikes_path,'r',encoding='utf-8') as cookieFile:
		cookiesJson = json.load(cookieFile)


	for Num in range(1,11):
		time.sleep(3)
		# if Num == 1:
		# 	url = url.replace("/?page={}","")
		# 	brow = requests.get(url=url,cookies=cookiesJson,headers = HEA)
		# else:
		brow = requests.get(url=url.format(str(Num)), cookies=cookiesJson, headers=HEA)
		soup = BeautifulSoup(brow.text,'lxml')
		trget = soup.find_all("tr",class_='gradeX')
		LLIST = []
		dupList = []
		for n,ii in enumerate(trget):

			ddict = {}
			ddict['pageNum'] = Num
			ddict['artNum'] = n+1
			ddict['mark'] = 0

			ddict['title'] = ii.find("a").get_text()
			ddict['href'] = ii.find("a").get('href')
			pprint.pprint(ddict)

			print('---------------------------',Num,n)


	exit()

