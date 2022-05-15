import aiohttp
import asyncio
import csv
import json
import random
import re
import requests
import time
import pprint

from jzsc_mohurd2016.decrypt import AESDecrypt
from jzsc_mohurd2016.settings import USER_AGENT
HEA = {
'Connection': 'close',
'User-Agent': USER_AGENT
}


class JZSC:
	apt_url = "http://jzsc.mohurd.gov.cn/api/webApi/asite/qualapt/aptData"
	region_url = "http://jzsc.mohurd.gov.cn/api/webApi/asite/region/index"
	file_header = ('企业名称', '企业法定代表人', '企业注册属地', '统一社会信用代码', '文章代码', '旧代码', '发布时间', 'IS_FAKE')
	# 获取地区信息
	def get_region_list(self):
		response = requests.get(self.region_url, headers=HEA)
		if not response.ok:
			return []
		data = AESDecrypt.decrypt(response.text)
		return [(item['region_id'], item['region_name']) for item in json.loads(data)['data']['category']['provinces']]
	# 获取资质信息
	def get_apt_list(self):
		# 获取资质信息
		response = requests.get(self.apt_url, headers=HEA)
		if not response.ok:
			return []
		data = AESDecrypt.decrypt(str(response.text))
		return [(item['APT_CODE'], item['APT_CASENAME']) for item in json.loads(data)['data']['pageList']]

	# 根据不同API获取企业信息
	def artinfo(self,apiUrl,token):
		# 根据不同API获取企业信息
		HEA['accessToken'] = token
		ok = False
		aes = ''
		for i in range(3):
			response = requests.get(apiUrl, headers=HEA,timeout=(10,10))
			if response.ok:
				ok = True
				aes = response.text
				break
		if not ok:
			print('not response')
			return None
		else:
			return AESDecrypt.decrypt(aes)


def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)
if __name__ == '__main__':
	import os
	obj = JZSC()
	aptAll = obj.get_apt_list()
	regionAll = obj.get_region_list()
	# aaa = obj.artinfo()
	baseUrl = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?qy_region={region}&apt_code={aptcode}&pg=0123456789abcd&pgsz=15"
	root= r"D:\PythonCode\jzsc_mohurd2016\jzsc_mohurd2016\urlAll"
	llist = []
	for reg in regionAll:
		for apt in aptAll:
			ddict = {}
			apt_temp = apt[0].replace('\t','')
			# apt_temp = apt[0]
			url= baseUrl.format(region=reg[0],aptcode=apt_temp)
			ddict['url'] = url.replace('0123456789abcd','{}')
			ddict['reg_Name'] = reg[1]
			ddict['apt_Name'] = apt[1].replace('/','_')
			ddict['reg_id'] = reg[0]
			ddict['apt_id'] = apt_temp
			ddict['total'] = 0
			ddict['crawled_pageNum'] = 0
			ddict['crawled_articleNum'] = 0
			ddict['status'] = 0
			llist.append(ddict)
			# pprint.pprint(ddict)
			# print('-----------')

	for info in llist:
		info_folder = os.path.join(root,info['reg_id'])
		mkdir(info_folder)
		info_Name = str(info['apt_id']) + '_Info.json'
		info_path = os.path.join(info_folder,info_Name)

		try:
			with open(info_path,'w',encoding='utf-8') as ff:
				json.dump(info,ff,ensure_ascii=False)
		except:
			pprint.pprint(info)