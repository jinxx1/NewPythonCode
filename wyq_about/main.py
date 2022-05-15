# -*- coding: utf-8 -*-
import re

import pandas as pd
import numpy as np
import cpca

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
import os


class keysObj():
	classDict = {'shanghumingcheng': "商户名称",
	             "shanghumignchengsuoxie": "商户名称缩写",
	             "mac": '设备mac',
	             "kuangdaizhanghao": '宽带账号',
	             "shanghuzhanghao_shoujihao": '商户账号',
	             "yijihangye": '一级行业',
	             "erjihangye": '二级行业',
	             "lianxiren": '联系人',
	             "lianxifangshi": '联系方式',
	             "shanghudizhi": '商户地址',
	             "ssid": '设备SSID',
	             "province": '省',
	             "city": '市',
	             "district": '区',
	             "longitude": '经度',
	             "latitude": '纬度',
	             "fangjianhao": '房间号'}

	def __init__(self):
		self.mac = np.nan
		self.kuangdaizhanghao = np.nan
		self.shanghuzhanghao_shoujihao = np.nan
		self.shanghumingcheng = np.nan
		self.yijihangye = '酒店住宿'
		self.erjihangye = '星级'
		self.lianxiren = np.nan
		self.lianxifangshi = np.nan
		self.shanghudizhi = np.nan
		self.ssid = np.nan
		self.province = np.nan
		self.city = np.nan
		self.district = np.nan
		self.longitude = np.nan
		self.latitude = np.nan
		self.shanghumignchengsuoxie = np.nan
		self.fangjianhao = np.nan

	def __repr__(self):
		word = f'''
【设备mac】\tmac\t={self.mac}
【宽带账号】\tkuangdaizhanghao\t=\t{self.kuangdaizhanghao}
【商户账号(手机号)】\tshanghuzhanghao_shoujihao\t=\t{self.shanghuzhanghao_shoujihao}
【商户名称】\tshanghumingcheng\t=\t{self.shanghumingcheng}
【一级行业】\tyijihangye\t=\t{self.yijihangye}
【二级行业】\terjihangye\t=\t{self.erjihangye}
【联系人】\tlianxiren\t=\t{self.lianxiren}
【联系方式】\tlianxifangshi\t=\t{self.lianxifangshi}
【商户地址】\tshanghudizhi\t=\t{self.shanghudizhi}
【设备SSID】\tssid\t=\t{self.ssid}
【省】\tprovince\t=\t{self.province}
【市】\tcity\t=\t{self.city}
【区】\tdistrict\t=\t{self.district}
【经度】\tlongitude\t=\t{self.longitude}
【纬度】\tlatitude\t=\t{self.latitude}
【商户名称缩写】\tshanghumignchengsuoxie\t=\t{self.shanghumignchengsuoxie}
【房间号】\tfangjianhao\t=\t{self.fangjianhao}
'''
		return word


def pandas_readExcel(excelPath):
	sheet_1 = pd.read_excel(excelPath)
	keysFinal = keysObj()
	for i in sheet_1.columns:
		shanghumingcheng_Regx = re.compile("\(|\)|（|）")
		mac_Regx = re.compile("MAC:|mac:|MAC：|mac：|-|：|:| ")

		if '缩写' in i:
			keysFinal.shanghumignchengsuoxie = [x for x in sheet_1[i]]
		if '缩写' not in i and '名称' in i:
			keysFinal.shanghumingcheng = [shanghumingcheng_Regx.sub('', str(x)) for x in sheet_1[i]]
		if 'MAC' in i.upper():
			keysFinal.mac = [mac_Regx.sub('', str(x).upper().replace('O', '0')) for x in sheet_1[i]]
		if '人' in i:
			keysFinal.lianxiren = [x for x in sheet_1[i]]
		if '联系电话' in i:
			keysFinal.lianxifangshi = [str(x).replace('.0', '') for x in sheet_1[i]]
			keysFinal.shanghuzhanghao_shoujihao = [str(x).replace('.0', '') for x in sheet_1[i]]
		if '房间号' in i:
			keysFinal.fangjianhao = [x for x in sheet_1[i]]
		if '区域' in i or i == '区(例:西湖区)':
			keysFinal.district = [x for x in sheet_1[i]]
		if '地市' in i or '城市' == i or '市(例:杭州)' == i:
			keysFinal.city = [x for x in sheet_1[i]]
			keysFinal.province = getProvince(keysFinal.city)
		# if i == '宽带账号' or i == "IP地址" or i == 'IP账号' or i == '宽带号':
		# 	keysFinal.kuangdaizhanghao = [str(x).replace('\t', '') for x in sheet_1[i]]
		if '装机地址' in i:
			keysFinal.shanghudizhi = [x for x in sheet_1[i]]

	newdf = pd.DataFrame(keysFinal.__dict__)
	newdf.rename(columns=keysFinal.classDict, inplace=True)

	newdf['设备mac'] = newdf['设备mac'].map(lambda x: x.split('/'))
	newdf = newdf.explode('设备mac')
	newdf['商户名称'].fillna(method='pad', inplace=True)
	newdf['商户名称缩写'].fillna(method='pad', inplace=True)
	newdf['市'] = newdf['市'].apply(lambda x: x.replace('市', ''))

	newdf.fillna(value="", inplace=True)

	return newdf


def getProvince(xList):
	llist = []
	for i in xList:
		aa = cpca.transform([i])
		a = aa.iloc[0]['省']
		a = a.replace('省', '')
		llist.append(a)
	return llist


if __name__ == '__main__':

	DBroot = r"D:\PythonCode\wyq_about\DBexcel20211206"
	# cleanroot = r"D:\PythonCode\wyq_about\clean"
	cleanroot = r"D:\PythonCode\wyq_about\clean-noIP"

	for root, dirs, files in os.walk(DBroot):
		if files:
			for num, file in enumerate(files):
				# if num > 1:
				# 	break
				excelPath = os.path.join(root, file)
				if '尚品居酒店（孟桂芳）' in excelPath:
					continue
				# if '蓝鲸悦海（郝芳芳）174' not in excelPath:
				# 	continue
				print(excelPath)

				'''
				D:\PythonCode\wyq_about\DBexcel20211206\张家口凯嘉酒店建设桥店（郝芳芳）67.xlsx
				'''
				newPD = pandas_readExcel(excelPath)
				# print(newPD)
				cleanPath = os.path.join(cleanroot, file)
				newPD.to_excel(cleanPath, index=False)

				print(cleanPath)
				print('------------------------------------------------------', num)
