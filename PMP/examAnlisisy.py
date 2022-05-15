# -*- coding: utf-8 -*-
import time
from bs4 import BeautifulSoup
loginInfo = {'user': 'Jinxx1@163.com', 'password': 'hxjinxiao'}
def webdriver_getCookie():
	UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
	pageUrl = "https://idp.pmi.org/Account/Login"
	from selenium.webdriver import Chrome
	from selenium.webdriver.chrome.options import Options
	import os
	root = os.getcwd()
	stealthPath = os.path.join(root, "wd/stealth.min.js")
	chrodriverPath = os.path.join(root, "wd/chromedriver")

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
	try:
		time.sleep(3)
		driver.find_element_by_id("Username").send_keys(loginInfo['user'])
		driver.find_element_by_id("Password").send_keys(loginInfo['password'])
		time.sleep(3)
		driver.find_element_by_id('login_btn').click()
		time.sleep(3)
		driver.get('https://ccrs.pmi.org/reporting/examanalysis')
		time.sleep(3)
		c = driver.page_source
		driver.quit()
		return c
	except:
		driver.quit()
		return None


def sendEmail(ddict):
	import smtplib
	from email.mime.text import MIMEText
	from email.header import Header
	mail_host = 'smtp.exmail.qq.com'
	mail_user = 'umservice@uxuepai.net'
	mail_pass = 'Um20170927'
	mail_port = 465
	sender = mail_user
	receivers = ['jinxx1@163.com']
	message = MIMEText(ddict['body'], 'plain', 'utf-8')
	message['To'] = Header(';'.join(receivers), 'utf-8')
	message['Subject'] = Header(ddict['title'], 'utf-8')
	smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
	smtpObj.ehlo()
	smtpObj.login(mail_user, mail_pass)
	smtpObj.sendmail(sender, receivers, message.as_string())
	smtpObj.quit()


if __name__ == "__main__":
	while True:
		pagesource = webdriver_getCookie()
		if not pagesource:
			continue
		if "erformance" in pagesource or 'Unable to show exam analysis' not in pagesource:
			ddict={}
			ddict['title'] = 'PMP成绩查询页面有变动'
			ddict['body'] = BeautifulSoup(pagesource,'lxml').prettify()
			sendEmail(ddict)
		time.sleep(3600*1)
