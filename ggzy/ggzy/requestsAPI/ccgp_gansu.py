# -*- coding: utf-8 -*-
import pprint
import time, re, datetime
import requests, sys
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from dateutil.relativedelta import relativedelta
import json, os
from mysqlODM import urlIsExist
from bs4 import BeautifulSoup
from urllib import parse as urlparse
# from redis_dup import BloomFilter
from redis_dup import BloomFilter
bl = BloomFilter('uxue:url')

header_raw = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-TW;q=0.8
Connection: close
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36
'''
HEA = dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


def save_api(dict1):
	try:
		dict1['attachmentListJson'] = json.dumps(dict1['attachmentListJson'], ensure_ascii=False)
	except:
		pass
	HEA = {"Connection": "close"}
	try:
		a = requests.post(url='http://183.6.136.70:8035/pc/api/caijiApi/save', data=dict1, headers=HEA)
		if not bl.exists(dict1['url']):
			bl.insert(dict1['url'])
		return json.loads(a.text)
	except Exception as f:
		print('save ERROR ---')
		print(f)
		return None


def get_ListInfo():
	global DOMAIN, INPUTWORD
	datePost = {
		'articleSearchInfoVo.releasestarttime': '',
		'articleSearchInfoVo.releaseendtime': '',
		'articleSearchInfoVo.tflag': '1',
		'articleSearchInfoVo.classname': '128',
		'articleSearchInfoVo.dtype': '',
		'articleSearchInfoVo.days': '',
		'articleSearchInfoVo.releasestarttimeold': '',
		'articleSearchInfoVo.releaseendtimeold': '',
		'articleSearchInfoVo.title': '',
		'articleSearchInfoVo.agentname': '',
		'articleSearchInfoVo.bidcode': '',
		'articleSearchInfoVo.proj_name': '',
		'articleSearchInfoVo.buyername': '',
		'total': '5',
		'limit': '20',
		'current': '1',
		'sjm': '7466',
	}
	baseurl = 'http://www.ccgp-gansu.gov.cn/web/doSearchmxarticlelssj.action?limit=20&start={}'.format(
		str(pageNum * 20))
	brow = requests.post(url=baseurl, data=datePost, headers=HEA)
	if brow.status_code > 299:
		return None
	soup = BeautifulSoup(brow.text, 'lxml')
	linksoup = soup.find('ul', class_='Expand_SearchSLisi')
	linksoup_li = linksoup.find_all('li')
	if len(linksoup_li) == 0:
		return None
	llist = []
	for num, nn in enumerate(linksoup_li):
		item = {}
		try:
			soup_url = nn.find('a').get('href')
			item['url'] = urlparse.urljoin(baseurl, soup_url)
			if bl.exists(item['url']):
				continue
			item['title'] = nn.find('a').get_text()
			issue_time = re.findall("发布时间.*(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})", nn.prettify())
			item['issueTime'] = ''.join(issue_time)
			strongsoup = nn.find('strong')
			subclass_reg = re.findall("<strong>(.*?)\|",
			                          strongsoup.prettify().replace(' ', '').replace('\r', '').replace('\n',
			                                                                                           '').replace(
				                          '\t', ''), re.M | re.S)
			item['subclass'] = ''.join(subclass_reg)
		except:
			continue
		item['site'] = DOMAIN
		if not item['issueTime'] or not item['title'] or not soup_url or not item['subclass'] or not item['url']:
			continue
		llist.append(item)
	return llist


def get_content(ddict):
	global INPUTWORD, DOMAIN
	brow = requests.get(url=ddict['url'], headers=HEA)
	htmll = brow.text.encode(brow.encoding).decode('utf-8')
	soup = BeautifulSoup(htmll, 'lxml')
	# soup.prettify()
	ddict['content'] = soup.find('div', class_='conTxt').prettify()

	hrefall = soup.find_all(href=re.compile("upload/article"))
	ddict['attachmentListJson'] = []
	for nn in hrefall:
		ddict1 = {}
		download_url = nn.get('href')
		ddict1['download_url'] = urlparse.urljoin(ddict['url'], download_url)
		ddict1['name'] = nn.get_text()
		if not ddict1['name']:
			continue
		ddict['attachmentListJson'].append(ddict1)
	return ddict


if __name__ == '__main__':
	INPUTWORD = sys.argv[1]
	# INPUTWORD = 'yes'
	DOMAIN = "www.ccgp-gansu.gov.cn"
	if INPUTWORD == 'yes':
		startNum = 100
	else:
		startNum = 0

	for pageNum in range(startNum, 10000):
		time.sleep(3)
		pageListMark = 0
		while True:
			try:
				llist = get_ListInfo()
				break
			except Exception as f:
				pageListMark += 1
				if pageListMark == 20:
					print('pageListMark erroe')
					print(f)
					exit()
				time.sleep(60)
		if not llist:
			if INPUTWORD == 'no':
				break
			else:
				continue
		for ddict in llist:
			contentMark = 0
			while True:
				try:
					item = get_content(ddict)
					break
				except Exception as ff:
					contentMark += 1
					if contentMark == 20:
						print('Content erroe')
						print(ff)
						exit()
					time.sleep(60)

			a = save_api(item)
			item['content'] = len(item['content'])
			pprint.pprint(item)
			print(a)
			print('-*' * 50)
			time.sleep(3)
