# -*- coding: utf-8 -*-
import requests
import execjs
import time
from pprint import pprint

def get_page(pageNum,parameters,headers):
	url = "http://match.yuanrenxue.com/api/match/1?page={}&m={}".format(pageNum,parameters)
	print(url)
	brow = requests.get(url,headers=headers)
	return brow.json()

def calcovlat_a_value():
	with open('match1.js','r',encoding='utf-8') as f:
		jsdate = f.read()
	jsdate = execjs.compile(jsdate)
	psd = jsdate.call('request')
	psd = psd.replace("丨",'%E4%B8%A8')
	print('psd is ')
	print(psd)
	print('-------------------------------')
	return psd

if __name__ == '__main__':
	# parameters = calcovlat_a_value()
	# print(parameters)
	headers = {'Host': 'match.yuanrenxue.com',
		'Referer': 'http://match.yuanrenxue.com/match/1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
		'X-Requested-With': 'XMLHttpRequest',
		'Accept': 'application/json,text/javascript,*/*;q=0.01'}
	sum_count = 0
	sum_num = 0
	for i in range(1,6):
		if i == 4 or i == 5:
			headers['User-Agent'] = 'yuanrenxue.project'
		jsonT = get_page(i,calcovlat_a_value(),headers=headers)['data']
		sList = [x['value'] for x in jsonT]
		sum_count += sum(sList)
		sum_num += len(sList)
		print(sum_count,sum_num)
	print(sum_count/sum_num)


