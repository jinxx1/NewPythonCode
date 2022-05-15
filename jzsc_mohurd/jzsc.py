import aiohttp
import asyncio
import csv
import json
import random
import re
import requests
import time
import pprint

from decrypt import AESDecrypt

HEA = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}


class JZSC:
	url = 'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?pg=%d&pgsz=%d'
	apt_url = "http://jzsc.mohurd.gov.cn/api/webApi/asite/qualapt/aptData"
	region_url = "http://jzsc.mohurd.gov.cn/api/webApi/asite/region/index"
	proxy_url = "http://127.0.0.1:5010"
	art_url = 'http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/caDetailList?qyId=002105291239451309&pg=0&pgsz=15'

	file_header = ('企业名称', '企业法定代表人', '企业注册属地', '统一社会信用代码', '文章代码', '旧代码', '发布时间', 'IS_FAKE')

	# 每页大小100条
	pgsz = 100

	def __init__(self, start_page=1, end_page=3838):
		# 设置抓取的起始页和结束页
		self.start_page = start_page
		self.end_page = end_page

	# 获取地区信息
	def get_region_list(self):

		response = requests.get(self.region_url, headers=HEA)
		if not response.ok:
			return []
		data = AESDecrypt.decrypt(response.text)

		print('--------get_region_list---------star')
		pprint.pprint(data)
		print('--------get_region_list---------end')

		return [(item['region_id'], item['region_name']) for item in json.loads(data)['data']['category']['provinces']]

	# 获取资质信息
	def get_apt_list(self):
		# 获取资质信息

		response = requests.get(self.apt_url, headers=HEA)
		if not response.ok:
			return []

		data = AESDecrypt.decrypt(str(response.text))

		print('--------get_apt_list---------star')
		pprint.pprint(data)
		print('--------get_apt_list---------end')
		return [(item['APT_CODE'], item['APT_CASENAME']) for item in json.loads(data)['data']['pageList']]

	# 获取资质信息
	def artinfo(self):
		# 获取资质信息
		HEA['accessToken'] = 'jkFXxgu9TcpocIyCKmJ+tfpxe/45B9dbWMUXhdY7vLWdrHGu7svGXuj5YuAfxvnxhpUUKvcMtoMqfGfwdLCb8g=='

		response = requests.get(self.art_url, headers=HEA)
		print(response)
		if not response.ok:
			print('not response')
			return []
		print(response.text)
		data = AESDecrypt.decrypt(response.text)

		print('--------get_apt_list---------star')
		pprint.pprint(data)
		print('--------get_apt_list---------end')

	# return [(item['APT_CODE'], item['APT_CASENAME']) for item in json.loads(data)['data']['pageList']]

	async def request(self, session, page):
		HEA = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
		}
		# 请求目标页面
		# 随机睡1-300秒不等，防止并发太高
		await asyncio.sleep(random.randint(1, 60))
		while True:
			# proxy = await self.get_proxy(session)
			try:
				# async with session.get(self.url % (page, self.pgsz), proxy=proxy, timeout=30) as response:
				async with session.get(self.url % (page, self.pgsz), timeout=30, hearder=HEA) as response:
					if response.status == 200:
						print(f'第{page}页数据已抓取！')
						return (await response.text(), page)
					elif response.status == 401:
						print(f'{page} 系统繁忙。。。')
						await asyncio.sleep(5)
					else:
						print('else -----')
					# await self.delete_proxy(session, proxy)
			except Exception:  # 代理异常
				# await self.delete_proxy(session, proxy)
				print('-------Exception')

	async def parse_data(self, enc_str):

		try:
			data = json.loads(AESDecrypt.decrypt(enc_str))


		except ValueError:
			return []
		items = data['data']['list']
		ret = []
		for item in items:
			ret.append((item['QY_NAME'], item['QY_FR_NAME'], item['QY_REGION_NAME'], item['QY_ORG_CODE'], item['QY_ID'],
			            item['OLD_CODE'], item['COLLECT_TIME'], item['IS_FAKE']))
		return ret

	async def fetch(self):

		async with aiohttp.ClientSession() as session:
			tasks = []
			for page in range(self.start_page, self.end_page + 1):
				# task = asyncio.create_task(self.request(session, page))
				tasks.append(asyncio.create_task(self.request(session, page)))
				with open(f'data/jzsc_{self.start_page}_{self.end_page}.csv', 'w') as fp:
					writer = csv.writer(fp)
					writer.writerow(self.file_header)
					for task in tasks:
						enc_str, page = await task
						items = await self.parse_data(enc_str)
						if not items:  # 如果数据为空，说明抓取错误，则重新抓取
							tasks.append(asyncio.create_task(self.request(session, page)))
						for item in items:
							writer.writerow(item)

	async def get_proxy(self, session):
		async with session.get(f"{self.proxy_url}/get") as response:
			while True:
				try:
					return json.loads(await response.text())['proxy']
				except KeyError:
					await asyncio.sleep(60)

	async def delete_proxy(self, session, proxy):
		async with session.get(f"{self.proxy_url}/delete?proxy={proxy}"): return





if __name__ == '__main__':
	import os
	obj = JZSC()
	aptAll = obj.get_apt_list()
	regionAll = obj.get_region_list()
	# aaa = obj.artinfo()
	baseUrl = "http://jzsc.mohurd.gov.cn/api/webApi/dataservice/query/comp/list?qy_region={region}&apt_code={aptcode}&pg=0123456789abcd&pgsz=15"
	root= r"D:\PythonCode\jzsc_mohurd\urlAll"
	for reg in regionAll:
		llist = []
		for apt in aptAll:

			ddict = {}
			url= baseUrl.format(region=reg[0],aptcode=apt[0])
			ddict['url'] = url.replace('0123456789abcd','{}')
			ddict['reg_Name'] = reg[1]
			ddict['apt_Name'] = apt[1].replace('/','_')
			ddict['total'] = 0
			ddict['crawled'] = 0
			llist.append(ddict)
			# pprint.pprint(ddict)
			# print('-----------')
		fileName = str(reg[0]) + '_allInfo.json'
		filePath = os.path.join(root,fileName)
		with open(filePath,'w',encoding='utf-8') as ff:
			json.dump(llist,ff,ensure_ascii=False)