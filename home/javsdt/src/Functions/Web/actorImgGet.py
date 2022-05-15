# coding=utf-8
import json
import pprint

import requests, os, sys, shutil
from bs4 import BeautifulSoup
from urllib import parse as urlparse
from requests.adapters import HTTPAdapter


class get_actor_img():
	def __init__(self):
		self.req = requests.session()
		# self.req.headers = HEA
		self.req.mount('http://', HTTPAdapter(max_retries=3))
		self.req.mount('https://', HTTPAdapter(max_retries=3))
		self.actorPath = r"D:\PythonCode\home\javsdt\src\演员头像"

	# self.actorPath = r"D:\PythonCode\home\javsdt\src\text"

	def main(self, hhtml, url):
		soup = BeautifulSoup(hhtml, 'lxml')
		actorList = soup.find_all(class_='star-name')
		for i in actorList:
			ddict = {}
			hreff = i.a.get('href')
			ddict['actorID'] = hreff.split('/')[-1]
			ddict['actorName'] = i.a.get_text()
			ddict['actorImgUrl'] = urlparse.urljoin(url, i.parent.find('img').get('src'))
			self.getActorImgPath(ddict=ddict)

	def getActorImgPath(self, ddict):
		folder = os.path.join(self.actorPath, ddict['actorName'][0])
		self.mkdir(folder)
		try:
			sp= ddict['actorImgUrl'].split('.')[-1]
		except:
			sp='jpg'
		imgFilePath = os.path.join(folder, ddict['actorName'] + "." + sp)
		if not os.path.exists(imgFilePath):
			# try:
			imgBrow = self.req.get(ddict['actorImgUrl'], timeout=(10, 10))
			with open(imgFilePath, 'wb') as imgF:
				imgF.write(imgBrow.content)
			print('imgSucess----------', )
			print(imgFilePath)
			print(ddict['actorName'])
			print(ddict['actorImgUrl'])
			print('---------------------')
			return True

	# else:
	#
	# 	print('got Img')
	# 	print(ddict['actorName'])
	# 	print('---------------------')
	# except Exception as f1:
	# 	print('ERROR')
	# 	print(f1)
	# 	pass

	def mkdir(self, path):
		folder = os.path.exists(path)
		if not folder:
			os.makedirs(path)


def file_name_walk(file_dir=None):
	listpath = []
	for root, dirs, files in os.walk(file_dir):
		dictTemp = {}
		dictTemp['root'] = root  # 当前目录路径
		dictTemp['dirs'] = dirs  # 当前路径下所有子目录
		dictTemp['files'] = files  # 当前路径下所有非目录子文件
		if not files:
			continue

		if 'info.json' in files:
			jsonPath = os.path.join(root, 'info.json')
			yield jsonPath


if __name__ == '__main__':


	allPath = r"Z:\x299\寄生虫.720p.1080p.HD中字\6v电影APP 有他不迷路\appsiteweb\PIDEO_ROOT"
	mark = 0
	for num, InfoJson in enumerate(file_name_walk(allPath)):

		if mark == 0 or mark % 5 == 0:
			actorImgObj = None
			actorImgObj = get_actor_img()

		with open(InfoJson, 'r', encoding='utf-8') as f:
			jsonT = json.load(f)
		for actor in jsonT['actor']:
			try:
				a = actorImgObj.getActorImgPath(ddict=actor)
				if a:
					mark += 1
					print(mark)
			except:
				import time
				print('出错了。休息2分钟')
				time.sleep(120)
				mark = 0
# a = os.path.exists(path)
# print(a)
