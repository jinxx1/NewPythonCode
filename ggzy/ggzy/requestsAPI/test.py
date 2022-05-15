# -*- coding: utf-8 -*-
import pprint
import time, re, datetime
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dateutil.relativedelta import relativedelta
import json,os
from bs4 import BeautifulSoup

def timeCovert(timeword):
	# timeword = "Sun Jun 13 22:19:34 GMT+08:00 2021"
	try:
		GMT_FORMAT = '%a %b %d %H:%M:%S GMT+08:00 %Y'
		time_format = datetime.datetime.strptime(timeword, GMT_FORMAT)
	except:
		time_format = timeword
	return time_format

def encode64_forDonload(s):
	import base64
	s1 = s.encode('utf-8')
	a = base64.b64encode(s1)
	baseUrl = 'http://www.ccgp-hubei.gov.cn:8090/gpmispub/download?id={}'.format(a.decode('utf-8'))
	return baseUrl

def save_api(dict1):
	HEA = {
		"Connection": "close",
	}

	a = requests.post(url='http://183.6.136.70:8035/pc/api/caijiApi/save', data=dict1, headers=HEA)
	return json.loads(a.text)


header_raw = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36
'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')



def get_csf_imgcod():
	from urllib import parse as urlparse
	fujianurl = "http://zfcg.czt.fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/"
	codeImgBase = "http://zfcg.czt.fujian.gov.cn/"
	brow = requests.get(url=fujianurl)
	# print(brow.text)
	soup = BeautifulSoup(brow.text, 'lxml')
	verifycode = soup.find('img', id='verifycode2').get('src')
	imgcodeIMG = urlparse.urljoin(codeImgBase, verifycode)
	print(imgcodeIMG)
	csrfmiddlewaretokenCODE = soup.find(name='input', attrs={'name': 'csrfmiddlewaretoken'}).get('value')
	print(csrfmiddlewaretokenCODE)

	imgBrow = requests.get(url=imgcodeIMG)
	with open('imgcode.gif', 'wb') as f:
		f.write(imgBrow.content)
		f.flush()
		f.close()
	return csrfmiddlewaretokenCODE



if __name__ == '__main__':
	# csrtoken1 = get_csf_imgcod()
	csrtoken = 'iHFW50YKWiSgfCMkMjEU2HZFFKQj4i7JcRwDIwJ2hdTUUVx5Kq9fCTJIUwnd6CPW'
	imgcode = '丛四册瓜'
	postUrl = "http://zfcg.czt.fujian.gov.cn/3500/noticelist/d03180adb4de41acbb063875889f9af1/?csrfmiddlewaretoken={csrfmiddlewaretoken}&zone_code=&zone_name=&croporgan_name=&project_no=&fromtime=&endtime=&gpmethod=&agency_name=&title=&notice_type=&open_type=&verifycode={verifycode}"
	postUrlget =postUrl.format(csrfmiddlewaretoken=csrtoken,verifycode=imgcode)

	brow = requests.get(url=postUrlget)
	print(brow.text)

